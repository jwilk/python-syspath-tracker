# encoding=UTF-8

# Copyright © 2016-2024 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

'''
track who changes sys.path

Usage:

    syspath_tracker.install(file=sys.stderr)
'''

from __future__ import print_function

import difflib
import itertools
import sys

b''  # Python >= 2.6 is required

def strjoin(lst):
    return str.join('', lst)

def lformat(lst):
    return '[\n{0}]'.format(strjoin('  {0!r},\n'.format(item) for item in lst))

class state:
    sys_path = None
    file = None

def trace_sys_path(frame, event, arg):
    del event, arg
    try:
        sys_path = sys.path
    except AttributeError:
        # could happen during interpreter cleanup
        return
    if sys_path is None:
        # could happen during interpreter cleanup
        return
    if sys_path != state.sys_path:
        print('sys.path changed at {f.f_code.co_filename}:{f.f_lineno}:'.format(f=frame), end='', file=state.file)
        state.sys_path_f = lformat(state.sys_path).splitlines()
        sys_path_f = lformat(sys_path).splitlines()
        diff = difflib.unified_diff(state.sys_path_f, sys_path_f, n=9999)
        for line in itertools.islice(diff, 3, None):
            print(line, file=state.file)
        state.file.flush()
    state.sys_path = list(sys_path)
    return trace_sys_path

def install(file=sys.stderr):
    state.file = file
    state.sys_path = list(sys.path)
    print('Initial sys.path = ' + lformat(sys.path), file=file)
    sys.settrace(trace_sys_path)

__all__ = ['install']

# vim:ts=4 sts=4 sw=4 et
