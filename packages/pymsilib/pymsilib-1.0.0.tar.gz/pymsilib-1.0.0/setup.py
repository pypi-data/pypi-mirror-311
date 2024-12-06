from setuptools import Extension, setup

module = Extension('pymsilib._msi',
    libraries = ['Msi','Rpcrt4', 'Cabinet'],
    sources = ['src/_msi.c'],
)

setup(
    #name="pymsilib",
    #description = 'msilib replacement',
    #long_description_content_type = 'text/x-rst',
    #author = 'Trevor Hamm',
    #author_email = 'alohaeh@gmail.com',
    ext_modules=[module],
)

