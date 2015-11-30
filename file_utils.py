from __future__ import print_function

import fnmatch
import os
import shutil


def ifind_files(start='.', pattern='*'):
    abs_start = os.path.abspath(start)
    for root, dirnames, filenames in os.walk(abs_start):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def find_files(start='.', pattern='*'):
    return list(ifind_files(start, pattern))


def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        print("Copied {} to {}.".format(src, dst))
    except Exception as e:
        print("Copying {} to {} failed: {}!".format(src, dst, e))
