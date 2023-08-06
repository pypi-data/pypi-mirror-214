import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='lxml_to_dict_total',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://github.com/admelix/lxml_to_dict',
    license='MPL-2.0 license',
    author='Jose Sakuda',
    author_email='sakudacastro@gmail.com',
    description='A simple conversion of an lxml.objectify element to a python dictionary.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pytest-cov',
        'pytest',
        'twine',
        'lxml'
    ]
)