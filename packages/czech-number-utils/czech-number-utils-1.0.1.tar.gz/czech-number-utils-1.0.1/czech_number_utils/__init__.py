"""
Czech Number Utilities

A Python module for converting numbers to their textual representations in Czech, 
both cardinal and ordinal forms. Includes support for millions, billions, and 
common grammatical cases.
"""
import re

def number_to_czech_word(number):
    """
    Converts a number to its text representation in Czech.

    Parameters:
        number (int): The number to convert.

    Returns:
        str: The text representation of the number in Czech.
    """
    ones = ["", "jedna", "dva", "tři", "čtyři", "pět", "šest", "sedm", "osm", "devět"]
    teens = ["deset", "jedenáct", "dvanáct", "třináct", "čtrnáct", "patnáct", "šestnáct", "sedmnáct", "osmnáct", "devatenáct"]
    tens = ["", "", "dvacet", "třicet", "čtyřicet", "padesát", "šedesát", "sedmdesát", "osmdesát", "devadesát"]
    hundreds = ["", "jedno sto", "dvě stě", "tři sta", "čtyři sta", "pět set", "šest set", "sedm set", "osm set", "devět set"]
    thousands = ["", "jeden tisíc", "dva tisíce", "tři tisíce", "čtyři tisíce"]
    millions = ["", "jeden milión", "dva milióny", "tři milióny", "čtyři milióny"]
    milliards = ["", "jedna miliarda", "dvě miliardy", "tři miliardy", "čtyři miliardy"]
    teens_ordinals = ["", "desátý", "dvacátý", "třicátý", "čtyřicátý", "padesátý", "šedesátý", "sedmdesátý", "osmdesátý", "devadesátý"]

    if number == 0:
        return "nula"

    parts = []

    if number >= 1_000_000_000:
        index = number // 1_000_000_000
        if index < len(milliards):
            parts.append(milliards[index])
        else:
            parts.append(number_to_czech_word(number // 1_000_000_000) + " miliard")
        number %= 1_000_000_000

    if number >= 1_000_000:
        index = number // 1_000_000
        if index < len(millions):
            parts.append(millions[index])
        else:
            parts.append(number_to_czech_word(number // 1_000_000) + " milionů")
        number %= 1_000_000

    if number >= 1_000:
        index = number // 1_000
        if index < len(thousands):
            parts.append(thousands[index])
        else:
            parts.append(number_to_czech_word(number // 1_000) + " tisíc")
        number %= 1_000

    if number >= 100:
        parts.append(hundreds[number // 100])
        number %= 100

    if number >= 10 and number < 20:
        parts.append(teens[number - 10])
    else:
        if number >= 20:
            parts.append(tens[number // 10])
            number %= 10
        if number > 0:
            parts.append(ones[number])

    return " ".join(filter(None, parts))

ordinals = {
    1: "první",
    2: "druhý",
    3: "třetí",
    4: "čtvrtý",
    5: "pátý",
    6: "šestý",
    7: "sedmý",
    8: "osmý",
    9: "devátý",
    10: "desátý",
}

# Extend ordinal mappings for larger numbers
for i in range(1, 10):
    number = i + 10
    ordinals[number] = f"{number_to_czech_word(i)}náctý"

for i in range(2, 10):
    number = i * 10
    ordinals[number] = teens_ordinals[i]

    for j in range(1, 10):
        number_inside = number + j
        ordinals[number_inside] = f"{ordinals[number]} {ordinals[j]}"

def number_to_czech_ordinal(number):
    """
    Converts a number to its ordinal representation in Czech.

    Parameters:
        number (int): The number to convert.

    Returns:
        str: The ordinal text representation of the number in Czech.
    """
    return ordinals.get(number, number_to_czech_word(number))

def replace_numbered_list_and_numbers(text):
    """
    Replaces numbered list items and inline numbers with their Czech text equivalents.

    Parameters:
        text (str): The input text.

    Returns:
        str: The text with numbers replaced by words.
    """
    def replace_list_items(match):
        number = int(match.group(1))
        ordinal_word = number_to_czech_ordinal(number) + " bod: "
        return ordinal_word

    def replace_inline_numbers(match):
        number = int(match.group(0))
        return number_to_czech_word(number)

    text = re.sub(r"\b(\d+)\.\s", replace_list_items, text)
    text = re.sub(r"\b\d+\b", replace_inline_numbers, text)

    return text

# Example usage
if __name__ == "__main__":
    example_text = """1. Tohle je první
2. Tohle je druhý.
3. Tohle je třetí
20. Tohle je dvacátý.
99. Nákupní seznam: 11 rohlíků, 333 lahví mléka a 1379 kilo másla."""
    translated_text = replace_numbered_list_and_numbers(example_text)
    print(translated_text)
