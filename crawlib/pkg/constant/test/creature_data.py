#!/usr/bin/env python
# -*- coding: utf-8 -*-

metadata = {
    "classname": "Creature",
    "attrs": ["id", "name"],
    "keys": ["name",],
    "collection": [
        {"data": {"id": 0, "name": "None"}},
        {"data": {"id": 1, "name": "Beast"}},
        {"data": {"id": 2, "name": "Dragonkin"}},
        {"data": {"id": 3, "name": "Demon"}},
        {"data": {"id": 4, "name": "Elemental"}},
        {"data": {"id": 5, "name": "Giant"}},
        {"data": {"id": 6, "name": "Undead"}},
        {"data": {"id": 7, "name": "Humanoid"}},
        {"data": {"id": 8, "name": "Critter"}},
        {"data": {"id": 9, "name": "Mechanical"}},
        {"data": {"id": 10, "name": "NotSpecified"}},
        {"data": {"id": 11, "name": "Totem"}},
        {"data": {"id": 12, "name": "NonCombatPet"}},
        {"data": {"id": 13, "name": "GasCloud"}},
    ],
}

if __name__ == "__main__":
    from constant import gencode
    
    path = "creature.py"
    with open(path, "wb") as f:
        f.write(gencode(metadata).encode("utf-8"))