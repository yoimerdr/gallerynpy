import typing

import sphinx.application
import docutils.nodes as nodes
import docutils.parsers.rst as docrst


def string_option(arg):
    if arg is None:
        return None
    return "".join(map(str.strip, str(arg).split("\n")))


def item_option(arg, sep=","):
    if arg is None:
        raise ValueError("Invalid argument. Its necessary at least one member name.")

    return (member.strip() for member in string_option(arg).split(sep) if member.strip())


def item_options_option(arg):
    if arg is None:
        return None
    options = []
    for option in item_option(arg, "||"):
        if not option:
            continue
        values = option.split("=")
        if len(values) != 2:
            raise ValueError("Invalid member option: {}".format(option))
        options.append(tuple(values))

    return tuple(options)


def add_directives(app: sphinx.application.Sphinx, directives):
    for item in directives:
        size = len(item)
        if size == 2:
            app.add_directive(*item)
        elif size == 3:
            app.add_directive_to_domain(*item)


class PyMultiDirective(docrst.Directive):
    option_spec = {
        "items": item_option,
        "source": string_option,
        "items-options": item_options_option,
        "directive": string_option
    }

    def __init__(self, *args, **kwargs):
        super(PyMultiDirective, self).__init__(*args, **kwargs)
        try:
            name = self.options["directive"]
            if not name:
                raise ValueError("Directive name is required.")
        except KeyError:
            raise ValueError("Not directive name given in:\n{}".format(self.block_text))

    @classmethod
    def name(cls) -> str:
        return "multi-directive"

    def get_item_directive_name(self) -> str:
        return self.options["directive"]

    def item_name(self, item) -> str:
        if source := self.options.get("source", None):
            return "{}.{}".format(source, item)
        return item

    def build_item_directive(self, directive_name, item_name) -> list[str]:
        content = [".. {}:: {}".format(directive_name, item_name)]
        if options := self.options.get("items-options"):
            for (option, value) in options:
                try:
                    append = not value
                    if not append:
                        value = eval(value)
                        append = value in (None, True, "")
                    if append:
                        content.append("   :{}: ".format(option))
                except SyntaxError:
                    content.append("   :{}: {}".format(option, value))
        return content

    def run(self):
        items = self.options["items"]
        name = self.get_item_directive_name()

        content = []
        for item in items:
            content.extend(self.build_item_directive(name, self.item_name(item)))
            content.append("")

        content.append("")

        for (index, line) in enumerate(content):
            self.content.data.append(line)
            self.content.items.append((None, index))

        node = nodes.container()
        self.state.nested_parse(self.content, self.content_offset, node)
        return node.children


def multi_directives(items: list[typing.Type[PyMultiDirective]]):
    return [(cls.name(), cls) for cls in items]


def setup(app: sphinx.application.Sphinx):
    add_directives(app, multi_directives([
        PyMultiDirective
    ]))
