from __future__ import print_function

import os
from file_utils import copy_file, ifind_files
from subprocess import Popen, PIPE, STDOUT

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')

from .configuration import Configuration
cfg = Configuration()


def copy_mobi(lib_dir, dest_dir, make_author_dir=True):
    for src, author, book in find_book_and_author(lib_dir):
        if make_author_dir:
            dst = os.path.abspath(os.path.join(dest_dir, author, book))
            try:
                os.makedirs(os.path.split(dst)[0])
            except OSError:
                pass
        else:
            dst = os.path.abspath(os.path.join(dest_dir, book))

        copy_file(src, dst)


def find_book_and_author(lib_dir=cfg['CALIBRE_LIBRARY'], file_type='*.mobi'):
    lib_dir = os.path.abspath(lib_dir)
    author_position = len(lib_dir.split('/'))
    book_position = -1

    for book_path in ifind_files(lib_dir, file_type):
        chunks = book_path.split('/')
        yield book_path, chunks[author_position], chunks[book_position]


def convert(book_path, target_dir='.', target_ext='mobi'):
    book_filename = os.path.splitext(os.path.basename(book_path))[0]
    dst = os.path.join(target_dir, '.'.join([book_filename, target_ext]))

    p = Popen([cfg['CONVERTER'], book_path, dst], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
    p.communicate()
    if p.returncode != 0:
        print("Something went wrong, return code was {}".format(p.returncode))


def gather_epub(lib_dir=cfg['CALIBRE_LIBRARY'], target_dir='.'):
    for src in ifind_files(lib_dir, pattern='*.epub'):
        dst = os.path.abspath(os.path.join(target_dir, os.path.split(src)[0]))
        copy_file(src, dst)


def convert_epubs_to_mobi(source_dir, target_dir):
    for book_path in ifind_files(source_dir, '*.epub'):
        convert(book_path, target_dir)
