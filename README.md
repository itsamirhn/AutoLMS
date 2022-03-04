# AutoLMS

AutoLMS is a tool for automating LMS and get into class automatically on specified times.

### Suported Universities

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
2) Choose your Chrome corresponding version in the list
    1) For example if you are using Chrome version 97.xx then choose
       `ChromeDriver 97.xx`
    2) Be careful, if you got error on run, it may because of difference between Chrome and ChromeDriver versions
3) Select the file compatible with your system (Mac or Linux or Win)
4) Unzip the downloaded file
5) Put the `chromedriver` anywhere you want
6) On the setup of AutoLMS, type the path for `chromedriver` or just drag & drop the file into terminal

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