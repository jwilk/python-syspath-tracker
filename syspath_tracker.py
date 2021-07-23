# encoding=UTF-8

# Copyright © 2016-2021 Jakub Wilk <jwilk@jwilk.net>
# SPDX-License-Identifier: MIT

from __future__ import print_function

import itertools
import difflib
import sys

b''  # Python >= 2.6 is required

def lformat(lst):
    return '[\n{0}]'.format(''.join('  {0!r},\n'.format(item) for item in lst))

orig_sys_path = None
tfile = None

def trace_sys_path(frame, event, arg):
    global orig_sys_path
    try:
        sys_path = sys.path
    except AttributeError:
        # could happen during interpreter cleanup
        return
    if sys_path is None:
        # could happen during interpreter cleanup
        return
    if sys_path != orig_sys_path:
        print('sys.path changed at {f.f_code.co_filename}:{f.f_lineno}:'.format(f=frame), end='', file=tfile)
        orig_sys_path_f = lformat(orig_sys_path).splitlines()
        sys_path_f = lformat(sys_path).splitlines()
        diff = difflib.unified_diff(orig_sys_path_f, sys_path_f, n=9999)
        for line in itertools.islice(diff, 3, None):
            print(line, file=tfile)
        tfile.flush()
    orig_sys_path = list(sys_path)
    return trace_sys_path

def install(file=sys.stderr):
    global tfile
    global orig_sys_path
    tfile = file
    orig_sys_path = list(sys.path)
    print('Initial sys.path = ' + lformat(sys.path), file=file)
    sys.settrace(trace_sys_path)

__all__ = ['install']

# vim:ts=4 sts=4 sw=4 et
