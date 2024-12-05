from setuptools import setup, find_packages

setup(
    name='remdex',
    version='0.26',
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
                full_path = os.path.join(root, file)
                pyx_files.append(full_path)
    return pyx_files

package_name = "remdex"  # Replace with your package's name
package_dir = os.path.dirname(__file__)   # Replace with the directory containing the package

pyx_files = find_pyx_files(package_dir)

# Define extensions for the package
extensions = [
    Extension(
        pyx_file.replace(package_dir + os.sep, "").replace(os.sep, ".")[:-4], 
        [pyx_file]
    )
    for pyx_file in pyx_files
]

setup(
    name=package_name,
    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},  # Use Python 3 syntax
    ),
    packages=find_packages(),
)
'''
