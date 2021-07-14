#!/usr/bin/python
# -*- coding: utf-8 -*-
def _init():
    global _global_dict
    _global_dict = {
    }


def set_value(name, value):
    global _global_dict
    _global_dict[name] = value


def get_value(name, defValue=0):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


# 缓存
def _init_cache():
    global _global_cache
    _global_cache = {
    }


def set_cache(name, value):
    global _global_cache
    _global_cache[name] = value


def get_cache(name, defValue=0):
    try:
        return _global_cache[name]
    except KeyError:
        return defValue
