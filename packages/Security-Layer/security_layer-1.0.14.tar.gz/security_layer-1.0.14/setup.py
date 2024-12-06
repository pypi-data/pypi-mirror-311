from setuptools import setup

setup(
    name='Security_Layer',
    version='1.0.14',
    author='Rawaa Ahmed',
    author_email='rawaa.ahmed@ejada.com',
    description='Details about the package',
    packages=['Security_Layer_Package'],#, 'module_name.config'],
    package_data={
        # 'module_name': ['config/rules.yml'],
    },
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        # 'dependency2',
        # List any other dependencies your module requires
    ],
)