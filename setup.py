from setuptools import setup, find_packages

setup(name="saaskit-main",
           version="0.1",
           description="Django project for main site of saaskit",
           author="SaaSKit",
           author_email="admin@saaskit.org",
           packages=find_packages(),
           include_package_data=True,
)

