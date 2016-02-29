# -*- coding: utf-8; mode: sage -*-
from sage.repl.rich_output.output_catalog import OutputImagePng
from sage.repl.rich_output.backend_ipython import BackendIPythonCommandline
from sage.repl.rich_output import get_display_manager
from emacs_sage_shell import ip


class LastState(object):

    def __init__(self):
        # Used for image files
        self.filename = None
        self.result = None

last_state = LastState()


class BackendEmacsBabel(BackendIPythonCommandline):

    def _repr_(self):
        return "Emacs babel"

    def displayhook(self, plain_text, rich_output):
        if isinstance(rich_output, OutputImagePng):
            msg = rich_output.png.filename(ext='png')
            babel_filename = last_state.filename
            if babel_filename is not None:
                rich_output.png.save_as(babel_filename)
                msg = babel_filename
            return ({u'text/plain': msg}, {})
        else:
            return super(BackendEmacsBabel, self).displayhook(plain_text, rich_output)


backend_ob_sage = BackendEmacsBabel()
gdm = get_display_manager()


def run_cell_babel(code, filename=None):
    last_state.filename = filename
    last_state.result = None
    prv = gdm.switch_backend(backend_ob_sage, shell=ip)
    try:
        res = ip.run_cell(code)
        if res.success:
            last_state.result = res.result
            print 1
        else:
            print 0
    finally:
        gdm.switch_backend(prv, shell=ip)


def print_last_result():
    print last_state.result
