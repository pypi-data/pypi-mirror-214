""" Setup file for pypi package."""

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='LuaAutoDoc',
    version='0.9.1',
    description='Generates full HTML documentation of a Lua project with LuaDoc tags.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/UlrikHD/LuaAutoDoc',
    project_urls={
        'Bug Tracker': 'https://gitlab.com/UlrikHD/LuaAutoDoc/-/issues',
    },
    entry_points={
        'console_scripts': [
            'LuaAutoDoc=lua_auto_doc.lua_auto_doc:main',
        ],
    },
    author='Ulrik Holtgaard Digerud',
    author_email='githubuhd@runbox.com',
    license='MIT License',
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Documentation',
        'Topic :: Software Development :: Documentation',
        'Typing :: Typed',
    ],
    keywords='Lua, documentation, LuaDoc, HTML, LuaAutoDoc, autodoc, auto documentation, Lua documentation',
    packages=find_packages(),
    package_data={
        'lua_auto_doc': [
            'Config_LuaAutoDoc.json',
            'modules/highlighter/LuaBuiltInCache.json',
            'Assets/*.svg',
            'Assets/*.txt',
            'Assets/*.ttf',
            'Favicon/*.png',
            'Favicon/*.svg',
            'Favicon/*.xml',
            'Favicon/*.webmanifest',
            'HTMLFragments/*/*.html',
            'Scripts/*.js',
            'StyleSheets/*.css',
        ]
    },
    python_requires='>=3.10',
)
