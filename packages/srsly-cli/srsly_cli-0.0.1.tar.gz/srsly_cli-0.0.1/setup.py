from setuptools import find_packages, setup

entry_point = "srsly = srsly_cli.__main__:main"


with open("requirements.txt", encoding="utf-8") as f:
    requires = []
    for line in f:
        req = line.split("#", 1)[0].strip()
        if req and not req.startswith("--"):
            requires.append(req)

long_description = """
Please see:
https://github.com/Minyus/srsly-cli
"""

setup(
    name="srsly_cli",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": [entry_point]},
    install_requires=requires,
    description="CLI to convert between JSON, JSONL, YAML, MessagePack, and Pickle using srsly",
    license="Apache Software License (Apache 2.0)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Minyus/srsly-cli",
    author="Yusuke Minami",
    author_email="me@minyus.github.com",
    zip_safe=False,
    keywords="JSON, JSONL, YAML, MessagePack, Pickle",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
)
