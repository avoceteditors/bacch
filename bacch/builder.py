
from sphinx.builders import Builder
from sphinx.util import texescape, logging
logger = logging.getLogger("bacch")

class BacchBuilder(Builder):
    name = "bacch"
    format = "latex"
    allow_parallel = True
    epilog = "Bacch LaTeX Build is available in %(outdirs)s"

    def init(self):
        self.docnames = []
        self.document_Data = []
        self.usepackages = []
        self.build_map = False
        texescape.init()

    def build_all(self):
        self.build_map = True
        self.build()

    def build_specific(files):
        pass


    def init_document_data(self):
        print("YES")

