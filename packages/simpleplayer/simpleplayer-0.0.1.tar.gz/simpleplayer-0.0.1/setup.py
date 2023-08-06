from setuptools import setup

# Read the contents of README.md file
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='simpleplayer',
    version='0.0.1',
    description='Discover the pinnacle of audio elegance with this simple-player module, boasting a sophisticated blend of advanced features and seamless compatibility across multiple platforms.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TOWDIO',
    author_email='thowiestudio@gmail.com',
    packages=['simpleplayer'],
    install_requires=[
        'soundfile',
        'sounddevice',
        'numpy',
        'gtts',
    ],
    entry_points={
        'console_scripts': [
            'simpleplayer = simpleplayer.simpleplayer:main',
            'voicegen = simpleplayer.voicegen:main',
        ],
    },
    license='MIT',
)