from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Utils for tg_promo microservices.'

# Setting up
setup(
    name="tg-utils",
    version=VERSION,
    author="NeuralNine (Florian Dedov)",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'fastapi', 'idna', 'pydantic', 'pydantic_core', 'sniffio', 'SQLAlchemy',
        'starlette', 'typing_extensions', 'annotated-types', 'anyio', 'aio_pika'
    ],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6'
)