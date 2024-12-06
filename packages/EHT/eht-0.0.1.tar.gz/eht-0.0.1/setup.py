from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# 확장 모듈 설정
ext_modules = [
    Extension(
        "EHT.EHT",
        sources=["EHT/EHT.pyx"],  # 올바른 소스 경로 지정
    )
]

setup(
    name="EHT",
    version="0.0.1",
    description="EHT",
    long_description_content_type="text/markdown",
    author='fourchains_R&D',
    author_email='fourchainsrd@gmail.com',
    package_dir={"EHT": "EHT"},
    packages=["EHT"],
    ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "MetaMorphic": ["*.pxd", "*.c", "*.h", "*.pyd"],
    },
    exclude_package_data={
        "MetaMorphic": ["*.py", "*.pyx"],  # .py와 .pyx 파일 제외
    },
    python_requires=">=3.6",
    install_requires=["pandas"],  # 추가 종속성
)
