from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='pytrics',
    version='1.1.0',
    description='Python based Qualtrics survey integration',
    long_description_content_type="text/markdown",
    long_description=README,
    license='GPLv2',
    packages=find_packages(),
    author='60 Decibels Inc.',
    author_email='tech@60decibels.com',
    keywords=['Qualtrics', 'Survey', 'Tool'],
    url='https://github.com/60decibels/pytrics',
    download_url='https://pypi.org/project/pytrics/',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
    ],
)

install_requires = [
    'requests>=2.21.0',
    'progress>=1.5'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
