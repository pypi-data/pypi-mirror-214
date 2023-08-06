import glob
import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name = 'scmagneto',
                 version = open("scmagneto/_version.py").readlines()[-1].split()[-1].strip("\"'"),
                 description = 'MAGNETO: Marker pAnels GeNEraTor with multi-Objective optimization',
                 long_description=long_description,
                 author = 'Simone Riva',
                 author_email = 'simo.riva15@gmail.com',
                 url = 'https://gitlab.com/andrea-tango/magneto',
                 license='LICENSE',
                 classifiers = ['Programming Language :: Python :: 3.9'],
                 python_requires='>=3.9',
                 packages=setuptools.find_packages(where='scmagneto'),
                 package_dir={'': 'scmagneto'},
                 py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob.glob('scmagneto/*.py')],
                 install_requires=[ 'numpy>=1.23.0',
                                    'pandas>=1.5',
                                    'scikit-learn>=1.1.3',
                                    'scanpy>=1.9.0',
                                    'pymoo>=0.6.0',
                                    'loguru>=0.6.0',
                                    'matplotlib>=3.6.0',
                                    'seaborn>=0.12.0'
                                    ]
                )
