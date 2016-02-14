from setuptools import setup

__version__ = '0.6.3'

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
