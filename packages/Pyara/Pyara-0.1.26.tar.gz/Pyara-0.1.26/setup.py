"""Metadata of package"""
from setuptools import setup, find_packages   # ,  pkg_resources

requirements = ['torch>=1.13.1',
                'torchaudio>=0.13.1'
                ]

# Создаст библиотеку для загрузки на PyPI
setup(name='Pyara',
      version='0.1.26',
      url='https://github.com/Millcool/Pyara.git',
      license='MIT',
      author='Ilya Mironov',
      author_email='ilyamironov210202@gmail.com',
      description='Library for audio classification',
      long_description=open('README.md').read(),
      long_description_content_type="text/markdown",
      packages=find_packages(exclude=['tests']), #where='src', include=['pyara*'],
      #package_dir={"":"src"},
      package_data={"pyara": ["*.bin"]},
      include_package_data=True,
      zip_safe=False,
      install_requires=requirements,
      platform='Any',
      classifiers=[
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent"
      ],
      )
