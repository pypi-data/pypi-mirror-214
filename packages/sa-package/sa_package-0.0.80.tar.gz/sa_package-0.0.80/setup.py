from setuptools import setup, find_packages

setup(
    name="sa_package",
    version="0.0.80",
    
    url="https://github.com/tmddk2709/sa_package",
    author="Seunga Shin",
    author_email="seungashin9275@gmail.com",

    packages=find_packages(),
    py_modules=["sa_package"],

    install_requires=[
        "bs4",
        "pandas",
        "gspread",
        "oauth2client",
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "selenium",
        "sqlalchemy==1.4.45",
        "webdriver-manager",
        "packaging",
        "psycopg2-binary",
        "pymysql",
    ]
)