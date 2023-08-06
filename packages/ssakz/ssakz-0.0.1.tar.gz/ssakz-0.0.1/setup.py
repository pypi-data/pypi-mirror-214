from setuptools import setup

setup(
    name='ssakz',
    version='0.0.1',
    description='Client API for ssa.fai.kz',
    url='https://github.com/fai-kz/ssakz',
    author='FAI',
    author_email='ssakz@fai.kz',
    license='MIT',
    py_modules=['ssakz'],
    install_requires=[
        'pyzmq',
    ],
    zip_safe=False
)
