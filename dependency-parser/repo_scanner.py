# multi_lang_dep_parser.py

import os
import json
import sys
import logging
import shutil
from git import Repo
import tempfile

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import parsers using relative paths
from parsers.python_parser import extract_dependencies as extract_python_deps
from parsers.cpp_parser import extract_dependencies as extract_cpp_deps
from parsers.rust_parser import extract_dependencies as extract_rust_deps
from parsers.go_parser import extract_dependencies as extract_go_deps

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_repo_path():
    """Get a unique temporary directory for cloning repositories"""
    temp_dir = tempfile.mkdtemp(prefix='repo_', dir=os.path.join(SCRIPT_DIR, "repo"))
    return temp_dir

def clone_repo(git_url):
    """Clone a GitHub repository to a temporary directory."""
    repo_path = get_repo_path()
    try:
        logging.info(f"Cloning repository from {git_url} to {repo_path}")
        try:
            Repo.clone_from(git_url, repo_path)
        except Exception as e:
            logging.error(f"Git clone failed: {e}")
            raise Exception(f"Git clone failed: {e}")
            
        return repo_path
    except Exception as e:
        # Clean up the temporary directory if something goes wrong
        if os.path.exists(repo_path):
            try:
                shutil.rmtree(repo_path)
            except:
                pass
        logging.error(f"Failed to clone repository: {e}")
        raise Exception(f"Failed to clone repository: {str(e)}")

def cleanup_repo(repo_path):
    """Clean up the temporary repository directory"""
    try:
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
    except Exception as e:
        logging.warning(f"Failed to clean up repository directory: {e}")

def detect_languages(path):
    """Detect languages based on file extensions."""
    langs = set()
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".py"): langs.add("python")
            elif f.endswith(".rs"): langs.add("rust")
            elif f.endswith(".go"): langs.add("go")
            elif f.endswith((".c", ".cpp", ".h", ".hpp")): langs.add("cpp")
    logging.info(f"Detected languages: {list(langs)}")
    return list(langs)

def build_dependency_manifest(language_data):
    """Build a unified JSON dependency manifest."""
    manifest = {
        "base_image": "ubuntu:22.04",
        "system_packages": ["build-essential", "curl"],
        "languages": language_data
    }
    logging.info("Dependency manifest created successfully")
    return manifest

def main(github_repo_url):
    """
    Main function to process a GitHub repository
    Args:
        github_repo_url: URL of the GitHub repository to analyze
    Returns:
        dict: Dependency manifest
    """
    if not github_repo_url:
        raise Exception("GitHub repository URL is required")
        
    if not (github_repo_url.startswith('http://') or github_repo_url.startswith('https://')):
        raise Exception("Invalid GitHub URL format. URL must start with http:// or https://")
    
    repo_path = None
    try:
        # Create repo directory if it doesn't exist
        os.makedirs(os.path.join(SCRIPT_DIR, "repo"), exist_ok=True)
        
        # Clone repository to specific path
        repo_path = clone_repo(github_repo_url)
        
        # Detect languages in the repository
        languages = detect_languages(repo_path)
        
        # Extract dependencies for each detected language
        language_data = []
        
        if "python" in languages:
            python_deps = extract_python_deps(repo_path)
            if python_deps["packages"]:
                language_data.append(python_deps)
                
        if "cpp" in languages:
            cpp_deps = extract_cpp_deps(repo_path)
            if cpp_deps["packages"]:
                language_data.append(cpp_deps)
                
        if "rust" in languages:
            rust_deps = extract_rust_deps(repo_path)
            if rust_deps["packages"]:
                language_data.append(rust_deps)
                
        if "go" in languages:
            go_deps = extract_go_deps(repo_path)
            if go_deps["packages"]:
                language_data.append(go_deps)

        manifest = build_dependency_manifest(language_data)
        
        # Get repository name from URL
        repo_name = github_repo_url.split('/')[-1].replace('.git', '')
        
        # Create manifest filename with repository name
        manifest_file = os.path.join(SCRIPT_DIR, f"dependencies_{repo_name}.json")
        
        # Write manifest to JSON file (optional, for debugging)
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        logging.info(f"Dependency manifest written to {manifest_file}")
        
        # Return the manifest
        return manifest
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise  # Re-raise the exception to be handled by the caller
    finally:
        # Clean up the temporary repository
        if repo_path:
            cleanup_repo(repo_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python repo_scanner.py <github_repo_url>")
        sys.exit(1)
    main(sys.argv[1])
