from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Dutch-Document-Validator',
  version='0.0.1',
  description='A basic ducth document validator',
  url='',  
  author='Ankit Gupta',
  author_email='devankitgupta01@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='dutch document validator', 
  packages=find_packages(),
  install_requires=[''] 
)