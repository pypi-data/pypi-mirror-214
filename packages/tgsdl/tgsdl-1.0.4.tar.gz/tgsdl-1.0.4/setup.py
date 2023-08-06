from setuptools import setup, find_packages
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_dir, 'README.md')

setup(
    name='tgsdl',
    version='1.0.4',
    description='Telegram Sticker Pack Downloader Library',
    author='Bevlil',
    author_email='voidlillis@gmail.com',
    url='https://github.com/lillisfeb/TGSDL/',
    long_description = open(readme_path).read(),
    long_description_content_type='text/markdown',
    keywords=['telegram', 'bot', 'sticker', 'download', 'stickerpack'],
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorclip'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'tgsdl = tgsdl:main'
        ]
    }
)
