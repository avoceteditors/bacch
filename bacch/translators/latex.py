import re
import roman
from docutils import nodes
from docutils.nodes import NodeVisitor
from sphinx.writers.latex import LaTeXTranslator

from ..log import BacchLogger

# Title Formatter
class TitleFormat(BacchLogger):

    def __init__(self):
        self.init_logger()

    def fetch_formats(self):
        text = []
        for i in ['part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']:
            val = self.fetch_format(i)

            if val != '':
                text.append(val)

        return '\n'.join(text)
            
    def fetch_value(self, key, target):
        try:
            return getattr(self, '_'.join([target, key]))
        except Exception as err:
            return None

    def fetch_format(self, key):
        val = [] 
        try:
            val.append("\\titleformat{\\%s}%s" % (key, self.title_format[key]))
        except:
            pass
        try:
            val.append("\\titlespacing{\\%s}%s" % (key, self.title_spacing[key]))
        except:
            pass
        return '\n'.join(val)

class NovelFormat(TitleFormat):

    title_format = {
        "part": "[block]{\Huge\center\\bfseries\MakeUppercase{#1}}{}{}{}",
        "chapter": "[block]{\\vspace{0.25in}}{}{}{}[\\addcontentsline{toc}{chapter}{\small - #1}]",
        "section": "[display]{}{}{}{}[\\phantomsection]",
        "subsection": "[display]{}{}{}{}[\\phantomsection]"
    }

    title_spacing = {
        "part": "{0in}{0in}{0in}",
        "chapter": "{0in}{0in}{0in}",
    }


    
    # Shapes 
    shape_part = "[block]"
    shape_chapter = "[block]"

    # Formatting
    format_part = "{\\Huge\\center\\bfseries\\Makeuppercase{#1}}"
    format_chapter = "{\\vspace{0.25in}}"

    # Label
    label_part = ""
    label_chapter = ""

    # Separator
    sep_part = ""
    sep_chapter = ""

    # Before Code
    before_part = ""
    before_chapter = ""

    # After Code
    after_part = None 
    after_chapter = "[\\addcontentsline{toc}{chapter}{\small - #1}]"

    # Part Spacing
    space_left_part = "{0in}"
    space_before_part = "{0in}"
    space_after_part ="{0in}"
    space_right_part = None

    # Chapter Spacing
    space_left_chapter = "{0in}"
    space_before_chapter = "{0in}"
    space_after_chapter ="{0in}"
    space_right_chapter = None




# Translator
class BacchLaTeXTranslator(NodeVisitor, BacchLogger):

    latex_substitution = [
        ("\\\\", "\\textbackslash{}"),
        ("\{", "\\{"),
        ("\}", "\\}"),
        ("\$", "\\$"),
        ("\&", "\\&"),
        ("\#", "\\#"),
        ("\^", "\\textasciicircum{}"),
        ("_", "\\_"),
        ("\~", "\\textasciitilde{}"),
        ("%", "\\%"),
        ("\<", "\\textless{}"),
        ("\>", "\\textgreater{}"),
        ("\|", "\\textbar{}")
    ]

    sections = [
        'part', 'chapter', 'section', 'subsection', 'subsubsection',
        'paragraph', 'subparagraph']


    def __init__(self, document, builder):
        NodeVisitor.__init__(self, document)
        self.init_logger()
        self.body = []
        self.config = builder.config
        self.builder = builder

        level = 0
        if not self.config.bacch_build_chapters:
            if not self.config.bacch_use_parts:
                level = -1
            else:
                level = -2
        self.level_sect = self.level_start = level
        self.lettrine_rubric = None 
        self.count = 0
        self.chapter_key = ''
        self.chapter_titles = {}




    # Helper Methods
    def astext(self):
        # Document Options
        formatter = ''

        if self.config.bacch_options == []:
            if self.config.bacch_build_chapters:
                self.config.bacch_options = ['10pt', 'lettersize', 'onesided']
            else:
                self.config.bacch_options = ['10pt', 'b5paper', 'twosided']

        if self.config.bacch_type == 'novel':
            formatter = NovelFormat()
            titlepage = [
                "\n\\begin{titlepage}",
                "\n\\begin{center}",
                "\\vspace{2in}",
                "\\bfseries",
                "\\Large\\MakeUppercase{%s}" % self.title,
                "\n\\vspace{1in}",
                "\\large\\emph{%s}" % self.config.bacch_subtitle,
                "\n\\vspace{4.4in}",
                self.config.bacch_author,
                "\n\\vspace{0.5in}",
                "\\rule{0.75\\textwidth}{0.4pt}",
                "\n\\normalsize\emph{%s}" % self.config.bacch_publisher,
                "\n\\small %s" % ' + '.join(self.config.bacch_publisher_cities),
                "\n\\end{center}",
                "\\end{titlepage}\n"
            ]
            titlepage = '\n'.join(titlepage)

        conf = [
            '\n\\frenchspacing',
            '\\MakeOuterQuote{"}',
            '\\addto\\captionenglish{\\renewcommand{\\contentsname}{Table of Contents}}',
            '\\tocloftpagestyle{plain}',
            '\\renewcommand{\\cfttoctitlefont}{\\large\\vspace{-1in}\\bfseries}\n'
        ]

        if self.config.bacch_build_chapters:
            conf += [
                '\\linespread{1.25}\n'
            ]
        else:
            conf += [
                '\\linespread{1.00}\n'
            ]
        conf = '\n'.join(conf)

        commands = ["""
\\newcommand{\sectionline}{%
\\nointerlineskip\\noindent\\vspace{.8\\baselineskip}\hspace{\\fill}
{
\\resizebox{0.5\linewidth}{2ex}
{{%
{\\begin{tikzpicture}
\\node  (C) at (0,0) {};
\\node (D) at (5,0) {};
\path (C) to [ornament=88] (D);
\end{tikzpicture}}}}}%
\hspace{\\fill}
\par\\nointerlineskip \\vspace{.8\\baselineskip}
}"""
        ]

        for key, titles in self.chapter_titles.items():
            commands.append('\n')
            commands.append("".join([ 
                "\\newcommand{\\%s}{" % key,
                "\\vspace{0.25in}",
                "\\textsc{\\footnotesize ",
                ", ".join(titles),
                ".}}\n"]))

        commands = '\n'.join(commands)

        if self.config.bacch_build_chapters:
            fancy = [
                "\\pagestyle{fancy}"
                "\\fancyhead[RO, RE]{\\footnotesize %s - \\emph{%s}}" % (
                    self.config.bacch_surname, self.title),
                "\\fancyhead[LO, LE, CO, CE]{}",
                "\\fancyfoot[RO, RE]{\\small\\thepage}",
                "\\fancyfoot[LE, LO, CO, CE]{}"
            ]
        else:
            fancy = [
                "\\pagestyle{fancy}",
                "\\fancyhead[RO]{\\footnotesize %s \\normalsize}" % self.config.bacch_surname,
                "\\fancyhead[LE]{\\footnotesize \\textsc{%s}\\normalsize}" % self.title,
                "\\fancyhead[LO, RE, CO, CE]{}",
                "\\fancyfoot[LE, RO]{\\footnotesize \\thepage \\normalsize}",
                "\\fancyfoot[LO, RE, CO, CE]{}"
            ]
        fancy = '\n'.join(fancy)

        
        text = ['\\documentclass[%s]{book}\n' % ', '.join(self.config.bacch_options)]

        for (package, options) in self.config.bacch_packages.items():
            if options == None:
                text.append('\\usepackage{%s}\n' % package)
            else:
                text.append('\\usepackage[%s]{%s}\n' % (', '.join(options), package))

        text.append(commands)
        text.append(conf)
        text.append(formatter.fetch_formats())

        text.append(fancy)

        text.append("\n\n\\begin{document}\n")
        text.append(titlepage)

        text = text + self.body 

        text.append("\n\\end{document}")

        return ''.join(text)

    def skip_node(self, node):
        raise nodes.SkipNode

    def add(self, text):
        self.body.append(text)


    # Structural Elements
    def visit_compound(self, node):
        pass
    def depart_compound(self, node):
        pass

    def visit_start_of_file(self, node):
        pass

    def depart_start_of_file(self, node):
        pass

    def visit_document(self, node):
        self.open_paragraph = True

    def depart_document(self, node):
        pass


    def visit_section(self, node):

        # Collect Metadata
        title = self.latex_escape(node.next_node().astext())
        self.level_sect += 1
        self.open_paragraph = True

        if self.level_start == self.level_sect - 1 or self.level_start == self.level_sect:
            self.title = title
        elif self.level_sect > -1:
            section = self.sections[self.level_sect]
            self.add("\n\\%s*{%s}\n" % (section, title))

        # Title Block
        if self.config.bacch_type == "novel" and self.level_sect > -1:
            if section == "chapter":
                self.count += 1
                self.chapter_key = re.sub(" ", "", "%s%s" % (title, roman.toRoman(self.count)))
                self.chapter_titles[self.chapter_key] = [title]

                self.add('\n\\%s\n' % self.chapter_key)


                self.add("\n\\vspace{0.1in}\n\n\\sectionline")
            elif self.chapter_key != '':
                self.chapter_titles[self.chapter_key].append(title)



    def depart_section(self, node):
        self.open_paragraph = False
        self.level_sect += -1

    def visit_rubric(self, node):
        self.open_paragraph = True 
        self.add("\\textbf{")

    def depart_rubric(self, node):
        self.add("}")

    def visit_paragraph(self, node):
        self.add("\n")

        if self.open_paragraph:
            self.open_paragraph = False
            self.add("\\noindent ")

    def depart_paragraph(self, node):
        self.add("\n")

    def visit_Text(self, node):
        text = self.latex_escape(node.astext())

        # Word Counter?

        # Lettrine
        if self.lettrine_rubric is None:
            pass
        elif self.lettrine_rubric:
            if text[1] == '"':
                rub = text[0:2]
                text = text[2:]
            else:
                rub = text[0]
                text = text[1:]
            text = "%s}{%s" % (rub, text)
        else:
            text = "}{%s" % (text)

        self.lettrine_rubric = None
        self.add(text)


    def latex_escape(self, text):
        # Sanitize for LaTeX
        for (match, replace) in self.latex_substitution:
            if re.match("^.*?%s" % match, text):
                text = re.sub(match, replace, text)
        return text

    def visit_lettrine(self, node):
        self.add("\\lettrine{")
        self.lettrine_rubric = False

    def depart_lettrine(self, node):
        self.lettrine_rubric = None
        self.add("}")

    def visit_lettrine_rubric(self, node):
        self.add("\\lettrine{")
        self.lettrine_rubric = True

    def depart_lettrine_rubric(self, node):
        self.add("}")




    def depart_Text(self, node):
        pass

    # Block Elements
    def visit_title(self, node):
        raise nodes.SkipNode()

    def depart_title(self, node):
        pass

    # Inline ELemnts
    def visit_strong(self, node):
        self.add("\\textbf{")

    def depart_strong(self, node):
        self.add("}")

    def visit_emphasis(self, node):
        self.add("\\textit{")

    def depart_emphasis(self, node):
        self.add("}")




