from setuptools import setup, find_packages

setup(
    name="vulheader",
    version="1.0.1",
    description="A Python tool for checking missing HTTP security headers for better web security.",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author="MrFidal",
    author_email="mrfidal@proton.me",
    url='https://mrfidal.in/cyber-security/vulheader',
    packages=find_packages(),
    install_requires=[
        "requests",
        "validlink",
    ],
    entry_points={
        'console_scripts': [
            'vulheader=vulheader.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=[
        "security headers",
        "web security",
        "HTTP headers",
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "Referrer-Policy",
        "vulnerability scanner",
        "website security",
    ],
    python_requires='>=3.7',
    license="MIT",
    project_urls={
        "Documentation": "https://mrfidal.in/cyber-security/vulheader",
        "Source": "https://github.com/mr-fidal/vulheader",
        "Tracker": "https://github.com/mr-fidal/vulheader/issues",
    },
)
