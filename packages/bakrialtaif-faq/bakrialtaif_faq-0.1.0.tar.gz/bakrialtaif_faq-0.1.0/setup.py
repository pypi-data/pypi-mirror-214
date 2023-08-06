from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()
    
setup(
    name='bakrialtaif_faq',
    version='0.1.0',    
    description='A example Python package',
    long_description=readme(),
    url='https://github.com/Bakrialtaif/bakrialtaif_faq',
    author='Bakri Altaif',
    author_email='altaif.bakri@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)
