from setuptools import setup, find_packages

#Definimos el distribuible y su configuración
setup(
	name='Mensajes-Luis_David',
	version='6.0',
	description='Un paquete para saludar y despedir',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	author='Luis David López-Roberts Luzón',
	author_email='luisdavid.lrlmp@gmail.com',
	url='https://noesmidireccion.com',	
	license_files=['LICENSE'],
	packages=find_packages(),
	scripts=[],	
	test_suite='tests',
	install_requires=[paquete.strip() 
		for paquete in open("requirements.txt").readlines()],
	classifiers=[
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.12',
		'Topic :: Utilities'
	]
)
