from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "KitronikPicoSmartAirQuality",
    version = "1.0.1",
    description = "Kitronik Air Quality Datalogging Board for Pico",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ["PicoAirQuality"],
)