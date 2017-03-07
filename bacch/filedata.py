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

from . import xml

from logging import getLogger
logger = getLogger()

class FileData():

    valid = True

    def __init__(self, name, path):

        # Load Doctree
        logger.info("Initializing File Data: %s" % name)
        self.doctree = xml.read_xml(path)
        if self.doctree is None:
            self.valid = False
        else:
            self.load_data()


    def load_data(self):

        # Fetch Sections
        xpath = "//book:book|//book:part|//book:chapter|//book:section"
        sections = xml.fetch_xpath(self.doctree, xpath)
        self.sectdata = {}
        for section in sections:
            attr = section.attrib
            idref = attr["id"]

            # Fetch and Format Title
            title_elements = xml.fetch_xpath(section, "/*/book:title|/*/book:info/book:title")
            if len(title_elements) > 0:
                title_element = title_elements[0]
                try:
                    title_attrs = title_element.attrib
                    title_format = title_element["{%s}format" % xml.fetch_rxmlns()["bacch"]]
                except:
                    title_format = "normal"

                title = title_element.text
            else:
                title = idref
                title_format = "normal"

            # Save Data
            self.sectdata[idref] = {
                    "title": title,
                    "format": title_format
                }


    def fetch_sectdata(self):
        return self.sectdata

