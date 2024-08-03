"""
    https://skippd.medium.com/handling-multiple-versions-of-a-package-in-python-73055998ce73

"""

PYDANTIC_FOLDER = './pydantic_versions'
NECESSARY_VERSIONS = ['1.10.17', '2.8.2']


from pypi_multi_versions.importer import import_helper
from pypi_multi_versions.installer import install_version


for version in NECESSARY_VERSIONS:
    try:
        with import_helper('pydantic', version, PYDANTIC_FOLDER):
            import pydantic
    
    except Exception as e:
        install_version('pydantic', version, PYDANTIC_FOLDER)
