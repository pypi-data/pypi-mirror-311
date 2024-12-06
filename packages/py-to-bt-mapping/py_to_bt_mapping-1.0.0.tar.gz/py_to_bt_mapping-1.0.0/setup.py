from setuptools import setup 

with open('DESCRIPTION.txt') as file: 
    long_description = file.read() 

REQUIREMENTS = [
	'pywin32>=306',
    'pyserial>=3'	
] 

CLASSIFIERS = [ 
	'Intended Audience :: Developers', 
	'Topic :: Software Development :: Libraries :: Python Modules',  
	'Programming Language :: Python :: 3', 
	] 

setup(name='py_to_bt_mapping', 
	version='1.0.0', 
	description='BT-Basic to Python Mapping', 
    long_description=long_description,
    long_description_content_type='text/x-rst',
	url='https://bitbucket.it.keysight.com/projects/I3070SM/repos/i3070_2025/browse/BT_Basic_Mapping/operations.py?at=refs%2Fheads%2Ffeature%2FBT-Basic-to-Python-Mapping',  
	packages=['mapping'], 
	classifiers=CLASSIFIERS, 
	install_requires=REQUIREMENTS, 
	keywords='maps BT-Basic functions'
	) 