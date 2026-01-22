from __future__ import annotations

from pathlib import Path
from setuptools import setup, Extension, find_packages

def read_readme() -> str:
    readme = Path(__file__).with_name("README.md")
    return readme.read_text(encoding="utf-8") if readme.exists() else ""

# --- Cython is optional at sdist time, but required to build from .pyx ---
try:
    from Cython.Build import cythonize
except Exception as e:
    cythonize = None

extensions = []

# Compile stock_ledger as an extension module that imports as `package.stock_ledger`
pyx_path = Path("package") / "stock_ledger.pyx"
if pyx_path.exists():
    if cythonize is None:
        raise RuntimeError(
            "Cython is required to build from package/stock_ledger.pyx. "
            "Install it with: pip install cython"
        )
    extensions = cythonize(
        [
            Extension(
                name="package.stock_ledger",
                sources=[str(pyx_path)],
            )
        ],
        compiler_directives={"language_level": "3"},
    )

setup(
    name="trading_deque_2",
    version="1.0.0",
    author="Alan MH Beem",
    author_email="Alan.Beem@seattlecolleges.edu",
    description="Refactored project from the CS DS Program at NSC",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlanBeem/TradingDeque_2",
    packages=find_packages(exclude=("tests", "docs")),
    ext_modules=extensions,
    include_package_data=True,  # allows MANIFEST/package_data to matter
    install_requires=[],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
