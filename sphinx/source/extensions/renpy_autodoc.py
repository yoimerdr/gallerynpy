import re
import inspect
from typing import Any

import sphinx.application
import sphinx.config
import sphinx.util.inspect as sphinspect
from docutils.statemachine import StringList
from sphinx.ext import autodoc
from . import py_autodoc


class Namespace(object):
    pass


config = Namespace()
config.module = "store"
config.class_module = {}
config.module_references = {}
config.references = {}
config.enum_classes = ()


def first_where(iterable, predicate, index_instead=False):
    for (index, element) in enumerate(iterable):
        if predicate(element):
            return index if index_instead else element
    return None


def is_stored_module_documenter(documenter):
    return isinstance(documenter, RenpyStoredModuleDocumenter)


def _can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any, ) -> bool:
    if not is_stored_module_documenter(parent):
        return False
    return cls.can_document_member(member, membername, isattr, parent)


class RenpyStoredModuleDocumenter(autodoc.Documenter):
    module_pattern = re.compile(r":module: (.+)", re.MULTILINE)
    value_pattern = re.compile(r":value: (.+)", re.MULTILINE)

    def print_directive(self):
        print("\n".join(self.directive.result))

    def __init__(self, *args, **kwargs):
        super(RenpyStoredModuleDocumenter, self).__init__(*args, **kwargs)

    def format_module(self, others):
        if not isinstance(others, (list, tuple)):
            others = [others]

        others = tuple(others)
        modname = config.module
        if self.modname != modname and self.modname.startswith(modname):
            others = (self.modname[len(modname) + 1:],) + others

        return "{}.{}".format(config.module, ".".join(map(str.strip, others)))

    def format_name(self) -> str:
        if self.objpath and len(self.objpath) > 1 and "::" not in self.name:
            first = self.objpath[0]
            for clsmod in config.class_module:
                if first == clsmod[0]:
                    if len(clsmod) == 2:
                        _, first = clsmod
                    else:
                        first = clsmod[0].lower()
                    return self.format_module([first] + self.objpath[1:])

        return self.format_module(self.objpath)

    def add_line(self, line: str, source: str, *lineno: int) -> None:
        if (match := self.module_pattern.search(line)) and match.group(1):
            return
        if (match := self.value_pattern.search(line)) and match.group(1):
            if self.objpath and (last := self.objpath[-1]):
                src = self.name.replace(".{}".format(last), "").replace("::", ".")

                def format_module(name):
                    return "{}.{}".format(config.module, name)

                if any(src == format_module(name) for name in config.enum_classes):
                    return

        super(RenpyStoredModuleDocumenter, self).add_line(line, source, *lineno)

    def generate(
            self,
            more_content: StringList | None = None,
            real_modname: str | None = None,
            check_module: bool = False,
            all_members: bool = False,
    ) -> None:
        super(RenpyStoredModuleDocumenter, self).generate(more_content, real_modname, check_module, all_members)


class RenpyAttributeDocumenter(autodoc.AttributeDocumenter, RenpyStoredModuleDocumenter):
    objtype = "renstoredattr"
    directivetype = autodoc.AttributeDocumenter.objtype

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return _can_document_member(autodoc.AttributeDocumenter, member, membername, isattr, parent)


class RenpyClassDocumenter(autodoc.ClassDocumenter, RenpyStoredModuleDocumenter):
    objtype = "renstoredcls"
    directivetype = autodoc.ClassDocumenter.objtype

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return _can_document_member(autodoc.ClassDocumenter, member, membername, isattr, parent)


class RenpyMethodDocumenter(autodoc.MethodDocumenter, RenpyStoredModuleDocumenter):
    objtype = "renstoredmet"
    directivetype = autodoc.MethodDocumenter.objtype

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return _can_document_member(autodoc.MethodDocumenter, member, membername, isattr, parent)


class RenpyFunctionDocumenter(autodoc.FunctionDocumenter, RenpyStoredModuleDocumenter):
    objtype = "renstoredfunc"
    directivetype = autodoc.FunctionDocumenter.objtype

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return _can_document_member(autodoc.FunctionDocumenter, member, membername, isattr, parent)


class RenpyPropertyDocumenter(autodoc.PropertyDocumenter, RenpyStoredModuleDocumenter):
    objtype = "renstoredprop"
    directivetype = autodoc.PropertyDocumenter.objtype

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        return _can_document_member(autodoc.PropertyDocumenter, member, membername, isattr, parent)


class RenpyExceptionDocumenter(autodoc.ExceptionDocumenter, RenpyStoredModuleDocumenter):
    objtype = "renstoredexc"
    directivetype = autodoc.ExceptionDocumenter.objtype

    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any,
                            ) -> bool:
        return _can_document_member(autodoc.ExceptionDocumenter, member, membername, isattr, parent)


def generate_references(items: list[tuple[str, str]]) -> dict[str, tuple[str, str]]:
    result = {}
    for item in items:
        rep = None
        full = False
        size = len(item)
        if size == 4:
            tp, name, rep, full = item
        elif size == 3:
            tp, name, rep = item
        else:
            tp, name = item

        value = rep
        if not full:
            value = "~{}.".format(config.module)
            if rep:
                value += rep
                if value[-1] != ".":
                    value += "."
            value += name
        if value[0] != "~":
            value = "~" + value
        result[name] = tp, value

    return result


references_pattern = re.compile(r"`(.+?)`|\"(.+?)\"", re.MULTILINE)
role_break = "br"


def property_docs(prop, type_name, lines, clear_lines=False):
    prop_types = ("setter", "getter", "deleter")
    if isinstance(prop, property) and type_name in prop_types and sphinspect.safe_getattr(prop, type_name):
        if clear_lines:
            lines.clear()

        def append(line):
            lines.append(line)
            lines.append("")

        tag = ":{}:".format(type_name)
        if any([tag in line for line in lines]):
            return

        if docs := inspect.getdoc(sphinspect.safe_getattr(prop, "f{}".format(type_name[:3]))):
            docs = tuple(filter(str.strip, docs.split("\n")))
            param_index = first_where(docs, lambda line: line.startswith((":param ", ":return:")), True)
            role = " |{}| ".format(role_break)
            if param_index:
                append("{} {}".format(tag, role.join(docs[:param_index])))
                for line in docs[param_index:]:
                    append(line)
            else:
                append("{} {}".format(tag, role.join(docs)))


def replace_references(text):
    for match in re.finditer(references_pattern, text):
        if group := match.group(1) or match.group(2):
            if key := config.references.get(group, None):
                tp, name = key
                text = text.replace(match.group(), ":{}:`{}` ".format(tp, name))

    return text


def format_docstrings(lines: list[str]):
    formatted = []

    def append(line, empty):
        formatted.append(line)
        if empty:
            formatted.append("")

    itr = iter(lines)
    start = True
    nxt = None

    while True:
        if start:
            line = next(itr, None)
            start = False
        else:
            line = nxt

        nxt = next(itr, None)
        if nxt is None:
            break

        if not re.sub(":.+?:", "", line).strip():
            continue

        stp_nxt = nxt.strip()
        empty = (line.startswith(":") and nxt != "") or stp_nxt.startswith(":") or nxt == ""

        if stp_nxt and re.match(r" {2,}", nxt):
            line = "{} {}".format(line, stp_nxt)
            while nxt2 := next(itr, None):
                if nxt2.startswith(":"):
                    nxt = nxt2
                    break
                line = "{} {}".format(line, nxt2.strip())

            if nxt2 is None:
                append(line, empty)
                break
            elif not nxt2:
                nxt = nxt2

        append(line, empty)
    return formatted


def process_docstring(app: sphinx.application.Sphinx, what: str, name: str, obj, options, lines: list[str]):
    property_docs(obj, "getter", lines, True)
    property_docs(obj, "setter", lines)

    if text := "\n".join(lines):
        lines.clear()
        lines.extend(replace_references(text).split("\n"))

    formatted = format_docstrings(lines)
    lines.clear()
    lines.extend(formatted)


signature_ref_pattern = re.compile(r"~(\S*)")


def process_signatures(app, what, name, obj, options, signature, return_annotation):
    def format_signature(sig):
        if not sig:
            return sig

        if match := signature_ref_pattern.search(sig):
            if group := match.group(1):
                for (key, value) in config.module_references.items():
                    if group.startswith(key):
                        sig = sig.replace(match.group(), "~{}{}".format(value, group[len(key):]))

        sig = replace_references(sig)

        return sig

    return format_signature(signature), format_signature(return_annotation)


documenters = (
    RenpyClassDocumenter,
    RenpyAttributeDocumenter,
    RenpyMethodDocumenter,
    RenpyPropertyDocumenter,
    RenpyFunctionDocumenter,
    RenpyExceptionDocumenter
)


def builder_inited(app: sphinx.application.Sphinx):
    if renpy_stored := app.config.renpy_stored_config:
        for (key, value) in renpy_stored.items():
            setattr(config, key, value)

    if config.references:
        config.references = generate_references(config.references)


events = (
    ("autodoc-process-docstring", process_docstring),
    ("autodoc-process-signature", process_signatures),
    ("builder-inited", builder_inited)
)


def setup(app: sphinx.application.Sphinx):
    app.add_config_value("renpy_stored_config", {}, "env")
    for (event, manager) in events:
        app.connect(event, manager)

    for documenter in documenters:
        app.add_autodocumenter(documenter)
