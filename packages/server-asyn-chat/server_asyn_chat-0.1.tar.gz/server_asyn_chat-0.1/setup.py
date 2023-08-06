from setuptools import setup, find_packages

setup(name='server_asyn_chat',
      version='0.1',
      description='Server packet',
      packages=find_packages(),
      author_email='ya_alexander@mail.ru',
      author='Alex Ya',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )