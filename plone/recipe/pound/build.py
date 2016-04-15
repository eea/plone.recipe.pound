# -*- coding: utf-8 -*-
"""Build Recipe pound"""

import os
import stat
import zc
import logging

from zc.recipe.cmmi import Recipe as CMMIRecipe
from plone.recipe.pound import utils

TEMPLATE = """\
#!/bin/sh

%(pound)s -f %(cfg)s -p %(pid)s

"""


class BuildRecipe(CMMIRecipe):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        CMMIRecipe.__init__(self, buildout, name, options)
        self.buildout = buildout
        self.logger=logging.getLogger(self.name)

    def install(self):
        """installer"""
        # building extra options
        owner = self.options.get('owner', utils.get_sysuser())
        group = self.options.get('group', utils.get_sysgroup())
        ssl_dir = self.options.get('ssl_dir', None)
        t_rsa = self.options.get('t_rsa', None)
        extra_options = self.options.get('extra-options', '')
        extra = ''
        if '--with-owner' not in extra_options:
            extra += ' --with-owner=%s' % owner
        if '--with-group' not in extra_options:
            extra += ' --with-group=%s' %  group
        if ssl_dir is not None:
            if os.path.isdir(ssl_dir):
                extra += ' --with-ssl=%s' % ssl_dir
            else:
                self.logger.error(
                    "You need to specify an valid directory for ssl directory")
                raise zc.buildout.UserError("ssl directory is invalid")
        if t_rsa is not None:
            try:
                t_rsa = int(t_rsa)
                extra += ' --with-t_rsa=%d' % (t_rsa,)

            except ValueError:
                self.logger.error(
                    "You need to specify an integer for timeout rsa")
                raise zc.buildout.UserError("Time out rsa is invalid")
        if extra_options is not None:
            extra += ' %s' % (extra_options,)
        self.logger.info('compilation option : %s' % (extra,))

        self.extra_options = extra

        # uses cmmi installer
        installed = CMMIRecipe.install(self)

        # building the script that launches pound
        command = os.path.join(self.options['location'], 'sbin', 'pound')
        var_dir = os.path.join(self.options['location'], 'var')
        pid = os.path.join(var_dir, 'pound.pid')

        script = TEMPLATE % {'pound': command, 'cfg': self.getFileNameConfig(),
                             'pid': pid}

        bin_dir = self.buildout['buildout']['bin-directory']
        script_name = os.path.join(bin_dir, self.name)
        f = open(script_name, 'wb')
        f.write(script)
        f.close()
        mode = os.stat(script_name).st_mode
        os.chmod(script_name, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        return (installed, script_name)


    def getFileNameConfig(self):
        return 'pound.cfg'

    def update(self):
        pass
