# Mystit (MysticAttack) – Ressourcenpaket

Erz (Stein + Deepslate), fünf Werkzeuge, komplette Rüstung in Violett. Namespace
`mysticattack`, alles 16x16 Pixel, Vanilla-Optik.

## Inhalt

| ID | Typ | Datei |
| --- | --- | --- |
| `mysticattack:mystit_ore` | Block | `textures/block/mystit_ore.png` + `models/block/mystit_ore.json` |
| `mysticattack:mystit_deepslate_ore` | Block | `textures/block/mystit_deepslate_ore.png` |
| `mysticattack:mystit_sword` | Item | `textures/item/mystit_sword.png` (`item/handheld`) |
| `mysticattack:mystit_pickaxe` | Item | `textures/item/mystit_pickaxe.png` |
| `mysticattack:mystit_axe` | Item | `textures/item/mystit_axe.png` |
| `mysticattack:mystit_shovel` | Item | `textures/item/mystit_shovel.png` |
| `mysticattack:mystit_hoe` | Item | `textures/item/mystit_hoe.png` |
| `mysticattack:mystit_helmet` | Item | `textures/item/mystit_helmet.png` (`item/generated`) |
| `mysticattack:mystit_chestplate` | Item | `textures/item/mystit_chestplate.png` |
| `mysticattack:mystit_leggings` | Item | `textures/item/mystit_leggings.png` |
| `mysticattack:mystit_boots` | Item | `textures/item/mystit_boots.png` |
| `mysticattack:mystit_ingot` | Item | `textures/item/mystit_ingot.png` (`item/generated`) |
| `mysticattack:mystit_nugget` | Item | `textures/item/mystit_nugget.png` |
| `mysticattack:raw_mystit` | Item | `textures/item/raw_mystit.png` |
| `mysticattack:mystit_block` | Block | `textures/block/mystit_block.png` (+ `models/block/mystit_block.json`) |

Kette wie bei Eisen: Erz droppt `raw_mystit`, Schmelzen gibt `mystit_ingot`, neun Barren
ergeben `mystit_block`, ein Barren neun `mystit_nugget`.

Rüstung am Spielermodell: `equipment/mystit.json` plus
`textures/entity/equipment/humanoid/mystit.png` (Helm, Brust, Stiefel) und
`textures/entity/equipment/humanoid_leggings/mystit.png` (Beine) – das ist die Ablage ab
1.21.2. Für ältere Versionen liegen dieselben Bilder zusätzlich unter
`textures/models/armor/mystit_layer_1.png` und `_2.png`.

## Wichtig: ein Ressourcenpaket erzeugt keine neuen Items

Ein Ressourcenpaket kann nur Texturen und Modelle liefern. Die Blöcke und Items selbst müssen
serverseitig entstehen (Paper-Plugin), das Paket liefert dann nur das Aussehen:

- Items: Plugin setzt das Komponenten-Feld `minecraft:item_model` auf z. B.
  `mysticattack:mystit_sword` (1.21.2+) oder `custom_model_data` (älter).
- Block: `minecraft:note_block`/`mushroom_block`-Trick oder ein echtes Custom-Block-Plugin,
  Blockstate zeigt auf `mysticattack:block/mystit_ore`.
- Rüstung: das Plugin registriert das Equipment-Asset `mysticattack:mystit` als Rüstungsmaterial
  (bei 1.21.2+ über das `equipment`-Asset, das hier schon liegt).

## Palette

| Farbe | Hex |
| --- | --- |
| Outline | `#1A1028` |
| Kristall dunkel | `#3A1E58` |
| Kristall mittel | `#6E38A0` |
| Kristall hell | `#A66BE0` |
| Glanz | `#D9B6F5` |
| Holz hell / dunkel | `#7A5832` / `#4E3520` |

## Formen

Werkzeug- und Rüstungs-Silhouetten stammen von den Vanilla-Sprites; übernommen wurde nur die
Form (Alpha-Kanal unverändert), alle Farben sind neu. Erz-Texturen (Stein, Deepslate) und das
Kristallmuster sind eigenständig gebaut.

## Neu bauen

```
python3 build_pack.py     # erzeugt mystit-pack/, contact_sheet.png und das ZIP
```
