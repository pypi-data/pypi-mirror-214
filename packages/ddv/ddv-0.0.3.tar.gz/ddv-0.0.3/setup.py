from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ddv',
  version='0.0.3',
  description='A basic dutch document validator',
  url='',  
  author='Ankit Gupta',
  author_email='devankitgupta01@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='dutch-docs-validator', 
  packages=find_packages(),
  install_requires=[''] 
)