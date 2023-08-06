from setuptools import setup,find_packages
 
setup(name='chanpackage',
      version='0.2',
      description='insert zabbix SLA',
      url='',
      author='channox',
      author_email='std3.40160@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires= ['numpy','urllib3','requests'],
      python_requires='>=3.8',
      zip_safe=False)