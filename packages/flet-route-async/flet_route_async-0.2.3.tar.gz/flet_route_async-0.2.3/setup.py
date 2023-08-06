from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name = "flet_route_async",
    version = "0.2.3",
    author="Saurabh Wadekar [ INDIA ]",
    packages=["flet_route_async"],
    license="MIT",
    requires=["flet","repath"],
    maintainer="Saurabh Wadekar",
    maintainer_email="saurabhwadekar420@gmail.com",
    keywords=["flet","routing","flet_route","routes","flet app","flet-route","flet simple routing"],
    description="This makes it easy to manage multiple views with dynamic routing.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/saurabhwadekar/flet_route"   
)