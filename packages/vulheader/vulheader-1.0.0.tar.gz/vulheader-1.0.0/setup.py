from setuptools import setup, find_packages

setup(
    name="vulheader",
    version="1.0.0",
    description="A tool for checking missing HTTP security headers",
    author="MrFidal",
    author_email="mrfidal@proton.me",
    url='https://mrfidal.in/cyber-security/vulheader',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown', 
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'vulheader=vulheader.cli:main',
        ],
    },
)
