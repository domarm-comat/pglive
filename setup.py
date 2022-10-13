import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pglive",
    version="0.5.3",
    license='MIT',
    author="Martin Domaracký",
    author_email="domarm@comat.sk",
    description="Pyqtgraph live plot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/domarm-comat/pglive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
    ],
    install_requires=[
        "pyqtgraph"
    ],
    extras_requires={
    },
    python_requires='>=3.7',
)
