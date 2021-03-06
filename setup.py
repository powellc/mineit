from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

version = __import__('mineit').__version__

install_requires = [
    'setuptools',
    'docopt==0.6.1',
]


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

setup(
    name="mineit",
    version=version,
    url='http://github.com/powellc/mineit',
    license='BSD',
    platforms=['OS Independent'],
    description="A simple command line tool for spinning up minecraft servers.",
    author="Colin Powell",
    author_email='colin.powell@gmail.com',
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    tests_require=['tox'],
    cmdclass={'test': Tox},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    package_dir={
        'mineit': 'mineit',
        #'mineit/templates': 'mineit/templates',
    },
    entry_points={
        'console_scripts': [
            'mineit = mineit.mineit:main',
        ],
    },
)
