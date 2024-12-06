from setuptools import setup, find_packages

setup(
    name='filesortify',
    version='0.1',
    packages=find_packages(),
    description='A tool for organizing files by extension.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Himanshu Kumar Jha',
    author_email='himanshukrjha004@gmail.com',
    url='https://github.com/himanshu-kr-jha/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
