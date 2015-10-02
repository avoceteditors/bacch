#!/usr/bin/env python3

###############################
# Module Imports
import builders.bacchbuilder as bacchbuilder
import builders.gnomonbuilder as gnomonbuilder

###############################
# General Functions
def add_nodes(app):
    pass


###############################
# Setup Module
def setup(app):

    # Add Builders
    app.add_builder(bacchbuilder.BacchBuilder)
    app.add_builder(gnomonbuilder.GnomonBuilder)
    
    # Custom Nodes
    add_nodes(app)

    # Custom Nodes and Directives


    # Define Project Variables

    app.add_config_value('bacch_use_parts', None, '')


    # Define Section Header Formatting
    app.add_config_value('bacch_part_format', None, '')


    app.add_config_value('bacch_show_toc', True, '')
    app.add_config_value('bacch_publisher','','')
    app.add_config_value('bacch_pubcities','','')
    app.add_config_value('bacch_font_size', '','')

    app.add_config_value('bacch_author','none','')
    app.add_config_value('bacch_surname','none','')
    app.add_config_value('bacch_title','none','')
    app.add_config_value('bacch_title_second','none','')
    app.add_config_value('bacch_title_runner','','')
    app.add_config_value('bacch_subtitle','','')

    app.add_config_value('bacch_build_type','','')


    app.add_config_value('bacch_chapter_format',{},'')
    app.add_config_value('bacch_section_format',{},'')
    app.add_config_value('bacch_subsection_format',{},'')
    app.add_config_value('bacch_subsubsection_format',{},'')
    app.add_config_value('bacch_paragraph_format',{},'')
    app.add_config_value('bacch_subparagraph_format',{},'')
    app.add_config_value('bacch_header_format',{},'')


    app.add_config_value('gnomon_font_size','','')
