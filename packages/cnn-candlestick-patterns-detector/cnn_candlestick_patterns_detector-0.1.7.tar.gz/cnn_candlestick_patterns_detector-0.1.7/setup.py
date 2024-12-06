from setuptools import setup, find_packages

setup(
    name='cnn_candlestick_patterns_detector',
    version='0.1.7',
    packages=find_packages(include=['cnn_candlestick_patterns_detector', 'cnn_candlestick_patterns_detector.*']),
    include_package_data=True,
    package_data={
        'cnn_candlestick_patterns_detector': ['**/*.pth', '**/*.py'],
    },
    install_requires=[
        'torch',
        'numpy',
    ],
    author='Maksym Usanin',
    author_email='usanin.max@gmail.com',
    description='CNN classifier for candlestick patterns size 7',
    python_requires=">=3.11",
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)