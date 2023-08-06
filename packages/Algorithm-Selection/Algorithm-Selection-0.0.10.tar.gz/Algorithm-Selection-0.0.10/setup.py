from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Algorithm-Selection',
    version='0.0.10',
    license='MIT License',
    author='valfridojr',
    long_description='readme.MD',
    author_email='juniorprado@alu.ufc.br',
    keywords='metalearning',
    description=u'Functions dedicated to The Algoritm Selection problem with a focus on a metalearning approach',
    packages=['Algorithm-Selection'],
    install_requires=['requests','numpy','pandas','scikit-learn','scipy', 'os'],
    url = 'https://github.com/Junior-Prado/Algorithm-Selection'
)
