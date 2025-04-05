import os
import sys
import logging
import subprocess
import re
import ast

def parse_setup_py(setup_path):
    """Parse setup.py for dependencies."""
    deps = set()
    try:
        with open(setup_path, 'r') as f:
            content = f.read()
            
        # Try to find install_requires using AST
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'setup':
                    for keyword in node.keywords:
                        if keyword.arg == 'install_requires':
                            if isinstance(keyword.value, ast.List):
                                deps.update(ast.literal_eval(keyword.value))
                            elif isinstance(keyword.value, ast.Name):
                                # Try to find the variable definition
                                var_name = keyword.value.id
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.Assign):
                                        for target in node.targets:
                                            if getattr(target, 'id', '') == var_name:
                                                deps.update(ast.literal_eval(node.value))
        except:
            # Fallback to regex if AST parsing fails
            install_requires = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
            if install_requires:
                # Extract package names from the list
                packages = re.findall(r'[\'"]([^\'"]+)[\'"]', install_requires.group(1))
                deps.update(packages)
    except Exception as e:
        logging.error(f"Error parsing setup.py: {str(e)}")
    return list(deps)

def parse_requirements_txt(req_path):
    """Parse requirements.txt for dependencies."""
    deps = set()
    try:
        with open(req_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Remove any pip options
                    if ' -i ' in line:
                        line = line.split(' -i ')[0]
                    if ' --index-url ' in line:
                        line = line.split(' --index-url ')[0]
                    if ' -e ' in line:
                        line = line.split(' -e ')[1]
                    if line.startswith('-e '):
                        line = line[3:]
                    if line.startswith('git+'):
                        continue
                    deps.add(line)
    except Exception as e:
        logging.error(f"Error parsing requirements.txt: {str(e)}")
    return list(deps)

def check_pipreqs_installed():
    """Check if pipreqs is installed, install it if not."""
    try:
        subprocess.run(["pipreqs", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logging.info("pipreqs not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "pipreqs"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install pipreqs: {e}")
            return False

def extract_dependencies(repo_path):
    """Extract Python dependencies from the repository."""
    deps = set()
    
    # Check setup.py
    setup_py_path = os.path.join(repo_path, "setup.py")
    if os.path.exists(setup_py_path):
        setup_deps = parse_setup_py(setup_py_path)
        deps.update(setup_deps)
    
    # Check requirements.txt
    req_path = os.path.join(repo_path, "requirements.txt")
    if os.path.exists(req_path):
        req_deps = parse_requirements_txt(req_path)
        deps.update(req_deps)
    
    # Try pipreqs as a fallback
    if not deps and check_pipreqs_installed():
        try:
            logging.info(f"Extracting Python dependencies using pipreqs from {repo_path}...")
            subprocess.run(
                ["pipreqs", repo_path, "--force", "--ignore", "tests,examples"],
                capture_output=True,
                text=True
            )
            
            # Check if requirements.txt was generated
            if os.path.exists(req_path):
                pipreqs_deps = parse_requirements_txt(req_path)
                deps.update(pipreqs_deps)
        except Exception as e:
            logging.error(f"Error running pipreqs: {str(e)}")
    
    logging.info(f"Found {len(deps)} Python dependencies")
    return {
        "name": "python",
        "version": "3.9",  # Default version, could be detected from setup.py
        "packages": sorted(list(deps))
    } 