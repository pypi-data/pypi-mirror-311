from setuptools import setup

setup(
    name='Correct_TDS_Sami',
    version='0.1.1',    
    description='working correct TDS software by Le Guilcher Sami with all packages',
    url='https://github.com/THzbiophotonics/Correct-TDS-in-development/tree/Sami',
    author='Le Guilcher Sami',
    author_email='sami.leguil@gmail.com',
    license='IEMN',
    packages=['Correct_TDS_Sami'],
    python_requires='>=3.9, <3.13',
    install_requires=[
        'mpi4py>=2.0',
        'numpy',  
        'PyQt5>=5.15.0',
        'matplotlib>=3.5.0',
        'h5py>=3.6.0',
        'scipy>=1.8.0',
        'scikit-learn>=1.0.0',
        'numba>=0.57.0, <0.61.0',
        'pyswarm'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)