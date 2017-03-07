# Copyright (c) 2017, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
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

from os import listdir
from os.path import join, splitext
from re import match

from .filedata import FileData

# Logger
from logging import getLogger
logger = getLogger()

class Resource():

    def __init__(self, name, path, lang, typ):
        logger.info("Initializing Resource: %s" % name)

        # Set Variables
        self.name = name
        self.path = path
        self.lang = lang
        self.typ = typ

        # Initialize Path List
        base_files = listdir(self.path)
        self.data = {}
        self.sectdata = {}

        for i in base_files:
            pathdata = splitext(i)
            filename = pathdata[0]
            ext = pathdata[1]

            if ext == ".xml":
                filepath = join(self.path, i)
                filedata = FileData(filename, filepath)

                if filedata.valid:
                    self.data[filename] = filedata
                    sectdata = filedata.fetch_sectdata()
                    if sectdata != {}:
                        self.sectdata[filename] = sectdata
                else:
                    logger.warning("Invalid File: %s" % filepath)

    def __repr__(self):
        return "<class Resource name='%s' path='%s' lang='%s' type='%s'>" % (
                self.name, self.path, self.lang, self.typ)

