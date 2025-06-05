import os
import sys
import pytest
import nbformat
from nbconvert import PythonExporter
import glob

def convert_notebook_to_python(notebook_path):
    """Convert a Jupyter notebook to a Python script."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    exporter = PythonExporter()
    python_code, _ = exporter.from_notebook_node(notebook)
    return python_code

def run_notebook_as_python(notebook_path):
    """Run a notebook as a Python script and return any exceptions."""
    try:
        python_code = convert_notebook_to_python(notebook_path)
        # Create a temporary file to execute
        temp_file = f"{notebook_path}.py"
        with open(temp_file, 'w') as f:
            f.write(python_code)
        
        # Execute the Python code
        exec(python_code, {})
        return None
    except Exception as e:
        return str(e)
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_notebooks():
    """Test all notebooks in the notebooks directory."""
    notebooks_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notebooks')
    
    # Find all .ipynb files recursively
    notebook_files = glob.glob(os.path.join(notebooks_dir, '**', '*.ipynb'), recursive=True)
    
    for notebook_path in notebook_files:
        error = run_notebook_as_python(notebook_path)
        assert error is None, f"Error in notebook {notebook_path}: {error}" 