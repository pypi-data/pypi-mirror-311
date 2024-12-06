from setuptools import setup, find_packages
#pypi-AgEIcHlwaS5vcmcCJDFmN2UxNjliLWYwOGItNDVhYi1iZjdmLTIwNmFkZTg4ZTZlNQACGlsxLFsic2lkZWJlbmQtZGV0ZWN0aW9uIl1dAAIsWzIsWyJjYTVkYzFmNS1lMjVlLTRhYzgtYTc3My0wNDFkYzQ3YTBmMDAiXV0AAAYgezniL_VsoPvUE1h7JqmMUrQ_h_syAH08QWg2r5h2tFc
setup(
    name='Sidebend_detection',
    version='0.2',
    packages=find_packages(),
    description='Sidebend detection',
    # long_description=open('README.md').read(),
    # python3，readme文件中文报错
    # long_description=open('README.md', encoding='utf-8').read(),
    # long_description_content_type='text/markdown',
    url='http://github.com/1104934392/Sidebend_detection',
    author='1104934392',
    author_email='1104934392@qq.com',
    license='MIT',
    install_requires=['numpy',
                    #   'math'
        # 依赖列表
    ],
    classifiers=[
        # 分类信息
    ]
)
