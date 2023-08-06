from setuptools import setup, find_namespace_packages


with open('./README.md', 'r') as f: README = f.read()

setup(
    name="doe_toolbox", 
    version="1.3",
    author="miltos_90",
    description='Design of experiments toolbox.',
    long_description=README,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3.0",
    python_requires='>=3.10',
    include_package_data = True,
    packages=find_namespace_packages(),
    install_requires=["numpy", "scipy"],
    keywords=['python', 'statistics', 'doe'],
    classifiers=[
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Programming Language :: Python :: 3.10",
    ],
)