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
    "E": (43, 20, 68, 255),
    "D": (70, 32, 110, 255),
    "M": (107, 55, 168, 255),
    "L": (156, 99, 218, 255),
    "B": (199, 155, 240, 255),
    "W": (240, 227, 255, 255),
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
        "mystit_ingot": from_ascii(GEM, glints=[(6, 3)]),
        "mystit_nugget": from_ascii(NUGGET, glints=[(7, 5)]),
        "raw_mystit": from_ascii(RAW, glints=[(5, 5), (11, 2)]),
        "mystit_block": block(),
    }


if __name__ == "__main__":
    for k, v in build().items():
        v.save(f"/root/work/mystit/preview_{k}.png")
    print("ok")
