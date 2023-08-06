from setuptools import setup, find_packages


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3'
]

setup(
    name='co-geo',
    version='0.0.1',
    description='Python library for 2d/3d coordinate geometry',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type ='text/markdown',
    url='https://github.com/utkarsh-naman/co-geo',
    author='Utkarsh Naman',
    author_email='its.utnam@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='co-geo geometry coordinate-geometry math evaluate calculate',
    packages=find_packages(),
    install_requires=['']
)