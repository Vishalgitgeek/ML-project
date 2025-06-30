from setuptools import setup

# it would return retquirements list
def get_requirements(file_path:str)->list[str]:

    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [requirement.replace("\n", "") for requirement in requirements]

        return requirements


setup(
    name='Mlproject',
    version='0.0.1',
    author='Vishal Kumar',
    author_email='vishal29.ku@gmail.com',
    description='A sample Python package',
    packages= get_requirements('requirements.txt'),
    install_requires=[
        'numpy', 'pandas', 'seaborn'
    
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
