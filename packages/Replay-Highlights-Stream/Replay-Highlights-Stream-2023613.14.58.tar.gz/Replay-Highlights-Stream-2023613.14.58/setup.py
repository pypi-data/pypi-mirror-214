from setuptools import setup

setup(
    name="Replay-Highlights-Stream",
    version="2023613.14.58",
    author="Oliver Consterla Araya",
    author_email="oliver_consterla@yahoo.cl",
    description="Replay de las mejores jugadas de capturadas por apps de Overwolf",
    long_description="Utilizando aplicaciones y tecnologia de python para crear un programa que permita reproducir los mejores momentos de un juego obtenido por medio de una app del software Overwolf como Outplayed.",
    long_description_content_type="text/markdown",
    url="https://github.com/Alderan-Smile/Replay-Highlights-Stream",
    packages=["replay_highlights_stream"],
    install_requires=[
        "watchdog",
        "moviepy",
        "pyglet",
        "pydub"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
