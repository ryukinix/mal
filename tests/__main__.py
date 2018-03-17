#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#    Copyright © Manoel Vilela 2016
#
#    @project: Decorating
#     @author: Manoel Vilela
#      @email: manoel_vilela@engineer.com
#

import unittest
import sys
from os.path import dirname

__base__ = dirname(__file__)
sys.path.insert(0, dirname(__base__))

tests = unittest.defaultTestLoader.discover(__base__)
suite = unittest.defaultTestLoader.suiteClass(tests)
unittest.TextTestRunner(verbosity=2).run(suite)
