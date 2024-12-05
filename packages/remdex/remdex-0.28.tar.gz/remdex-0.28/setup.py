

from setuptools import setup, find_packages

setup(
    name='remdex',
    version='0.28',
    description='Fast and lightweight federated learning framework',
    packages=find_packages(), 
    install_requires=[
        'cloudpickle',
        'numpy'
    ],
    license='MIT'
)

'''


from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize
import os

# Gather all .pyx files in the package
def find_pyx_files(package_dir):
    pyx_files = []
    for root, _, files in os.walk(package_dir):
        for file in files:
            if file.endswith('.pyx'):
                pyx_files.append(os.path.join(root, file))
    return pyx_files

package_name = "remdex"  # Replace with your package's name
package_dir = os.path.abspath(package_name)  # Set to the directory containing the package

pyx_files = find_pyx_files(package_dir)

# Convert file paths to Python module names
extensions = []
for pyx_file in pyx_files:
    # Get the module name in dot notation
    module_name = os.path.relpath(pyx_file, package_dir).replace(os.sep, ".")[:-4]
    extensions.append(Extension(module_name, [pyx_file]))

setup(
    name=package_name,
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},  # Use Python 3 syntax
    ),
    packages=find_packages(),
)

'''
