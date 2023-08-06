from setuptools import find_packages, setup

setup(
    name='netbox_sb_dc_accessdata',
    version='1.1',
    description='SB DC Accessdata',
    long_description='Speedbone Datacenter Accessdata integration for netbox via plugin',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    author='Marco Krajniak',
    license='All rights reserved',
    keywords=['netbox', 'netbox-plugin', 'datacenter'],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)