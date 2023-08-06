from setuptools import setup

with open("scraper/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="coursera-scraper",
    version="0.1.0",
    author="Talha Khalid",
    author_email="talhakhalidmtk@gmail.com",
    description="This Python script utilizes Selenium to scrape data from Coursera, providing detailed information about various courses such as title, rating, recent views, students enrolled, time requirement, skills, learner count, difficulty level, duration, and sub-course details.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talhakhalidmtk/coursera-scraper",
    packages=["scraper"],
    install_requires=[
        "pandas",
        "selenium",
        "webdriver_manager",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
