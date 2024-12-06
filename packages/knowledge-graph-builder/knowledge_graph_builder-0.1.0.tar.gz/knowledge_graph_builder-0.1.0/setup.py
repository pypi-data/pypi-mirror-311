import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knowledge-graph-builder", 
    version="0.1.0",
    author="Cuibinge",
    author_email="cuibinge@sdust.edu.cn",
    description="Constructing Knowledge Graph Based on Given Entity Relation Ontology and Entity Attribute Ontology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)