# Module Imports
import bacch
import os.path

class BaseWriter():

    def __init__(self, build, builder, datahandler):
        self.build = build
        self.elements = builder.elements
        self.datahandler = datahandler

        self.init_subclass()


    def parse(self):
        translator = self.trans
        translator.walkthrough()
        self.file_content = translator.fetch()
        
    def write(self):
        outputdir = self.build['path']
        ext = self.build['format']
        
        for write in self.file_content:
            path = os.path.join(outputdir, 
            '%s.%s' % (write, ext))

            text = self.file_content[write]
            print(text) 

        



class HTMLWriter(BaseWriter):

    def init_subclass(self):
        self.trans = bacch.HTMLTranslator(self.build, self.elements, self.datahandler)


class LATEXWriter(BaseWriter):

    pass
