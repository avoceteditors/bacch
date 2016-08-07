# Multimarkdown Library
import re

# Heading
class Heading():
    def __init__(self, text):
        self.text = text


    def parse(self):
        # Extract Title
        self.title = re.split('^#* ', self.text, maxsplit=1)[1]

        # Generate Idref
        link = re.findall('[A-Za-z1-9\s]', self.title)
        link = re.sub(' ', '-', ''.join(link))
        self.idref = link.lower()

        # Determine Heading Level
        level = 0
        for char in self.text:
            if char == '#':
                level += 1
            elif char == ' ':
                break
        self.level = level


# Metadata
class Metadata():
    def __init__(self, text):
        self.text = [text]
        
 
    def parse(self):
        text = self.text[0]
        split = re.split(': ', text, maxsplit=1)
        if len(split) == 2:
            self.parameter = split[0].strip()
            self.value = split[1].strip()
        else:
            raise ValueError("Bad Parameter")

    def get_metadata(self):
        return (self.parameter, self.value)

# Code Block
class CodeBlock():
    def __init__(self, text):
        self.text = [text]

    def append(self, text):
        self.text.append(text)
 
 
    def parse(self):
        self.syntax = re.split('```', self.text[0])[1]
        self.code = self.text[1:-1]
      
# List Block
class ListBlock():
    def __init__(self):
        self.entries = {}


    def list_type(self, typ):
        self.list_type = typ


    def add(self, entry, text):
        try:
            self.entries[entry].append(text)
        except:
            self.entries[entry] = [text]

    def parse(self):
        self.text = []
        for i in self.entries:
            text = self.entries[i]
            
            # Remove Markup
            text[0] = re.split('^#\. |^[1-9]\. |^- |^\* ', text[0])[1]

            # Strip Whitespace
            block = Paragraph('')
            for line in text:
                block.append(line.strip())

            self.text.append(block)

    def get_paras(self):
        return self.text

class Paragraph():

    def __init__(self, text):
        if text != '':
            self.text = [text]
        else:
            self.text = []

    def append(self, text):
        if text != '':
            self.text.append(text)

    def parse(self):
        
        # Join List in Line
        line = ' '.join(self.text).split(' ')

        new_text = []
        enum = enumerate(line)
        for i in enum:
            word = i[1]

            # Match Link
            if re.match('^[\[\!\[].*$', word):
                link = Link()
                link.add(word)
                
                if not re.match('^[\[|\!\[].*\]\(.*\)', word):
                    # Find Title Close
                    link = inline_match_link(enum, link, 
                            '.*\]\([.*|.*\)$')
                    if not link.closed():
                        # Find Href Close
                        link = inline_match_link(enum, link,
                                '.*\)$')
                word = link

            # Match Strong
            elif re.match('^\*\*', word):
                word = inline_match(enum, word, '\*\*', 'strong') 
              
            # Match Italic
            elif re.match('^\*', word):
                word = inline_match(enum, word, '\*', 'italic')

            new_text.append(word)

        self.text = new_text


def inline_match_link(enum, link, match):

    while True:
        try:
            new = next(enum)[1]
            link.add(new)

            if re.match(match, new):
                return link
        except:
            return link
    


def inline_match(enum, word, match, typ):

    new_text = []

    if typ == 'strong':
        form = Strong()
    elif typ == 'italic':
        form = Italic()
    
    if re.match('^%s' % match, word):
        form.add(word)

        if not re.match('^%s.*%s[.]'% (match, match), word):

            while True:
                try:
                    new = next(enum)[1]
                    form.add(new)

                    if re.match('^.*%s' % match, new):
                        new_text.append(form)
                        break
                except:
                    break
        else:
            new_text.append(form)

    return new_text


#######################################
# Inline Markup

# Strong
class Strong():

    def __init__(self):
        self.text = []

    def add(self, text):
        self.text.append(text)

class Italic():

    def __init__(self):
        self.text = []

    def add(self, text):
        self.text.append(text)

class Link():

    def __init__(self):
        self.text = []
        self.close = False

    def add(self, text):
        self.text.append(text)
        if re.match('.*\)', text):
            self.close = True

    def closed(self):
        return self.close

    def print_text(self):
        print(self.text)
