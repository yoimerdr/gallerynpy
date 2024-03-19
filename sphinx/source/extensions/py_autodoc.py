import re
import typing
from typing import Any

import sphinx.application
import sphinx.domains.python as pydom
from docutils.statemachine import StringList
from sphinx.ext import autodoc
from . import multi_directive as mdrv


class PyObjectDirective(pydom.PyClasslike):
    pass


class ClassLikeObjectDocumenter(autodoc.ClassDocumenter):
    objtype = "-class-object"
    directivetype = "object"
    directive_pattern = re.compile(r"(\w*?:)\w*?::", re.MULTILINE)
    option_spec = {
        **autodoc.ClassDocumenter.option_spec,
        "custom-name": mdrv.string_option,
        "custom-doc": mdrv.string_option
    }

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any,
                            ) -> bool:
        return False

    def document_members(self, all_members: bool = False) -> None:
        super(ClassLikeObjectDocumenter, self).document_members(all_members)

    def start_name(self):
        return super(ClassLikeObjectDocumenter, self).format_name()

    def format_name(self) -> str:
        if custom := self.options.get("custom-name", None):
            if custom.startswith(self.modname):
                return custom[len(self.modname) + 1:]
            return custom

        if len(self.objpath) == 1:
            return self.objpath[0].lower()

        return "{}.{}".format(self.objpath[:-1], self.objpath[-1].lower())

    def add_directive_header(self, sig: str) -> None:
        super(ClassLikeObjectDocumenter, self).add_directive_header("")

    def generate(
            self,
            more_content: StringList | None = None,
            real_modname: str | None = None,
            check_module: bool = False,
            all_members: bool = False,
    ) -> None:
        super(ClassLikeObjectDocumenter, self).generate(more_content, real_modname, check_module, all_members)

        members_patterns = r"( +?.. .*?:: +?)" + re.escape(self.start_name())
        name = self.format_name()

        def map_directives(line: str) -> str:
            def replace(match: re.Match) -> str:
                if group := match.group(1):
                    return "{}{}".format(group, name)
                return match.group()

            return re.sub(members_patterns, replace, line)

        self.directive.result.data = list(map(map_directives, self.directive.result.data))

    def get_doc(self) -> list[list[str]] | None:
        if custom := self.options.get("custom-doc"):
            lines = []
            for line in custom.split("||"):
                lines.append(line.strip())
                lines.append("")

            return [lines]

        return super(ClassLikeObjectDocumenter, self).get_doc()


def pydom_directives(items: list[tuple[str, type]]) -> list[tuple[str, str, str]]:
    return [("py", name, cls) for (name, cls) in items]


def pydom_multi_directives(items: list[typing.Type[mdrv.PyMultiDirective]]):
    return pydom_directives(mdrv.multi_directives(items))


directives = pydom_directives([
    ("object", PyObjectDirective)
])

documenters = (
    ClassLikeObjectDocumenter,
)


def setup(app: sphinx.application.Sphinx):
    mdrv.add_directives(app, directives)
    for item in documenters:
        app.add_autodocumenter(item)
