# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2016, Continuum Analytics, Inc. All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import absolute_import, print_function, unicode_literals

import codecs
import os
import pytest

from conda_kapsel.commands.bug_handler import handle_bugs


def test_no_bug_happens(capsys):
    def unbuggy_main():
        print("hi")
        return 0

    code = handle_bugs(unbuggy_main, program_name="myprogram", details_dict=dict())
    assert code is 0

    out, err = capsys.readouterr()

    assert 'hi\n' == out
    assert '' == err


def test_bug_handling(capsys):
    def buggy_main():
        raise AssertionError("It did not work")

    # we name the program something wonky to be sure we slugify
    # it, and use a non-BMP unicode char to be sure we handle that
    code = handle_bugs(buggy_main,
                       program_name=u"my$ 🌟program",
                       details_dict=dict(thing1="foo",
                                         thing2="bar",
                                         thing3=u"🌟"))

    assert code is 1
    out, err = capsys.readouterr()

    assert '' == out
    assert err.startswith(u"""An unexpected error occurred, most likely a bug in my$ 🌟program.
    (The error was: AssertionError: It did not work)
Details about the error were saved to """)
    filename = err.split()[-1]
    assert filename.endswith(".txt")
    assert os.path.basename(filename).startswith("bug_details_my---program_")
    assert os.path.isfile(filename)

    with codecs.open(filename, 'r', 'utf-8') as f:
        lines = f.readlines()
        report = "".join(lines)

    # we can't easily test the exact value (it contains line
    # numbers of full file paths), but check the major items are
    # in there.
    assert report.startswith(u"Bug details for my$ 🌟program error on ")
    assert 'sys.argv' in report
    assert 'test_bug_handler.py' in report
    assert 'Traceback' in report
    assert 'AssertionError' in report
    assert 'It did not work' in report

    os.remove(filename)


def test_bug_handling_is_buggy(capsys, monkeypatch):
    def buggy_main():
        raise AssertionError("It did not work")

    def mock_temporary_file(*args, **kwargs):
        raise IOError("no temporary file")

    monkeypatch.setattr('tempfile.NamedTemporaryFile', mock_temporary_file)

    with pytest.raises(AssertionError) as exc_info:
        handle_bugs(buggy_main, program_name=u"myprogram", details_dict=dict())
    assert 'It did not work' == str(exc_info.value)

    out, err = capsys.readouterr()

    assert '' == out
    assert """An unexpected error occurred, most likely a bug in myprogram.
    (The error was: AssertionError: It did not work)
""" == err


def test_keyboard_interrupt(capsys):
    def buggy_main():
        raise KeyboardInterrupt("ctrl-c")

    code = handle_bugs(buggy_main, program_name=u"myprogram", details_dict=dict())

    assert code is 1
    out, err = capsys.readouterr()

    assert '' == out
    assert 'myprogram was interrupted.\n' == err
