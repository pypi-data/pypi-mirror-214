from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Dataselector',
  version='0.0.1',
  description='A handy library to import dataset from various excel file types and URls',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Siddharth Mishra',
  author_email='Siddharth.mishra@ganitinc.co.in',
  license='MIT', 
  classifiers=classifiers,
  keywords='Dataset, Import, URl, CSV', 
  packages=find_packages(),
  install_requires=[''] 
)