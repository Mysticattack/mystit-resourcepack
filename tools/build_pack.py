#!/usr/bin/env python3
"""Baut das Mystit-Ressourcenpaket: Erz, Werkzeuge, Ruestung, Modelle, JSON.

Formen der Werkzeuge und der Ruestung stammen aus den Vanilla-Sprites (Silhouette und
Alpha bleiben unveraendert), nur die Farben werden auf die Mystit-Palette gelegt.
"""
import json, os, random, shutil, zipfile
from PIL import Image, ImageDraw

ROOT = "/root/work/mystit"
PACK = os.path.join(ROOT, "mystit-pack")
NS = "mysticattack"
REF = os.path.join(ROOT, "ref")
OUT_TEX = os.path.join(PACK, "assets", NS, "textures")

CRYSTAL_RAMP = [(26, 16, 40, 255), (58, 30, 88, 255), (110, 56, 160, 255),
                (166, 107, 224, 255), (217, 182, 245, 255)]
WOOD_RAMP = [(38, 24, 12, 255), (72, 49, 28, 255), (114, 81, 46, 255), (156, 118, 70, 255)]

STONE = [(126, 126, 126), (117, 117, 117), (108, 108, 108), (99, 99, 99), (134, 134, 134)]
DEEPSLATE = [(80, 80, 84), (72, 72, 76), (64, 64, 68), (56, 56, 60), (90, 90, 94)]

TOOLS = ["sword", "pickaxe", "axe", "shovel", "hoe"]
ARMOR_ITEMS = ["helmet", "chestplate", "leggings", "boots"]


def luminance(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def rank_map(colors, ramp):
    ordered = sorted(colors, key=luminance)
    lut = {}
    for i, c in enumerate(ordered):
        pos = round(i / max(1, len(ordered) - 1) * (len(ramp) - 1))
        lut[c] = ramp[pos]
    return lut


def recolor(im, split_wood=False):
    """Farben auf die eigene Rampe legen, Alpha und Silhouette unveraendert."""
    src = im.convert("RGBA")
    out = Image.new("RGBA", src.size, (0, 0, 0, 0))
    sp, op = src.load(), out.load()
    opaque = [(sp[x, y]) for y in range(src.height) for x in range(src.width) if sp[x, y][3] > 8]
    if split_wood:
        wood = {p[:3] for p in opaque if p[0] > p[2]}      # braune Griffe
        cry = {p[:3] for p in opaque if p[0] <= p[2]}      # Koepfe
        lut_wood, lut_cry = rank_map(wood, WOOD_RAMP), rank_map(cry, CRYSTAL_RAMP)
        for y in range(src.height):
            for x in range(src.width):
                r, g, b, a = sp[x, y]
                if a > 8:
                    lut = lut_wood if r > b else lut_cry
                    op[x, y] = lut[(r, g, b)][:3] + (a,)
    else:
        lut = rank_map({p[:3] for p in opaque}, CRYSTAL_RAMP)
        for y in range(src.height):
            for x in range(src.width):
                r, g, b, a = sp[x, y]
                if a > 8:
                    op[x, y] = lut[(r, g, b)][:3] + (a,)
    return out


# Kristall-Cluster fuer das Erz: kleine, zusammenhaengende Truemmer wie bei Vanilla-Erz
CLUSTERS = [
    [(4, 2), (4, 3)],
    [(12, 2), (13, 2), (12, 3)],
    [(6, 6), (7, 6), (7, 7)],
    [(10, 5), (10, 6), (11, 6)],
    [(1, 8), (2, 8), (2, 9)],
    [(9, 8), (8, 9), (9, 9), (10, 9)],
    [(11, 11), (12, 11), (12, 12)],
    [(4, 12), (3, 13), (4, 13)],
    [(10, 12), (9, 13), (10, 13)],
]


def ore_texture(base_palette, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    px = im.load()
    for y in range(16):
        for x in range(16):
            c = base_palette[rnd.choices(range(len(base_palette)), weights=[30, 30, 20, 12, 8])[0]]
            px[x, y] = c + (255,)
    for _ in range(12):
        x, y = rnd.randrange(16), rnd.randrange(16)
        px[x, y] = base_palette[3] + (255,)
    for cl in CLUSTERS:
        if rnd.random() < 0.12:          # einzelne Cluster weglassen, damit es nicht zu dicht wird
            continue
        for i, (x, y) in enumerate(cl):
            if i == 0:
                px[x, y] = CRYSTAL_RAMP[4]
            elif i == len(cl) - 1:
                px[x, y] = CRYSTAL_RAMP[2]
            else:
                px[x, y] = CRYSTAL_RAMP[3]
    return im


def wr(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def main():
    if os.path.exists(PACK):
        shutil.rmtree(PACK)
    for d in ("block", "item", "models/armor"):
        os.makedirs(os.path.join(OUT_TEX, d), exist_ok=True)

    made = {}

    # --- Erz ---
    for name, pal, seed in (("mystit_ore", STONE, 11), ("mystit_deepslate_ore", DEEPSLATE, 23)):
        p = os.path.join(OUT_TEX, "block", name + ".png")
        ore_texture(pal, seed).save(p)
        made[name] = p

    # --- Werkzeuge: Vanilla-Silhouette, Mystit-Farben ---
    for t in TOOLS:
        van = Image.open(os.path.join(REF, f"tool_{t}.png")).convert("RGBA")
        rec = recolor(van, split_wood=True)
        assert list(van.getchannel("A").get_flattened_data()) == list(rec.getchannel("A").get_flattened_data())
        p = os.path.join(OUT_TEX, "item", f"mystit_{t}.png")
        rec.save(p)
        made[f"mystit_{t}"] = p

    # --- Ruestung am Spielermodell: Vanilla-Form, Mystit-Farben ---
    for layer, src in (("1", "l1_1.21.1.png"), ("2", "l2.png")):
        van = Image.open(os.path.join(REF, src)).convert("RGBA")
        rec = recolor(van)
        assert list(van.getchannel("A").get_flattened_data()) == list(rec.getchannel("A").get_flattened_data())
        # alte Ablage (bis 1.21.1)
        p = os.path.join(OUT_TEX, "models", "armor", f"mystit_layer_{layer}.png")
        rec.save(p)
        made[f"mystit_layer_{layer}"] = p
        # neue Ablage (1.21.2+): entity/equipment/<slot>/<name>.png
        slot = "humanoid" if layer == "1" else "humanoid_leggings"
        p2 = os.path.join(OUT_TEX, "entity", "equipment", slot, "mystit.png")
        os.makedirs(os.path.dirname(p2), exist_ok=True)
        rec.save(p2)
        made[f"equipment_{slot}"] = p2

    # --- Ruestungs-Items ---
    for piece in ARMOR_ITEMS:
        van = Image.open(os.path.join(REF, f"item_{piece}.png")).convert("RGBA")
        rec = recolor(van)
        p = os.path.join(OUT_TEX, "item", f"mystit_{piece}.png")
        rec.save(p)
        made[f"mystit_{piece}"] = p

    # --- Kristall-Formen: Barren, Nugget, Roherz, Block (eigene Silhouetten) ---
    import crystal_art
    for name, img in crystal_art.build().items():
        folder = "block" if name == "mystit_block" else "item"
        p = os.path.join(OUT_TEX, folder, name + ".png")
        img.save(p)
        made[name] = p

    # --- Modelle ---
    for blk in ("mystit_ore", "mystit_deepslate_ore", "mystit_block"):
        wr(os.path.join(PACK, "assets", NS, "models", "block", blk + ".json"),
           {"parent": "block/cube_all", "textures": {"all": f"{NS}:block/{blk}"}})
        wr(os.path.join(PACK, "assets", NS, "items", blk + ".json"),
           {"model": {"type": "minecraft:model", "model": f"{NS}:block/{blk}"}})

    for t in TOOLS:
        wr(os.path.join(PACK, "assets", NS, "models", "item", f"mystit_{t}.json"),
           {"parent": "item/handheld", "textures": {"layer0": f"{NS}:item/mystit_{t}"}})
        wr(os.path.join(PACK, "assets", NS, "items", f"mystit_{t}.json"),
           {"model": {"type": "minecraft:model", "model": f"{NS}:item/mystit_{t}"}})

    for it in ("mystit_ingot", "mystit_nugget", "raw_mystit"):
        wr(os.path.join(PACK, "assets", NS, "models", "item", f"{it}.json"),
           {"parent": "item/generated", "textures": {"layer0": f"{NS}:item/{it}"}})
        wr(os.path.join(PACK, "assets", NS, "items", f"{it}.json"),
           {"model": {"type": "minecraft:model", "model": f"{NS}:item/{it}"}})

    for piece in ARMOR_ITEMS:
        wr(os.path.join(PACK, "assets", NS, "models", "item", f"mystit_{piece}.json"),
           {"parent": "item/generated", "textures": {"layer0": f"{NS}:item/mystit_{piece}"}})
        wr(os.path.join(PACK, "assets", NS, "items", f"mystit_{piece}.json"),
           {"model": {"type": "minecraft:model", "model": f"{NS}:item/mystit_{piece}"}})

    # Equipment (1.21.2+): Ruestungstextur am Spielermodell
    wr(os.path.join(PACK, "assets", NS, "equipment", "mystit.json"), {
        "layers": {
            "humanoid": [{"texture": f"{NS}:mystit"}],
            "humanoid_leggings": [{"texture": f"{NS}:mystit"}],
        }
    })

    wr(os.path.join(PACK, "pack.mcmeta"), {"pack": {
        "description": "Mystit (MysticAttack) - Erz, Werkzeuge, Ruestung",
        "min_format": 88, "max_format": 97}})

    icon = ore_texture(STONE, 7).resize((64, 64), Image.NEAREST)
    icon.save(os.path.join(PACK, "pack.png"))

    # --- Kontaktbogen zur Sichtpruefung ---
    items = list(made.items())
    cols, zoom, pad, label_h = 4, 6, 12, 14
    cell = 16 * zoom
    rows_n = (len(items) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * (cell + pad) + pad,
                               rows_n * (cell + pad + label_h) + pad), (28, 28, 32, 255))
    dr = ImageDraw.Draw(sheet)
    for i, (name, path) in enumerate(items):
        cx = pad + (i % cols) * (cell + pad)
        cy = pad + (i // cols) * (cell + pad + label_h)
        for by in range(0, cell, 8):
            for bx in range(0, cell, 8):
                shade = (60, 60, 68, 255) if (bx // 8 + by // 8) % 2 else (44, 44, 50, 255)
                sheet.paste(Image.new("RGBA", (8, 8), shade), (cx + bx, cy + label_h + by))
        tile = Image.open(path).convert("RGBA").resize((cell, cell), Image.NEAREST)
        sheet.alpha_composite(tile, (cx, cy + label_h))
        dr.text((cx + 1, cy + 1), name, fill=(235, 235, 240, 255))
    sheet.save(os.path.join(ROOT, "contact_sheet.png"))

    # --- ZIP ---
    zpath = os.path.join(ROOT, "Mystit-Resourcepack.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(PACK):
            for f in files:
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, PACK))
    print("textures:", len(made))
    print("zip bytes:", os.path.getsize(zpath))


if __name__ == "__main__":
    main()
