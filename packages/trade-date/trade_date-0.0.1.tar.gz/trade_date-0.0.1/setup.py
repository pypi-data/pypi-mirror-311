from setuptools import setup
setup(name='trade_date',
      version='0.0.1',
      description='High frequency functions and class for business day',
      url='https://gitee.com/wdy0401/trade_date',
      author='wangdeyang',
      author_email='wdy0401@gmail.com',
      license='MIT',
      package_data={
      'trade_date': ['bizd.txt'],
      },

      packages=['trade_date'],
      zip_safe=False)