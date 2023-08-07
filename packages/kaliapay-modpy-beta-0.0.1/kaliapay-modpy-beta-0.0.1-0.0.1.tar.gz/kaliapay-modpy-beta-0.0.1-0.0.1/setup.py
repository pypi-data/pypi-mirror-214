from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Module de paiement Kaliapay'
LONG_DESCRIPTION = "Module de paiement développer pour faciliter l'intégration de Kaliapay dans vos projets."

# Setting up
setup(
    name="kaliapay-modpy-beta-0.0.1",
    version=VERSION,
    author="Fabio",
    author_email="<nadefabrice83@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'paiement', 'kaliapay', 'module']
)