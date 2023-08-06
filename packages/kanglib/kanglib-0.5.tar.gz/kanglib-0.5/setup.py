from setuptools import setup, find_packages

setup(
    name='kanglib',
    version='0.5',
    packages=find_packages(),
    description='Kang lib of Python package: calculate my math function',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # 添加这一行
    url='https://github.com/williampolicy/code_pypi',
    author='xiaowen kang',
    author_email='kangxiaowen@gmail.com',
    license='MIT',
)





# from setuptools import setup, find_packages

# setup(
#     name="kanglib",
#     version="0.2",
#     packages=find_packages()
# )
