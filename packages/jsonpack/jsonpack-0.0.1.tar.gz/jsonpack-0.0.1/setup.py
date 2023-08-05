import setuptools

with open('README.md') as f:
    long_description = f.read()

required_modules = []

setuptools.setup(
    name='jsonpack',
    version='0.0.1',
    author='Legopitstop',
    description='Easily create JSON packs for your Python Application.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/legopitstop/jsonpack',
    packages=setuptools.find_packages(),
    install_requires=required_modules,
    license='MIT',
    keywords=['json', 'pack', 'manifest', 'scripts', 'events', 'components', 'Pillow'],
    author_email='officiallegopitstop@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6'
)