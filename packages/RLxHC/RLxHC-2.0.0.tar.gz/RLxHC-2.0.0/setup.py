import setuptools
setuptools.setup(

    name='RLxHC',
    version='2.0.0',
    author='Santiago Ulloa',
    author_email='nestor2215739@correo.uis.edu.co',
    description='esta libreria resuelve circuitos RLC en serie y paralelo',
    url='https://github.com/santiagou02/programacion',
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
        classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
   
)