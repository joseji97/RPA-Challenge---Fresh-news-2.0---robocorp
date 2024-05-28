https://thoughtfulautomation.notion.site/RPA-Challenge-Fresh-news-2-0-37e2db5f88cb48d5ab1c972973226eb4
# Fresh news 2.0
Fresh-news 2.0 is a Python application that scrape news using a pre-defined set of words

# Scraping L.A. Times website

This project uses Python, RPA Framework and Selenium library to scrape the L.A. Times website for news articles. The program allows the user to select a search phrase, topic, and date range for the articles they want to retrieve. The data is extracted and saved to a Excel file.

# Prerequisites

This program requires Python and the following libraries:

    RPA Framework
    Selenium
    Robocorp

The program can be run on any operating system that supports Python.

# Getting Started

To use this program, follow these steps:

    Clone the repository
    Install the prerequisites using pip or any other package manager
    Check the properties.json file and set your variables
    Run the main.py file with Python

# How to use

To use the program, set the following variables in the properties.json file and run the main.py file:
    
    URL: The URL for the L.A. Times website
    SEARCH_PHRASE: The search phrase for the articles you want to retrieve
    CATEGORY: The category of the articles you want to retrieve
    NUMBER_OF_MONTHS: The number of months in the past to search for articles
    DELAY: Time to wait between certain procedures

Sample properties.json file
    
    {
        "URL": "https://www.latimes.com/",
        "SEARCH_PHRASE": "price",
        "TOPIC": ["Business"],
        "NUMBER_OF_MONTHS": 1,
        "DELAY": 5
    }

Once you have set these variables, you can run the program using Python.