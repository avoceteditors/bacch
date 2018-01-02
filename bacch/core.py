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
from docutils import nodes

# General Node Functions
def skip_node(node):
    raise nodes.SkipNode

def pass_node(node):
    pass

# Active Nodes
active_nodes = [
    ('abbreviation', 'skip'),
    ('acks', 'skip'),
    ('admonition', 'skip'),
    ('attribution', 'skip'),
    ('bullet_list', 'skip'),
    ('caption', 'skip'),
    ('centered', 'skip'),
    ('citation', 'skip'),
    ('citation_reference', 'skip'),
    ('classifier', 'skip'),
    ('collected_footnote', 'skip'),
    ('colspec', 'skip'),
    ('comment', 'skip'),
    ('compact_paragraph', 'skip'),
    ('compound', 'pass'),
    ('container', 'skip'),
    ('decoration', 'skip'),
    ('definition', 'skip'),
    ('definition_list', 'skip'),
    ('definition_list_item', 'skip'),
    ('desc', 'skip'),
    ('desc_addname', 'skip'),
    ('desc_annotation', 'skip'),
    ('desc_content', 'skip'),
    ('desc_name', 'skip'),
    ('desc_optional', 'skip'),
    ('desc_parameter', 'skip'),
    ('desc_parameterlist', 'skip'),
    ('desc_returns', 'skip'),
    ('desc_signature', 'skip'),
    ('desc_type', 'skip'),
    ('description', 'skip'),
    ('docinfo', 'skip'),
    ('download_reference', 'skip'),
    ('entry', 'skip'),
    ('enumerated_list', 'skip'),
    ('field', 'skip'),
    ('field_list', 'skip'),
    ('figure', 'skip'),
    ('footer', 'skip'),
    ('footnote', 'skip'),
    ('footnote_reference', 'skip'),
    ('generated', 'skip'),
    ('glossary', 'skip'),
    ('header', 'skip'),
    ('highlightlang', 'skip'),
    ('hlist', 'skip'),
    ('hlistcol', 'skip'),
    ('image', 'skip'),
    ('index', 'skip'),
    ('inline', 'pass'),
    ('label', 'skip'),
    ('legend', 'skip'),
    ('list_item', 'skip'),
    ('literal', 'pass'),
    ('literal_block', 'pass'),
    ('literal_emphasis', 'pass'),
    ('literal_inline','pass'),
    ('meta', 'skip'),
    ('option', 'skip'),
    ('option_argument', 'skip'),
    ('option_group', 'skip'),
    ('option_list', 'skip'),
    ('option_list_item', 'skip'),
    ('option_string', 'skip'),
    ('pending_xref', 'skip'),
    ('problematic', 'skip'),
    ('production', 'skip'),
    ('productionlist', 'skip'),
    ('raw', 'skip'),
    ('refcount', 'skip'),
    ('reference', 'skip'),
    ('row', 'skip'),
    ('rubric', 'skip'),
    ('seealso', 'skip'),
    ('start_of_file', 'pass'),
    ('subscript', 'skip'),
    ('substitution_definition', 'skip'),
    ('substitution_reference', 'skip'),
    ('subtitle', 'skip'),
    ('superscript', 'skip'),
    ('suppress_numbering', 'pass'),
    ('system_message', 'skip'),
    ('table', 'skip'),
    ('tabular_col_spec', 'skip'),
    ('target', 'skip'),
    ('tbody', 'skip'),
    ('term', 'skip'),
    ('tgroup', 'skip'),
    ('thead', 'skip'),
    ('title', 'skip'),
    ('title_reference', 'skip'),
    #('toctree','skip'),
    ('todo','pass'),
    ('topic', 'skip'),
    ('transition', 'skip'),
    ('versionmodified', 'skip'),
]






