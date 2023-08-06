from setuptools import setup

requirements_list = [
	'certifi',
	'charset-normalizer',
	'click',
	'colorama',
	'enum34',
	'idna',
	'pexpect',
	'ptyprocess',
	'typing_extensions',
	'urllib3==1.26.6',
	'requests',
	'passpy',
]

setup(
	name='vaultpass',
    	version='1.0.16',    
    	description='VaultPass: A CyberArk Search Script. Search for accounts and retrieve their passwords in the CyberArk elevated access management application. You can only retrieve accounts that you are able to view.',
    	url='https://github.com/mjackstewart/vaultpass',
    	author='Jack Stewart',
    	author_email='mjackstewart@gmail.com',
    	license='Unilicense',
    	packages=['vaultpass'],
	setup_requires=requirements_list,
    	install_requires=requirements_list,

	classifiers=[
		'Development Status :: 1 - Planning',
		'Intended Audience :: Information Technology',
		'License :: Free for non-commercial use',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3',
	],

	scripts=[
		'scripts/vaultpass.py',
		'scripts/vaultpass-direct.py',
	],
)

