import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="taxontabletools2", # Replace with your own username
    version="2.0.0",
    author="Till-Hendrik Macher",
    author_email="macher@uni-trier.de",
    description="taxontabletools - A comprehensive, platform-independent graphical user interface software to explore and visualise DNA metabarcoding data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/taxontabletools2",
    packages=setuptools.find_packages(),
    license = 'MIT',
    install_requires = [
            'matplotlib == 3.6.3',
            'matplotlib_venn == 0.11.7',
            'numpy == 2.1.3',
            'pandas == 2.2.3',
            'plotly == 5.9.0',
            'psutil == 5.9.4',
            'pymannkendall == 1.4.3',
            'Requests == 2.32.3',
            'scipy == 1.14.1',
            'seqconverter == 3.1.0',
            'statsmodels == 0.13.5',
            'stqdm == 0.0.5',
            'streamlit == 1.25.0',
            'update_checker == 0.18.0'
    ],
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points = {
        "console_scripts" : [
            "taxontabletools2 = taxontabletools2.__main__:main",
        ]
    },
)
