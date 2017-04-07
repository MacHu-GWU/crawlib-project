#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constant.base import Base

class Apple(Base):
    __attrs__ = ['id', 'name']

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
class Banana(Base):
    __attrs__ = ['id', 'name']

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
class Fruit(Base):
    __attrs__ = ['id', 'name']

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
class Meat(Base):
    __attrs__ = ['id', 'name']

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
class Food(Base):
    __attrs__ = ['id', 'name']

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
# Apple
apple_name____red_apple = Apple(id=1, name='red apple')
apple_name____green_apple = Apple(id=2, name='green apple')


class AppleCol(Fruit):
    _collection = list()
    
    _collection.append(apple_name____red_apple)
    name____red_apple = apple_name____red_apple
    
    _collection.append(apple_name____green_apple)
    name____green_apple = apple_name____green_apple
    
    
# Banana
banana_name____yellow_banana = Banana(id=1, name='yellow banana')
banana_name____green_banana = Banana(id=2, name='green banana')


class BananaCol(Fruit):
    _collection = list()
    
    _collection.append(banana_name____yellow_banana)
    name____yellow_banana = banana_name____yellow_banana
    
    _collection.append(banana_name____green_banana)
    name____green_banana = banana_name____green_banana
    
    
# Fruit
fruit_name____Apple = AppleCol(id=1, name='Apple')
fruit_name____Banana = BananaCol(id=2, name='Banana')


class FruitCol(Food):
    _collection = list()
    
    _collection.append(fruit_name____Apple)
    name____Apple = fruit_name____Apple
    
    _collection.append(fruit_name____Banana)
    name____Banana = fruit_name____Banana
    
    
# Meat
meat_name____Pork = Meat(id=1, name='Pork')
meat_name____Beef = Meat(id=2, name='Beef')


class MeatCol(Food):
    _collection = list()
    
    _collection.append(meat_name____Pork)
    name____Pork = meat_name____Pork
    
    _collection.append(meat_name____Beef)
    name____Beef = meat_name____Beef
    
    
# Food
food_name____Fruit = FruitCol(id=1, name='Fruit')
food_name____Meat = MeatCol(id=2, name='Meat')


class FoodCol(Base):
    _collection = list()
    
    _collection.append(food_name____Fruit)
    name____Fruit = food_name____Fruit
    
    _collection.append(food_name____Meat)
    name____Meat = food_name____Meat
    
    
food_col = FoodCol()