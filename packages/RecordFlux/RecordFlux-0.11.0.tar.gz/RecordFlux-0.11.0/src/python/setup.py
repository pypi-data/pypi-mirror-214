


from setuptools import setup, find_packages


setup(
    name='Librflxlang',
    version='0.10.1.dev12+gcd91b2fa.d20230615',
    packages=['librflxlang'],
    package_data={
        'librflxlang':
            ['*.{}'.format(ext) for ext in ('dll', 'so', 'so.*', 'dylib')]
            + ["py.typed"],
    },
    zip_safe=False,
)
