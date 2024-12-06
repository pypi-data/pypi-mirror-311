import setuptools

setuptools.setup(
    name='gru',
    version='0.0.1rc11',
    install_requires=['requests>=2.31.0', 'typing==3.7.4.3','chardet==5.1.0','click>=8.1.7','langgraph>=0.2.50', 'fastapi>=0.115.5', 'uvicorn>=0.32.0', 'langgraph-checkpoint-postgres>=2.0.3', 'psycopg[binary,pool]', 'celery>=5.4.0', 'redis>=5.2.0'],
    entry_points={
        'console_scripts': [
            'yugenml = gru.cookiecutter.mlops_templates_cli:mlops_template_cli',
            'yserve = gru.ml_serving.server:serve'
        ],
    },
    packages=setuptools.find_packages(),
    )