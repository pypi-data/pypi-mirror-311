from distutils.core import setup
from setuptools import find_packages

# with open("README.rst", "r") as f:
#   long_description = f.read()
setup(name='manteia_qa_pylinac',  # 包名
      version='1.3.0',  # 版本号
      description='pylinac custom made by manteia',
      long_description="use like pylinac,but some change for manteia",
      author='dengjianping',
      author_email='1601246283@qq.com',
      url='',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )