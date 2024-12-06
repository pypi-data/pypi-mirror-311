from setuptools import setup, find_packages

setup(
    name='my_latex_generator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Здесь можно указать зависимости, если они есть
    ],
    author='Mikhail Borisov',
    author_email='mishaborisov2013@gmail.com',
    description='A small package to generate LaTeX',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
