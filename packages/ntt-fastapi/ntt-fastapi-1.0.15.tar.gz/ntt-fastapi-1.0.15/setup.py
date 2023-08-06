from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='ntt-fastapi',
    version='1.0.15',
    author='threezinedine',
    author_email='threezinedine@email.com',
    description='The Framework which helps developers work with FastAPI easier',
    packages=find_packages(),
    package_data={
        '': ['*.env', '.txt', '.gitignore'],
    },
    data_files=[('nttfastapi\source_code_assets', ['nttfastapi\source_code_assets\.env',
                      'nttfastapi\source_code_assets\.example.env', 
                      'nttfastapi\source_code_assets\.gitignore'])],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/threezinedine/ntt-fastapi',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'nttfastapi=nttfastapi.cli:main'
        ],
    },
)