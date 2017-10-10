from setuptools import setup

from rap import watermark

setup(
    name=watermark.__pkgname__,
    description=watermark.__description__,
    version=watermark.__version__,
    packages=["rap.watermark"],
    entry_points="""
        [console_scripts]
        watermark=rap.watermark.entry:cli
    """
)
