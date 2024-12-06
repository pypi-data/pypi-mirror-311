import pathlib

import setuptools

setuptools.setup(
    name="dammy7878carberra",
    version="0.1.0",
    description="A simple Python package",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://dammy7878.carberra.xyz",
    author="dabioye",
    author_email="dammyabioye1@gmail.com",
    license="The Unlicense",
    project_urls={
        "Documentation": "https://dammy7878.carberra.xyz",
        "Source": "https://github.com/dammy7878.carberra/pypi-tutorial",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10,<3.13",
    install_requires=["requests", "pandas>=2.0"],
    extra_require={
        "excel": ["openpyxl"],
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dammy7878_carberra = dammy7878carberra.cli:main",
        ],
    },
)
