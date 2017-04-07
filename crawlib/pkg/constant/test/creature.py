#!/usr/bin/env python
# -*- coding: utf-8 -*-

from constant.base import Base

class Creature(Base):
    __attrs__ = ['id', 'name']

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        
# Creature
creature_name____None = Creature(id=0, name='None')
creature_name____Beast = Creature(id=1, name='Beast')
creature_name____Dragonkin = Creature(id=2, name='Dragonkin')
creature_name____Demon = Creature(id=3, name='Demon')
creature_name____Elemental = Creature(id=4, name='Elemental')
creature_name____Giant = Creature(id=5, name='Giant')
creature_name____Undead = Creature(id=6, name='Undead')
creature_name____Humanoid = Creature(id=7, name='Humanoid')
creature_name____Critter = Creature(id=8, name='Critter')
creature_name____Mechanical = Creature(id=9, name='Mechanical')
creature_name____NotSpecified = Creature(id=10, name='NotSpecified')
creature_name____Totem = Creature(id=11, name='Totem')
creature_name____NonCombatPet = Creature(id=12, name='NonCombatPet')
creature_name____GasCloud = Creature(id=13, name='GasCloud')


class CreatureCol(Base):
    _collection = list()
    
    _collection.append(creature_name____None)
    name____None = creature_name____None
    
    _collection.append(creature_name____Beast)
    name____Beast = creature_name____Beast
    
    _collection.append(creature_name____Dragonkin)
    name____Dragonkin = creature_name____Dragonkin
    
    _collection.append(creature_name____Demon)
    name____Demon = creature_name____Demon
    
    _collection.append(creature_name____Elemental)
    name____Elemental = creature_name____Elemental
    
    _collection.append(creature_name____Giant)
    name____Giant = creature_name____Giant
    
    _collection.append(creature_name____Undead)
    name____Undead = creature_name____Undead
    
    _collection.append(creature_name____Humanoid)
    name____Humanoid = creature_name____Humanoid
    
    _collection.append(creature_name____Critter)
    name____Critter = creature_name____Critter
    
    _collection.append(creature_name____Mechanical)
    name____Mechanical = creature_name____Mechanical
    
    _collection.append(creature_name____NotSpecified)
    name____NotSpecified = creature_name____NotSpecified
    
    _collection.append(creature_name____Totem)
    name____Totem = creature_name____Totem
    
    _collection.append(creature_name____NonCombatPet)
    name____NonCombatPet = creature_name____NonCombatPet
    
    _collection.append(creature_name____GasCloud)
    name____GasCloud = creature_name____GasCloud
    
    
creature_col = CreatureCol()