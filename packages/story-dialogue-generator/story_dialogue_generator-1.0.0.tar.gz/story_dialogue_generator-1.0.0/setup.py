from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="story-dialogue-generator",
    version="1.0.0",
    author="Narrify",
    author_email="narrifyengine@gmail.com",
    description="Librería para generar diálogos e historias utilizando modelos de lenguaje",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries"
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "python-dotenv>=0.19.2",
        "keyring>=23.0.1"
    ],
    entry_points={
        "console_scripts": [
            "story-dialogue-cli=story_dialogue_generator.cli:main",
        ]
    },
    keywords=["stories", "dialogues", "generator", "llm", "cli"],
    license="Apache License 2.0",
    project_urls={
        "Source Code": "https://github.com/Narrify"
    },
)
