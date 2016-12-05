import bacch.latex
import os.path

class Writer():


    def __init__(self, read, doctree, build):
        data = read.fetch_data()
        self.config = data['config'] 

        # Initialize Translator
        transname = build['format']

        try:
            translator = getattr(bacch, transname).Translator()
        except:
            raise ValueError("Invalid Build Format: %s" % transname)

        translator.init(self.config, data, doctree, build) 

        # Walkthrough
        translator.walkthrough()

        # Fetch Text
        self.text = translator.fetch()

        # Initialize Write Process
        self.name = doctree.attrib['id']
        self.ext = translator.extension

        self.outdir = build['path']
        self.tmpdir = os.path.join(self.outdir, 'tmp')


    # Wrte File
    def write(self):

        filename = '.'.join([self.name, self.ext])

        path = os.path.join(self.tmpdir, filename)
        f = open(path, 'w')
        f.write(self.text)
        f.close()

        #print(self.text)
