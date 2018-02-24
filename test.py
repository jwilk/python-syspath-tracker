# encoding=UTF-8

# Copyright © 2016-2018 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

import sys

import syspath_tracker

del syspath_tracker  # hi, pyflakes!

def f():
    sys.path += ['/eggs']

def g():
    del sys.path[0]

f()
g()

# vim:ts=4 sts=4 sw=4 et
