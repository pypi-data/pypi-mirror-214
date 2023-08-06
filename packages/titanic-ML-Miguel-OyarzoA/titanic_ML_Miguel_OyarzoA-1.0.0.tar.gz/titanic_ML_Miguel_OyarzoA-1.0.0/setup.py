from setuptools import setup, find_packages

setup(
    name='titanic_ML_Miguel_OyarzoA',
    version='1.0.0',
    description='Prediccion en base a variables pclass, sex, age, fare',
    author='Miguel Oyarzo',
    author_email='your@email.com',
    packages=find_packages(),
    install_requires=[
        'feature-engine',
        'pandas',
        'numpy',
        'scikit-learn',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)