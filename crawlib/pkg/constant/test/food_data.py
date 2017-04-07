#!/usr/bin/env python
# -*- coding: utf-8 -*-

metadata = {
    "classname": "Food",
    "attrs": ["id", "name"],
    "keys": ["name",],
    "collection": [
        {
            "classname": "Fruit",
            "attrs": ["id", "name"],
            "keys": ["name",],
            "collection": [
                {
                    "classname": "Apple",
                    "attrs": ["id", "name"],
                    "keys": ["name",],
                    "collection": [
                        {"data": {"id": 1, "name": "red apple"}},
                        {"data": {"id": 2, "name": "green apple"}}
                    ],
                    "data": {"id": 1, "name": "Apple"},
                },
                {
                    "classname": "Banana",
                    "attrs": ["id", "name"],
                    "keys": ["name",],
                    "collection": [
                        {"data": {"id": 1, "name": "yellow banana"}},
                        {"data": {"id": 2, "name": "green banana"}},
                    ],
                    "data": {"id": 2, "name": "Banana"},
                },
            ],
            "data": {"id": 1, "name": "Fruit"},
        },
        {
            "classname": "Meat",
            "attrs": ["id", "name"],
            "keys": ["name",],
            "collection": [
                {"data": {"id": 1, "name": "Pork"}},
                {"data": {"id": 2, "name": "Beef"}},
            ],
            "data": {"id": 2, "name": "Meat"},
        },
    ],
}

if __name__ == "__main__":
    from constant import gencode
    
    path = "food.py"
    with open(path, "wb") as f:
        f.write(gencode(metadata).encode("utf-8"))