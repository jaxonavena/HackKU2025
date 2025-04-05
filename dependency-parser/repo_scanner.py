# multi_lang_dep_parser.py

import os
import subprocess
import json
import sys
import logging
import shutil
from git import Repo

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path of the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths relative to the script's directory
REPO_PATH = os.path.join(SCRIPT_DIR, "repo")

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

def clone_repo(git_url):
    """Clone a GitHub repository to the specified directory."""
    try:
        # Remove existing directory if it exists
        if os.path.exists(REPO_PATH):
            logging.info(f"Removing existing directory {REPO_PATH}")
            shutil.rmtree(REPO_PATH)
        
        # Create new directory
        os.makedirs(REPO_PATH, exist_ok=True)
        logging.info(f"Cloning repository to {REPO_PATH}")
        Repo.clone_from(git_url, REPO_PATH)
        return REPO_PATH
    except Exception as e:
        logging.error(f"Failed to clone repository: {e}")
        raise

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

def extract_python_dependencies(repo_path):
    """Extract Python dependencies using pipreqs from the target repository."""
    if not check_pipreqs_installed():
        logging.error("Cannot extract Python dependencies without pipreqs")
        return []

    try:
        logging.info(f"Extracting Python dependencies from {repo_path}...")
        # Run pipreqs directly instead of through python -m
        result = subprocess.run(
            ["pipreqs", repo_path, "--force"],
            capture_output=True,
            text=True
        )
        
        # Log any output from pipreqs
        if result.stdout:
            logging.info(f"pipreqs output: {result.stdout}")
        if result.stderr:
            logging.error(f"pipreqs error: {result.stderr}")
            
        # Check if the command failed
        if result.returncode != 0:
            logging.error(f"pipreqs failed with return code {result.returncode}")
            return []
        
        requirements_path = os.path.join(repo_path, "requirements.txt")
        if os.path.exists(requirements_path):
            with open(requirements_path) as f:
                deps = [line.strip() for line in f if line.strip()]
                logging.info(f"Found {len(deps)} Python dependencies")
                return deps
        else:
            logging.error(f"requirements.txt not found at {requirements_path}")
            return []
    except Exception as e:
        logging.error(f"Error extracting Python dependencies: {e}")
        return []

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
    try:
        # Clone repository to specific path
        repo_path = clone_repo(github_repo_url)
        
        # Extract dependencies from the cloned repository
        deps = extract_python_dependencies(repo_path)
        
        language_data = [{
            "name": "python",
            "version": "3.9",
            "packages": deps
        }]

        manifest = build_dependency_manifest(language_data)
        print(json.dumps(manifest, indent=2))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python repo_scanner.py <github_repo_url>")
        sys.exit(1)
    main(sys.argv[1])
