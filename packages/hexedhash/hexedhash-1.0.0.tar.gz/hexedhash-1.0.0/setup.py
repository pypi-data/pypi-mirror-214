from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='hexedhash',
  version='1.0.0',
  author='maj0r',
  description='Creates hash by salt + hex',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/ltcp-security',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.10'
)