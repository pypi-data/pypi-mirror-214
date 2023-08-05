
def WtToAt(constituents: dict[any, float]) -> dict[any, float]:
    """
    Converts weight fraction from dictionary to atomic fraction
    """

    try:
        # calculate (constant) denominator for conversion
        denominator = sum([wtFraction / constituent.atomicWeight for constituent, wtFraction in constituents.items()])

        # convert and overwrite to atomic fraction
        conv_constituents: dict[any, float] = {}
        for constituent, wtFraction in constituents.items():
            conv_constituents[constituent] = (wtFraction/constituent.atomicWeight) / denominator # now atomic fraction

        return conv_constituents

    except:
        raise TypeError(f"One of the constituents does not have an atomic weight.")

def AtToWt(constituents: dict[any, float]) -> dict[any, float]:
    """
    Converts atomic fraction from dictionary to weight fraction 
    """

    try:
        # calculate (constant) denominator for conversion
        denominator = sum([atFraction * constituent.atomicWeight for constituent, atFraction in constituents.items()])

        # convert and overwrite to weight fraction
        conv_constituents: dict[any, float] = {}
        for constituent, atFraction in constituents.items():
            conv_constituents[constituent] = (atFraction * constituent.atomicWeight) / denominator # now weight fraction

        return conv_constituents

    except:
        raise TypeError(f"One of the constituents does not have an atomic weight.")