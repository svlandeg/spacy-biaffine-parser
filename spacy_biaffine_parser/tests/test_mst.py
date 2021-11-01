import numpy as np
import pytest

from spacy_biaffine_parser.mst import chu_liu_edmonds

def random_scores(n_tokens: int):
    return np.random.rand(n_tokens * n_tokens).astype("f").reshape(n_tokens, n_tokens)


def test_non_square():
    scores = np.random.rand(20).astype("f").reshape(5, 4)
    with pytest.raises(ValueError, match=r"Edge weight matrix.*not a square matrix"):
        chu_liu_edmonds(scores, 0)


def test_head_out_of_bounds():
    scores = random_scores(5)
    with pytest.raises(IndexError, match=r"Head 5 out of bounds.*(5, 5)"):
        chu_liu_edmonds(scores, 5)


def test_correctly_decodes_random_large_matrices():
    scores = np.array(
        [
            [
                0.15154335,
                0.21364425,
                0.02926004,
                0.24640401,
                0.05929783,
                0.98366485,
                0.53015432,
                0.07778964,
                0.00989446,
                0.17998191,
            ],
            [
                0.68921352,
                0.33551225,
                0.91974265,
                0.08476561,
                0.48800752,
                0.87661821,
                0.31723634,
                0.51386131,
                0.97963044,
                0.36960274,
            ],
            [
                0.13969799,
                0.46092784,
                0.75821582,
                0.78823102,
                0.63945137,
                0.42556879,
                0.81997744,
                0.12978648,
                0.40536874,
                0.4744205,
            ],
            [
                0.40688978,
                0.25514681,
                0.59851297,
                0.82950985,
                0.46627791,
                0.05888491,
                0.97450763,
                0.90287058,
                0.35996474,
                0.6448661,
            ],
            [
                0.30530523,
                0.76566773,
                0.64714425,
                0.1424588,
                0.14283951,
                0.00153444,
                0.9688441,
                0.87582559,
                0.63371798,
                0.67004456,
            ],
            [
                0.88822529,
                0.26780501,
                0.61901697,
                0.35049028,
                0.06430303,
                0.44334551,
                0.15308377,
                0.42145127,
                0.87420229,
                0.3309963,
            ],
            [
                0.31808055,
                0.35399265,
                0.31438455,
                0.63534316,
                0.36917357,
                0.7707749,
                0.1686939,
                0.66622048,
                0.67872444,
                0.28663183,
            ],
            [
                0.82167446,
                0.15910145,
                0.6654594,
                0.54279563,
                0.19068867,
                0.17368633,
                0.07199292,
                0.29239669,
                0.60002772,
                0.75121407,
            ],
            [
                0.74016819,
                0.28619099,
                0.71608573,
                0.64490596,
                0.05975497,
                0.8792097,
                0.85888953,
                0.90590799,
                0.62783992,
                0.12660846,
            ],
            [
                0.80810707,
                0.10910174,
                0.11777376,
                0.36885688,
                0.88732921,
                0.82053854,
                0.84096041,
                0.53546477,
                0.49554398,
                0.21705035,
            ],
        ],
        dtype="f",
    )
    assert chu_liu_edmonds(scores, 0) == [None, 4, 1, 2, 9, 0, 3, 8, 5, 7]

    scores2 = np.array(
        [
            [
                0.63699522,
                0.87615555,
                0.45236657,
                0.5188734,
                0.13080447,
                0.30954603,
                0.70385654,
                0.00940039,
                0.99012901,
                0.91048303,
            ],
            [
                0.6110081,
                0.11629512,
                0.91845679,
                0.55938488,
                0.45709085,
                0.16727591,
                0.3338458,
                0.87262039,
                0.26543677,
                0.78429413,
            ],
            [
                0.06226577,
                0.3509711,
                0.8738929,
                0.77723445,
                0.83439156,
                0.72800083,
                0.70465176,
                0.9323746,
                0.01803918,
                0.50092784,
            ],
            [
                0.30294811,
                0.65599656,
                0.23342294,
                0.01840916,
                0.78500845,
                0.78103093,
                0.82584077,
                0.72756822,
                0.60326683,
                0.44574654,
            ],
            [
                0.75513096,
                0.06980882,
                0.72330091,
                0.94334981,
                0.262673,
                0.84566782,
                0.6318016,
                0.0442728,
                0.2669838,
                0.59781991,
            ],
            [
                0.27443631,
                0.33890352,
                0.83353679,
                0.88552379,
                0.89789705,
                0.00165288,
                0.17836232,
                0.59181986,
                0.426987,
                0.91632828,
            ],
            [
                0.55585136,
                0.87230681,
                0.10995064,
                0.65543565,
                0.96603594,
                0.34425304,
                0.07438735,
                0.21991817,
                0.53278602,
                0.46460502,
            ],
            [
                0.78368679,
                0.55949995,
                0.42268737,
                0.1681499,
                0.62903574,
                0.75765237,
                0.07484798,
                0.37319298,
                0.62900207,
                0.26623339,
            ],
            [
                0.66636035,
                0.19227743,
                0.48126272,
                0.14611228,
                0.6107612,
                0.30056951,
                0.77329224,
                0.93780084,
                0.12710157,
                0.96506847,
            ],
            [
                0.76441608,
                0.25583239,
                0.14817458,
                0.68389535,
                0.85748418,
                0.81745151,
                0.71656758,
                0.11733889,
                0.98476048,
                0.26556185,
            ],
        ],
        dtype="f",
    )

    assert chu_liu_edmonds(scores2, 0) == [None, 0, 1, 4, 6, 4, 8, 8, 0, 8]

    scores3 = np.array(
        [
            [
                0.32226934,
                0.03494655,
                0.13943128,
                0.77627796,
                0.32289177,
                0.20728151,
                0.79354934,
                0.44277001,
                0.70666543,
                0.76361263,
            ],
            [
                0.89787456,
                0.19412729,
                0.2769623,
                0.42547065,
                0.78306101,
                0.99639906,
                0.44910723,
                0.69166559,
                0.5974235,
                0.6019087,
            ],
            [
                0.01936413,
                0.77783413,
                0.2635923,
                0.24239049,
                0.15320177,
                0.58810727,
                0.93770173,
                0.97238493,
                0.40536974,
                0.28189387,
            ],
            [
                0.21176774,
                0.90580752,
                0.48167285,
                0.17517493,
                0.35126148,
                0.09566258,
                0.77651317,
                0.844114,
                0.32902123,
                0.93356815,
            ],
            [
                0.68965019,
                0.98577739,
                0.06460552,
                0.103729,
                0.59807881,
                0.82418659,
                0.20288672,
                0.55119795,
                0.01953631,
                0.75208802,
            ],
            [
                0.49706455,
                0.52543525,
                0.16288358,
                0.72442708,
                0.57151594,
                0.68195141,
                0.47521668,
                0.56127222,
                0.6673682,
                0.93037853,
            ],
            [
                0.12841745,
                0.89183647,
                0.21585613,
                0.73852511,
                0.09812739,
                0.06616884,
                0.12730214,
                0.8322976,
                0.93773286,
                0.23950978,
            ],
            [
                0.73496813,
                0.52910843,
                0.94925765,
                0.77135859,
                0.85716859,
                0.47158383,
                0.88753378,
                0.00141653,
                0.47463287,
                0.33777619,
            ],
            [
                0.76116294,
                0.77581507,
                0.99508616,
                0.24001213,
                0.13688175,
                0.57771731,
                0.1435426,
                0.18420174,
                0.07373099,
                0.15492254,
            ],
            [
                0.88146862,
                0.27868822,
                0.41427004,
                0.989063,
                0.08847578,
                0.31721111,
                0.13694788,
                0.99730908,
                0.8523681,
                0.81020978,
            ],
        ],
        dtype="f",
    )

    assert chu_liu_edmonds(scores3, 0) == [None, 4, 8, 9, 7, 1, 0, 2, 6, 5]

    scores4 = np.array(
        [
            [
                0.94146094,
                0.08429249,
                0.11658879,
                0.7209569,
                0.04588338,
                0.41361274,
                0.00335799,
                0.58725318,
                0.37633847,
                0.50978681,
            ],
            [
                0.50163181,
                0.96919669,
                0.16614751,
                0.15533209,
                0.15054694,
                0.08811524,
                0.13978445,
                0.65591973,
                0.95264964,
                0.17669406,
            ],
            [
                0.36864862,
                0.95739286,
                0.65356991,
                0.71690581,
                0.29263559,
                0.98409776,
                0.61308834,
                0.50921288,
                0.49160935,
                0.53610581,
            ],
            [
                0.23275999,
                0.60587704,
                0.55893549,
                0.69733286,
                0.30008536,
                0.13133368,
                0.90196987,
                0.52283165,
                0.96302483,
                0.44467621,
            ],
            [
                0.15057842,
                0.58499236,
                0.11330645,
                0.57510935,
                0.39645653,
                0.53736407,
                0.08391498,
                0.06004636,
                0.88086527,
                0.25429321,
            ],
            [
                0.40042428,
                0.08725659,
                0.87216523,
                0.18444633,
                0.61547065,
                0.8032823,
                0.16163181,
                0.81884952,
                0.51741822,
                0.73005934,
            ],
            [
                0.08460523,
                0.01342742,
                0.70127922,
                0.45693109,
                0.40153192,
                0.07611445,
                0.74831201,
                0.3385515,
                0.24000027,
                0.33290993,
            ],
            [
                0.01990056,
                0.28629396,
                0.85476794,
                0.68330081,
                0.93204836,
                0.14587584,
                0.06681271,
                0.50342723,
                0.30878763,
                0.51632671,
            ],
            [
                0.22297607,
                0.99004514,
                0.02590417,
                0.61425698,
                0.16932825,
                0.06197453,
                0.58227628,
                0.46317503,
                0.21611736,
                0.88426682,
            ],
            [
                0.21695749,
                0.52528143,
                0.9569687,
                0.70641648,
                0.45516634,
                0.59951297,
                0.82591367,
                0.6038499,
                0.14423517,
                0.12984568,
            ],
        ],
        dtype="f",
    )

    assert chu_liu_edmonds(scores4, 0) == [None, 8, 9, 0, 7, 2, 3, 5, 3, 8]

    scores5 = np.array(
        [
            [
                0.19181828,
                0.07215655,
                0.49029481,
                0.40338361,
                0.77464947,
                0.15287357,
                0.33550702,
                0.9075557,
                0.16816009,
                0.12815985,
            ],
            [
                0.39814249,
                0.83951939,
                0.6197687,
                0.10285881,
                0.35754604,
                0.03372432,
                0.26903616,
                0.39758852,
                0.27831648,
                0.8626124,
            ],
            [
                0.32651809,
                0.36621293,
                0.55139869,
                0.48841691,
                0.86105511,
                0.95220918,
                0.99901665,
                0.43452191,
                0.51957831,
                0.12977951,
            ],
            [
                0.24777433,
                0.20835293,
                0.35423981,
                0.8647926,
                0.54734269,
                0.19705202,
                0.20262791,
                0.29885766,
                0.89558149,
                0.48529723,
            ],
            [
                0.99486246,
                0.02998787,
                0.94388915,
                0.16682153,
                0.04621821,
                0.78283825,
                0.32711021,
                0.11668783,
                0.54230828,
                0.01990573,
            ],
            [
                0.81816179,
                0.77223827,
                0.3778254,
                0.14590591,
                0.53032985,
                0.12751733,
                0.80951733,
                0.94590486,
                0.14917576,
                0.0905699,
            ],
            [
                0.56977204,
                0.6759112,
                0.86349563,
                0.30270709,
                0.03673155,
                0.8814458,
                0.52538187,
                0.97650872,
                0.9278274,
                0.73412665,
            ],
            [
                0.96577082,
                0.17352435,
                0.71417166,
                0.57713058,
                0.99690502,
                0.5856659,
                0.87223811,
                0.8265802,
                0.07539461,
                0.28718492,
            ],
            [
                0.64135636,
                0.53712009,
                0.98343642,
                0.68861079,
                0.33153221,
                0.86677607,
                0.65411023,
                0.97146557,
                0.78007143,
                0.24988737,
            ],
            [
                0.52704545,
                0.39384584,
                0.99308,
                0.03148114,
                0.43305557,
                0.11551732,
                0.13331425,
                0.17881437,
                0.05076005,
                0.20889167,
            ],
        ],
        dtype="f",
    )

    assert chu_liu_edmonds(scores5, 0) == [None, 5, 4, 8, 7, 2, 2, 0, 6, 1]