from setuptools import setup, find_packages
import os

version = '0.10.dev0'


install_requires = [
    'setuptools',
    'cromlech.marshallers',
    'redis',
    'zope.component',
]

tests_require = [
    'pytest',
    'pytest-redis >= 1.3.2',
]

setup(name='uvc.cache',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uvc'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      )
