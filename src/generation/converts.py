import re
import os
import black


def to_python_rpy_files(filenames: list[str], out_folder: str = "gallerynpy"):
    """
    Copy the contents of the given files and pass them to an .rpy file according to the renpy instruction present in it.
    :param filenames: The python (or any) file paths
    :param out_folder: The out folder where the rpy files will be created.
    """
    def write_text(data: str):
        basename, _ = os.path.splitext(os.path.basename(name))
        outfile = os.path.join(out_folder, basename.replace("_ren", "") + ".rpy")
        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        with open(outfile, "w", encoding="utf-8") as fs:
            fs.write(data)

    for name in filenames:
        try:
            with open(name, "r", encoding="utf-8") as fs:
                lines = fs.readlines()

            start = -1
            for (index, line) in enumerate(lines):
                if re.match(r'^"""renpy\n *?', line):
                    start = index
                    break

            text = lines[start + 1].strip()
            if text[-1] != ":":
                text += ":"
            text += "\n"

            def checks_not_empty(line: str):
                return not re.match(r'^[ \n]*$', line)

            def handle_typed(match: re.Match):
                if match.group(1):
                    return match.group(1)
                return ""

            handlers = [
                (re.compile(r': +[A-z0-9_ ."\'|]+([),=])'), handle_typed),
                (re.compile(r' +-> +[A-z0-9_, ."\'|]+(:)'), handle_typed)
            ]

            def check_declaration(declaration: str) -> str:
                decl = declaration
                for (regex, handler) in handlers:
                    decl = re.sub(regex, handler, decl)
                return decl

            lines = map(check_declaration, filter(checks_not_empty, lines[start + 3:]))
            indent_keyword = "def generate_rpy_files_keyword():\n"
            indent = "    "

            data = indent_keyword + indent + indent.join(lines)
            try:
                text += black.format_file_contents(data, fast=True, mode=black.FileMode())
            except black.NothingChanged as e:
                text += data
            text = text.replace(indent_keyword, "")

            write_text(text)
        except Exception as e:
            print("Error: " + str(e))
