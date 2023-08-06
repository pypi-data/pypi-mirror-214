import setuptools
setuptools.setup(

    name='trifasicos',
    version='1.0.0',
    author='Nicolas Velasco',
    author_email='nicolasvelascoalvarez7@gmail.com',
    description='esta libreria resuelvas sistemas trifasicos',
    url='https://github.com/nicolasve18/trifasicos',
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
        classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
   
)
