#!/usr/bin/env python2

import xpyvideos
from distutils.core import setup
from setuptools import find_packages
from os import remove


setup(name		=		'xpyvideos',
      version		=		'0.0.2-7',
      description	=		'Python program for downloading videos from xvideos, xhamster, and redtube.',
      author		=		'Darth_O-Ring',
      author_email	=		'darthoring@gmail.com',
      url		=		'https://github.com/Darth-O-Ring/xpyvideos',
      packages		=		find_packages(),
      package_dir	=		{'xpyvideos' : 'xpyvideos/'},
      scripts		=		['xpyvideos/xpyvideos.py', 'xpyvideos/regexes.py', 'xpyvideos/download.py',
      						'xpyvideos/filename.py'],
      data_files	=		[('share/xpyvideos', ['README.md', 'NOTICE'])]
	)
print '\n\nCleaning up...\n\n'
try:
	remove('/usr/bin/opts.py')
except:
	pass
