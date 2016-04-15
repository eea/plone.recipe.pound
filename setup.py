""" Installer
"""
import os
from setuptools import setup, find_packages

NAME = 'plone.recipe.pound'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(os.path.join(*PATH)).read().strip()

entry_points = {"zc.buildout": ["build = plone.recipe.pound:BuildRecipe",
                                "config = plone.recipe.pound:ConfigureRecipe",]}

setup(name=NAME,
      version=VERSION,
      description="Recipe to install and configure Pound",
      long_description=(open("README.txt").read() + "\n" +
                        open(os.path.join("docs", "HISTORY.txt")).read()),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
        ],
      keywords='pound zope plone recipe',
      author='European Environment Agency',
      author_email='webadmin@eea.europa.eu',
      url='http://eea.github.io/docs/plone.recipe.pound',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zc.buildout',
          # -*- Extra requirements: -*-
          'zc.recipe.cmmi',
          'Cheetah',
      ],
      entry_points=entry_points,
      )
