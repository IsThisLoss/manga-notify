import os
import setuptools


def get_dependencies():
    root = os.path.dirname(os.path.realpath(__file__))
    requirements = os.path.join(root, 'requirements.txt')
    result = []
    if os.path.isfile(requirements):
        with open(requirements) as f:
            result = f.read().splitlines()
    return result


setuptools.setup(
    name="manga_notify",
    version="1.0.0",
    author="isthisloss",
    author_email="kopturovdim@gmail.com",
    description="Tool to get notifications on feeds update",
    packages=setuptools.find_packages(),
    install_requires=get_dependencies(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
