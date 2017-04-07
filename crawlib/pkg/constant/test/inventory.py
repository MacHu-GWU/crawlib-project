#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constant.base import Base

class Inventory(Base):
    __attrs__ = ['id', 'name', 'name_en', 'item_surfix', 'modifier']

    def __init__(self, id=None, name=None, name_en=None, item_surfix=None, modifier=None):
        self.id = id
        self.name = name
        self.name_en = name_en
        self.item_surfix = item_surfix
        self.modifier = modifier
        
# Inventory
inventory_id____0 = Inventory(id=0, name='无', name_en='None', item_surfix='', modifier=0.0)
inventory_id____1 = Inventory(id=1, name='头部', name_en='Head', item_surfix='之帽', modifier=1.0)
inventory_id____2 = Inventory(id=2, name='颈部', name_en='Neck', item_surfix='之项链', modifier=0.5625)
inventory_id____3 = Inventory(id=3, name='肩部', name_en='Shoulder', item_surfix='之肩甲', modifier=0.75)
inventory_id____4 = Inventory(id=4, name='衬衣', name_en='Shirt', item_surfix='之衬衣', modifier=0.0)
inventory_id____5 = Inventory(id=5, name='胸部', name_en='Chest', item_surfix='之胸甲', modifier=1.0)
inventory_id____6 = Inventory(id=6, name='腰部', name_en='Waist', item_surfix='之腰带', modifier=0.75)
inventory_id____7 = Inventory(id=7, name='腿部', name_en='Legs', item_surfix='之腿甲', modifier=1.0)
inventory_id____8 = Inventory(id=8, name='脚部', name_en='Feet', item_surfix='之靴', modifier=0.75)
inventory_id____9 = Inventory(id=9, name='手腕', name_en='Wrist', item_surfix='之护腕', modifier=0.5625)
inventory_id____10 = Inventory(id=10, name='手部', name_en='Hands', item_surfix='之手套', modifier=0.75)
inventory_id____11 = Inventory(id=11, name='手指', name_en='Finger', item_surfix='之戒', modifier=0.5625)
inventory_id____12 = Inventory(id=12, name='饰品', name_en='Trinkets', item_surfix='之饰物', modifier=0.68)
inventory_id____13 = Inventory(id=13, name='单手', name_en='OneHand', item_surfix='', modifier=0.421875)
inventory_id____14 = Inventory(id=14, name='盾牌', name_en='Shield', item_surfix='之盾', modifier=0.5625)
inventory_id____15 = Inventory(id=15, name='弓 弩', name_en='Bows', item_surfix='', modifier=0.31640625)
inventory_id____16 = Inventory(id=16, name='背部', name_en='Back', item_surfix='之披风', modifier=0.5625)
inventory_id____17 = Inventory(id=17, name='双手武器', name_en='TwoHand', item_surfix='', modifier=1.0)
inventory_id____18 = Inventory(id=18, name='袋子', name_en='Bags', item_surfix='之背包', modifier=0.0)
inventory_id____19 = Inventory(id=19, name='徽章', name_en='Tabard', item_surfix='之徽章', modifier=0.0)
inventory_id____20 = Inventory(id=20, name='长袍', name_en='Robe', item_surfix='之袍', modifier=1.0)
inventory_id____21 = Inventory(id=21, name='主手武器', name_en='MainHand', item_surfix='', modifier=0.421875)
inventory_id____22 = Inventory(id=22, name='副手武器', name_en='OffHand', item_surfix='', modifier=0.421875)
inventory_id____23 = Inventory(id=23, name='副手物品', name_en='Tomb', item_surfix='', modifier=0.5625)
inventory_id____24 = Inventory(id=24, name='弹药', name_en='Waist', item_surfix='', modifier=0.0)
inventory_id____25 = Inventory(id=25, name='投掷武器和魔杖', name_en='Thrown', item_surfix='', modifier=0.31640625)
inventory_id____26 = Inventory(id=26, name='枪械', name_en='Gun', item_surfix='之枪', modifier=0.31640625)
inventory_id____27 = Inventory(id=27, name='箭袋', name_en='Quiver', item_surfix='之箭袋', modifier=0.0)
inventory_id____28 = Inventory(id=28, name='图腾 圣物 圣契 符印', name_en='Waist', item_surfix='', modifier=0.31640625)


class InventoryCol(Base):
    _collection = list()
    
    _collection.append(inventory_id____0)
    id____0 = inventory_id____0
    name____无 = inventory_id____0
    name_en____None = inventory_id____0
    item_surfix____ = inventory_id____0
    modifier____0d0 = inventory_id____0
    
    _collection.append(inventory_id____1)
    id____1 = inventory_id____1
    name____头部 = inventory_id____1
    name_en____Head = inventory_id____1
    item_surfix____之帽 = inventory_id____1
    modifier____1d0 = inventory_id____1
    
    _collection.append(inventory_id____2)
    id____2 = inventory_id____2
    name____颈部 = inventory_id____2
    name_en____Neck = inventory_id____2
    item_surfix____之项链 = inventory_id____2
    modifier____0d5625 = inventory_id____2
    
    _collection.append(inventory_id____3)
    id____3 = inventory_id____3
    name____肩部 = inventory_id____3
    name_en____Shoulder = inventory_id____3
    item_surfix____之肩甲 = inventory_id____3
    modifier____0d75 = inventory_id____3
    
    _collection.append(inventory_id____4)
    id____4 = inventory_id____4
    name____衬衣 = inventory_id____4
    name_en____Shirt = inventory_id____4
    item_surfix____之衬衣 = inventory_id____4
    modifier____0d0 = inventory_id____4
    
    _collection.append(inventory_id____5)
    id____5 = inventory_id____5
    name____胸部 = inventory_id____5
    name_en____Chest = inventory_id____5
    item_surfix____之胸甲 = inventory_id____5
    modifier____1d0 = inventory_id____5
    
    _collection.append(inventory_id____6)
    id____6 = inventory_id____6
    name____腰部 = inventory_id____6
    name_en____Waist = inventory_id____6
    item_surfix____之腰带 = inventory_id____6
    modifier____0d75 = inventory_id____6
    
    _collection.append(inventory_id____7)
    id____7 = inventory_id____7
    name____腿部 = inventory_id____7
    name_en____Legs = inventory_id____7
    item_surfix____之腿甲 = inventory_id____7
    modifier____1d0 = inventory_id____7
    
    _collection.append(inventory_id____8)
    id____8 = inventory_id____8
    name____脚部 = inventory_id____8
    name_en____Feet = inventory_id____8
    item_surfix____之靴 = inventory_id____8
    modifier____0d75 = inventory_id____8
    
    _collection.append(inventory_id____9)
    id____9 = inventory_id____9
    name____手腕 = inventory_id____9
    name_en____Wrist = inventory_id____9
    item_surfix____之护腕 = inventory_id____9
    modifier____0d5625 = inventory_id____9
    
    _collection.append(inventory_id____10)
    id____10 = inventory_id____10
    name____手部 = inventory_id____10
    name_en____Hands = inventory_id____10
    item_surfix____之手套 = inventory_id____10
    modifier____0d75 = inventory_id____10
    
    _collection.append(inventory_id____11)
    id____11 = inventory_id____11
    name____手指 = inventory_id____11
    name_en____Finger = inventory_id____11
    item_surfix____之戒 = inventory_id____11
    modifier____0d5625 = inventory_id____11
    
    _collection.append(inventory_id____12)
    id____12 = inventory_id____12
    name____饰品 = inventory_id____12
    name_en____Trinkets = inventory_id____12
    item_surfix____之饰物 = inventory_id____12
    modifier____0d68 = inventory_id____12
    
    _collection.append(inventory_id____13)
    id____13 = inventory_id____13
    name____单手 = inventory_id____13
    name_en____OneHand = inventory_id____13
    item_surfix____ = inventory_id____13
    modifier____0d421875 = inventory_id____13
    
    _collection.append(inventory_id____14)
    id____14 = inventory_id____14
    name____盾牌 = inventory_id____14
    name_en____Shield = inventory_id____14
    item_surfix____之盾 = inventory_id____14
    modifier____0d5625 = inventory_id____14
    
    _collection.append(inventory_id____15)
    id____15 = inventory_id____15
    name____弓_弩 = inventory_id____15
    name_en____Bows = inventory_id____15
    item_surfix____ = inventory_id____15
    modifier____0d31640625 = inventory_id____15
    
    _collection.append(inventory_id____16)
    id____16 = inventory_id____16
    name____背部 = inventory_id____16
    name_en____Back = inventory_id____16
    item_surfix____之披风 = inventory_id____16
    modifier____0d5625 = inventory_id____16
    
    _collection.append(inventory_id____17)
    id____17 = inventory_id____17
    name____双手武器 = inventory_id____17
    name_en____TwoHand = inventory_id____17
    item_surfix____ = inventory_id____17
    modifier____1d0 = inventory_id____17
    
    _collection.append(inventory_id____18)
    id____18 = inventory_id____18
    name____袋子 = inventory_id____18
    name_en____Bags = inventory_id____18
    item_surfix____之背包 = inventory_id____18
    modifier____0d0 = inventory_id____18
    
    _collection.append(inventory_id____19)
    id____19 = inventory_id____19
    name____徽章 = inventory_id____19
    name_en____Tabard = inventory_id____19
    item_surfix____之徽章 = inventory_id____19
    modifier____0d0 = inventory_id____19
    
    _collection.append(inventory_id____20)
    id____20 = inventory_id____20
    name____长袍 = inventory_id____20
    name_en____Robe = inventory_id____20
    item_surfix____之袍 = inventory_id____20
    modifier____1d0 = inventory_id____20
    
    _collection.append(inventory_id____21)
    id____21 = inventory_id____21
    name____主手武器 = inventory_id____21
    name_en____MainHand = inventory_id____21
    item_surfix____ = inventory_id____21
    modifier____0d421875 = inventory_id____21
    
    _collection.append(inventory_id____22)
    id____22 = inventory_id____22
    name____副手武器 = inventory_id____22
    name_en____OffHand = inventory_id____22
    item_surfix____ = inventory_id____22
    modifier____0d421875 = inventory_id____22
    
    _collection.append(inventory_id____23)
    id____23 = inventory_id____23
    name____副手物品 = inventory_id____23
    name_en____Tomb = inventory_id____23
    item_surfix____ = inventory_id____23
    modifier____0d5625 = inventory_id____23
    
    _collection.append(inventory_id____24)
    id____24 = inventory_id____24
    name____弹药 = inventory_id____24
    name_en____Waist = inventory_id____24
    item_surfix____ = inventory_id____24
    modifier____0d0 = inventory_id____24
    
    _collection.append(inventory_id____25)
    id____25 = inventory_id____25
    name____投掷武器和魔杖 = inventory_id____25
    name_en____Thrown = inventory_id____25
    item_surfix____ = inventory_id____25
    modifier____0d31640625 = inventory_id____25
    
    _collection.append(inventory_id____26)
    id____26 = inventory_id____26
    name____枪械 = inventory_id____26
    name_en____Gun = inventory_id____26
    item_surfix____之枪 = inventory_id____26
    modifier____0d31640625 = inventory_id____26
    
    _collection.append(inventory_id____27)
    id____27 = inventory_id____27
    name____箭袋 = inventory_id____27
    name_en____Quiver = inventory_id____27
    item_surfix____之箭袋 = inventory_id____27
    modifier____0d0 = inventory_id____27
    
    _collection.append(inventory_id____28)
    id____28 = inventory_id____28
    name____图腾_圣物_圣契_符印 = inventory_id____28
    name_en____Waist = inventory_id____28
    item_surfix____ = inventory_id____28
    modifier____0d31640625 = inventory_id____28
    
    
inventory_col = InventoryCol()