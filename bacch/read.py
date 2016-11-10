# Module Imports
import re
import os.path
import docutils.core

##################################
# File Reader
class Read():

    def __init__(self, config, path):
        self.config = config
        self.path = path

        # Read Content
        f = open(path, 'r')
        self.content = f.read()
        f.close()

        self.doctree = docutils.core.publish_doctree(
                self.content)

        # Compile Metadata
        self.compile_metadata()


    # Fetch Document Stats
    def fetch_stats(self):

        text = self.content
        chars = len(text)
        words = len(text.replace('\n', ' ').split())
        lines = len(text.split('\n'))

        stats = {
            "chars": chars,
            "words": words,
            "lines": lines}
        return stats



    # Compile Metadata
    def compile_metadata(self):

        metadata = {
            "date": "2014-01-01 00:00 EST",
            "tags": []
        }


