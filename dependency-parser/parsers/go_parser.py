# go_parser.py

import os
import subprocess
import logging
import json
import re
from pathlib import Path

def extract_dependencies(repo_path):
    """Extract Go dependencies from a repository."""
    logging.info(f"Extracting Go dependencies from {repo_path}...")
    
    # Initialize results
    result = {
        "name": "go",
        "version": "1.20",  # Default version, will be detected if possible
        "packages": []
    }
    
    try:
        # First try to detect Go version
        go_version = detect_go_version(repo_path)
        if go_version:
            result["version"] = go_version
        
        # Check for go.mod dependencies (modern Go projects)
        mod_deps = extract_gomod_dependencies(repo_path)
        
        # Check for Go imports in source files (fallback)
        import_deps = extract_import_dependencies(repo_path)
        
        # Check for dep dependencies (older Go projects)
        dep_deps = extract_dep_dependencies(repo_path)
        
        # Check for vendor directory (manually vendored dependencies)
        vendor_deps = extract_vendor_dependencies(repo_path)
        
        # Combine all dependencies, removing duplicates
        all_deps_with_paths = set(mod_deps + import_deps + dep_deps + vendor_deps)
        
        # Extract only package names (last part of path)
        simplified_deps = set()
        for dep in all_deps_with_paths:
            # Get just the last part of the path (actual package name)
            package_name = dep.split('/')[-1]
            simplified_deps.add(package_name)
        
        result["packages"] = sorted(list(simplified_deps))
        
        logging.info(f"Found {len(result['packages'])} Go dependencies")
        return result
    except Exception as e:
        logging.error(f"Error extracting Go dependencies: {e}")
        return result

def detect_go_version(repo_path):
    """Detect the Go version required by the project."""
    # First check go.mod file for the Go version
    go_mod_path = os.path.join(repo_path, "go.mod")
    if os.path.exists(go_mod_path):
        try:
            with open(go_mod_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Look for go 1.x directive
                match = re.search(r'go\s+(\d+\.\d+)', content)
                if match:
                    return match.group(1)
        except Exception as e:
            logging.warning(f"Error reading go.mod: {e}")
    
    # Try to detect from Go environment if Go is installed
    try:
        go_env = subprocess.run(
            ["go", "env", "GOVERSION"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=False
        )
        if go_env.returncode == 0 and go_env.stdout.strip():
            # Strip "go" prefix if present
            version = go_env.stdout.strip()
            if version.startswith("go"):
                version = version[2:]
            return version
    except Exception:
        pass
    
    # Default to 1.20 if we can't detect
    return "1.20"

def extract_gomod_dependencies(repo_path):
    """Extract dependencies from go.mod file."""
    deps = []
    go_mod_path = os.path.join(repo_path, "go.mod")
    
    if os.path.exists(go_mod_path):
        try:
            # First try using 'go list -m all' which is the most accurate
            try:
                go_list = subprocess.run(
                    ["go", "list", "-m", "all"],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=30  # Timeout after 30 seconds
                )
                if go_list.returncode == 0:
                    lines = go_list.stdout.strip().split('\n')
                    # Skip first line (module name)
                    for line in lines[1:]:
                        parts = line.split()
                        if len(parts) >= 1:
                            # Just use the module path (not version)
                            deps.append(parts[0])
                    return deps
            except (subprocess.SubprocessError, subprocess.TimeoutExpired):
                logging.warning("Failed to run 'go list -m all', falling back to go.mod parsing")
            
            # Fallback: Parse go.mod file directly
            with open(go_mod_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Remove comments
                content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                
                # Look for require statements
                # Single-line requires: require github.com/example/pkg v1.2.3
                for match in re.finditer(r'require\s+([^\s]+)\s+v', content):
                    deps.append(match.group(1))
                
                # Multi-line requires block: require ( ... )
                require_blocks = re.finditer(r'require\s*\((.*?)\)', content, re.DOTALL)
                for block_match in require_blocks:
                    block = block_match.group(1)
                    for line in block.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('//'):
                            parts = line.split()
                            if len(parts) >= 1:
                                deps.append(parts[0])
        except Exception as e:
            logging.warning(f"Error processing go.mod: {e}")
    
    return deps

def extract_import_dependencies(repo_path):
    """Extract external imports from Go source files."""
    deps = set()
    standard_libs = get_standard_libraries()
    
    # Find all .go files
    for path in Path(repo_path).rglob('*.go'):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Find import blocks
                import_blocks = re.findall(r'import\s*\((.*?)\)', content, re.DOTALL)
                for block in import_blocks:
                    for line in block.split('\n'):
                        line = line.strip()
                        if line and not line.startswith('//'):
                            # Extract quoted package path
                            match = re.search(r'"([^"]+)"', line)
                            if match:
                                pkg = match.group(1)
                                # Skip standard library packages
                                if not any(pkg == lib or pkg.startswith(f"{lib}/") for lib in standard_libs):
                                    # Extract root package (e.g., github.com/user/repo)
                                    parts = pkg.split('/')
                                    if len(parts) >= 3 and (
                                        parts[0] == "github.com" or 
                                        parts[0] == "gitlab.com" or 
                                        parts[0] == "bitbucket.org" or
                                        parts[0] == "golang.org" or
                                        parts[0] == "gopkg.in"
                                    ):
                                        # Add as github.com/user/repo
                                        deps.add('/'.join(parts[:3]))
                                    else:
                                        # Add as is for other packages
                                        deps.add(pkg)
                
                # Find single-line imports
                single_imports = re.findall(r'import\s+"([^"]+)"', content)
                for pkg in single_imports:
                    # Skip standard library packages
                    if not any(pkg == lib or pkg.startswith(f"{lib}/") for lib in standard_libs):
                        # Extract root package
                        parts = pkg.split('/')
                        if len(parts) >= 3 and (
                            parts[0] == "github.com" or 
                            parts[0] == "gitlab.com" or 
                            parts[0] == "bitbucket.org" or
                            parts[0] == "golang.org" or
                            parts[0] == "gopkg.in"
                        ):
                            # Add as github.com/user/repo
                            deps.add('/'.join(parts[:3]))
                        else:
                            # Add as is for other packages
                            deps.add(pkg)
        except Exception as e:
            logging.warning(f"Error processing {path}: {e}")
    
    return list(deps)

def extract_dep_dependencies(repo_path):
    """Extract dependencies from Gopkg.toml or Gopkg.lock (dep tool)."""
    deps = []
    
    # Check for Gopkg.lock (more precise since it has resolved dependencies)
    gopkg_lock = os.path.join(repo_path, "Gopkg.lock")
    if os.path.exists(gopkg_lock):
        try:
            with open(gopkg_lock, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Find project sections
                for match in re.finditer(r'\[\[projects\]\]\s+name\s*=\s*"([^"]+)"', content):
                    deps.append(match.group(1))
        except Exception as e:
            logging.warning(f"Error processing Gopkg.lock: {e}")
    
    # Check for Gopkg.toml if lock file wasn't found
    if not deps:
        gopkg_toml = os.path.join(repo_path, "Gopkg.toml")
        if os.path.exists(gopkg_toml):
            try:
                with open(gopkg_toml, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Find constraint sections
                    for match in re.finditer(r'\[\[constraint\]\]\s+name\s*=\s*"([^"]+)"', content):
                        deps.append(match.group(1))
            except Exception as e:
                logging.warning(f"Error processing Gopkg.toml: {e}")
    
    return deps

def extract_vendor_dependencies(repo_path):
    """Extract dependencies from vendor directory."""
    deps = []
    vendor_dir = os.path.join(repo_path, "vendor")
    
    if os.path.exists(vendor_dir) and os.path.isdir(vendor_dir):
        # Get immediate subdirectories of vendor
        try:
            with os.scandir(vendor_dir) as entries:
                for entry in entries:
                    if entry.is_dir():
                        base_path = entry.name
                        # For github.com, gitlab.com, etc., include the org and repo
                        if base_path in ["github.com", "gitlab.com", "bitbucket.org", "golang.org", "gopkg.in"]:
                            # Look one level deeper
                            org_path = os.path.join(vendor_dir, base_path)
                            with os.scandir(org_path) as orgs:
                                for org in orgs:
                                    if org.is_dir():
                                        # Look one more level for the actual repo
                                        repo_path = os.path.join(org_path, org.name)
                                        with os.scandir(repo_path) as repos:
                                            for repo in repos:
                                                if repo.is_dir():
                                                    deps.append(f"{base_path}/{org.name}/{repo.name}")
                        else:
                            deps.append(base_path)
        except Exception as e:
            logging.warning(f"Error processing vendor directory: {e}")
    
    return deps

def get_standard_libraries():
    """Return a list of Go standard library packages."""
    # This list may not be complete but covers most common standard packages
    return [
        "archive", "bufio", "builtin", "bytes", "compress", "container", "context",
        "crypto", "database", "debug", "encoding", "errors", "expvar", "flag",
        "fmt", "go", "hash", "html", "image", "index", "io", "log", "math",
        "mime", "net", "os", "path", "plugin", "reflect", "regexp", "runtime",
        "sort", "strconv", "strings", "sync", "syscall", "testing", "text",
        "time", "unicode", "unsafe"
    ]

if __name__ == "__main__":
    # For testing
    import sys
    if len(sys.argv) != 2:
        print("Usage: python go_parser.py <repository_path>")
        sys.exit(1)
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    deps = extract_dependencies(sys.argv[1])
    print(json.dumps(deps, indent=2))