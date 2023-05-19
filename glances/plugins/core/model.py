# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# SPDX-FileCopyrightText: 2022 Nicolas Hennion <nicolas@nicolargo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only
#

"""CPU core plugin."""

from glances.plugins.plugin.model import GlancesPluginModel

import psutil

# Fields description
fields_description = {
    'phys': {
        'getter': 'self.cpu_count',
        'description': 'Number of physical cores (hyper thread CPUs are excluded).',
        'unit': 'number'
    },
    'log': {
        'getter': 'self.cpu_count',
        'description': 'Number of logical CPUs. A logical CPU is the number of \
physical cores multiplied by the number of threads that can run on each core.',
        'unit': 'number',
    },
}


class PluginModel(GlancesPluginModel):
    """Glances CPU core plugin.

    Get stats about CPU core number.

    stats is integer (number of core)
    """

    def __init__(self, args=None, config=None):
        """Init the plugin."""
        super(PluginModel, self).__init__(args=args, config=config, fields_description=fields_description)

        # We dot not want to display the stat in the curse interface
        # The core number is displayed by the load plugin
        self.display_curse = False

    def cpu_count(self):
        """Return the CPU core number."""
        stats = self.get_init_value()
        try:
            # The psutil 2.0 include psutil.cpu_count() and psutil.cpu_count(logical=False)
            # Return a dict with:
            # - phys: physical cores only (hyper thread CPUs are excluded)
            # - log: logical CPUs in the system
            stats['phys'] = psutil.cpu_count(logical=False)
            stats['log'] = psutil.cpu_count()
        except NameError:
            pass
        return stats

    # Do *NOT* uncomment the following line
    # @GlancesPluginModel._check_decorator
    @GlancesPluginModel._log_result_decorator
    def update(self):
        """Update core stats.

        Stats is a dict (with both physical and log cpu number) instead of a integer.
        """
        # Init new stats
        stats = self.get_init_value()

        if self.input_method == 'local':
            # Update stats using the standard system lib
            stats = self.update_local(stats)

        elif self.input_method == 'snmp':
            # Update stats using SNMP
            # http://stackoverflow.com/questions/5662467/how-to-find-out-the-number-of-cpus-using-snmp
            pass

        # Update the stats
        self.stats = stats

        return self.stats
