# Module Imports
import markdown
import re
import os.path
import xml.etree.ElementTree as etree

import bacch.parser

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

        #content = re.sub('<', '&lt;', content)
        #content = re.sub('>', '&gt;', content)

        extensions = [
            'markdown.extensions.meta',
            'markdown.extensions.attr_list',
            'markdown.extensions.fenced_code',
            'outline',
            'markdown.extensions.tables',
            'markdown.extensions.headerid(forceid=False)',
            'pymdownx.github(no_nl2br=False)',
            'pymdownx.superfences'
            ]

        # Read into HTML
        try:
            md = markdown.Markdown(extensions)
            html = md.convert(self.content)
            html = '<div id="content">%s</div>' % html
            try:
                xml = etree.fromstring(html)
            except etree.ParseError as err:
                xml = None
                msg = 'Invalid XML: Unable to read %s, due to %s' % (path, err)

        except:
            md = None
            html = None
            xml = None

        # Load Metadata
        try:
            meta = md.Meta
        except:
            meta = {}

        # Parse
        if xml is None:
            print("Error")
        else:
            self.data = bacch.parser.block(xml)


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




