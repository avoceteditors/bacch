##########################################################################
# Module Imports
import subprocess
import re
from bacch import core as bacch_core
from bacch import lib as bacch_lib

##########################################################################
# Parser Class
class Parser():

    def __init__(self, config, base_data):

        # Initialize Variables
        self.config = config
        self.name = base_data['name']
        self.filename = base_data['filename']
        self.path = base_data['path']
        self.stats = {
            "lines": 0,
            "words": 0,
            "chars": 0,
        }

        # Read File
        f = open(self.path, 'r')
        self.content = f.read()
        f.close()

        

    # Initial Parse Controller
    def initial(self):
        bacch_core.log(self.config.verbose, 'debug', '-- Initial Parse: %s' % self.filename)
        parser = InitialParser(self.config, self.content)

        # Break into Lines
        parser.split()

        # Fetch Line Count
        self.stats['lines'] = parser.get_lines()

        # Parse Blocks
        parser.parse_blocks()

        # Fetch Initial Parse
        self.content = parser.fetch()

    # Medial Parse Controller
    def medial(self):
        bacch_core.log(self.config.verbose, 'debug', '-- Medial Parse: %s' % self.filename)
        parser = MedialParser(self.config, self.content)

        # Parse Inline
        parser.parse_inline()



##########################################################################
# Initial Parser
class InitialParser():

    def __init__(self, config, content):
        self.config = config
        self.content = content

    def split(self):
        split = self.content.split('\n')
        self.lines = len(split)
        self.content = split

    # Get Document Stats
    def get_lines(self):
        return self.lines

    # Get Initial Parse
    def fetch(self):
        return self.blocks

    # Parse Block Level Objects
    def parse_blocks(self):

        blocks = []
        block = None
        enum = enumerate(self.content)
        for line in enum:
            i = line[0]
            text = line[1]
            
            # Match Code Blocks
            if re.match('^```', text):
                block = bacch_lib.CodeBlock(text)
                self.check_next(enum, block, '^```')
              
            # Match Numbered List Blocks
            elif re.match('^#\. |^[1-9]*\. ', text):
                block = bacch_lib.ListBlock()
                self.check_next_list(enum, block, text, 'ord')

            # Match Itemized List Blocks
            elif re.match('^\* |^\- ', text):
                block = bacch_lib.ListBlock()
                self.check_next_list(enum, block, text, 'item')

            # Match Headings
            elif re.match('^#.*', text):
                print(text)
                block = bacch_lib.Heading(text)

            # Match Metadata
            elif re.match('^[A-Za-z1-9\-]*: ', text):
                block = bacch_lib.Metadata(text)
            
            # Match Paragraph
            elif text == '':
                pass
            elif re.match('^[A-Za-z1-9]*', text):
                block = bacch_lib.Paragraph(text)
                self.check_next(enum, block, '^[\s\S]*')

            # Append Block
            if block != None:
                blocks.append(block)
                block = None

        # Store Blocks
        self.blocks = blocks

    def check_next(self, enum, block, close):

        while True:
            try:
                line = next(enum)[1]
                block.append(line)
            except:
                break

            if re.match(close, line):
                break


    def check_next_list(self, enum, block, start, list_type):

        # Initialize Block
        block.list_type(list_type)
        block.add(1, start)

        
        # Define Paragraph Spacing
        if list_type == 'ord':
            para = ' ' * 3
            match = '^#\. |^[1-9]*\. '
        else:
            para = ' ' * 2
            match = '^\- |^\* '

        prev = 'None'
        entry = 1

        # Add Entries
        while True:
            try:
                line = next(enum)[1]
            except:
                return None

            if re.match('^[\s\S]*\n$', prev):
                break
            elif re.match(match, line):
                entry += 1
                block.add(entry, line)

            elif re.match('^%s.' % para, line):
                block.add(entry, line)


            prev = line
 
        return None


###############################################################################
# Medial Parser
class MedialParser():

    def __init__(self, config, content):
        self.config = config
        self.content = content
        self.metadata = {}

    def parse_inline(self):

        for block in self.content:
            block.parse()

            block_type = type(block)

            if block_type == bacch_lib.Metadata:
                meta = block.get_metadata()
                self.metadata[meta[0]] = meta[1]

            elif block_type == bacch_lib.ListBlock:
                for para in block.get_paras():
                    para.parse()

            elif block_type == bacch_lib.Heading:
                print(block)

    def parse_metadata(self, parser):

        meta = self.metadata
        valid_meta = ['created', 'updated', 'tags', 'abstract']

        for key in meta:
            if key in valid_meta:
                setattr(parser, key, meta[key])
        






# File Metadata Storage Object
class MetaStore():
    pass


