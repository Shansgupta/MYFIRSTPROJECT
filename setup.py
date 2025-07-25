from setuptools import find_packages,setup
from typing import List

Hypen = '-e .'
def get_requirement(file_path:str)->List[str]:
    requirements=[]
    
    with open(file_path) as file_obj :
        requirements = file_obj.readlines()
        requirements =[req.strip() for req in requirements]
        if Hypen in requirements:
           requirements.remove(Hypen)

    return requirements        


setup(
    name = 'FIRSTPROJECT',
    version = '0.0.1',
    author = 'Shantanu',
    author_email = '22ucc094@lnmiit.ac.in',
    packages = find_packages(),
    install_requires = get_requirement('requirements.txt')
   ## install_requires = ['pandas','numpy','seaborn']
)