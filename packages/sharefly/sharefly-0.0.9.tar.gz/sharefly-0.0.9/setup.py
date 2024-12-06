from setuptools import setup, find_packages

setup(
    name =                      'sharefly',
    version =                   '0.0.9',
    url =                       'https://github.com/NelsonSharma/sharefly',
    author =                    'Nelson.S',
    author_email =              'mail.nelsonsharma@gmail.com',
    description =               'Flask based web app for sharing files and quiz evaluation',
    packages =                  find_packages(include=['sharefly']),
    classifiers=                ['License :: OSI Approved :: MIT License'],
)   