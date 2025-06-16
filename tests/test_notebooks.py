import os
import sys
import unittest
import pytest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import re
from pathlib import Path

class TestNotebooks(unittest.TestCase):
    # List of notebooks to skip during testing (just filenames)
    SKIP_NOTEBOOKS = [
        'demo_optimization_incomplete.ipynb',
        'micropolis_network.ipynb'
    ]

    def setUp(self):
        self.notebook_dir = Path(__file__).parent.parent / 'notebooks'
        self.ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        self.failed_notebooks = []
        # Store original working directory
        self.original_dir = os.getcwd()

    def tearDown(self):
        # Restore original working directory
        os.chdir(self.original_dir)

    def clean_ansi_escape_codes(self, text):
        """Remove ANSI escape codes from text."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def test_notebooks_run(self):
        """Test that all notebooks run without errors."""
        for notebook_path in self.notebook_dir.glob('**/*.ipynb'):
            if '.ipynb_checkpoints' in str(notebook_path):
                continue
            
            # Skip notebooks in the SKIP_NOTEBOOKS list by filename
            if notebook_path.name in self.SKIP_NOTEBOOKS:
                print(f"\nSkipping notebook: {notebook_path}")
                continue
                
            print(f"\nTesting notebook: {notebook_path}")
            try:
                # Change to the notebook's directory
                os.chdir(notebook_path.parent)
                
                with open(notebook_path) as f:
                    nb = nbformat.read(f, as_version=4)
                
                # Execute the notebook
                self.ep.preprocess(nb, {'metadata': {'path': str(notebook_path.parent)}})
                print(f"✓ {notebook_path} executed successfully")
                
            except Exception as e:
                error_msg = self.clean_ansi_escape_codes(str(e))
                print(f"\n❌ Error in {notebook_path}:")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {error_msg}")
                self.failed_notebooks.append((notebook_path, error_msg))
                
        if self.failed_notebooks:
            print("\nFailed notebooks summary:")
            for notebook_path, error in self.failed_notebooks:
                print(f"\n{notebook_path}:")
                print(f"Error: {error}")
            self.fail(f"{len(self.failed_notebooks)} notebooks failed to execute")

if __name__ == '__main__':
    unittest.main() 