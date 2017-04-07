#!/usr/bin/env python
# -*- coding: utf-8 -*-

def validate_implementation(metadata, root_col):
    """
    
    **中文文档**
    
    检验最后的实现是否正确。
    """
    if "collection" in metadata:
        for meta, child_col in zip(metadata["collection"], root_col._collection):
            assert meta["data"] == child_col.to_dict()
            
            for key in metadata["keys"]:
                method = "getattr_by_%s" % key
                value = child_col.to_dict()[key]
                obj = getattr(root_col, method)(value)
                assert getattr(obj, key) == value
            
            validate_implementation(meta, child_col)


if __name__ == "__main__":
    from constant.test.food_data import metadata
    from constant.test.food import food_col

    validate_implementation(metadata, food_col)