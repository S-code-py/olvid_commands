from setuptools import setup, find_packages

setup(
    name="olvid_command",
    version="0.3",
    packages=find_packages(),
    description="Integration of commands and commands group in olvid",
    author="SamBotPy",
    author_email="pypi.prideful261@passinbox.com",
    license="Open Source",
    install_requires=["olvid-bot", "asyncio", "typing"],
)