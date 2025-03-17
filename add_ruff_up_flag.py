#!/usr/bin/env python3
import os
from pathlib import Path

import toml


def clean_path(path):
    """Remove the prefix up to 'dora' in the path."""
    path_str = str(path)
    if "dora" in path_str:
        return path_str[path_str.find("dora"):]
    return path_str

def update_pyproject_toml(file_path):
    """Update a single pyproject.toml file to include UP rule."""
    try:
        # Read the existing toml file
        with open(file_path) as f:
            content = f.read()
            config = toml.loads(content)

        # Check if ruff.lint section exists
        if "tool" not in config:
            config["tool"] = {}
        if "ruff.lint" not in config["tool"]:
            config["tool"]["ruff.lint"] = {}

        # Create the formatted extend-select section
        formatted_section = """[tool.ruff.lint]
extend-select = [
  "D",   # pydocstyle
  "UP",  # Ruff's UP rule
  "PERF" # Ruff's PERF rule
]"""

        # Replace or add the section
        if "[tool.ruff.lint]" in content:
            # Find the section and replace it
            lines = content.split("\n")
            new_lines = []
            in_section = False
            for line in lines:
                if line.strip() == "[tool.ruff.lint]":
                    in_section = True
                    new_lines.append(formatted_section)
                elif in_section and line.strip() and not line.startswith("["):
                    continue
                elif in_section and line.strip().startswith("["):
                    in_section = False
                    new_lines.append(line)
                elif not in_section:
                    new_lines.append(line)

            # Write back to file
            with open(file_path, "w") as f:
                f.write("\n".join(new_lines))
        else:
            # Append the section at the end
            with open(file_path, "a") as f:
                f.write("\n\n" + formatted_section + "\n")

        print(f"✅ Updated {clean_path(file_path)}")
        return True
    except Exception as e:
        print(f"❌ Error processing {clean_path(file_path)}: {e!s}")
        return False

def find_pyproject_files(start_path):
    """Find all pyproject.toml files recursively."""
    return list(Path(start_path).rglob("pyproject.toml"))

def main():
    # Get the current directory
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "node-hub")

    # Find all pyproject.toml files
    pyproject_files = find_pyproject_files(current_dir)

    print(f"Found {len(pyproject_files)} pyproject.toml files")

    # Update each file
    success_count = 0
    for file_path in pyproject_files:
        if update_pyproject_toml(file_path):
            success_count += 1

    print("\nSummary:")
    print(f"Total files processed: {len(pyproject_files)}")
    print(f"Successfully updated: {success_count}")
    print(f"Failed: {len(pyproject_files) - success_count}")

if __name__ == "__main__":
    main()
