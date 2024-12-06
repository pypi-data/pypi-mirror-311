from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# 확장 모듈 설정
extensions = [
    Extension("EHT", ["EHT/EHT.pyx"], include_dirs=["/opt/sagemath-9.3/local/include"], library_dirs=["/opt/sagemath-9.3/local/lib"])
]

setup(
    name="EHT",
    version="0.0.10",
    description="EHT",
    long_description_content_type="text/markdown",
    author='fourchains_R&D',
    author_email='fourchainsrd@gmail.com',
    package_dir={"EHT": "EHT"},
    packages=["EHT"],
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"}),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "EHT": ["*.pxd", "*.c", "*.h", "*.pyd"],
    },
    exclude_package_data={
        "EHT": ["*.py", "*.pyx"],  # .py와 .pyx 파일 제외
    },
    python_requires=">=3.6",
    install_requires=["pandas", "random"],  # 추가 종속성
)
