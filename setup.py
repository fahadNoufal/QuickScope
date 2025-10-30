import setuptools

with open("README.md","r",encoding='utf-8') as f:
    description = f.read()

__version__ = "0.0.0"

REPO_NAME = 'QuickScope'
AUTHOR_USER_NAME ='fahadNoufal'
SRC_REPO = 'QuickScope'
AUTHOR_EMAIL = 'fhdnaufal@gmail.com'

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="QuickScope offers a smarter way to stay updated.",
    long_description=description,
    long_description_content_type='text/markdown',
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src")
)