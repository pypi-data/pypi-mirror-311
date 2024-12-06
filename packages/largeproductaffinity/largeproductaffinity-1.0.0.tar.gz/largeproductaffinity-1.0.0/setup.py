from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


# Setting up
setup(
    name="largeproductaffinity",
    version="1.0.0",
    author="sarath babu",
    author_email="babusarath05@gmail.com",
    description='Description: large_product_affinity is used to obtain Product Affinity using big data without PySpark environment',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    py_modules=['largeproductaffinity'],
    #install_requires=['sklearn','pandas'],
    keywords=['python', 'apriori','product affinity','market basket analysis'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
