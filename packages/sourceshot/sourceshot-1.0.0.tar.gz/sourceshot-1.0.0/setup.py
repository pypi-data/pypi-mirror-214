from setuptools import setup
def readme():
    with open('README.md','r') as f:
        return f.read()
setup(
    name='sourceshot',
    version='1.0.0',
    description='Takes pictures of code!',
    long_description=readme(),
    packages=['sshot'],
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts':[
            'sshot=sshot:_cli'
        ]
    },
    python_requires='>=3.6',
    install_requires=['pygments','pillow<10','numpy','opencv-python','colorama'],
    keywords=['code','picture']
)
