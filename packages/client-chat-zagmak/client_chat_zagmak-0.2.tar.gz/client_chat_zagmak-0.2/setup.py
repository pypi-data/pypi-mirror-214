from setuptools import setup, find_packages

setup(name='client_chat_zagmak',
      version='0.2',
      description='Client packet',
      packages=find_packages(),
      author_email='test@mail.ru',
      author='Maxim Zaghreba',
      install_requeres=['PyQt5', 'sqlalchemy', 'pycruptodome', 'pycryptodomex']
      )
