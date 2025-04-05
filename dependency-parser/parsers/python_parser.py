import os
import subprocess
import sys
import logging

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
    """Extract Python dependencies using pipreqs from the target repository."""
    if not check_pipreqs_installed():
        logging.error("Cannot extract Python dependencies without pipreqs")
        return []

    try:
        logging.info(f"Extracting Python dependencies from {repo_path}...")
        result = subprocess.run(
            ["pipreqs", repo_path, "--force"],
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            logging.info(f"pipreqs output: {result.stdout}")
        if result.stderr:
            logging.error(f"pipreqs error: {result.stderr}")
            
        if result.returncode != 0:
            logging.error(f"pipreqs failed with return code {result.returncode}")
            return []
        
        requirements_path = os.path.join(repo_path, "requirements.txt")
        if os.path.exists(requirements_path):
            with open(requirements_path) as f:
                deps = [line.strip() for line in f if line.strip()]
                logging.info(f"Found {len(deps)} Python dependencies")
                return {
                    "name": "python",
                    "version": "3.9",
                    "packages": deps
                }
        return {
            "name": "python",
            "version": "3.9",
            "packages": []
        }
    except Exception as e:
        logging.error(f"Error extracting Python dependencies: {e}")
        return {
            "name": "python",
            "version": "3.9",
            "packages": []
        } 