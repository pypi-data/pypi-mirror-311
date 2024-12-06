from setuptools import setup, Extension
from Cython.Build import cythonize
import os

SAGE_ROOT = os.environ.get("/opt/sagemath-9.3", "/opt/sagemath-9.3")  # SageMath 설치 경로
INCLUDE_DIRS = [os.path.join("/opt/sagemath-9.3", "local/include")]
LIBRARY_DIRS = [os.path.join("/opt/sagemath-9.3", "local/lib")]

ext_modules = [
    Extension(
        "EHT",
        sources=["EHT/EHT_test.pyx"],
        include_dirs=INCLUDE_DIRS,
        library_dirs=LIBRARY_DIRS,
    )
]

setup(
    name="EHT-fc",
    ext_modules=cythonize(ext_modules),
    version="0.0.3",
    description="Elliptic curve operations using SageMath",
    long_description_content_type="text/markdown",
    author='fourchains_R&D',
    author_email='fourchainsrd@gmail.com',
    packages=["EHT"],
    #ext_modules=cythonize(ext_modules, compiler_directives={"language_level": "3"}),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_data={
    #    "MetaMorphic": ["*.pxd", "*.c", "*.h", "*.pyd"],
    #},
    #exclude_package_data={
    #    "MetaMorphic": ["*.py", "*.pyx"],  # .py와 .pyx 파일 제외
    #},
    python_requires=">=3.6",
    install_requires=["pandas"],  # 추가 종속성
)

