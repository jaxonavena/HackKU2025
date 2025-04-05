# rust_parser.py

import os
import json
import logging
import subprocess
import toml


def extract_dependencies(repo_path):
    """Extract Rust dependencies from Cargo.toml."""
    try:
        logging.info(f"Extracting Rust dependencies from {repo_path}...")
        cargo_toml_path = os.path.join(repo_path, "Cargo.toml")
        
        if not os.path.exists(cargo_toml_path):
            logging.error(f"Cargo.toml not found at {cargo_toml_path}")
            return {
                "name": "rust",
                "version": "latest",
                "packages": []
            }
            
        # Read dependencies from Cargo.toml
        with open(cargo_toml_path, 'r') as f:
            try:
                cargo_data = toml.load(f)
                deps = []
                
                # Get regular dependencies
                if "dependencies" in cargo_data:
                    for name, spec in cargo_data["dependencies"].items():
                        if isinstance(spec, str):
                            deps.append(f"{name}=={spec}")
                        elif isinstance(spec, dict):
                            version = spec.get("version", "latest")
                            deps.append(f"{name}=={version}")
                
                # Get dev-dependencies
                if "dev-dependencies" in cargo_data:
                    for name, spec in cargo_data["dev-dependencies"].items():
                        if isinstance(spec, str):
                            deps.append(f"{name}=={spec} (dev)")
                        elif isinstance(spec, dict):
                            version = spec.get("version", "latest")
                            deps.append(f"{name}=={version} (dev)")
                
                logging.info(f"Found {len(deps)} Rust dependencies")
                return {
                    "name": "rust",
                    "version": "latest",
                    "packages": deps
                }
            except Exception as e:
                logging.error(f"Error parsing Cargo.toml: {str(e)}")
                return {
                    "name": "rust",
                    "version": "latest",
                    "packages": []
                }
    except Exception as e:
        logging.error(f"Error extracting Rust dependencies: {str(e)}")
        return {
            "name": "rust",
            "version": "latest",
            "packages": []
        }
