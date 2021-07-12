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
