# robo-advisor-assignment

## Description

This is an application that provides an investment recommendation on any stock or crypticurrency and displays its recent market data.

## Prerequisites

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Fork this remote repository https://github.com/EmilioAngelM/robo-advisor-assignment under your own control, then "clone" or download your remote copy onto your local computer.

Then navigate there from the command line (subsequent commands assume you are running them from the local repository's root directory):

```sh
cd ~/Desktop/robo-advisor-assignment
```
### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.8 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file :

```sh
pip install -r requirements.txt
```
Install the .env requirements:

```sh
pip install python-dotenv
```
Install the stock prices chart requirements:

```sh
pip install matplotlib
```

```sh
pip install pandas
```

```sh
pip install seaborn
```

### Security Requirements

Your program will need an API Key to issue requests to the [AlphaVantage API](https://www.alphavantage.co). 

In the webpage, cick in "GET YOUR FREE API KEY TODAY". 

Indicate if you are an Investor, Software Developer, Educator, Student, or Other.

Input your organization's name and your email.

Click in "I'm not a robot" checkbox and click in the "GET FREE API KEY."

Then, your API key should be displayed in your screen. Save it somewhere and do not show it to anyone!

#### Environment Variables Setup

In the root directory of your local repository, create a new file with the name ".env." In the ".env" file, create a variable called `AA_API_KEY`, and your program should read the API Key from this environment variable at run-time.

```
AA_API_KEY="abc123"
```


### Usage

```sh
python app/robo_advisor.py
```

Input a valid stock or cryptocurrency ticker (Example: IBM)


