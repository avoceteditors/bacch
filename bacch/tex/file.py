

from .doc import Document

def read_src(src, temps):
    data = {}
    source = {
        "book": [],
        "chapter": []
    }

    # Initialize Data
    for tex in src.rglob("*.tex"):
        with open(tex, "r") as f:
            content = f.read()
        data[tex] = Document(tex, content)

    for path, doc in data.items():
        if doc.book: 
            doc.compile(data)
            doc.template(temps)
            source["book"].append(doc)
        elif doc.chapter:
            doc.compile(data)
            doc.template(temps)
            source["chapter"].append(doc)

    return source 

