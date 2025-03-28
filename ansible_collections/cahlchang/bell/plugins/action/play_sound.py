#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, cahlchang
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os

from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleActionFail


class ActionModule(ActionBase):
    """Action plugin for play_sound module."""

    def run(self, tmp=None, task_vars=None):
        """Run the action plugin."""
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        result.update(dict(changed=False))

        # Get module arguments
        sound_file = self._task.args.get('sound_file', None)
        message = self._task.args.get('message', 'Ansible task completed')
        volume = float(self._task.args.get('volume', 1.0))

        # Validate sound_file if provided
        if sound_file and not os.path.isabs(sound_file):
            # If relative path, make it relative to the playbook directory
            playbook_dir = task_vars.get('playbook_dir', '')
            sound_file = os.path.join(playbook_dir, sound_file)
            self._task.args['sound_file'] = sound_file

        # Execute the module on the target
        module_return = self._execute_module(
            module_name='cahlchang.bell.play_sound',
            module_args=self._task.args,
            task_vars=task_vars,
            tmp=tmp
        )

        result.update(module_return)
        return result