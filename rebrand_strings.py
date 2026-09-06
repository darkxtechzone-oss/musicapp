"""
Inabadilisha maneno yanayoonekana na mtumiaji ndani ya <string> tags
(values ya strings.xml, kwa lugha zote) kutoka "Cubic" kwenda "DarkX".

MUHIMU: haigusi 'name=' attribute (ID ya resource, mfano name="cubic_canvas")
kwa sababu hizo zinatumika na msimbo wa Kotlin (R.string.cubic_canvas) -
kuzibadilisha kunahitaji kubadili pia kila mahali zinapotumika (hatari zaidi,
huo ni "deep rebrand"). Hapa tunabadilisha TU maandishi yanayosomwa na
mtumiaji.
"""

import os
import re
import xml.etree.ElementTree as ET

RES_ROOT = "composeApp/src/androidMain/res"

REPLACEMENTS = [
    ("Cubic-Music", "DarkX-Music"),
    ("Cubic Music", "DarkX Music"),
    ("CUBIC MUSIC", "DARKX MUSIC"),
    ("Cubic", "DarkX"),
    ("CUBIC", "DARKX"),
    ("cubic", "darkx"),
]


def rebrand_text(value: str) -> str:
    for old, new in REPLACEMENTS:
        value = value.replace(old, new)
    return value


def process_strings_file(path: str) -> int:
    tree = ET.parse(path)
    root = tree.getroot()
    changed = 0

    for string_el in root.findall("string"):
        if string_el.text and "ubic" in string_el.text:
            string_el.text = rebrand_text(string_el.text)
            changed += 1

    # plural / string-array items too
    for array_el in root.findall("string-array"):
        for item in array_el.findall("item"):
            if item.text and "ubic" in item.text:
                item.text = rebrand_text(item.text)
                changed += 1

    for plural_el in root.findall("plurals"):
        for item in plural_el.findall("item"):
            if item.text and "ubic" in item.text:
                item.text = rebrand_text(item.text)
                changed += 1

    if changed:
        for el in root.iter():
            el.tail = el.tail or "\n"
        tree.write(path, encoding="utf-8", xml_declaration=True)

    return changed


def main():
    total_files = 0
    total_strings = 0
    for dirpath, dirnames, filenames in os.walk(RES_ROOT):
        if "strings.xml" in filenames and os.path.basename(dirpath).startswith("values"):
            path = os.path.join(dirpath, "strings.xml")
            changed = process_strings_file(path)
            if changed:
                total_files += 1
                total_strings += changed
                print(f"  {path}: {changed} strings updated")

    print(f"\nJumla: faili {total_files}, maneno {total_strings} yamebadilishwa.")


if __name__ == "__main__":
    main()
