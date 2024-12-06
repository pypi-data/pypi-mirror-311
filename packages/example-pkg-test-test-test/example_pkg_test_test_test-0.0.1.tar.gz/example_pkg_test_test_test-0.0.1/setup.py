import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="example-pkg-test-test-test",
  version="0.0.1",
  author="LinBei",
  author_email="1249094042@qq.com",
  description="A small example package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/turuzidankii/compiler",
  packages=setuptools.find_packages(),
  install_requires=[
  "numpy>=1.21.0",
  ],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)