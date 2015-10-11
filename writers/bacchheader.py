#!/usr/bin/env python3.4


###########################
# Header Class
class BacchHeader():

    def __init__(self, config):
        self.config = config
        self.header = []
        self.set_documentclass()
        self.set_packages()
        self.set_commands()
        self.set_titles()
        self.set_headers()

        self.header.append('\n\n\n')


    def astext(self):
        return '\n'.join(self.header)


    def set_documentclass(self):
        options = ['openright', 'pdflatex']
        build = self.config.bacch_build_type
        
        # Font Configuration
        if build == "bacch":
            config_font = self.config.bacch_font_size
            options.append('twoside')
        elif build == "gnomon":
            config_font = self.config.gnomon_font_size
            
        if config_font in ['10pt', '12pt']:
            options.append(config_font)
        else:
            options.append('12pt')

        options = ','.join(options)
        self.header.append('\\documentclass[%s]{book}\n' % options)


    def set_packages(self):
        packages = {
            'titlesec':     ['explicit', 'noindentafter'],
            'fancyhdr':     [''],
            'setspace':     [''],
            'titletoc':     [''],
            'framed':       [''],
            'microtype':    ['tracking'],
            'inputenc':     ['utf8'],
            'bookmark':     [''],
            'lettrine':     [''],
            'geometry':     [''],
            'textcase':     ['']
        }
        build = self.config.bacch_build_type
        if build == "bacch":
            packages['geometry'] = ['b5paper']
        elif build == "gnomon":
            packages['geometry'] = ['letterpaper']


        for key in packages:
            if packages[key] == ['']:
                self.header.append('\\usepackage{%s}\n' % key)
            elif packages[key][0] != '':
                options = ','.join(packages[key])
                self.header.append('\\usepackage[%s]{%s}\n' % (options, key))

    def set_commands(self):


        showhrule = '\\rule{\\linewidth}{0.5mm}\n'

        newcommands = {
            'showauthor': self.config.bacch_author,
            'showsurname': self.config.bacch_surname,
            'showtitle': self.config.bacch_title,
            'showuptitle': self.config.bacch_title.upper(),
            'showruntitle': self.config.bacch_title_runner,
            'showsecondtitle': self.config.bacch_title_second,
            'showsubtitle': self.config.bacch_subtitle,
            'showhrule': showhrule,
            'showsecbreak': '---------',
            'showcreatedate': self.config.bacch_createdate,
            "showcompiledate": self.config.bacch_compiledate
        }

        if self.config.bacch_build_type == "gnomon":
            newcommands["showsectitle"] = self.config.section_title


        renewcommands = {}

        self.header.append('\\frenchspacing')

        commands = {
            'new': newcommands,
            'renew': renewcommands
        }

        for i in commands:
            for key in commands[i]:
                self.def_command(i, key, commands[i][key])


    # Add LaTeX Commands
    def def_command(self, command_type, variable, value):

        if value != '':
            if command_type == "new":
                self.header.append('\\newcommand{\\%s}{%s}\n' % (variable, value))
            elif command_type == 'renew':
                self.header.append('\\renewcommand{\\%s}{%s}' % (variable, value))



    # Title Classes, Format and Spacing
    def set_titles(self):
        titles_config = []
        build_type = self.config.bacch_build_type
        if build_type == "bacch":
            titles_config = [self.config.bacch_chapter_format,
                             self.config.bacch_section_format,
                             self.config.bacch_subsection_format,
                             self.config.bacch_subsubsection_format,
                             self.config.bacch_paragraph_format,
                             self.config.bacch_subparagraph_format
            ]

        elif build_type == "gnomon":
            titles_config =[self.config.gnomon_chapter_format,
                            self.config.gnomon_section_format,
                            self.config.gnomon_subsection_format,
                            self.config.gnomon_subsubsection_format,
                            self.config.gnomon_paragraph_format,
                            self.config.gnomon_subparagraph_format
            ]

        base = []
        for var in titles_config:
            base.append('\\titleclass{\\%s}{%s}'
                        '\n' % (var["name"],
                                var["class"]))
            
            titleformat = '\\titleformat{\\%s}' % var["name"]
            shape = var["format_shape"]
            if shape != '':
                titleformat += '[%s]' % shape
            titleformat += ('{%s}{%s}{%s}{%s}'
                            '\n')  % (var["format_format"],
                                      var["format_label"],
                                      var["format_sep"],
                                      var["format_before"])
            after = var["format_after"]
            if after != '':
                titleformat += '[%s]' % after
            base.append(titleformat)
                
            base.append('\\titlespacing{\\%s}'
                        '{%s}{%s}{%s}'
                        '\n' % (var["name"],
                                var["spacing_left"],
                                var["spacing_before_sep"],
                                var["spacing_after_sep"]))


            contents_use = var["contents_use"]
            contents_left = var["contents_left"]
            if contents_use:
                contents = '\\dottedcontents{%s}' % var["name"]
                if contents_left != '':
                    contents += '[%s]' % contents_left
                contents += '{%s}{%s}{%s}' % (var["contents_above"],
                                              var["contents_label_width"],
                                              var["contents_leader_width"])
                
                base.append(contents)
            base.append('\n')

        self.header.append('\n'.join(base))
                        

           

    def set_headers(self):
        header_format = {}
        build_type = self.config.bacch_build_type
        if build_type == "bacch":
            header_format = self.config.bacch_header_format
        elif build_type == "gnomon":
            header_format = self.config.gnomon_header_format


        self.header.append('\\pagestyle{fancy}\n')
        self.header.append('\\fancyhead{}\n\\fancyfoot{}')
        self.header.append('\\renewcommand{\\headrulewidth}{%s}\n'
                           '\\renewcommand{\\footrulewidth}{%s}\n'
                           % (header_format["headrulewidth"],
                              header_format["footrulewidth"]))
        for key in header_format:
            if 'format' in key:
                kind = key.split('_')
                self.header.append('\\fancy%s[%s]{%s}\n'
                                   % (kind[1], kind[2],
                                      header_format[key]))


        








###########################
# General Functions

# Bacch Header Format
def section_format(config, level, var):

    default = {
        "part": {
            "class": "page",
            "format": "",
            "spacing": {
                "left": "",
                "befsep": "0em",
                "aftsep": "0em",
                "right": ""
            },
            "contents": {
                "left": "0em",
                "above": "\\protect \\small",
                "label_width": "1em",
                "leader_width": "1em"

            }
        },
        "chapter": {
            "class": "top",
            "format": "",
            "spacing": {
                "left": "\\parindent",
                "befsep": "\\baselineskip",
                "aftsep": "0em",
                "right": ""
            },
            "contents": {
                "left": "2em",
                "above": "\\protect \\small",
                "label_width": "1em",
                "leader_width": "1em"

            }
        },
        "section": {
            "class": "straight",
            "format": "\\centering \\showsecbreak",
            "spacing": {
                "left": "\\parindent",
                "befsep": "1em",
                "aftsep": "1em",
                "right": ""
            },
            "contents": None
        },
        "subsection": {
            "class": "straight",
            "format": "",
            "spacing": {
                "left": "",
                "befsep": "0em",
                "aftsep": "0em",
                "right": ""
            },
            "contents": None
        },
        "subsubsection": {
            "class": "straight",
            "format": '',
            "spacing": {
                "left": "\\parindent",
                "befsep": "\\baselineskip",
                "aftsep": "-1em",
                "right": ""
            },
            "contents": None
        },
        "paragraph": {
            "class": "straight",
            "format": '',
            "spacing": {
                "left": "",
                "befsep": "0em",
                "aftsep": "0em",
                "right": ""
            },
            "contents": None
        },
        "subparagraph": {
            "class": "straight",
            "format": '',
            "spacing": {
                "left": "",
                "befsep": "",
                "aftsep": "",
                "right": ""
            },
            "contents": None
        }
    }


    length = len(var)
    value = ''
    if length == 1:
        try:
            value = config[var[0]]
        except:
            value = default[level][var[0]]

    elif length == 2:
        try:
            value = config[var[0]][var[1]]
        except:
            value = default[level][var[0]][var[1]]
    elif length == 3:
        try:
            value = config[var[0]][var[1]][var[2]]
        except:
            value = default[level][var[0]][var[1]][var[2]]
    elif length == 4:
        try:
            value = config[var[0]][var[1]][var[2]][var[3]]
        except:
            value = default[level][var[0]][var[1]][var[2]][var[3]]
    elif length == 5:
        try:
            value = config[var[0]][var[1]][var[2]][var[3]][var[4]]
        except:
            value = default[level][var[0]][var[1]][var[2]][var[3]][var[4]]
    elif length == 6:
        try:
            value = config[var[0]][var[1]][var[2]][var[3]][var[4]][var[5]]
        except:
            value = default[level][var[0]][var[1]][var[2]][var[3]][var[4]][var[5]]
    elif length == 6:
        try:
            value = config[var[0]][var[1]][var[2]][var[3]][var[4]][var[5]][var[6]]
        except:
            value = default[level][var[0]][var[1]][var[2]][var[3]][var[4]][var[5]][var[6]]

    return value

