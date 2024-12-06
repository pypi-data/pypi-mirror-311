from setuptools import setup, find_packages


def read(f):
    with open(f, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name='django-x-console',
    version='0.1.4',
    author='yuhua.yang',
    license='GNU',
    author_email='13yhyang1@gmail.com',
    description='A simple web console based on Django.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',

    packages=find_packages(exclude=('tests', 'docs', 'django_web_console')),
    include_package_data=True,
    install_requires=[
        'Django>=4.2',
    ],
    python_requires='>=3.9',
    project_urls={
        'Source': 'https://github.com/ananan/django_web_console.git',
    },
)
