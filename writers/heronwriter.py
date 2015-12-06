#!/usr/bin/env python3

############################
# Module Imports

import codecs, os.path, re, subprocess

from sphinx.builders import Builder
from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.compat import Directive

from docutils import nodes
import docutils.writers
from docutils.io import StringOutput
import json

###############################
# Writer Class
class HeronWriter(docutils.writers.Writer):

    def __init__(self, config):
        docutils.writers.Writer.__init__(self)
        self.config = config

    def translate(self):
        translator = HeronTranslator(self.document, self.config)
        self.document.walkabout(translator)
        self.output = translator.return_text()

    # Note: Add incremnetal value to HeronTranslator, so that Sphinx can 
    # track how many times it does walkabout on it, behaving differently 
    # on the second time through.


class HeronTranslator(nodes.NodeVisitor):

    def __init__(self, document, config):
        nodes.NodeVisitor.__init__(self, document)
        self.config = config
        self.data = []
        self.level = 0
        self.assign_node_handlers()

    def return_text(self):
        return self.data

    def assign_node_handlers(self):
        
        nodenames = get_nodenames()

        for name in nodenames:            
            if name[1] == "skip":
                setattr(self, 'visit_%s' % name[0],
                        skip_node)
            elif name[1] == "pass":
                setattr(self, 'visit_%s' % name[0],
                        pass_node)
                setattr(self, 'depart_%s' % name[0],
                        pass_node)
            else:
                raise ValueError("Error Node Handler:"
                                 "%s neither skip nor pass" % name[0])


    def section_data(self, data, level):
        if level == 1:
            self.data.append(data)
        elif level == 2:
            self.data[-1]["contents"].append(data)
        elif level == 3:
            self.data[-1]["contents"][-1]["contents"].append(data)
        elif level == 4:
            self.data[-1]["contents"][-1]["contents"][-1]["contents"].append(data)
        elif level == 5:
            self.data[-1]["contents"][-1]["contents"][-1]["contents"][-1]["contents"].append(data)
        elif level == 6:
            print("Level == 6, line 77 heronwriter.py")


    def add_data(self, typ, var, value, level):
        if level == 1:
            self.data[-1][typ][var] += value
        elif level == 2:
            self.data[-1]["contents"][-1][typ][var] += value
        elif level == 3:
            self.data[-1]["contents"][-1]["contents"][-1][typ][var] += value
        elif level == 4:
            self.data[-1]["contents"][-1]["contents"][-1]["contents"][-1][typ][var] += value
        elif level == 5:
            self.data[-1]["contents"][-1]["contents"][-1]["contents"][-1]["contents"][-1][typ][var] += value
        elif level == 6:
            print("Level == 6, ~ line 90 heronwriter.py")

    def collator(self, data, typ, var):
        count = 0
        for i in data["contents"]:
            count += i[typ][var]
        return count

    def collate_data(self, typ, var, level):
        if level == 1:
            self.data[-1][typ][var] += self.collator(
                self.data[-1], typ, var)
        elif level == 2:
            self.data[-1]["contents"][-1][typ][var] += self.collator(
                self.data[-1]["contents"][-1], typ, var)
        elif level == 3:
            self.data[-1]["contents"][-1]["contents"][-1][typ][var] += self.collator(
                self.data[-1]["contents"][-1]["contents"][-1], typ, var)
        elif level == 4:
            self.data[-1]["contents"][-1]["contents"][-1]["contents"][-1][typ][var] += self.collator(
                self.data[-1]["contents"][-1]["contents"][-1]["contents"][-1],
                typ, var)

    


    def visit_Text(self, node):
        self.add_data('stats','line',1, self.level)
        self.add_data('stats','word',len(node.split(' ')),self.level)
        self.add_data('stats','char',len(node),self.level)

    def depart_Text(self, node):
        pass

    def visit_document(self, node):
        pass

    def depart_document(self, node):
        self.data = {
            "title": self.config.bacch_title,
            "stats": {
                "line": 0,
                "word": 0,
                "char": 0
            },
            "contents": self.data
        }

        self.data["stats"]["line"] = self.collator(self.data, "stats", "line")
        self.data["stats"]["word"] = self.collator(self.data, "stats", "word")
        self.data['stats']["char"] = self.collator(self.data, "stats", "char")

    def visit_paragraph(self, node):
        pass

    def depart_paragraph(self, node):
        pass

    def visit_section(self, node):
        self.level += 1
        title = node.next_node().astext()
        data = {"title": title,
                "stats": {
                    "line": 0,
                    "word": 0,
                    "char": 0
                },
                "contents": [] }
        self.section_data(data, self.level)

    def depart_section(self, node):
        self.collate_data("stats","line",self.level)
        self.collate_data("stats","word",self.level)
        self.collate_data("stats","char",self.level)
        self.level += -1

    def visit_strong(self, node):
        pass 

    def depart_strong(self, node):
        pass

    def visit_emphasis(self, node):
        pass

    def depart_emphasis(self, node):
        pass

    def visit_literal(self, node):
       pass

    def depart_literal(self, node):
        pass

    def visit_literal_emphasis(self, node):
        pass

    def depart_literal_emphasis(self, node):
        pass

    # Parse Notes
    def visit_note(self, node):
        pass

    def depart_note(self, node):
        pass



########################
# General Functions
def skip_node(node):
    raise nodes.SkipNode

def pass_node(node):
    pass


def get_nodenames():            
    nodenames = [
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
            ('literal_block', 'skip'),
            ('literal_emphasis', 'skip'),
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
            ('toctree','skip'),
            ('todo','pass'),
            ('topic', 'skip'),
            ('transition', 'skip'),
            ('versionmodified', 'skip'),
    ]

    return nodenames







