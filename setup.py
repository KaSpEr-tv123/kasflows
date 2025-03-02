from setuptools import setup, find_packages

setup(
    name='kasflows',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
    ],
    author='kasperenok',
    description='A library designed for kasflows between a server and a cheat script in Roblox, kasflows is an imitation and/or alternative mechanics of websockets made with API requests.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)