#! /usr/bin/env python3
import sys, re
class BacchSystem():

    def __init__(self):
        self.platform = sys.platform
        


    def latex(self, bld, src):
        if self.platform == "linux":
            return ["rubber", "--into=%s" % bld, "--pdf", src]
