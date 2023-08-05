from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='bs_orm',
    version='0.8.5',
    description='fix bug',
    packages=['bs_orm'],
    author_email='mr.z.75@mail.ru',
    zip_safe=False
    )