
from .builder import BacchBuilder

def setup(app):
    app.add_builder(BacchBuilder)
