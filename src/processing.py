koatuu_mapping = {
    1: "Autonomous Republic of Crimea",
    5: "Vinnytsia Oblast",
    7: "Volyn Oblast",
    12: "Dnipro Oblast",
    14: "Donetsk Oblast",
    18: "Zhytomyr Oblast",
    21: "Zakarpattia Oblast",
    23: "Zaporizhzhia Oblast",
    26: "Ivano-Frankivsk Oblast",
    32: "Kyiv Oblast",
    35: "Kirovohrad Oblast",
    44: "Luhansk Oblast",
    46: "Lviv Oblast",
    48: "Mykolaiv Oblast",
    51: "Odesa Oblast",
    53: "Poltava Oblast",
    56: "Rivne Oblast",
    59: "Sumy Oblast",
    61: "Ternopil Oblast",
    63: "Kharkiv Oblast",
    65: "Kherson Oblast",
    68: "Khmelnytskyi Oblast",
    71: "Cherkasy Oblast",
    73: "Chernivtsi Oblast",
    74: "Chernihiv Oblast",
    80: "Kyiv",
    85: "Sevastopol",
}


def map_koatuu_to_region(koatuu_code: int) -> str:
    """
    Map a KOATUU code to a human-readable region name.

    :param koatuu_code (int): The KOATUU code to map.

    :return (str): The corresponding region name.
    """

    koatuu_level_1 = str(koatuu_code)[:2]

    first_pass = koatuu_mapping.get(int(koatuu_level_1), None)
    if first_pass is not None:
        return first_pass

    # Try to map using first digit only if 1, 5 or 7
    if koatuu_level_1[0] in {"1", "5", "7"}:
        return koatuu_mapping.get(int(koatuu_level_1[0]), "Unknown Region")

    return "Unknown Region"
