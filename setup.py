from setuptools import setup


def readme():
    with open('README.md') as readme_file:
        return readme_file.read()

__version__ = ''
#pylint: disable=exec-used
exec(open('boterham/version.py').read())

setup(
    name='panda3d-boterham',
    version=__version__,
    description='Pre-and-post-processor for blend2bam, a tool to convert Blender blend files to Panda3D BAM files',
    long_description=readme(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='panda3d gamedev',
    url='https://github.com/janentikan/panda3d-boterham',
    author='jan Entikan',
    license='MIT',
    packages=['boterham'],
    include_package_data=True,
    install_requires=[
        'panda3d',
        'panda3d-gltf',
        'panda3d-blend2bam',
    ],
    entry_points={
        'console_scripts':[
            'boterham=boterham.cli:main',
        ],
    },
)
