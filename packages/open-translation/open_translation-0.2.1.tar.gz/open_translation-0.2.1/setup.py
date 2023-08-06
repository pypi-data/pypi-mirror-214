from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='open_translation',
    version='0.2.1',
    description='Open Translation',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/cahya-wirawan/OpenTranslation',
    author='Cahya Wirawan',
    author_email='cahya.wirawan@gmail.com',
    license='MIT',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
    ],
)
