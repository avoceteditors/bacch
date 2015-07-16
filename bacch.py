#! /usr/bin/env python3
import sys
import bacchbuilder


#############################################
# General Functions
def add_nodes(app):
    pass

def skip_me(node):
    raise nodes.SkipNode

def pass_me(node):
    pass


##############################################
# Setup Module
def setup(app):
    
    # Add Builders
    app.add_builder(bacchbuilder.BacchFullBuilder)
    app.add_builder(bacchbuilder.BacchChapBuilder)

    # Custom Nodes
    add_nodes(app)

    # Define Project Variables
    app.add_config_value('bacch_buildtype','TPB','')
    app.add_config_value('bacch_show_todo',False,'')
    
    # Define Typesetting Variables
    app.add_config_value('bacch_chapter_block',None,'')
    app.add_config_value('bacch_chapblock_separator','--','')

    app.add_config_value('bacch_chapter_number',None,'')
    app.add_config_value('bacch_section_number', False,'')

    app.add_config_value('bacch_sect_numtype',None,'')
    
    app.add_config_value('bacch_show_toc',False,'')
    app.add_config_value('bacch_secbreak','---','')

    app.add_config_value('bacch_header_type','surname-title','')
    app.add_config_value('bacch_footer_type','pagenumout','')
    app.add_config_value('bacch_headfoot_size','small','')
    app.add_config_value('bacch_headfoot_space','2em','')
    app.add_config_value('bacch_headfoot_divider','|','')
    app.add_config_value('bacch_font_size','10pt','')


    # Define Metadata Variables
    app.add_config_value('bacch_author','Anonymous','')
    app.add_config_value('bacch_surname','Anonymous','')

    app.add_config_value('bacch_title','Untitled','')
    app.add_config_value('bacch_title_subtitle','','')
    app.add_config_value('bacch_title_second','','')
    app.add_config_value('bacch_title_runner','Untitled','')

    app.add_config_value('bacch_publisher','','')
    app.add_config_value('bacch_pubcities',[],'')

    

