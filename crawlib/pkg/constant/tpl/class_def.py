#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .env import t_class_def, t_collection_class_def, t_code
    from ..pkg import name_convention
    from ..exc import ValidationError
except:
    from constant.tpl.env import t_class_def, t_collection_class_def, t_code
    from constant.pkg import name_convention
    from constant.exc import ValidationError

TAB = "|   "

class ClassDef(object):

    """

    **中文文档**

    是一个包含了类的定义的数据容器。

    用于生成定义类的代码。形如::

        class MyClass(Base):
            __attrs__ = ['id', 'name']

            def __init__(self, id=None, name=None):
                self.id = id
                self.name = name

    :param classname: 类名称
    :param attrs: 属性的列表
    :param keys: 可以被索引的属性列表
    :param collection: 子数据的名称
    :param inherit_from: 继承的类名
    :param parent: 父容器的ClassDef
    :attr IS_COLLECTION: 是否是一个数据容器类
    :attr kwargs_text: __init__(self, id=None, name=None) 中的参数定义部分
    """

    def __init__(self, classname=None, attrs=None, keys=None, 
                 data=None, 
                 collection=None,
                 inherit_from="Base",
                 parent=None,
                 indent=0,
                 **kwargs):
        self.classname = classname
        self.attrs = attrs
        self.keys = keys
        self.data = data
        self.collection = collection
        self.inherit_from = inherit_from
        self.parent = parent
        self.indent = indent
        
        if (self.classname is not None) and \
                (self.attrs is not None) and \
                (self.keys is not None) and \
                (self.collection is not None):
            self.IS_COLLECTION = True
            
            # validate classname
            if not name_convention.is_valid_class_name(self.classname):
                raise ValidationError("%r is not a valid class name" % self.classname)
            
            # validate attrs
            for attr in self.attrs:
                if not name_convention.is_valid_variable_name(attr):
                    raise ValidationError("%r is not a valid attribute name" % attr)
            
            # validate keys
            for key in self.keys:
                if not name_convention.is_valid_variable_name(key):
                    raise ValidationError("%r is not a valid attribute name" % key) 
            
            # validate attrs and keys
            if set.union(set(self.attrs), set(self.keys)) != set(self.attrs):
                raise ValidationError("keys (%r) has to be subset of attrs (%r)" % (
                    self.keys, self.attrs))
            
            # validate attrs and data
            for metadata in self.collection:
                for attr, value in metadata["data"].items():
                    try:
                        assert attr in self.attrs
                    except:
                        msg = "{classname}.__attrs__ = {attrs!r} doesn't match: {data!r}!".format(
                            classname=self.classname,
                            attrs=self.attrs,
                            data=metadata["data"],
                        )
                        raise ValidationError(msg)
            
            self.classnameCol = self.classname + "Col"
            self.variable_name_col = name_convention.to_variable_name(self.classname) + "_col"
            self.kwargs_text = "".join([", %s=None" % attr for attr in attrs])
            self.variable_name = name_convention.to_variable_name(self.classname)
            # 2 more indent for nested ClassDef
            self.collection = [
                ClassDef(
                    indent=self.indent+2, 
                    inherit_from=self.classname, 
                    parent=self,
                    **metadata) for metadata in self.collection
            ]
            
        elif (self.classname is None) and \
                (self.attrs is None) and \
                (self.keys is None) and \
                (self.collection is None) and \
                (self.data is not None):
            self.IS_COLLECTION = False
            self.classnameCol = self.parent.classname
            
    def __repr__(self):
        """Pretty print the definition.
        """
        text = "\n{classname}(\n{indent}{args},\n)".format(
            classname=self.__class__.__name__,
            indent=TAB,
            args=",\n{indent}".format(indent=TAB).join([
                "%s=%r" % ("classname", self.classname),
                "%s=%r" % ("attrs", self.attrs),
                "%s=%r" % ("keys", self.keys),
                "%s=%r" % ("data", self.data),
                "%s=%r" % ("collection", self.collection),
            ]),
        ).replace(")],", "),\n{indent}],".format(indent=TAB))
        
        lines = list()
        for line in text.split("\n"):
            indent = self.indent * TAB
            if not line.startswith(indent):
                line = indent + line
            
            # Trim right white space
            while 1:
                if line.endswith(TAB):
                    line = line[:-len(TAB)]
                else:
                    break
            
            lines.append(line)
            
        text = "\n".join(lines)
        return text

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def code_class_def(self):
        """Generate the code for definition of generic class::
        
            class Apple(Base):
                __attrs__ = ["id", "name"]
            
                def __init__(self, id=None, name=None):
                    self.id = id
                    self.name = name
        
        **中文文档**
        
        生成类的定义部分的代码。
        """
        return t_class_def.render(class_def=self)

    @property
    def code_collection_class_def(self):
        """Generate the code for definition of collection class::
        
            # Apple
            apple_name____red_apple = Apple(id=1, name="red apple")
            apple_name____green_apple = Apple(id=2, name="green apple")
            
            
            class AppleCol(Fruit):
                _collection = list()
            
                _collection.append(apple_name____red_apple)
                name____red_apple = apple_name____red_apple
            
                _collection.append(apple_name____green_apple)
                name____green_apple = apple_name____green_apple
                
        **中文文档**
        
        生成容器类的定义部分的代码。
        """
        return t_collection_class_def.render(class_def=self, 
                                             name_convention=name_convention)
    
    @staticmethod
    def code_new_instance(classname, attrs, data):
        """
        
        ``fruit_id____1 = Fruit(id=1, name='Apple')`` 中 
        ``Fruit(id=1, name='Apple')`` 部分。
        """
        code = "{classname}({kwargs})".format(
            classname=classname,
            kwargs=", ".join(["%s=%r" % (attr, data.get(attr)) \
                              for attr in attrs]),
        )
        return code
    
    @staticmethod
    def code_new_instance_varname(classname, attr, value):
        """
        
        ``fruit_id____1 = Fruit(id=1, name='Apple')`` 中 ``fruit_id____1`` 部分。
        """
        code = "{var}_{attr}____{value}".format(
            var=name_convention.to_variable_name(classname),
            attr=attr,
            value=name_convention.to_index_key(value),
        )
        return code
    
    def iter_class_def_recursive_depth_first(self):
        """
        
        **中文文档**
        
        深度优先, 遍历所有ClassDef。
        """
        if self.IS_COLLECTION:
            for class_def in self.collection:
                for cd in class_def.iter_class_def_recursive_depth_first():
                    yield cd
            yield self
    
    @property
    def all_class_def(self):
        """List all identical ``ClassDef`` instance, include sub class_def.
        """
        return list(self.iter_class_def_recursive_depth_first())
    
    def gencode(self, import_from="constant"):
        """Generate code。
        """
        return t_code.render(class_def=self, import_from=import_from)


def gencode(metadata, import_from="constant"):
    return ClassDef(**metadata).gencode(import_from=import_from)

    
if __name__ == "__main__":
    from constant.test.food_data import metadata
    from pprint import pprint
    
    class_def = ClassDef(**metadata)
    print(class_def.code)
    
    def test_code_new_instance():
        code = ClassDef.code_new_instance(
            "Fruit", ["id", "name"], {"id": 1, "name": "Apple"})
        assert code == "Fruit(id=1, name='Apple')"

#     test_code_new_instance()
    
    def test_code_new_instance_varname():
        code = ClassDef.code_new_instance_varname("Fruit", "id", 1)
        assert code == "fruit_id____1"
        
#     test_code_new_instance_varname()
    
    def test_code_class_def():
        """
        """
#         print(class_def.code_class_def)
#         print(class_def.collection[0].code_class_def)
#         print(class_def.collection[0].collection[0].code_class_def)
#         print(class_def.collection[0].collection[1].code_class_def)
#         print(class_def.collection[1].code_class_def)

    test_code_class_def()

    def test_collection_class_def_code():
        """
        """
#         print(class_def.code_collection_class_def)
#         print(class_def.collection[0].code_collection_class_def)
#         print(class_def.collection[1].code_collection_class_def)        
        
    test_collection_class_def_code()
    
    def test_iter_class_def_recursive_depth_first():
        l = [cd.classname for cd in class_def.\
             iter_class_def_recursive_depth_first()]
        assert l ==  ['Apple', 'Banana', 'Fruit', 'Meat', 'Food']
        
    test_iter_class_def_recursive_depth_first()