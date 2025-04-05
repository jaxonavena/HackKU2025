import os
import logging
import subprocess

def extract_dependencies(repo_path):
    """Extract Go dependencies from the target repository."""
    try:
        logging.info(f"Extracting Go dependencies from {repo_path}...")
        
        # Look for go.mod
        go_mod_path = os.path.join(repo_path, "go.mod")
        if not os.path.exists(go_mod_path):
            return {
                "name": "go",
                "version": "latest",
                "packages": []
            }
            
        # Run go list to get dependencies
        result = subprocess.run(
            ["go", "list", "-m", "all"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logging.error(f"Failed to list Go dependencies: {result.stderr}")
            return {
                "name": "go",
                "version": "latest",
                "packages": []
            }
            
        # Parse dependencies
        dependencies = []
        for line in result.stdout.splitlines():
            if line.strip() and not line.startswith("go "):
                dependencies.append(line.strip())
                
        return {
            "name": "go",
            "version": "latest",
            "packages": dependencies
        }
    except Exception as e:
        logging.error(f"Error extracting Go dependencies: {e}")
        return {
            "name": "go",
            "version": "latest",
            "packages": []
        } 