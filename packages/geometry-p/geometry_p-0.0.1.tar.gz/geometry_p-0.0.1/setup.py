from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='geometry_p',
  version='0.0.1',
  author='me',
  author_email='example@gmail.com',
  description='This is the simplest module for quick work with files.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
)