from setuptools import setup, find_packages

setup(name="LwmaL_mess_server",
      version="0.8.7",
      description="LwmaL_mess_server",
      author="ivan",
      author_email="ivansyn2013@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
