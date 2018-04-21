# Copyright (c) 2017, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
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

from .builders import BacchBuilder, GnomonBuilder


#########################################
# Set Up the Module
def setup(app):
    """ Functions sets up the Sphinx extensions for Bacch """

    # Builders
    app.add_builder(BacchBuilder)
    app.add_builder(GnomonBuilder)

    #########################
    # Configuration

    show_titleformat = {
        "before": "",
        "after": ""}

    configs = [

            # Project Setup
            ('bacch_masters', None, []),
            ('bacch_master_override', None, ''),
            ('bacch_pdfbuild', None, ''),
            ('bacch_pdfbuild_options', None, []),
            ('bacch_use_parts', False, False),
            ('gnomon_use_parts', False, False),
            ('gnomon', False, ''),

            # Document Configuration
            ('bacch_options', None, []),
            ('gnomon_options', None, []),
            ('bacch_gnomon_packages', {}, {}),
            ('bacch_packages', {}, {}),
            ('gnomon_packages', {}, {}),
            ('bacch_gnomon_config', [], []),
            ('bacch_config', [], []),
            ('gnomon_config', [], []),
            ('bacch_showtitlelist', False, False),
            ('gnomon_showtitlelist', False, False),
            ('bacch_showtitlelist_format', {}, show_titleformat),
            ('gnomon_showtitlelist_format', {}, show_titleformat),

            ('bacch_noindent', False, False),
            ('gnomon_noindent', False, False),
            ('bacch_lettrine', False, False),
            ('bacch_lettrine_conf', {}, {}),
            ('gnomon_lettrine', False, False),
            ('gnomon_lettrine_conf', {}, {}),

            ('bacch_numbers', False, False),
            ('gnomon_numbers', False, False),
            ('bacch_pdf', False, False),

            # Formatting
            ('bacch_titlepage', None, ''),
            ('gnomon_titlepage', None, ''),
            ('bacch_tocpage', False, False),
            ('gnomon_tocpage', False, False),
            ('bacch_author', '', ''),
            ('bacch_author_runner', '', ''),
            ('bacch_title_runner', '', '')
    ]

    for (var, default, rebuild) in configs:
        app.add_config_value(var, default, rebuild)


