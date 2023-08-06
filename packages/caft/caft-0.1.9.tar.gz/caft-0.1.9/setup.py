"""Package setup for caft."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

short_name = "caft"
author = "Joshua Dunn"
git_author = "joshdunnlime"

setuptools.setup(
    name="caft",
    author=author,
    author_email="joshua.t.dunn@hotmail.co.uk",
    description=(
        "Continuous Affine Feature Transformations for feature mapping."
    ),
    keywords="feature-engineering feature-mapping, anomaly-detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{git_author}/{short_name}",
    project_urls={
        "Documentation": f"https://github.com/{git_author}/{short_name}",
        "Bug Reports": f"https://github.com/{git_author}/{short_name}/issues",
        "Source Code": f"https://github.com/{git_author}/{short_name}",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        # see https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "sympy>=1.11.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
    ],
    extras_require={
        "dev": ["check-manifest"],
        # 'test': ['coverage'],
    },
)
