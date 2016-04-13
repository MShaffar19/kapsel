# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2016, Continuum Analytics, Inc. All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import absolute_import, print_function

import os
import sys

from anaconda_project.project_file import DEFAULT_PROJECT_FILENAME
from anaconda_project.commands.main import _parse_args_and_run_subcommand
from anaconda_project.internal.test.tmpfile_utils import with_directory_contents


def _monkeypatch_pwd(monkeypatch, dirname):
    from os.path import abspath as real_abspath

    def mock_abspath(path):
        if path == ".":
            return dirname
        else:
            return real_abspath(path)

    monkeypatch.setattr('os.path.abspath', mock_abspath)


def _monkeypatch_isatty(monkeypatch, value):
    def mock_isatty():
        return value

    monkeypatch.setattr('sys.stdin.isatty', mock_isatty)


def test_init_in_pwd(capsys, monkeypatch):
    def check(dirname):
        _monkeypatch_pwd(monkeypatch, dirname)

        code = _parse_args_and_run_subcommand(['anaconda-project', 'init'])
        assert code == 0

        assert os.path.isfile(os.path.join(dirname, DEFAULT_PROJECT_FILENAME))

        out, err = capsys.readouterr()
        assert ("Project configuration is in %s\n" % (os.path.join(dirname, DEFAULT_PROJECT_FILENAME))) == out
        assert '' == err

    with_directory_contents(dict(), check)


def test_init_create_directory(capsys, monkeypatch):
    _monkeypatch_isatty(monkeypatch, True)

    def mock_input_yes(prompt):
        sys.stdout.write(prompt)
        return "yes"

    monkeypatch.setattr('anaconda_project.commands.console_utils._input', mock_input_yes)

    def check(dirname):
        subdir = os.path.join(dirname, "foo")

        code = _parse_args_and_run_subcommand(['anaconda-project', 'init', '--project', subdir])
        assert code == 0

        assert os.path.isfile(os.path.join(subdir, DEFAULT_PROJECT_FILENAME))

        out, err = capsys.readouterr()

        assert ("Create directory '%s'? Project configuration is in %s\n" %
                (subdir, os.path.join(subdir, DEFAULT_PROJECT_FILENAME))) == out
        assert '' == err

    with_directory_contents(dict(), check)


def test_init_do_not_create_directory(capsys, monkeypatch):
    _monkeypatch_isatty(monkeypatch, True)

    def mock_input_no(prompt):
        sys.stdout.write(prompt)
        return "no"

    monkeypatch.setattr('anaconda_project.commands.console_utils._input', mock_input_no)

    def check(dirname):
        subdir = os.path.join(dirname, "foo")

        code = _parse_args_and_run_subcommand(['anaconda-project', 'init', '--project', subdir])
        assert code == 1

        assert not os.path.isfile(os.path.join(subdir, DEFAULT_PROJECT_FILENAME))
        assert not os.path.isdir(subdir)

        out, err = capsys.readouterr()
        assert ("Create directory '%s'? " % subdir) == out
        assert ("Unable to load project:\n  Project directory '%s' does not exist.\n" % subdir) == err

    with_directory_contents(dict(), check)


def test_init_do_not_create_directory_not_interactive(capsys, monkeypatch):
    _monkeypatch_isatty(monkeypatch, False)

    def mock_input(prompt):
        raise RuntimeError("This should not have been called")

    monkeypatch.setattr('anaconda_project.commands.console_utils._input', mock_input)

    def check(dirname):
        subdir = os.path.join(dirname, "foo")

        code = _parse_args_and_run_subcommand(['anaconda-project', 'init', '--project', subdir])
        assert code == 1

        assert not os.path.isfile(os.path.join(subdir, DEFAULT_PROJECT_FILENAME))
        assert not os.path.isdir(subdir)

        out, err = capsys.readouterr()
        assert '' == out
        assert ("Unable to load project:\n  Project directory '%s' does not exist.\n" % subdir) == err

    with_directory_contents(dict(), check)
