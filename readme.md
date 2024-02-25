# Requirements

* Python 3
* Selenium 4.18
* Google Chrome
* Chromedriver

## Python and Selenium

```sh
pip install selenium
```

## Chromedriver

You need to have Google Chrome installed and Chromedriver. Easiest way to install on Mac (assuming you have homebrew):

```sh
brew install chromedriver
```

# Setup

* Copy `config.py.default` to `config.py`
* Change credentials and select unique class name that will allow script to uniquely identify the class

# Running

Set up your Crontab to the desired schedule and run the script using

```
python3 book-class.py
```