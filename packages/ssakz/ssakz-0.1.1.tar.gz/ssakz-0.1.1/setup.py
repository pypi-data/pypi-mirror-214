from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='ssakz',
    version='0.1.1',
    description='Client API for ssa.fai.kz',
    url='https://github.com/fai-kz/ssakz',
    author='FAI',
    author_email='ssakz@fai.kz',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    py_modules=['ssakz'],
    install_requires=[
        'pyzmq',
    ],
    zip_safe=False
)
