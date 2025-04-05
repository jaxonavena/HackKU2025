import os
import logging
import toml

def extract_dependencies(repo_path):
    """Extract Rust dependencies from the target repository."""
    try:
        logging.info(f"Extracting Rust dependencies from {repo_path}...")
        
        # Look for Cargo.toml
        cargo_path = os.path.join(repo_path, "Cargo.toml")
        if not os.path.exists(cargo_path):
            return {
                "name": "rust",
                "version": "latest",
                "packages": []
            }
            
        # Parse Cargo.toml
        with open(cargo_path) as f:
            cargo_data = toml.load(f)
            
        dependencies = []
        if "dependencies" in cargo_data:
            for dep, version in cargo_data["dependencies"].items():
                if isinstance(version, str):
                    dependencies.append(f"{dep}=={version}")
                else:
                    dependencies.append(dep)
                    
        return {
            "name": "rust",
            "version": "latest",
            "packages": dependencies
        }
    except Exception as e:
        logging.error(f"Error extracting Rust dependencies: {e}")
        return {
            "name": "rust",
            "version": "latest",
            "packages": []
        } 