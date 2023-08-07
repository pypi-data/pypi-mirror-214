from setuptools import setup, find_packages

setup_args = dict(
    name='faceid_core',
    version='0.1.1',
    description='Face Recognition',
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    author='Orhan Salahetdinov',
    author_email='salahetdinovorxan@gmail.com',
    keywords=['FaceId', 'Face Recognition', 'Python 3'],
    url='https://github.com/Or1onn/faceid-core',
    download_url='https://pypi.org/project/faceid-core/'
)

install_requires = [
    'opencv-python',
    'insightface',
    'numpy',
    'pathlib',
    'sklearn',
    'pyyaml',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
