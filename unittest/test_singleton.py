# -*- coding: utf-8 -*-
""" Tests for the SoCoSingletonBase and _ArgsSingleton classes in core"""

from __future__ import unicode_literals

import pytest
from soco.core import _SocoSingletonBase as Base

class ASingleton(Base):
    _identifier = 'arg'
    def __init__(self, arg, kw='4'):
        super(ASingleton, self).__init__()
        pass

class AnotherSingleton(ASingleton):
    # _identifier is also 'arg', by inheritance
    pass

class ThirdSingleton(Base):
    _class_group = 'somegroup'
    _identifier = 'arg'
    def __init__(self, arg):
        super(ThirdSingleton, self).__init__()
        pass

class FourthSingleton(ASingleton):
    _class_group = 'somegroup'
    pass

class FifthSingleton(Base):
    def __init__(self, arg):
        super(FifthSingleton, self).__init__()



def test_singleton():
    """ Check basic functionality. For a given arg, there is only one instance"""
    assert ASingleton('aa') is ASingleton('aa')
    assert ASingleton('aa') is not ASingleton('bb')
    # test for keyword params
    assert ASingleton('aa') is ASingleton('aa', kw='4')
    assert ASingleton('aa') is ASingleton(arg='aa')

def test_singleton_inherit():
    """ Check that subclasses behave properly"""
    assert ASingleton('aa') is not AnotherSingleton('aa')
    assert AnotherSingleton('aa') is AnotherSingleton('aa')
    assert AnotherSingleton('aa') is AnotherSingleton(arg='aa')

def test_class_group_singleton():
    """ Check _class_group functionality. For a given arg, instances of
    FourthGroup are Instances of ThirdGroup because they share a
    `_class_group` valur"""
    assert ThirdSingleton('aa') is FourthSingleton(arg='aa')
    assert ThirdSingleton('aa') is not FourthSingleton('bb')
    # Different class_group
    assert ThirdSingleton('aa') is not ASingleton('aa')

def test_no_identifier():
    assert FifthSingleton('aa') is FifthSingleton('aa')

