# rust_parser.py

import subprocess
import json
import logging


def extract_dependencies(repo_path):
    """Extract Rust dependencies using cargo metadata."""
    try:
        logging.info(f"Extracting Rust dependencies from {repo_path}...")
        output = subprocess.check_output(
            ["cargo", "metadata", "--format-version=1", "--no-deps"],
            cwd=repo_path
        )
        metadata = json.loads(output)
        package = metadata["packages"][0]
        deps = [f"{dep['name']} {dep['req']}" for dep in package["dependencies"]]
        logging.info(f"Found {len(deps)} Rust dependencies")
        return {
            "name": "rust",
            "version": "1.72",
            "packages": deps
        }
    except Exception as e:
        logging.error(f"Error extracting Rust dependencies: {e}")
        return {
            "name": "rust",
            "version": "1.72",
            "packages": []
        }
