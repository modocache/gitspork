from setuptools import setup

setup(
    name='gitspork',
    version='0.0.1a1',
    url='https://github.com/modocache/gitspork',
    author='modocache',
    author_email='modocache@gmail.com',
    description=(
        'Change the origin repository of your submodules '
        'to easily work on forks.'
    ),
    keywords='github submodule fork switch',
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Version Control',
    ],
    entry_points = {
        'console_scripts': [
            'gitspork = gitspork:main',
        ]
    }
)
