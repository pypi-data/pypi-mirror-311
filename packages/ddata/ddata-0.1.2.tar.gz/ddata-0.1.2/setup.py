from setuptools import setup, find_packages
import pathlib

# 获取当前目录
here = pathlib.Path(__file__).parent.resolve()

# 读取 README 文件内容作为长描述
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    # 包名称
    name='ddata',
    # 版本号
    version='0.1.2',
    # 简短描述
    description='A Python data package',
    # 长描述，通常是 README 文件内容
    long_description=long_description,
    # 长描述内容类型
    long_description_content_type='text/markdown',
    # 项目主页（如果有）
    url='https://github.com/flyphant/ddata',
    # 作者信息
    author='flyphant',
    author_email='your_email@example.com',
    # 分类信息，用于 PyPI 上的分类搜索
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 自动发现包内的所有 Python 包
    packages=find_packages(),
    # Python 版本要求
    python_requires='>=3.6, <4',
    # 安装时需要安装的依赖包
    install_requires=[
        'numpy',
    ],
    # 可选的额外依赖，用于不同的功能或场景
    extras_require={
        'dev': ['pytest>=3.7'],
    },
    # 包数据，例如包含一些非 Python 文件（如果有）
    package_data={
        'my_package': ['data/*.txt'],
    },
    # 数据文件，会被安装到指定的目录（如果有）
    # data_files=[('my_package_data', ['data/file1.txt', 'data/file2.txt'])],
    # 命令行入口点，定义可以在命令行中执行的脚本
    entry_points={
        'console_commands': [
            'my_command=my_package.my_module:main_function',
        ],
    },
    # 项目的关键字，用于搜索
    keywords='python, package, sample',
)