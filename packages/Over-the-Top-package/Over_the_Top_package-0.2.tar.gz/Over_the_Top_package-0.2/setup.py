from setuptools import setup, find_packages
setup(
    name="Over_the_Top_package",
    version="0.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pygame",
    ],
    entry_points={
        'console_scripts': [
            'Over_the_Top = Over_the_Top.__main__:main'
        ]
    },
    package_data={
        '': ['Over_the_Top_package/assets/*'],
        '': ['Over_the_Top_package/levels/*'],
        '': ['Over_the_Top_package/levels/Tutorial/*'],
        '': ['Over_the_Top_package/classes.py'],
    },
)