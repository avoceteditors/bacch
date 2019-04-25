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

from watchdog.events import FileSystemEventHandler
from watchdog.events import PatternMatchingEventHandler 
from watchdog.observers import Observer
from logging import getLogger
logger = getLogger()
import time
import subprocess


class SphinxEventHandler(PatternMatchingEventHandler):


    def set_dir(self, source, output, build):
        self.source = source
        self.command = ['sphinx-build', '-b', build, source, output]

    def on_any_event(self, event):
        logger.info("Update found in %s, running Sphinx" % self.source)
        subprocess.run(self.command)
        
class Server():
    """ Provides Watchdog functionality for running Sphinx
    processes. """

    def __init__(self, source, output, build):
        self.source = source
        self.output = output

        logger.info("Initializing Server")

        observer = Observer()
        patterns = ["*.rst", "conf.py", "_template"] 
        ignores = [".*", ".*.swp"] 
        event_handler = SphinxEventHandler(patterns=patterns, ignore_patterns=ignores)
        event_handler.set_dir(source, output, build)

        observer.schedule(event_handler, source, recursive=True)
        logger.info("Starting Server")
        observer.start()
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            logger.warning("Shutting down Server")
            observer.stop()
        observer.join()
