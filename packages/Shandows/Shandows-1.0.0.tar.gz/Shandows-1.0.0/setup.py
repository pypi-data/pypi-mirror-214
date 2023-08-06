from setuptools import setup

setup(
	name='Shandows',
	version='1.0.0',
	author='Winstang',
	author_email='Winstang@hotmail.com',
	entry_points={
		'console_scripts': [
			'Shandows=Shandows:CLI'
		]
	},
)
