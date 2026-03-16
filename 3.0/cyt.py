from setuptools import setup, Extension
from Cython.Build import cythonize
import glob, os

# Gather all Python files in the classes directory
classes_files = glob.glob("classes/*.py")
overlay_files = glob.glob("classes/overlay/*.py")
solhlf = glob.glob("solhl.py")

# Combine all files
all_files = ["Sol.py"] + classes_files + solhlf + overlay_files

# Create the Extension objects
extensions = [
    Extension(os.path.splitext(os.path.basename(file))[0], [file]) for file in all_files
]

# Setup function to build the extensions
setup(
    name="Sol",
    ext_modules=cythonize(extensions),
    zip_safe=False,
    package_data={
        "": ["game.txt"]
    },
    data_files=[
        ('', ['game.txt'])
    ]
)