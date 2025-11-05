"""Core packing functionality for Python Script Packer."""

import os
import re
import json
from typing import List, Dict, NamedTuple
from secrets import token_hex


class ModuleSpec(NamedTuple):
    """Specification for a packed module."""
    alloc: str
    link: str
    load: str


def find_library(library_name: str, is_main_library: bool, library_paths: List[str]) -> str:
    """
    Find a library in the given library paths.

    Args:
        library_name: Name of the library to find
        is_main_library: Whether this is the main library (must have __main__.py)
        library_paths: List of paths to search for libraries

    Returns:
        Path to the library

    Raises:
        ValueError: If library name is invalid or library not found
    """
    if re.search(r'[^\w]', library_name):
        raise ValueError('invalid library name')

    for library_base_path in library_paths:
        # construct library path
        library_path = os.path.join(library_base_path, library_name)

        # check if library exists
        pack_list_exists = os.path.exists(os.path.join(library_path, 'pack.list'))
        main_exists = os.path.exists(os.path.join(library_path, '__main__.py'))

        if pack_list_exists and (not is_main_library or main_exists):
            return library_path

    raise ValueError(f'could not find {library_name} in library paths (pack.list available?)')


def read_pack_list(library_path: str) -> List[str]:
    """
    Read and parse a pack.list file.

    Args:
        library_path: Path to the library containing pack.list

    Returns:
        List of pack entries (non-empty, trimmed lines)
    """
    pack_list_path = os.path.join(library_path, 'pack.list')
    with open(pack_list_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    return [line.strip() for line in lines if line.strip()]


def pack_modules(
    dialect: str,
    product_name: str,
    library_path: str,
    library_name: str,
    library_paths: List[str]
) -> Dict[str, ModuleSpec]:
    """
    Pack modules recursively.

    Args:
        dialect: Python dialect ('2.7' or '3.5')
        product_name: Name of the product/package
        library_path: Path to the library
        library_name: Name of the library
        library_paths: List of paths to search for dependencies

    Returns:
        Dictionary mapping module names to their specifications
    """
    # read pack list
    pack_list = read_pack_list(library_path)

    # add product base module
    modules = {}

    product_name_code = json.dumps(product_name)

    if dialect == '2.7':
        module_spec = ModuleSpec(
            alloc=(
                f"sys.modules[{product_name_code}] = imp.new_module({product_name_code})\n"
                f"sys.modules[{product_name_code}].__name__ = {product_name_code}\n"
                f"sys.modules[{product_name_code}].__package__ = {json.dumps(product_name)}\n"
                f"sys.modules[{product_name_code}].__path__ = []"
            ),
            link='',
            load=''
        )
    else:
        module_spec = ModuleSpec(
            alloc=f"sys.modules[{product_name_code}] = importlib.util.module_from_spec(importlib.util.spec_from_loader({product_name_code}, loader=None, is_package=True))",
            link='',
            load=''
        )

    modules[product_name] = module_spec

    # pack modules
    for pack_entry in pack_list:
        # handle library reference
        if not pack_entry.startswith('.'):
            # pack library
            lib_path = find_library(pack_entry, False, library_paths)
            lib_modules = pack_modules(dialect, product_name, lib_path, pack_entry, library_paths)

            for module_name, module_spec in lib_modules.items():
                if module_name not in modules:
                    modules[module_name] = module_spec
                else:
                    existing = modules[module_name]
                    if (existing.alloc != module_spec.alloc or
                        existing.link != module_spec.link or
                        existing.load != module_spec.load):
                        raise ValueError(f'two different scripts for {module_name} detected')

        # handle local file reference
        else:
            # lookup item path
            module_base_path = os.path.join(library_path, *pack_entry[1:].split('.'))
            module_paths = [
                module_base_path + '.py',
                os.path.join(module_base_path, '__init__.py')
            ]
            module_path = None
            for path in module_paths:
                if os.path.exists(path):
                    module_path = path
                    break

            if not module_path:
                raise ValueError(f'could not find {pack_entry} in {library_name}')

            # determine if module is a package
            is_package = module_path == module_paths[1]

            # build module name
            library_name_clean = library_name[:-1] if library_name.endswith('.') else library_name
            pack_entry_clean = pack_entry[:-1] if pack_entry.endswith('.') else pack_entry
            module_name = f"{product_name}.{library_name_clean}{pack_entry_clean}"
            module_name_code = json.dumps(module_name)

            # build parent module name
            module_local_name = module_name.split('.')[-1]
            module_parent_name = module_name[:-(len(module_local_name) + 1)]

            # build package name
            package_name = module_name if is_package else module_name.rsplit('.', 1)[0]

            # rewrite library imports
            with open(module_path, 'r', encoding='utf-8') as f:
                module_script = f.read().split('\n')

            # rewrite imports
            rewritten_script = []
            for line in module_script:
                m = re.match(r'^(\s*import\s+)(\w+)\s*$', line)
                if m and m.group(2) in pack_list:
                    rewritten_script.append(f"{m.group(1)}{product_name}.{m.group(2)} as {m.group(2)}")
                else:
                    rewritten_script.append(line)

            # escape script for embedding
            script_content = '\n'.join(rewritten_script)
            script_content = script_content.replace('\\', '\\\\').replace("'", "\\'")
            module_script_code = f"'''{script_content}'''"

            # pack
            link_code = f"setattr(sys.modules[{json.dumps(module_parent_name)}], {json.dumps(module_local_name)}, sys.modules[{module_name_code}])"

            if dialect == '2.7':
                module_spec = ModuleSpec(
                    alloc=(
                        f"sys.modules[{module_name_code}] = imp.new_module({module_name_code})\n"
                        f"sys.modules[{module_name_code}].__name__ = {module_name_code}\n"
                        f"sys.modules[{module_name_code}].__package__ = {json.dumps(package_name)}"
                        + (f"\nsys.modules[{module_name_code}].__path__ = []" if is_package else '')
                    ),
                    link=link_code,
                    load=(
                        "if '_packer_global_vars' in locals() or '_packer_global_vars' in globals():\n"
                        f"    sys.modules[{module_name_code}].__dict__.update(_packer_global_vars)\n"
                        f"exec {module_script_code} in sys.modules[{module_name_code}].__dict__"
                    )
                )
            else:
                is_package_str = 'True' if is_package else 'None'
                module_spec = ModuleSpec(
                    alloc=f"sys.modules[{module_name_code}] = importlib.util.module_from_spec(importlib.util.spec_from_loader({module_name_code}, loader=None, is_package={is_package_str}))",
                    link=link_code,
                    load=(
                        "if '_packer_global_vars' in locals() or '_packer_global_vars' in globals():\n"
                        f"    sys.modules[{module_name_code}].__dict__.update(_packer_global_vars)\n"
                        f"exec({module_script_code}, sys.modules[{module_name_code}].__dict__)"
                    )
                )

            modules[module_name] = module_spec

    return modules


def pack(
    dialect: str,
    product_name: str,
    library_name: str,
    library_paths: List[str]
) -> str:
    """
    Pack a Python library into a single executable script.

    Args:
        dialect: Python dialect ('2.7' or '3.5')
        product_name: Name of the product (use '*' for random name)
        library_name: Name of the library to pack
        library_paths: List of paths to search for libraries

    Returns:
        The packed Python script as a string

    Raises:
        ValueError: If arguments are invalid
    """
    # generate unique product name if requested
    if product_name == '*':
        product_name = token_hex(8)

    # validate args
    if dialect not in ('2.7', '3.5'):
        raise ValueError('unknown dialect')

    if re.search(r'[^\w]', product_name):
        raise ValueError('invalid product name')

    # read main script
    library_path = find_library(library_name, True, library_paths)
    main_script_path = os.path.join(library_path, '__main__.py')

    with open(main_script_path, 'r', encoding='utf-8') as f:
        main_script = f.read().split('\n')

    # rewrite library imports
    pack_list = read_pack_list(library_path)
    rewritten_main = []
    for line in main_script:
        m = re.match(r'^(\s*import\s+)(\w+)\s*$', line)
        if m and (m.group(2) == library_name or m.group(2) in pack_list):
            rewritten_main.append(f"{m.group(1)}{product_name}.{m.group(2)} as {m.group(2)}")
        else:
            rewritten_main.append(line)

    main_script = rewritten_main

    # pack modules
    modules = pack_modules(dialect, product_name, library_path, library_name, library_paths)

    # insert packed modules
    if dialect == '2.7':
        import_code = 'import sys, imp'
    else:
        import_code = 'import sys, importlib.util'

    # find pack marker
    pack_line = -1
    for i, line in enumerate(main_script):
        if re.match(r'^\s*#\s+!!!\s+PACK\s+HERE\s+!!!\s*$', line, re.IGNORECASE):
            pack_line = i
            break

    # build packed code
    packed_code_parts = [
        f"\n{import_code}\n",
        '\n'.join(spec.alloc for spec in modules.values()),
        '\n',
        '\n'.join(spec.link for spec in modules.values()),
        '\n',
        '\n\n'.join(spec.load for spec in modules.values()),
        '\n'
    ]
    packed_code = '\n'.join(packed_code_parts)

    # insert into main script
    if pack_line != -1:
        main_script[pack_line:pack_line + 1] = [packed_code]
    else:
        main_script.insert(0, packed_code)

    # assemble result
    return '\n'.join(main_script)
