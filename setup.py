from setuptools import setup

setup(name='link-backup',
      version='0.1',
      description='Program to create an incremental backup',
      url='https://github.com/xadlien/link-backup',
      author='Daniel Martin',
      author_email='djm24862@gmail.com',
      packages=['link-backup'],
      entry_points = {
          'console_scripts': ['link-backup=link-backup.__main__.main']
      },
      zip_safe=False)