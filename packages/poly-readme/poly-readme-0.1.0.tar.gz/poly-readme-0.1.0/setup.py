from setuptools import setup, find_packages

setup(
    name='poly-readme',  # Package name
    version='0.1.0',  # Package version
    description='A tool to translate README files into multiple languages using ChatGPT.',
    long_description=open('README.md').read(),  # PyPI 페이지에서 보여질 설명
    long_description_content_type='text/markdown',  # README 형식
    author='Chad Lee',  # Author name
    author_email='think.bicycle@gmail.com',  # Author email
    url='https://github.com/drllr/poly-readme',  # GitHub URL
    packages=find_packages(where="src"),  # Find packages in the src directory
    package_dir={"": "src"},  # Specify src directory as the package root
    install_requires=[
        'openai>=1.0.0',
        'questionary>=1.10.0',
        'keyring>=24.0.0',
        'PyYAML>=6.0.0',
    ],
    entry_points={
        'console_scripts': [
            'poly-readme=poly_readme.cli:main',  # Map CLI command to entry point
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Minimum Python version
    license="MIT",  # Package license
)
