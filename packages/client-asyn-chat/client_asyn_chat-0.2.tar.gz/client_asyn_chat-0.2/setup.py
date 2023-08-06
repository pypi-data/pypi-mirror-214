from setuptools import setup, find_packages

setup(name='client_asyn_chat',
      version='0.2',
      description='Client packet',
      packages=find_packages(),
      author_email='ya_alexander@mail.ru',
      author='Alex Ya',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )
