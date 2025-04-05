import os
import logging
import subprocess

def extract_dependencies(repo_path):
    """Extract C/C++ dependencies from the target repository."""
    try:
        logging.info(f"Extracting C/C++ dependencies from {repo_path}...")
        
        # For C/C++, we'll look for common build systems and package managers
        dependencies = set()
        
        # Check for CMakeLists.txt
        if os.path.exists(os.path.join(repo_path, "CMakeLists.txt")):
            dependencies.add("cmake")
            
        # Check for Makefile
        if os.path.exists(os.path.join(repo_path, "Makefile")):
            dependencies.add("make")
            
        # Check for conanfile.txt
        if os.path.exists(os.path.join(repo_path, "conanfile.txt")):
            dependencies.add("conan")
            
        # Check for vcpkg.json
        if os.path.exists(os.path.join(repo_path, "vcpkg.json")):
            dependencies.add("vcpkg")
            
        # Add common C/C++ build tools
        dependencies.update(["gcc", "g++", "clang", "clang++"])
        
        return {
            "name": "cpp",
            "version": "latest",
            "packages": list(dependencies)
        }
    except Exception as e:
        logging.error(f"Error extracting C/C++ dependencies: {e}")
        return {
            "name": "cpp",
            "version": "latest",
            "packages": []
        } 