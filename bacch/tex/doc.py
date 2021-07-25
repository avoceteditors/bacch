##############################################################################
# Copyright (c) 2021, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
##############################################################################

# Module Imports
import re
import jinja2

newline = re.compile("\n")
book_pattern = re.compile("^%BOOK")
chapter_pattern = re.compile("^%CHAPTER")
inc_pattern = re.compile("^%INCLUDE\\{(.*?)\\}\s*$")

class Document:

    def __init__(self, path, content):
        self.path = path
        self.content = content
        self.mtime = path.stat().st_mtime
        self.mtimes = [self.mtime]
        self.book = False
        self.chapter = False

        lines = re.split(newline, content)
        if len(lines) > 0:
            if re.match(book_pattern, lines[0]):
                self.book = True
            elif re.match(chapter_pattern, lines[0]):
                self.chapter = True
        self.lines = lines

    def __repr__(self):
        return self.content

    def compile(self, texs):

        newcon = []
        for line in self.lines:
            incs = re.findall(inc_pattern, line)

            if len(incs) > 0:
                key = self.path.parent.joinpath(incs[0])

                if key in texs:
                    newdoc = texs[key]
                    newdoc.compile(texs)
                    self.mtimes += newdoc.mtimes
                    newcon.append(newdoc.content)
            else:
                newcon.append(line)

        self.content = "\n".join(newcon)

    def template(self, temps):

        temp = None
        if self.book and "book" in temps:
            temp = temps["book"]
        elif self.chapter and "chapter" in temps:
            temp = temps["chapter"]

        if temp is not None:
            self.content = temp.render(
                body = self.content
            )



