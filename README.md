# AutoLMS

AutoLMS is a tool for automating LMS and get into class automatically on specified times.

### Supported Universities

- University of Tehran
- Kharazmi University
- Shahid Beheshti University

if your university is not listed, feel free to contribute or make an issue.

## Install

Use the pip package manager to install AutoLMS:

```sh
$ pip install autolms
```

## Requirements

You have to install these manually:

- python3
- Chrome
- [ChromeDriver](https://chromedriver.chromium.org/downloads)

### How to download ChromeDriver?

If you are new to ChromeDriver, follow instructions below:

1) Go this [Address](https://chromedriver.chromium.org/downloads)
2) Find out your Chrome app version by going to `chrome://version` address with Chrome
3) Choose your Chrome corresponding version in the list
    1) For example if you are using Chrome version 97.xx then choose
       `ChromeDriver 97.xx`
    2) Be careful, if you got error on run, it may because of difference between Chrome and ChromeDriver versions
4) Select the file compatible with your system (Mac or Linux or Win)
5) Unzip the downloaded file
6) Put the `chromedriver` anywhere you want
7) In the setup of AutoLMS, **program will try to find your `chromdriver` automatically**, If it doesn't found or the
   path is wrong, type `chromedriver` path manually or just drag & drop the file into terminal

## Configuration

Just as easy as a command:

```sh
$ autolms setup
```

And anytime you wanted to edit configs (e.g. add new session or course):

```sh
$ autolms edit
```

## Run

Finally, run the program for always:

```sh
$ autolms run
```

## License

AutoLMS is MIT licensed.