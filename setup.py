from setuptools import setup

setup(name='SkillzUtil',
      version='1.0',
      description='Utility for Skillz 2018',
      url='http://github.com/ykaridi/CLI.py',
      author='ykaridi',
      license='MIT',
      packages=['SkillzUtil'],
      install_requires=[
          'selenium',
          'argparse'
      ],
      scripts=['bin/SkillzUtil'],
      entry_points={
          'console_scripts': ['SkillzUtil = SkillzUtil.CLI:main'],
      },
      zip_safe=False)
