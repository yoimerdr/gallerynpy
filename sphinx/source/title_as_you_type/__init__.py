"""
Package edited from https://github.com/rmcgibbo/sphinxcontrib-lunrsearch

It was edited to allow the search of titles present in the sphinx documentation,
but without disabling the default search.
"""

import os
import warnings
from os.path import dirname, join, exists
import json
import itertools

import six
import sphinx.search
from sphinx.application import Sphinx
from sphinx.util.osutil import copyfile
from sphinx.jinja2glue import SphinxFileSystemLoader

stored = {}


class IndexBuilder(sphinx.search.IndexBuilder):
    def freeze(self):
        """Create a usable data structure for serializing."""
        data = super(IndexBuilder, self).freeze()
        try:
            names = data['docnames']
        except KeyError:
            names = data['filenames']

        c = itertools.count()
        for (title, content) in data['alltitles'].items():
            for (index, path) in content:
                if not path:
                    continue
                stored[next(c)] = {
                    "anchor": path,
                    "root": names[index],
                    'title': title,
                }

        for prefix, items in six.iteritems(data['objects']):
            for item in items:
                index, type_index, _, _, prop = item
                title = "{}.{}".format(prefix, prop)
                stored[next(c)] = {
                    'title': title,
                    'root': names[index],
                    'anchor': title,
                }

        return data


def builder_inited(app):
    # adding a new loader to the template system puts our searchbox.html
    # template in front of the others, it overrides whatever searchbox.html
    # the current theme is using.
    # it's still up to the theme to actually _use_ a file called searchbox.html
    # somewhere in its layout. but the base theme and pretty much everything
    # else that inherits from it uses this filename.
    app.builder.templates.loaders.insert(0, SphinxFileSystemLoader(dirname(__file__)))

    # adds the variable to the context used when rendering the searchbox.html
    app.config.html_context.update({
        'lunrsearch_highlight': json.dumps(bool(app.config.lunrsearch_highlight))
    })


def copy_static_files(app, _):
    # because we're using the extension system instead of the theme system,
    # it's our responsibility to copy over static files outselves.
    files = ['js/lunr-searchbox.js', 'css/lunr-searchbox.css']
    for f in files:
        src = join(dirname(__file__), f)
        dest = join(app.outdir, '_static', f)
        if not exists(dirname(dest)):
            os.makedirs(dirname(dest))
        copyfile(src, dest)

    with open(join(app.outdir, "_static", "js", "lunr-search-data.js"), "w", encoding="utf-8") as fs:
        fs.write("var LunrDataSearch = { data: " + json.dumps(stored) + " }")


def setup(app: Sphinx):
    # adds <script> and <link> to each of the generated pages to load these
    # files.
    app.add_js_file('https://cdnjs.cloudflare.com/ajax/libs/lunr.js/0.6.0/lunr.min.js')
    app.add_css_file('css/lunr-searchbox.css')
    app.add_js_file('js/lunr-searchbox.js')
    app.add_js_file('js/lunr-search-data.js')

    app.connect('builder-inited', builder_inited)
    app.connect('build-finished', copy_static_files)
    app.add_config_value('lunrsearch_highlight', True, 'html')

    sphinx.search.IndexBuilder = IndexBuilder
