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
import lxml.etree

from logging import getLogger
logger = getLogger()

# Global Namespace Variables
xmlns = {
    "book": "http://docbook.org/ns/docbook",
    "bacch": "http://avoceteditors.com/2016/bacch",
    "dion": "http://avoceteditors.com/2016/dion",
    "xi": "http://www.w3c.org/2001/XInclude"}

# Fetch XMLNS
def fetch_xmlns():
    return xmlns

# Fetch Reveresed XMLNS
def fetch_rxmlns():
    return {value:key for key, value in xmlns.items()}

# Read File Content
def read_xml(path):
    logger.info("Reading File: %s" % path)

    try:
        logger.debug("Opening File")
        # Open Path
        f = open(path, 'rb')
        content = f.read()
        f.close()

        # Read XML
        logger.debug("Parsing XML")
        try:
            doctree = lxml.etree.fromstring(content)
        except:
            logger.warning("Error Parsing XML")
            doctree = None

    except:
        logger.warning("Reader Failed to Open: %s" % path)
        doctree = None

    return doctree

# XPath Query
def fetch_xpath(doctree, xpath):

    return doctree.xpath(xpath, namespaces=xmlns)
