from setuptools import setup, find_packages

setup(
    name='my_package_windt',
    version='0.1.0',
    author='windt',
    author_email='sugar_626@163.com',
    description='A brief description of your package',
    # long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your_package',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
