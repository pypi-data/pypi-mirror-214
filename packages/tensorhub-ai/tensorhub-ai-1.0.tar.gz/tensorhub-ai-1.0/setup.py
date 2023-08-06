# Copyright 2023 The TensorHub Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import setuptools

with open("README.md", mode="r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tensorhub-ai",
    version="1.0",
    author="Udyam AI",
    author_email="",
    description="A simple, modular and repeatable abstractions framework to accelerate deep learning research and application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udyam-ai/tensorhub-ai",
    license="Apache-2.0",
    packages=setuptools.find_packages(exclude=[".github", "metadata", "notebooks"]),
    install_requires=[
        "tensorflow"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
