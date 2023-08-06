from setuptools import setup

setup(
    name='cropnet',
    version='0.1.1',
    description='A Python package for the CropNet dataset',
    author='Anonymous AI4Science',
    author_email='anonymous.ai4science@gmail.com',
    license='Free for non-commercial use',
    packages=['dataset'],
    install_requires=[
        'torch >= 1.11.0',
        'numpy',
        'torchvision',
        'numpy',
        'pandas',
        'h5py',
        'Pillow',
        'einops',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
