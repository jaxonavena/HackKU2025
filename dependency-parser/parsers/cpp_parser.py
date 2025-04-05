# c_parser.py

import os
import subprocess
import logging
import json
import re
from pathlib import Path

def parse_cmake_file(cmake_path):
    """Parse CMake file for dependencies."""
    deps = set()
    try:
        with open(cmake_path, 'r') as f:
            content = f.read()
            
            # Find minimum CMake version
            cmake_version = re.search(r'cmake_minimum_required\s*\(\s*VERSION\s+([0-9.]+)', content)
            if cmake_version:
                deps.add(f"cmake>={cmake_version.group(1)}")
            
            # Find project version
            project_version = re.search(r'project\s*\([^)]*VERSION\s+([0-9.]+)', content)
            if project_version:
                version = project_version.group(1)
            
            # Find required packages
            find_packages = re.finditer(r'find_package\s*\(\s*([^)\s]+)', content)
            for match in find_packages:
                deps.add(match.group(1))
            
            # Find target link libraries
            link_libs = re.finditer(r'target_link_libraries\s*\(\s*\w+\s+([^)]+)\)', content)
            for match in link_libs:
                libs = match.group(1).split()
                deps.update(lib for lib in libs if not lib.startswith('$'))
            
            # Check for compiler requirements
            if 'cxx_std_17' in content:
                deps.add('gcc>=7.0 or clang>=5.0')
            elif 'cxx_std_14' in content:
                deps.add('gcc>=5.0 or clang>=3.4')
            elif 'cxx_std_11' in content:
                deps.add('gcc>=4.8 or clang>=3.3')
                
    except Exception as e:
        logging.error(f"Error parsing CMake file: {str(e)}")
    return list(deps)

def extract_dependencies(repo_path):
    """Extract C/C++ dependencies from the repository."""
    try:
        logging.info(f"Extracting C dependencies from {repo_path}...")
        deps = set()
        
        # Check for CMakeLists.txt
        cmake_path = os.path.join(repo_path, "CMakeLists.txt")
        if os.path.exists(cmake_path):
            cmake_deps = parse_cmake_file(cmake_path)
            deps.update(cmake_deps)
            
        # Check for conanfile.txt
        conan_path = os.path.join(repo_path, "conanfile.txt")
        if os.path.exists(conan_path):
            with open(conan_path, 'r') as f:
                content = f.read()
                if '[requires]' in content:
                    conan_deps = [line.strip() for line in content.split('[requires]')[1].split('[')[0].split('\n') if line.strip()]
                    deps.update(conan_deps)
        
        # Check for vcpkg.json
        vcpkg_path = os.path.join(repo_path, "vcpkg.json")
        if os.path.exists(vcpkg_path):
            with open(vcpkg_path, 'r') as f:
                vcpkg_data = json.load(f)
                if 'dependencies' in vcpkg_data:
                    deps.update(dep['name'] for dep in vcpkg_data['dependencies'])
        
        logging.info(f"Found {len(deps)} C dependencies")
        return {
            "name": "cpp",
            "version": "c++11",  # Default to C++11 unless specified otherwise
            "packages": list(deps)
        }
    except Exception as e:
        logging.error(f"Error extracting C dependencies: {str(e)}")
        return {
            "name": "cpp",
            "version": "c++11",
            "packages": []
        }

def extract_makefile_dependencies(repo_path):
    """Extract dependencies from Makefiles."""
    deps = []
    
    # Find all Makefiles
    makefiles = []
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.lower() in ["makefile", "gnumakefile"]:
                makefiles.append(os.path.join(root, file))
    
    # Process each Makefile
    for makefile in makefiles:
        try:
            with open(makefile, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Look for -l flags (library links)
                lib_flags = re.findall(r'-l(\w+)', content)
                for lib in lib_flags:
                    deps.append(f"lib{lib}-dev")
                    
                # Look for pkg-config usage
                pkg_config = re.findall(r'pkg-config\s+--libs\s+(\w+)', content)
                for pkg in pkg_config:
                    deps.append(pkg)
        except Exception as e:
            logging.warning(f"Error processing {makefile}: {e}")
    
    return deps

def extract_include_dependencies(repo_path):
    """Extract system dependencies from #include statements in C files."""
    deps = []
    system_includes = set()
    
    # Find all .c and .h files
    for ext in ['.c', '.h']:
        for path in Path(repo_path).rglob(f'*{ext}'):
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        # Check for system includes: #include <something.h>
                        match = re.search(r'#include\s*<([^/]*)/?[^>]*>', line)
                        if match:
                            include = match.group(1).strip()
                            # Extract the library name from the include
                            lib_name = include.split('.')[0]  # Remove .h extension if present
                            system_includes.add(lib_name)
            except Exception as e:
                logging.warning(f"Error processing {path}: {e}")
    
    # Convert system includes to likely package names
    for include in system_includes:
        # Skip standard C library headers
        if include in ['stdio', 'stdlib', 'string', 'math', 'assert', 'ctype',
                      'errno', 'float', 'limits', 'locale', 'setjmp', 'signal',
                      'stdarg', 'stddef', 'time', 'wchar', 'stdbool', 'complex',
                      'inttypes', 'iso646', 'stdalign', 'stdatomic', 'stdint',
                      'stdnoreturn', 'tgmath', 'threads', 'uchar', 'wctype']:
            continue
            
        # Map common includes to package names
        if include == 'pthread':
            deps.append('libpthread-dev')
        elif include == 'curl':
            deps.append('libcurl4-openssl-dev')
        elif include == 'openssl':
            deps.append('libssl-dev')
        elif include == 'sqlite3' or include == 'sqlite':
            deps.append('libsqlite3-dev')
        elif include == 'zlib' or include == 'zlib':
            deps.append('zlib1g-dev')
        elif include == 'png' or include == 'png':
            deps.append('libpng-dev')
        elif include == 'jpeg' or include == 'jpeglib':
            deps.append('libjpeg-dev')
        elif include == 'tiff' or include == 'tiff':
            deps.append('libtiff-dev')
        elif include == 'xml2' or include == 'libxml':
            deps.append('libxml2-dev')
        elif include == 'pcre':
            deps.append('libpcre3-dev')
        elif include == 'glib':
            deps.append('libglib2.0-dev')
        elif include == 'gtk':
            deps.append('libgtk-3-dev')
        elif include == 'readline':
            deps.append('libreadline-dev')
        elif include == 'ncurses':
            deps.append('libncurses-dev')
        elif include == 'expat':
            deps.append('libexpat1-dev')
        elif include == 'bzip2':
            deps.append('libbz2-dev')
        elif include == 'gmp':
            deps.append('libgmp-dev')
        elif include == 'gsl':
            deps.append('libgsl-dev')
        elif include == 'fftw3':
            deps.append('libfftw3-dev')
        elif include == 'SDL' or include == 'SDL2':
            deps.append('libsdl2-dev')
        elif include == 'X11':
            deps.append('libx11-dev')
        elif include == 'GL' or include == 'gl':
            deps.append('libgl1-mesa-dev')
        else:
            # Add unknown libraries with lib prefix and -dev suffix
            if not include.startswith('lib'):
                deps.append(f"lib{include}-dev")
            else:
                deps.append(f"{include}-dev")
    
    return deps

def extract_autoconf_dependencies(repo_path):
    """Extract dependencies from autoconf files (configure.ac, configure.in)."""
    deps = []
    
    # Check for configure.ac or configure.in
    autoconf_files = []
    for name in ["configure.ac", "configure.in"]:
        path = os.path.join(repo_path, name)
        if os.path.exists(path):
            autoconf_files.append(path)
    
    for autoconf_file in autoconf_files:
        try:
            with open(autoconf_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Look for PKG_CHECK_MODULES
                for match in re.finditer(r'PKG_CHECK_MODULES\s*\(\s*\w+\s*,\s*\[?([^\]\)]+)', content):
                    pkgs = match.group(1).strip()
                    # Split by spaces or commas and clean up
                    for pkg in re.split(r'[ ,]+', pkgs):
                        pkg = pkg.strip('"\'')
                        if pkg:
                            deps.append(pkg)
                
                # Look for AC_CHECK_LIB
                for match in re.finditer(r'AC_CHECK_LIB\s*\(\s*([^,\)]+)', content):
                    lib = match.group(1).strip('"\'')
                    if lib:
                        deps.append(f"lib{lib}-dev")
        except Exception as e:
            logging.warning(f"Error processing {autoconf_file}: {e}")
    
    return deps

def extract_pkgconfig_dependencies(repo_path):
    """Extract dependencies from .pc files or pkg-config usage."""
    deps = []
    
    # Look for .pc.in files which indicate pkg-config dependencies
    for path in Path(repo_path).rglob('*.pc.in'):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Look for Requires: line
                for match in re.finditer(r'Requires:([^#\n]+)', content):
                    pkgs = match.group(1).strip()
                    # Split by spaces or commas and clean up
                    for pkg in re.split(r'[ ,]+', pkgs):
                        pkg = pkg.strip()
                        if pkg and not pkg.startswith('>') and not pkg.startswith('<') and not pkg.startswith('='):
                            deps.append(pkg)
        except Exception as e:
            logging.warning(f"Error processing {path}: {e}")
    
    return deps

def detect_c_standard(repo_path):
    """Attempt to detect which C standard is used in the project."""
    # Check Makefile for -std= flags
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.lower() in ["makefile", "gnumakefile"]:
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Look for C standard specifications
                        match = re.search(r'-std=(c\d+|gnu\d+)', content)
                        if match:
                            std = match.group(1)
                            if std.startswith('c'):
                                return f"C{std[1:]}"
                            elif std.startswith('gnu'):
                                return f"GNU{std[3:]}"
                except Exception:
                    pass
    
    # Check for configure.ac or configure.in
    autoconf_files = []
    for name in ["configure.ac", "configure.in"]:
        path = os.path.join(repo_path, name)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    match = re.search(r'AC_PROG_CC.*-std=(c\d+|gnu\d+)', content)
                    if match:
                        std = match.group(1)
                        if std.startswith('c'):
                            return f"C{std[1:]}"
                        elif std.startswith('gnu'):
                            return f"GNU{std[3:]}"
            except Exception:
                pass
    
    # Check CMakeLists.txt for CMAKE_C_STANDARD
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file == "CMakeLists.txt":
                try:
                    with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        match = re.search(r'CMAKE_C_STANDARD\s+(\d+)', content)
                        if match:
                            return f"C{match.group(1)}"
                except Exception:
                    pass
    
    # Default to C11 if we couldn't detect
    return "C11"

if __name__ == "__main__":
    # For testing
    import sys
    if len(sys.argv) != 2:
        print("Usage: python c_parser.py <repository_path>")
        sys.exit(1)
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    deps = extract_dependencies(sys.argv[1])
    print(json.dumps(deps, indent=2))