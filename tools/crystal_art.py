#!/usr/bin/env python3
"""Kristall-Optik fuer Mystit: eigene Formen statt umgefaerbtem Eisen.

Barren = facettierter Kristall, Nugget = Splitter, Roherz = Brocken mit Splitter,
Block = Kristallflaeche. Zeichen: o Outline, E tief, D dunkel, M mittel, L hell,
B Glanz, W Weiss.
"""
import random
from PIL import Image

P = {
    "o": (21, 11, 34, 255),
    "E": (34, 16, 54, 255),
    "D": (55, 26, 88, 255),
    "d": (88, 44, 139, 255),
    "M": (107, 55, 168, 255),
    "m": (131, 77, 193, 255),
    "L": (156, 99, 218, 255),
    "l": (177, 127, 229, 255),
    "B": (199, 155, 240, 255),
    "W": (240, 227, 255, 255),
}

# Nachbartöne für die Koernung: helle und dunkle Variante je Stufe
NEIGHBOURS = {
    P["E"]: (None, P["D"]),
    P["D"]: (P["E"], P["d"]),
    P["d"]: (P["D"], P["M"]),
    P["M"]: (P["d"], P["m"]),
    P["m"]: (P["M"], P["L"]),
    P["L"]: (P["m"], P["l"]),
    P["l"]: (P["L"], P["B"]),
    P["B"]: (P["l"], P["W"]),
}

GEM = [
    "................",
    ".......oo.......",
    "......oBBo......",
    ".....oBLLLo.....",
    ".....oBLLMo.....",
    "....oBLLMMDo....",
    "....oLLMMMDo....",
    "....oLLMMMDo....",
    "....oLLMMMDo....",
    "....oLLMMMDo....",
    "....oLLMMDDo....",
    "...oLLMMMDDo....",
    "...oMMMMDDDo....",
    "...oMMMDDDDo....",
    "...ooooooooo....",
    "................",
]

NUGGET = [
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "........oo......",
    ".......oBo......",
    "......oBLMo.....",
    "......oLMDo.....",
    ".....oLLMDo.....",
    ".....oMMDDo.....",
    "....ooMMDDoo....",
    ".....oooooo.....",
    "................",
    "................",
]

RAW = [
    "................",
    "...........oo...",
    "..........oBLo..",
    ".........oBLLo..",
    "....oo...oMLMo..",
    "...oBLo..oMMDo..",
    "..oBLLMo.ooDo...",
    "..oLLMMo........",
    ".oLLMMDDo.......",
    ".oLMMDDDo.......",
    ".oMMDDDDo.......",
    "..oDDDDo........",
    "...oooo.........",
    "................",
    "................",
    "................",
]


def grain(im, amount=0.28, seed=3, only=None):
    """Koernung: Pixel innerhalb einer Farbstufe durch Nachbartöne ersetzen.

    only = Menge von Farben, die gekoernt werden darf (None = alle ausser Outline/Glanz).
    """
    rnd = random.Random(seed)
    px = im.load()
    for y in range(16):
        for x in range(16):
            col = px[x, y]
            if col[3] == 0 or col == P["o"] or col == P["W"]:
                continue
            if only is not None and col not in only:
                continue
            pair = NEIGHBOURS.get(col)
            if not pair:
                continue
            if rnd.random() < amount:
                darker, lighter = pair
                # oben links heller, unten rechts dunkler -> gerichtete Koernung
                pick = lighter if (rnd.random() < 0.5 + (7 - y) / 32 + (7 - x) / 32) else darker
                if pick:
                    px[x, y] = pick
    return im


def from_ascii(rows, glints=()):
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = im.load()
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, len(row), row)
        for x, ch in enumerate(row):
            if ch != ".":
                px[x, y] = P[ch]
    for (x, y) in glints:
        if px[x, y][3]:
            px[x, y] = P["W"]
    return im


def block(seed=5):
    """Kristallblock: ruhige Kristallflaeche mit groben Facetten und wenigen Einschluessen."""
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16), P["M"])
    px = im.load()
    # zwei grobe Facetten: linke Bahn heller, Ecke unten rechts dunkler
    for y in range(16):
        for x in range(16):
            if x - y < -4:
                px[x, y] = P["L"]
            if x - y > 7:
                px[x, y] = P["D"]
    # Facettenkante als weiche Linie aus Glanzpixeln
    for t in range(16):
        for x, y in ((t, t + 5),):
            if 0 <= x < 16 and 0 <= y < 16:
                px[x, y] = P["B"]
    # dunkle Kristallnester
    for _ in range(6):
        cx, cy = rnd.randrange(1, 14), rnd.randrange(1, 14)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
            if rnd.random() < 0.7:
                px[cx + dx, cy + dy] = P["D"]
    # Glanzpunkte
    for (x, y) in ((3, 4), (10, 8), (6, 12)):
        px[x, y] = P["W"]
        if x - 1 >= 0:
            px[x - 1, y] = P["B"]
    return im


def build():
    return {
        "mystit_ingot": grain(from_ascii(GEM, glints=[(6, 3)]), amount=0.22, seed=11),
        "mystit_nugget": grain(from_ascii(NUGGET, glints=[(7, 5)]), amount=0.2, seed=12),
        "raw_mystit": grain(from_ascii(RAW, glints=[(5, 5), (11, 2)]), amount=0.26, seed=13),
        "mystit_block": grain(block(), amount=0.3, seed=14,
                              only={P["M"], P["D"], P["d"]}),
    }


if __name__ == "__main__":
    for k, v in build().items():
        v.save(f"/root/work/mystit/preview_{k}.png")
    print("ok")
