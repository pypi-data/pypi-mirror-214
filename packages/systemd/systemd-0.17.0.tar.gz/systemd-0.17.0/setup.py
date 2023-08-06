from setuptools import setup


setup(
    name="systemd",
    version="0.17.0",
    packages=['.'],
    package_dir={'': 'src'},
    license="Apache",
    description="systemd wrapper in Cython",
    long_description=open("README.rst").read(),
    platforms=["POSIX"],
    url='http://github.com/mosquito/cysystemd',
    provides=["systemd"],
    install_requires=['cysystemd'],
    keywords="systemd, python, daemon, sd_notify, cython",
)
