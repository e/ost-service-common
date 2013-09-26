from setuptools import setup, find_packages
readme = open('README.md').read()
setup(name='tdaf-ost-service-common',
      version='0.1',
      author='Marcos Bartolome',
      author_email='m@rcosbartolo.me',
      license='MIT',
      description='Common code for tdaf openstack service daemons',
      long_description=readme,
      packages=find_packages())

