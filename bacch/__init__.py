##################################################################################
# __init__.py - configures the Bacch builder
#
# Copyright (c) 2019, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##################################################################################

# Module Imports
from docutils import nodes

# Local Imports
from .builders import bacch
from .roles import lettrine


def visit_node(self, node):
    raise nodes.SkipNode

def setup(app):
    """Configures Sphinx extension"""

    # Builders
    app.add_builder(bacch.BacchBuilder)

    # Nodes
    app.add_node(lettrine.lettrine)
    app.add_node(lettrine.lettrine_rubric)

    # Roles
    app.add_role('lett', lettrine.lettrine_role)
    app.add_role('lettrub', lettrine.lettrine_rubric_role)


    # Configuration Values
    config_vals = [

        # Publication Type
        ('bacch_author', 'None', True),
        ('bacch_chapter_packages', {}, True),
        ('bacch_lettrine', True, True),
        ('bacch_lettrine_levels', 2, True),
        ('bacch_masters', [], True),
        ('bacch_options', [], True),
        ('bacch_packages', {}, True),
        ('bacch_publisher', None, True),
        ('bacch_publisher_cities', [], True),
        ('bacch_subtitle', None, True),
        ('bacch_surname', None, True),
        ('bacch_type', 'novel', True),
        ('bacch_use_parts', True, True)
    ]

    for (var, default, rebuild) in config_vals:
        app.add_config_value(var, default, rebuild)

