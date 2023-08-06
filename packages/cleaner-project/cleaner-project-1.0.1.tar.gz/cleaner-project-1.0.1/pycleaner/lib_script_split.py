"""
`lib_script_split` module helps to find out the most relevant files to the core
of a project, also giving a clue about which files one might consider for
deletion.

To be precise, it parses import statements of the core project files (those
that are specified as such) and check if there are corresponding python files
in the project directory.

TODO: Take into account the possibility of site-package paths being modified.
      It may be partially addressed in some way.
"""
import importlib.util
import logging
from pathlib import Path


def dot_parent_stem_split(name: str):
    """
    Return parent and name of a file given as the string `name`.
    """
    dot_id = name.rfind(".")
    prefix, name = name[:dot_id], name[dot_id + 1 :]
    return prefix, name


def dotted_name_spec(dotted_name: str, silent=False):
    """
    Return a spec of the module given as `dotted_name`.
    If `silent` is True, dismiss warnings.
    """
    try:
        spec = importlib.util.find_spec(dotted_name)
    except (ValueError, ImportError, ModuleNotFoundError):
        spec = None

    if silent:
        if spec is None:
            logging.warning("No module named '%s'", dotted_name)
        elif spec.origin is None:
            logging.warning("No source found for module '%s'", dotted_name)

    return spec


class PyProjectDeps:
    """
    Parse import statements of the core project files, find all direct
    or indirect dependencies among Python files in the project directory.

    Params:
      parser - Python tree-sitter parser
      target_files - core project py-files
      project_dir - Python project directory
    """

    def __init__(self, parser, target_files: str, project_dir: str):
        self.parser = parser
        self.target_files = target_files
        self.cwd = Path(project_dir).resolve()
        assert (
            self.cwd.is_dir()
        ), f"Check --project='{self.cwd}' exists and is a directory"

        ## `simple_imports` and `from_imports` are currently local to
        ## `module_paths` and `file_imports` methods. However, one can
        ## make them the class attributes.
        # self.simple_imports = []
        # self.from_imports = []

        self.not_found = []
        self.may_found = []

        self.core_files = [str(x) for x in self.add_targets(target_files)]
        self.wd_files = {str(x) for x in self.cwd.rglob("*.py")}
        self._scripts = {}

    def recursive_call(self):
        """
        Check imports of the core files (target_files).
        If there are local python libraries imported continue to
        check their imports recursively.
        """
        libs = []
        self._scripts = self.wd_files.copy()
        for x in self.core_files:
            self._scripts.remove(x)

        while len(self._lifo_queue) > 0:
            filename = self._lifo_queue.pop()
            for path in self.module_paths(filename):
                if path in self._scripts:
                    self._lifo_queue.append(path)
                    self._scripts.remove(path)
                    libs.append(path)

        scripts = []
        add_flag = True
        for path in self._scripts:
            for miss in self.not_found:
                if miss.lstrip(".") in path:
                    add_flag = False
                    break

            if add_flag:
                scripts.append(path)

        return libs, scripts

    def non_recursive_call(self):
        """
        Check only imports of the core files (target_files).
        Not sure about this method's use cases.
        """
        paths = []
        for filename in self.core_files:
            paths.extend(self.module_paths(filename))

        libs, scripts = [], []
        for name in self.wd_files:
            if name in paths:
                libs.append(name)
            elif name in self.not_found:
                pass
            else:
                scripts.append(name)
        return libs, scripts

    def add_targets(self, path):
        """
        Add the core project files to a LIFO queue - `self._lifo_queue`.
        """
        p = self.cwd / path
        assert p.exists(), f"Not found --target='{path}'"
        self._lifo_queue = list(p.glob("*.py")) if p.is_dir() else [p]
        return self._lifo_queue.copy()

    def raw_import_lines(self, filename):
        """
        Parse file `filename` with `self.parser`.
        """
        with open(filename, "rb") as fd:
            tree = self.parser.parse(fd.read())
            return tree.root_node.children

    def module_paths(self, filename):
        """
        Return absolute paths to py-files that are direct and indirect
        dependencies of the core project files. If a path cannot be
        extracted, then its dotted name or parent thereof is added to
        `self.not_found` list.
        """
        import_lines = self.raw_import_lines(filename)
        simple_imports, from_imports = self.file_imports(import_lines)

        paths = []
        for modules in simple_imports:
            self._parse_raw_modules(modules, paths)

        for modules in from_imports:
            self._parse_raw_modules(modules[1:], paths, modules[0])

        return paths

    def _parse_raw_modules(self, modules, paths, prefix=None):
        for m in modules:
            dn = m if prefix is None else f"{prefix}.{m}"
            name = self._module_path(m, prefix)
            if name in (dn, prefix):
                self.not_found.append(name)
                continue

            paths.append(name)

    def _module_path(self, name, prefix=None):
        if prefix is None:
            dotted_name = name
            prefix, name = dot_parent_stem_split(name)
        else:
            dotted_name = f"{prefix}.{name}"

        spec = dotted_name_spec(dotted_name)
        if spec is None:
            spec = dotted_name_spec(prefix)
        if spec is None:
            return self.similar_to_dotted_name(dotted_name)

        if spec.origin is None:
            return dotted_name
        if spec.origin.endswith(".py"):
            return spec.origin

        return f"{spec.origin}/__init__.py"

    def similar_to_dotted_name(self, dotted_name):
        """
        Try to find similar module, package to `dotted_name` or parent thereof.
        The `dotted_name` is first transformed to path suffix by trimming the
        leading dot if need be and replacing dots with right slash.
        """
        name = dotted_name.lstrip(".").replace(".", "/")
        similar = set(self.cwd.rglob(f"{name}.py"))
        may_found = similar.copy()
        fallback = dotted_name

        if len(similar) == 0:
            pat = f"{name}/__init__.py"
            similar = set(self.cwd.rglob(pat))
            may_found |= similar

        if len(similar) == 0:
            name = str(Path(name).parent)
            similar = set(self.cwd.rglob(f"{name}.py"))
            dotted_name, _ = dot_parent_stem_split(dotted_name)
            may_found |= similar

        if len(similar) == 0:
            pat = f"{name}/__init__.py"
            similar = set(self.cwd.rglob(pat))
            may_found |= similar

        if len(similar) == 0:
            dotted_name = fallback

        if len(similar) == 1:
            return str(next(iter(similar)))

        self.may_found.extend(list(map(str, may_found)))
        return dotted_name

    def file_imports(self, import_lines):
        """
        Process parsed import statements `import lines`, split it into
        imports starting from keywords `import` (`simple_imports`) and
        `from` (`from_imports`).
        """
        simple_imports = []
        from_imports = []

        for node in import_lines:
            if node.type in ["import_statement", "import_from_statement"]:
                self._extract_imports(node, simple_imports, from_imports)

        return simple_imports, from_imports

    def _extract_imports(self, node, simple_imports, from_imports):
        import_type = node.children[0].type
        content = []

        if import_type == "from":
            content.append(node.children[1].text.decode("ascii"))
            content.extend(self._unalias(node.children[3:]))
            from_imports.append(content)
        elif import_type == "import":
            content.extend(self._unalias(node.children[1:]))
            simple_imports.append(content)
        else:
            raise ValueError("Unknown import type")

    def _unalias(self, imports):
        texts = []
        for node in imports:
            text = node.text.decode("ascii")
            if node.type == "aliased_import":
                texts.append(text.replace(" as ", " ").split()[0])
            elif node.type == "dotted_name":
                texts.append(text)
            else:
                continue

        return texts
