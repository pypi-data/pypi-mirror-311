from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='ticketbooking',
  version='0.0.1',
  description='This is a simple booking notification alert shown for booking confirmation.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Syam Sundar Reddy Maddula ',
  author_email='x23307862@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='ticketbooking', 
  packages=find_packages(),
  install_requires=[
    'flask',
    ] 
)
