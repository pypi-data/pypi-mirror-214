from setuptools import setup

setup(name='hurricaneapi',
      version='0.1.5',
      url='https://github.com/daniil49926/hurricaneapi',
      license='MIT',
      author='Shchipko Daniil',
      description='Hurricaneapi framework',
      packages=['hurricaneapi', 'hurricaneapi.responses', 'hurricaneapi.routing'],
      author_email='daniil49925@ya.ru',
      long_description=open('README.md').read(),
      zip_safe=False
      )
