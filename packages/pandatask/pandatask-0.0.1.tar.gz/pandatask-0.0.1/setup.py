from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pandatask',
    version='0.0.1',
    author='panda',
    author_email='915615059@qq.com',
    description='上传本地代码到服务端的工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['pandatask'],
    install_requires=['cloudpickle', 'requests']
)