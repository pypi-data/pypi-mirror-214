from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pillar1',
    version='0.1.1',
    packages=find_packages(),
    description='Official package for Pillar1 company',
    author='Ayman Hajja',
    author_email='amhajja@gmail.com',
    url='https://github.com/amhajja/pillar1',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
