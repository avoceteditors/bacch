# Module Imports
import bacch

class BaseWriter():

    def __init__(self, build, builder, datahandler):
        self.build = build
        self.builder = build
        self.elements = builder.elements
        self.datahandler = datahandler

        self.init_subclass()


    def parse(self):
        translator = self.trans
        translator.walkthrough()
        

class HTMLWriter(BaseWriter):

    def init_subclass(self):
        self.trans = bacch.HTMLTranslator(self.build, self.builder, self.elements, self.datahandler)


class LATEXWriter(BaseWriter):

    pass
