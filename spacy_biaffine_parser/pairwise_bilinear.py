from typing import List, Optional, Tuple, cast

from spacy import registry
from spacy.tokens.doc import Doc
from thinc.api import Model, PyTorchWrapper_v2
from thinc.api import chain, get_width, list2array, torch2xp
from thinc.api import with_getitem, xp2torch
from thinc.shims.pytorch_grad_scaler import PyTorchGradScaler
from thinc.types import ArgsKwargs, Floats2d, Floats3d, Floats4d, Ints1d

from .pytorch_pairwise_bilinear import (
    PairwiseBilinearModel as PyTorchPairwiseBilinearModel,
)


@registry.architectures("PairwiseBilinear.v1")
def build_pairwise_bilinear(
    tok2vec: Model[List[Doc], List[Floats2d]],
    nO=None,
    *,
    hidden_width: int = 128,
    mixed_precision: bool = False,
    grad_scaler: Optional[PyTorchGradScaler] = None
):
    nI = None
    if tok2vec.has_dim("nO") is True:
        nI = tok2vec.get_dim("nO")

    pairwise_bilinear = Model(
        "pairwise_bilinear",
        forward=pairswise_bilinear_forward,
        init=pairwise_bilinear_init,
        dims={"nI": nI, "nO": nO},
        attrs={
            "hidden_width": hidden_width,
            "mixed_precision": mixed_precision,
            "grad_scaler": grad_scaler,
        },
    )

    model = chain(
        with_getitem(0, chain(tok2vec, list2array())),
        pairwise_bilinear,
    )
    model.set_ref("pairwise_bilinear", pairwise_bilinear)

    return model


def pairwise_bilinear_init(model: Model, X=None, Y=None):
    if model.layers:
        return

    if X is not None and model.has_dim("nI") is None:
        model.set_dim("nI", get_width(X))
    if Y is not None and model.has_dim("nO") is None:
        model.set_dim("nO", get_width(Y))

    hidden_width = model.attrs["hidden_width"]
    mixed_precision = model.attrs["mixed_precision"]
    grad_scaler = model.attrs["grad_scaler"]

    model._layers = [
        PyTorchWrapper_v2(
            PyTorchPairwiseBilinearModel(
                model.get_dim("nI"),
                model.get_dim("nO"),
                hidden_width=hidden_width,
            ),
            convert_inputs=convert_inputs,
            convert_outputs=convert_outputs,
            mixed_precision=mixed_precision,
            grad_scaler=grad_scaler,
        )
    ]


def pairswise_bilinear_forward(model: Model, X, is_train: bool):
    return model.layers[0](X, is_train)


def convert_inputs(
    model: Model, Xr_lenghts: Tuple[Floats2d, Ints1d], is_train: bool = False
):
    flatten = model.ops.flatten
    unflatten = model.ops.unflatten
    pad = model.ops.pad
    unpad = model.ops.unpad

    Xr, lengths = Xr_lenghts

    Xt = xp2torch(pad(unflatten(Xr, lengths)), requires_grad=is_train)
    Lt = xp2torch(lengths)

    def convert_from_torch_backward(d_inputs: ArgsKwargs) -> Tuple[Floats2d, Ints1d]:
        dX = cast(Floats3d, torch2xp(d_inputs.args[0]))
        return flatten(unpad(dX, list(lengths))), lengths

    output = ArgsKwargs(args=(Xt, Lt), kwargs={})

    return output, convert_from_torch_backward


def convert_outputs(model, inputs_outputs, is_train):
    flatten = model.ops.flatten
    unflatten = model.ops.unflatten
    pad = model.ops.pad
    unpad = model.ops.unpad

    (_, lengths), Y_t = inputs_outputs

    def convert_for_torch_backward(dY: Tuple[Floats2d, Floats3d]) -> ArgsKwargs:
        dY_t = xp2torch(pad(unflatten(dY, lengths)))
        return ArgsKwargs(
            args=([Y_t],),
            kwargs={"grad_tensors": [dY_t]},
        )

    Y = cast(Floats4d, torch2xp(Y_t))
    Y = flatten(unpad(Y, lengths))

    return Y, convert_for_torch_backward
