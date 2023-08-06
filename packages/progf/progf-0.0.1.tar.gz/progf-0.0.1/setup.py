from setuptools import setup, find_packages

setup(
    name='progf',
    version='0.0.1',
    description='Python game framework with pygame',
    author='Coder-Jang',
    author_email='jsb060624@kakao.com',
    install_requires=['pygame'],
    packages=["Project"],
    keywords=['game', 'project', 'pygame'],
    python_requires='>=3.6',
    package_data={"Project":["project.jpg"]},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)