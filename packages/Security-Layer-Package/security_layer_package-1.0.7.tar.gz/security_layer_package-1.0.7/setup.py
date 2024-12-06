from setuptools import setup

setup(
    name='Security_Layer_Package',
    version='1.0.7',
    author='Rawaa Ahmed',
    author_email='rawaa.ahmed@ejada.com',
    description='this is a description of my package.',
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