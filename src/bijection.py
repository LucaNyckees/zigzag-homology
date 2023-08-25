import gudhi as gd


def get_skel(K: gd.SimplexTree(), p: int) -> list:
    """
    Args:
        K : a simplicial complex
        p : a dimension
    Returns:
        skel_new : list, a list of all p-simplices of K
    """
    return [s for s in list(K.get_skeleton(p)) if len(s[0]) == p + 1]


def EP_to_LZZ(dgms: list | tuple) -> list[tuple]:
    """
    This function translates the extended persistence barcode to its levelset zigzag barcode equivalent.

    Args :
        dgms : extended persistence diagrams with types 'ordinary', 'relative', 'extended+' and 'extended-'.
    Returns :
        B : equivalent levelset zigzag barcode.
    """

    def interval_tranform(type: str, interval: tuple | list) -> list:
        if type == 'REL':
            return [interval[1], interval[0]]
        else:
            return [interval[0], interval[1]]

    B = []
    types = ["ORD", "REL", "EP+", "EP-"]

    for i, t in enumerate(types):
        B += [(t, dim, interval_tranform(t, I)) for (dim, I) in dgms[i]]

    return B
