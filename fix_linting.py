#!/usr/bin/env python3
import os
import re
from pathlib import Path


def add_docstring(file_path, content):
    """Add docstring to a file if missing."""
    if not content.strip().startswith('"""'):
        content = '"""Module docstring."""\n\n' + content
    return content

def add_class_docstring(content):
    """Add docstring to classes if missing."""
    class_pattern = r"class\s+(\w+)\s*\([^)]*\):"
    doc_pattern = r'class\s+(\w+)\s*\([^)]*\):\s*"""'

    def add_doc(match):
        class_name = match.group(1)
        return f'{match.group(0)}\n    """{class_name} class docstring."""'

    return re.sub(class_pattern, add_doc, content, flags=re.MULTILINE)

def add_function_docstring(content):
    """Add docstring to functions if missing."""
    func_pattern = r"def\s+(\w+)\s*\([^)]*\):"
    doc_pattern = r'def\s+(\w+)\s*\([^)]*\):\s*"""'

    def add_doc(match):
        func_name = match.group(1)
        return f'{match.group(0)}\n    """{func_name} function docstring."""'

    return re.sub(func_pattern, add_doc, content, flags=re.MULTILINE)

def fix_formatting(content):
    """Fix common formatting issues."""
    # Fix line spacing between functions
    content = re.sub(r'def\s+(\w+)\s*\([^)]*\):\s*"""', r"\n\ndef \1(", content)

    # Fix line spacing between classes
    content = re.sub(r'class\s+(\w+)\s*\([^)]*\):\s*"""', r"\n\nclass \1(", content)

    return content

def process_file(file_path):
    """Process a single Python file."""
    try:
        with open(file_path) as f:
            content = f.read()

        # Add module docstring if missing
        content = add_docstring(file_path, content)

        # Add class docstrings
        content = add_class_docstring(content)

        # Add function docstrings
        content = add_function_docstring(content)

        # Fix formatting
        content = fix_formatting(content)

        # Write back to file
        with open(file_path, "w") as f:
            f.write(content)

        print(f"✅ Updated {file_path}")
        return True
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e!s}")
        return False

def find_python_files(start_path):
    """Find all Python files recursively."""
    return list(Path(start_path).rglob("*.py"))

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Find all Python files
    python_files = find_python_files(current_dir)

    print(f"Found {len(python_files)} Python files")

    # Process each file
    success_count = 0
    for file_path in python_files:
        if process_file(file_path):
            success_count += 1

    print("\nSummary:")
    print(f"Total files processed: {len(python_files)}")
    print(f"Successfully updated: {success_count}")
    print(f"Failed: {len(python_files) - success_count}")

if __name__ == "__main__":
    main()
