from setuptools import setup, find_packages

setup(name="LwmaL_mess_client",
      version="0.8.7",
      description="LwmaL_mess_client",
      author="Ivan_syn",
      author_email="ivansyn2013@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
