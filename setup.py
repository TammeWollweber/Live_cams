import setuptools

with open('README.md', 'r') as fptr:
    long_desc = fptr.read()

setuptools.setup(
    name='live_cams',
    version='0.1',
    author='Fabian Scheiba and Tamme Wollweber',
    author_email='fabian.scheiba@cfel.de',
    description='GUI for live view of basler cameras',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='git@github.com:TammeWollweber/live_cams.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Visualization',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pyqt5',
        'matplotlib',
        'pyqtgraph',
        'pyyaml',
	'pypylon',
	'pillow',
    ],
)
