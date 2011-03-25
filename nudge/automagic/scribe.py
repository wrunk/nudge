#
# Copyright (C) 2011 Evite LLC

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import os
from jinja2 import Environment, FileSystemLoader

template_dir = "/".join(__file__.split("/")[0:-1]) + "/templates" 
print "template dir: ", template_dir
template_env = Environment(loader=FileSystemLoader(template_dir))

__all__ = [
    'get_template',
    'AutomagicGenerator',
]

def get_template(filename=None):
    assert filename, "I need a filename, smartypants"
    text=None
    filepath = os.path.join(template_dir, filename)
    assert os.path.exists(filepath), "The template file doesn't exist"
    text = open(filepath, "r").read()
    assert text, "How about some text"
    return template_env.get_template(filename)

class AutomagicGenerator(object):
    extension = 'txt'
    template = get_template('default.html')

    def __init__(self, dir='.', module=None):
        self.dir = dir
        self.module = module

    def ensure_output_file(self, overwrite=False):
        filepath = os.path.join(self.dir,'%s.%s' % (self.module, self.extension))
        if not os.path.exists(filepath):
            return True
        if overwrite:
            os.remove(filepath)
            return True
        raise Exception("This module already exists.  Please remove it to continue")

    def generate(self, project):
        self.ensure_output_file()
        stuff = self.template.render({"project":project})
        print stuff

class PythonStubs(AutomagicGenerator):
    extension = 'py'
    template = get_template('python.py')

class JSClient(AutomagicGenerator):
    extension = 'js'
    template = get_template('javascript.js')

class SphinxDocs(object):
    extension = 'rst'
    template = get_template('sphinx.rst')