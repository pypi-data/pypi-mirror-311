from setuptools import setup, find_packages

setup(
    name='jaiii',
    version='1.0.0',
    author='Jaisrinivasan J',
    author_email='jaiisrinivasan2305@gmail.com',
    description='A module with details and interesting facts about Jaisrinivasan J.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jaiisrinivasan',  # Add a GitHub URL if applicable
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
