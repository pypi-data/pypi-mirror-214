from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='micropython_wifi_communication',
    version='0.0.1',
    license='MIT License',
    author='issei momonge',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='mggyggf@gmail.com',
    keywords='socket communication via wifi',
    description=u'um substituto para em vez de uma comunicação RF utilizar wifi',
    packages=['comu'],
    install_requires=[''],)