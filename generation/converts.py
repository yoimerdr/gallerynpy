import os
import pathlib
import re
import black
import strip_hints

INDENT = "    "


def strip_types(code: str):
    return strip_hints.strip_string_to_string(code)


def formate_code(code: str):
    try:
        return black.format_file_contents(code, fast=True, mode=black.FileMode())
    except black.NothingChanged as _:
        pass
    return code


def to_rpys(text: str) -> str:
    """
    Transform the contents of the given text and transform it according to the renpy instruction present in it.
    :param text: The code content
    :return: The transformed code content
    """
    lines = text.split("\n")

    def check_empty(line: str):
        return not re.match(r"^\s*$", line)

    text = str("\n".join(filter(check_empty, lines)))
    text = strip_types(text)

    text = formate_code(text)

    matches = [(match.group(1), text.count("\n", 0, match.start()))
               for match in re.finditer(r'^"""renpy\n([\s\w:$=.\',()"-]*)\n"""$', text, re.MULTILINE)]

    if matches:
        lines = text.split("\n")
        blocks = []
        sep = "\n" + INDENT

        def make_block(indexes: tuple[int, tuple[int, int]], end: int = -1) -> str:
            start, (ini, sl) = indexes
            block = ""
            if ini == -1:
                return "\n".join(lines[start + 1:start + sl + 1])
            if ini > 0:
                block = "\n".join(lines[start + 1: start + ini + 1]) + "\n"
            block += sep.join(lines[start + ini + 1:start + sl + 1] + lines[start + sl + 2:end])

            return block

        for (match, line) in matches:
            statements = match.split('\n')
            size = len(statements)
            init = False
            for (index, statement) in enumerate(statements):
                if "init" in statement:
                    blocks.append((line, (index, size)))
                    init = True
            if not init:
                blocks.append((line, (-1, size)))

        if not blocks:
            return text

        bsize = len(blocks)
        if bsize > 1:
            text = ""
            for (index, item) in enumerate(blocks, start=1):
                if index >= bsize:
                    break
                end, _ = blocks[index]
                text += make_block(item, end) + "\n\n"

            return text + make_block(blocks[-1])

        return make_block(blocks[0])
    return ""


def to_rpyf(filepaths: list[str] | list[pathlib.Path], out_folder: str):
    """
    Transform and copy the contents of the given files and pass them to an .rpy file according to
    the renpy instruction present in it.
    :param filepaths: The python (or any) file paths
    :param out_folder: The out folder where the rpy files will be created.
    """
    if filepaths is None:
        raise ValueError("The filepaths is required.")
    elif isinstance(filepaths, str):
        filepaths = [filepaths]

    for filepath in filepaths:
        if not isinstance(filepath, pathlib.Path):
            filepath = pathlib.Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError("The file {} does not exist".format(filepath))

        outpath = os.path.join(out_folder, str(filepath).replace("_ren.", "."))
        outpath = pathlib.Path(outpath).with_suffix(".rpy")
        outpath.parent.mkdir(parents=True, exist_ok=True)
        code = to_rpys(filepath.read_text(encoding="utf-8"))
        if code:
            outpath.write_text(code, encoding="utf-8")
