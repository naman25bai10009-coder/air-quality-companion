Project Title
Air Quality Companion - Real-time Air Quality Analysis and Health Advisory System

Overview
Air Quality Companion is an intelligent, user-friendly application that analyzes real air quality data to provide personalized health recommendations. Using historical data from Indian cities, it helps users understand current air quality conditions and make informed decisions about their daily activities. The project combines data analysis with practical health advice in a conversational, easy-to-understand format.

Features
Real Data Analysis: Uses authentic air quality data from Indian cities (2015-2020)
Intelligent Matching: Finds historical air quality patterns similar to current conditions
Practical Health Advice: Provides actionable recommendations based on AQI levels
City Comparisons: Shows how your air quality compares to major Indian cities
Activity Suggestions: Recommends suitable activities for current air conditions
Quick Analysis: Fast AQI estimation for integration with other applications
Conversational Interface: Easy-to-use, human-like interaction


Technologies/Tools Used
Python 3.6+ - Core programming language

Pandas - Data manipulation and analysis

NumPy - Numerical computations

Kaggle Dataset - "Air Quality Data in India (2015-2020)"

CSV Processing - Handling real air quality data

Standard AQI Formulas - Indian air quality index calculations


Steps to Install & Run the Project
Prerequisites
Python 3.6 or higher installed on your system

Basic understanding of command line operations


Install Required Packages

pip install pandas numpy

Download the Dataset

Visit: Kaggle - Air Quality Data in India

Download the dataset

Save city_day.csv in the project root directory

Run the Application

python air_quality_companion.py
Instructions for Testing
Test 1: Basic Functionality
Run the application: python air_quality_companion.py

Follow the interactive prompts

Enter test values:

PM2.5: 25

PM10: 50

Verify the output includes:

AQI calculation

Health recommendations

Activity suggestions

Test 2: Different Air Quality Scenarios
Test with various PM2.5 levels to see different recommendations:

Clean Air Test: PM2.5=15, PM10=30

Moderate Air Test: PM2.5=45, PM10=80

Poor Air Test: PM2.5=120, PM10=200

Dangerous Air Test: PM2.5=300, PM10=400

Test 3: Quick Analysis Function

from air_quality_companion import quick_air_lookup

# Test the quick analysis function
result = quick_air_lookup(35, 65)
print(f"AQI: {result['aqi']}")
print(f"Recommendation: {result['suggestion']}")


Test 4: Data Validation
Ensure city_day.csv is properly loaded

Check that similar day matching works

Verify AQI calculations match standard formulas



Expected Output Examples
Good Air Quality (PM2.5=20):

😊 Fantastic air quality!
Estimated AQI: 42
My suggestions: This is perfect air - get outside and enjoy it!


Poor Air Quality (PM2.5=100):
😷 Poor air quality  
Estimated AQI: 185
My suggestions: Better to stay inside mostly, use air filters if available




