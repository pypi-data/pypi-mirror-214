from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='english-pidgin-dictionary',
    version='0.0.6',
    author='Isaac Yakubu',
    author_email='engrisaac1234@gmail.com',
    description='A simple pidgin-english dictionary for various applications',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Zeecoworld/pidgin-english-dictionary',
    packages=['english_pidgin_dict'],
    include_package_data=True,
    package_data={
        'english_pidgin_dict': ['data.json'],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

