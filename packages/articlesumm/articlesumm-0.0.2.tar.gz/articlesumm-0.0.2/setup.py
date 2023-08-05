from setuptools import setup, find_packages


classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]


with open("README.md", "r") as fh:
    long_description = fh.read()

#long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
setup(
  name='articlesumm',
  version='0.0.2',
  description='Custom scientific/research article summarization library based on Statistical features',
  #long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='',  
  author='Maxwell Tetteh',
  author_email='tettehmaxwell11@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='text summarization, scientific articles', 
  packages=find_packages(),
  install_requires=[
    'requests>=2.26.0',
    'nltk>=3.6.5',
    ]
)
