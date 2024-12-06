# -*- coding: utf-8 -*-
#
# copyright (c) 06-2024 G. Benabdellah
# Departement of physic
# University of Tiaret , Algeria
# E-mail ghlam.benabdellah@gmail.com
#
# this program is part of btpgui 
# first creation 15-11-2024
#  
#
# License: GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#  log change:
#
#
#


import sys
from setuptools import setup, find_packages


# Custom function to check for tkinter
def check_tkinter():
    try:
        import tkinter
    except ImportError:
        print("")
        print("tkinter is not installed. Please install it to use this package.")
        print("")
        print("For Debian-based systems, run:    sudo apt-get install python3-tk")
        print("For Red Hat-based systems, run:   sudo dnf install python3-tkinter")
        print("For Arch Linux, run: sudo pacman -S tk")
        print("")
        sys.exit(1)

# Run the tkinter check
check_tkinter()

setup(
    name='btpgui',
    version='1.0.2',
    author='G. Benabdellah',
    author_email='ghlam.benabdellah@gmail.com',
    description='Interface graphic to BoltzTraP2',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ghlam14',  # Replace with your project's URL
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'btpgui': ['gather_energys.pl'],
    },
    install_requires=[
        'packaging ',
        'matplotlib',
        'Pillow',
        'tk',
        'BoltZtraP2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'btpgui = boltzGUI.main:main',
        ],
    },
)

