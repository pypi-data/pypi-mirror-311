from setuptools import setup

setup(
    name='Security_Layer',
    version='1.0.8',
    author='Rawaa Ahmed',
    author_email='rawaa.ahmed@ejada.com',
    description='Security Layer Package to make it easier to add security features to your LLM.',
    packages=['Security_Layer_Package'], #, 'Security_Layer_Package.config'
    package_data={
        'Security_Layer_Package': [],
    },
    include_package_data=True,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', #'description-content-type' must be one of ['text/markdown', 'text/plain', 'text/x-rst'], not 'code'.
    install_requires=[
        'requests'
        # List any other dependencies your module requires
    ],
)