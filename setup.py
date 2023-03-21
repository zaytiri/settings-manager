from setuptools import setup
import pathlib
from version.progsettings import get_version

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

version = get_version()

setup(
    name="margument",
    version=version,
    description="python library to manage configurations from program arguments including doing commands and saving configurations in a yaml file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zaytiri/settings-manager",
    project_urls={
        'GitHub': 'https://github.com/zaytiri/settings-manager',
        'Changelog': 'https://github.com/zaytiri/settings-manager/blob/main/CHANGELOG.md',
    },
    author="zaytiri",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    keywords="manager, configurations, settings, arguments, argparse, yaml, save",
    package_data={'margument': ['progsettings.yaml']},
    packages=["margument", "margument"],
    python_requires=">=3.10.6",
    install_requires=[
      "PyYAML~=6.0"
    ],
    # entry_points={
    #     "console_scripts": [
    #         "margument=margument:app.main",
    #     ],
    # }
)