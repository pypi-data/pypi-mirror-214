from setuptools import setup, find_packages
from setuptools.extension import Extension

# extension = Extension('your_module_name', ['your_module.py'], libraries=['your_dll'])
dll_files=['lib/AudioPrecision.API.dll','lib/AudioPrecision.API2.dll']
setup(
    name='ap_package',
    version='1.0.0',
    author='hatcher',
    author_email='your@email.com',
    description='A description of your library',
    packages=find_packages(),
    package_data={'ap_package': ['lib/*.dll']},
    data_files=[('', dll_files)],

    install_requires=[],
)
        