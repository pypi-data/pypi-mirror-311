from setuptools import setup, find_packages

setup(
    name='mpplot',
    version='0.2',
    packages=find_packages(),
    install_requires=["h5py>=3.12.1","matplotlib>=3.9.2"],
    entry_points={
        'console_scripts': [
            'my_package_script = my_package.module1:main_function',
        ],
    },
    author='kevin',
    author_email='kevin2059@163.com',
    description='mpplot that connect matplotlib and matlab',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/your_username/my_package',
    license='MIT',
)
