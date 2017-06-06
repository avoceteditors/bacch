import bacch

extensions = ['bacch.book']

bacch_masters = ['index']
master_doc = 'index'

bacch_options = ['10pt']

bacch_gnomon_packages = {
    "graphicx": None,
    "fancyhdr": None,
    "inputenc": ['utf8'],
    "hyperref": None,
    'titlesec': ['noindentafter'],
    'setspace': None,
    'babel': ['english'],
    'csquotes': ['autostyle', 'english=american'],
    'lettrine': None

}

bacch_packages = {
    'geometry': ['margin=1in']
}

bacch_gnomon_config = [
    '\\pagestyle{fancy}'
]

bacch_config = [

    '\\lhead{}',
    '\\chead{}',
    '\\rhead{Dyer \\emph{\\title}}',
    '\\lfoot{}',
    '\\cfoot{}',
    '\\rfoot{\\small\\thepage}',
    '\\titleformat{\\chapter}[block]{\huge\\flushright\\bfseries}{}{}{}',
    '\\titlespacing{\\chapter}{0in}{0.5}{1in}',
    '\\frenchspacing',
    '\\linespread{1.5}',
    '\\MakeOuterQuote{"}'
]

