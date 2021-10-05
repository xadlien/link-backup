from setuptools import setup

setup(name='link-backup',
      version='0.2',
      description='Program to create an incremental backup',
      url='https://github.com/xadlien/link-backup',
      author='Daniel Martin',
      author_email='djm24862@gmail.com',
      packages=['linkbackup'],
      entry_points = {
          'console_scripts': ['link-backup=linkbackup.link_backup:main']
      },
      zip_safe=False)
