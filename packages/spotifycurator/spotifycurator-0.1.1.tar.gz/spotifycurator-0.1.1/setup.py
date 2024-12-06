from setuptools import setup, find_packages

setup(
    name="spotifycurator", 
    version="0.1.1",
    description="A tool to create public Spotify playlists from liked songs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Noah Mathew",
    author_email="n.t.mathew@outlook.com",
    url="https://github.com/dysous/spotifycurator",
    license="MIT",  # Choose an open-source license
    packages=find_packages(),  # Automatically find packages in your project
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
        "spotifycurator=spotifycurator.spotifycurator:main",
        ]
    },
    python_requires=">=3.7",
)
