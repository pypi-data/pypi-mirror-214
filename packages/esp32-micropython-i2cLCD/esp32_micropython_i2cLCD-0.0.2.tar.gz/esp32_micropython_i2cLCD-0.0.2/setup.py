from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='esp32_micropython_i2cLCD',
    version='0.0.2',
    license='MIT License',
    author='issei momonge',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mggyggf@gmail.com',
    keywords='esp32 micropython i2c LCD',
    description=u'uma biblioteca para utilização de um display i2c no esp32 micropython',
    packages=['LCD'],
    install_requires=[''],)