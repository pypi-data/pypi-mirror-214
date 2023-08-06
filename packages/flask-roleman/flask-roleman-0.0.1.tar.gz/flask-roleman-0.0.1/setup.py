from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Flask Extension to add the Authorization functionality to your apps.'

# Setting up
setup(
    name="flask-roleman",
    version=VERSION,
    author="Mohamed El-Hasnaouy",
    author_email="<elhasnaouymed@proton.me>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['flask', 'flask_login', 'flask_sqlalchemy'],
    keywords=['flask', 'role', 'authorization', 'permissions', 'security'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
