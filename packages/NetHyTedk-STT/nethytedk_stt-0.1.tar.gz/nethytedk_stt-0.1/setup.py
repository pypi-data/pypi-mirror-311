from setuptools import setup, find_packages

setup(
    name='NetHyTedk-STT',
    version='0.1',
    author='DIPU SARDAR',
    author_email='sardardipu397@gmail.com',
    description='This is a speech-to-text package created by Dipu Sardar',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver_manager'
    ],
    python_requires='>=3.6',
)
