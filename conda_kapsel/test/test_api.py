# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2016, Continuum Analytics, Inc. All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------
from __future__ import absolute_import

import inspect

from conda_kapsel import api
from conda_kapsel import provide


def _verify_args_match(function1, function2, ignored=('self', )):
    f1spec = inspect.getargspec(function1)
    f2spec = inspect.getargspec(function2)
    args1 = list(f1spec.args)
    args2 = list(f2spec.args)
    for param in ignored:
        if param in args1:
            args1.remove(param)
        if param in args2:
            args2.remove(param)
    assert args1 == args2


def test_create_project(monkeypatch):
    params = dict(args=(), kwargs=dict())

    def mock_create_project(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.create', mock_create_project)

    p = api.AnacondaProject()
    kwargs = dict(directory_path=1, make_directory=2, name='foo', icon='bar', description='blah')
    result = p.create_project(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_load_project(monkeypatch):
    from conda_kapsel.project import Project
    _verify_args_match(api.AnacondaProject.load_project, Project.__init__, ignored=['self', 'plugin_registry'])

    class MockProject(object):
        def __init__(self, *args, **kwargs):
            self.kwargs = kwargs

    monkeypatch.setattr('conda_kapsel.project.Project', MockProject)
    p = api.AnacondaProject()
    kwargs = dict(directory_path='foo')
    project = p.load_project(**kwargs)
    assert kwargs == project.kwargs


def _monkeypatch_prepare_without_interaction(monkeypatch):
    params = dict(args=(), kwargs=dict())

    def mock_prepare_without_interaction(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.prepare.prepare_without_interaction', mock_prepare_without_interaction)
    return params


def _test_prepare_without_interaction(monkeypatch, api_method, provide_mode):
    from conda_kapsel.prepare import prepare_without_interaction
    _verify_args_match(
        getattr(api.AnacondaProject, api_method),
        prepare_without_interaction,
        ignored=['self', 'mode', 'provide_whitelist'])

    params = _monkeypatch_prepare_without_interaction(monkeypatch)
    p = api.AnacondaProject()
    kwargs = dict(project=43,
                  environ=57,
                  env_spec_name='someenv',
                  command_name='foo',
                  command=1234,
                  extra_command_args=['1', '2'])
    result = getattr(p, api_method)(**kwargs)
    assert 42 == result
    assert params['kwargs']['mode'] == provide_mode
    del params['kwargs']['mode']
    assert kwargs == params['kwargs']


def test_prepare_project_locally(monkeypatch):
    _test_prepare_without_interaction(monkeypatch, 'prepare_project_locally', provide.PROVIDE_MODE_DEVELOPMENT)


def test_prepare_project_production(monkeypatch):
    _test_prepare_without_interaction(monkeypatch, 'prepare_project_production', provide.PROVIDE_MODE_PRODUCTION)


def test_prepare_project_check(monkeypatch):
    _test_prepare_without_interaction(monkeypatch, 'prepare_project_check', provide.PROVIDE_MODE_CHECK)


def test_prepare_project_browser(monkeypatch):
    from conda_kapsel.prepare import prepare_with_browser_ui
    _verify_args_match(api.AnacondaProject.prepare_project_browser,
                       prepare_with_browser_ui,
                       ignored=['self', 'keep_going_until_success'])

    params = dict(args=(), kwargs=dict())

    def mock_prepare_with_browser_ui(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.prepare.prepare_with_browser_ui', mock_prepare_with_browser_ui)
    p = api.AnacondaProject()
    kwargs = dict(project=43,
                  environ=57,
                  env_spec_name='someenv',
                  command_name='foo',
                  command=1234,
                  extra_command_args=['1', '2'],
                  io_loop=156,
                  show_url=8909)
    result = p.prepare_project_browser(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_unprepare(monkeypatch):
    from conda_kapsel.prepare import unprepare
    _verify_args_match(api.AnacondaProject.unprepare, unprepare)

    params = dict(args=(), kwargs=dict())

    def mock_unprepare(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.prepare.unprepare', mock_unprepare)
    p = api.AnacondaProject()
    kwargs = dict(project=43, prepare_result=44, whitelist=45)
    result = p.unprepare(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_set_properties(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.set_properties, project_ops.set_properties)

    params = dict(args=(), kwargs=dict())

    def mock_set_properties(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.set_properties', mock_set_properties)

    p = api.AnacondaProject()
    kwargs = dict(project=43, name='foo', icon='bar', description='blah')
    result = p.set_properties(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_add_variables(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.add_variables, project_ops.add_variables)

    params = dict(args=(), kwargs=dict())

    def mock_add_variables(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.add_variables', mock_add_variables)

    p = api.AnacondaProject()
    kwargs = dict(project=43, vars_to_add=45, defaults=12345)
    result = p.add_variables(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_remove_variables(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.remove_variables, project_ops.remove_variables)

    params = dict(args=(), kwargs=dict())

    def mock_remove_variables(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.remove_variables', mock_remove_variables)

    p = api.AnacondaProject()
    kwargs = dict(project=43, vars_to_remove=45, env_spec_name='foo')
    result = p.remove_variables(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_set_variables(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.set_variables, project_ops.set_variables)

    params = dict(args=(), kwargs=dict())

    def mock_set_variables(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.set_variables', mock_set_variables)

    p = api.AnacondaProject()
    kwargs = dict(project=43, vars_and_values=45, env_spec_name='foo')
    result = p.set_variables(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_unset_variables(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.unset_variables, project_ops.unset_variables)

    params = dict(args=(), kwargs=dict())

    def mock_unset_variables(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.unset_variables', mock_unset_variables)

    p = api.AnacondaProject()
    kwargs = dict(project=43, vars_to_unset=45, env_spec_name='foo')
    result = p.unset_variables(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_add_download(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.add_download, project_ops.add_download)

    params = dict(args=(), kwargs=dict())

    def mock_add_download(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.add_download', mock_add_download)

    p = api.AnacondaProject()
    kwargs = dict(project=43, env_var='boo', url='baz', filename="fname", hash_algorithm="md5", hash_value="foo")
    result = p.add_download(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_remove_download(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.remove_download, project_ops.remove_download)

    params = dict(args=(), kwargs=dict())

    def mock_remove_download(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.remove_download', mock_remove_download)

    p = api.AnacondaProject()
    kwargs = dict(project=43, prepare_result='winnebago', env_var='boo')
    result = p.remove_download(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_add_env_spec(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.add_env_spec, project_ops.add_env_spec)

    params = dict(args=(), kwargs=dict())

    def mock_add_env_spec(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.add_env_spec', mock_add_env_spec)

    p = api.AnacondaProject()
    kwargs = dict(project=43, name='foo', packages=['a'], channels=['b'])
    result = p.add_env_spec(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_remove_env_spec(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.remove_env_spec, project_ops.remove_env_spec)

    params = dict(args=(), kwargs=dict())

    def mock_remove_env_spec(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.remove_env_spec', mock_remove_env_spec)

    p = api.AnacondaProject()
    kwargs = dict(project=43, name='foo')
    result = p.remove_env_spec(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_export_env_spec(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.export_env_spec, project_ops.export_env_spec)

    params = dict(args=(), kwargs=dict())

    def mock_export_env_spec(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.export_env_spec', mock_export_env_spec)

    p = api.AnacondaProject()
    kwargs = dict(project=43, name='foo', filename='bar')
    result = p.export_env_spec(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_add_packages(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.add_packages, project_ops.add_packages)

    params = dict(args=(), kwargs=dict())

    def mock_add_packages(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.add_packages', mock_add_packages)

    p = api.AnacondaProject()
    kwargs = dict(project=43, env_spec_name='foo', packages=['a'], channels=['b'])
    result = p.add_packages(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_remove_packages(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.remove_packages, project_ops.remove_packages)

    params = dict(args=(), kwargs=dict())

    def mock_remove_packages(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.remove_packages', mock_remove_packages)

    p = api.AnacondaProject()
    kwargs = dict(project=43, env_spec_name='foo', packages=['a'])
    result = p.remove_packages(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_add_command(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.add_command, project_ops.add_command)

    params = dict(args=(), kwargs=dict())

    def mock_add_command(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.add_command', mock_add_command)

    p = api.AnacondaProject()

    kwargs = dict(project=43,
                  command_type='bokeh_app',
                  name='name',
                  command='file.py',
                  env_spec_name='foo',
                  supports_http_options=True)
    result = p.add_command(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_update_command(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.update_command, project_ops.update_command)

    params = dict(args=(), kwargs=dict())

    def mock_update_command(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.update_command', mock_update_command)

    p = api.AnacondaProject()

    kwargs = dict(project=43, command_type='bokeh_app', name='name', command='file.py', new_name='foo')
    result = p.update_command(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_remove_command(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.remove_command, project_ops.remove_command)

    params = dict(args=(), kwargs=dict())

    def mock_remove_command(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.remove_command', mock_remove_command)

    p = api.AnacondaProject()

    kwargs = dict(project=43, name='name')
    result = p.remove_command(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_add_service(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.add_service, project_ops.add_service)

    params = dict(args=(), kwargs=dict())

    def mock_add_service(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.add_service', mock_add_service)

    p = api.AnacondaProject()
    kwargs = dict(project=43, service_type='abc', variable_name='xyz')
    result = p.add_service(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_remove_service(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.remove_service, project_ops.remove_service)

    params = dict(args=(), kwargs=dict())

    def mock_remove_service(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.remove_service', mock_remove_service)

    p = api.AnacondaProject()
    kwargs = dict(project=43, prepare_result=123, variable_name='xyz')
    result = p.remove_service(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_clean(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.clean, project_ops.clean)

    params = dict(args=(), kwargs=dict())

    def mock_clean(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.clean', mock_clean)

    p = api.AnacondaProject()
    kwargs = dict(project=43, prepare_result=123)
    result = p.clean(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_archive(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.archive, project_ops.archive)

    params = dict(args=(), kwargs=dict())

    def mock_archive(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.archive', mock_archive)

    p = api.AnacondaProject()
    kwargs = dict(project=43, filename=123)
    result = p.archive(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_unarchive(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.unarchive, project_ops.unarchive)

    params = dict(args=(), kwargs=dict())

    def mock_unarchive(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.unarchive', mock_unarchive)

    p = api.AnacondaProject()
    kwargs = dict(filename=43, project_dir=123, parent_dir=456)
    result = p.unarchive(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']


def test_upload(monkeypatch):
    import conda_kapsel.project_ops as project_ops
    _verify_args_match(api.AnacondaProject.upload, project_ops.upload)

    params = dict(args=(), kwargs=dict())

    def mock_upload(*args, **kwargs):
        params['args'] = args
        params['kwargs'] = kwargs
        return 42

    monkeypatch.setattr('conda_kapsel.project_ops.upload', mock_upload)

    p = api.AnacondaProject()
    kwargs = dict(project=43, site=123, token=456, username=789, log_level='LOTS')
    result = p.upload(**kwargs)
    assert 42 == result
    assert kwargs == params['kwargs']
