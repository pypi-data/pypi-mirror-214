from setuptools import setup

setup(
    name="ADTomo",
    version="0.1.0",
    long_description="ADTomo",
    long_description_content_type="text/markdown",
    packages=["adtomo"],
    install_requires=["numpy",  "h5py", "matplotlib", "pandas"],
)
