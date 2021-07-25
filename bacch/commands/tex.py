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


# Configure Logger
from logging import getLogger

import bacch.tex
import pathlib
import jinja2
import subprocess
import shutil

LOGGER = getLogger()

def read_tex(src, temps):
    """Finds TeX files in directory, returns list of Documents"""
    if src.exists():
        texs = bacch.tex.read_src(src, temps)
    return texs

def read_templates(src):
    """Finds .template files in directory, returns dict of templates"""
    temps = {}
    for temp in src.rglob("*template"):
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(temp.parent)))
        temps[temp.stem] = env.get_template(temp.name)
    return temps

def run(args, pdf):
    src = pathlib.Path(args.source)
    temps = read_templates(src)
    texs = read_tex(src, temps)

    output = src.parent.joinpath(args.output)
    out_tex = output.joinpath("tex")
    out_pdf= output.joinpath("pdf")

    for key, targets in texs.items():

        for target in targets:
            name = f"{key}-{target.path.stem}"

            otex = out_tex.joinpath(f"{name}.tex")
            ttex = out_tex.joinpath(f"{name}.pdf")
            opdf = out_pdf.joinpath(f"{name}.pdf")

            with open(otex, "w") as f:
                f.write(target.content)

            if pdf:
                subprocess.run(
                    ["lualatex", f"--output-directory={str(out_tex)}", str(otex)],
                    shell=False)
                shutil.copy(str(ttex), str(opdf))


def run_tex(args):
    """CLI tex command"""
    LOGGER.info("Called LaTeX operation")
    run(args, False)

def run_pdf(args):
    """CLI PDF command"""
    LOGGER.info("Called PDF operation")
    run(args, True)

