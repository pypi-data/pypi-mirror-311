from setuptools import setup, find_packages

setup(
  name='ticketbookinglib',
  version='0.0.6',
  description='This is a simple booking notification alert shown for booking confirmation.',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Syam Sundar Reddy Maddula ',
  author_email='x23307862@student.ncirl.ie',
  license='MIT', 
  classifiers=[
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
],
  keywords='ticketbookinglib', 
  packages=find_packages(),
  python_requires=">=3.6"
)
