from setuptools import setup, find_packages

setup(
    name='LinguAI',                     # 包的名字
    version='0.1.0',                    # 包的版本
    packages=find_packages(),           # 自动找到包
    install_requires=[                  # 依赖项
        # 'torch',                      # 例如，如果你的包需要torch库
    ],
    author='xiaomingx',                 # 更新作者信息
    author_email='support@uhaka.com',   # 更新作者邮箱
    description='一个用于大语言模型处理的Python包',  # 简短的描述
    long_description=open('README.md').read(),  # 从README.md读取详细描述
    long_description_content_type='text/markdown',
    url='https://github.com/XiaomingX/LinguAI',  # 更新GitHub项目地址
    classifiers=[                       # 代码的分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
