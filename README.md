# AutoLMS

AutoLMS is a tool for automating LMS and get into class automatically on specified times.

## Install

Clone the project:

```sh
$ git clone https://github.com/itsamirhn/AutoLMS
$ cd AutoLMS
```

## Requirements

You have to install these manually:

- python3
- Chrome
- [chromedriver](https://chromedriver.chromium.org/downloads)

Then install python requirements:

```sh
$ pip install -r requirements.txt
```

## Configuration

Just as easy as a command:

```sh
$ python main.py setup
```

And anytime you wanted to edit configs (e.g. add new session or course):

```sh
$ python main.py edit
```

## Run

Finally, run the program for always:

```sh
$ python main.py run
```

### Suported Universities

- Kharazmi University
