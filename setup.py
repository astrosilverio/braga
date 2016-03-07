import os
from setuptools import setup

version_file_py = os.path.join(os.path.split(__file__)[0], "braga/version.py")
with open(version_file_py) as version_file:
    __version__ = ""
    exec(compile(version_file.read(), version_file_py, 'exec'))

if __name__ == '__main__':
    setup(name='braga',
          version=__version__,
          description='Entity-Component system',
          url='http://github.com/astrosilverio/braga',
          author='astrosilverio',
          author_email='astrosilverio@gmail.com',
          license='MIT',
          packages=['braga'],
          zip_safe=False)
