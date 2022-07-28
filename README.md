<p align="center">
  <h3 align="center">Bozo</h3>

  <p align="center">
    A text editor writen in python for linux and other unix like operating systems
    <br>
  <img src="https://img.shields.io/github/license/Proxin666/Bozo?style=for-the-badge&logo=appveyor">
  <img src="https://img.shields.io/github/stars/Proxin666/Bozo?style=for-the-badge">
  <img src="https://img.shields.io/github/forks/Proxin666/Bozo?style=for-the-badge">
  </p>
</p>


## Table of contents
# Im Having a little trouble running bozo i dont know why it just exits when i run it and i dont know why and im not going to fix it since im done on this project, im pretty shure that it may happen because one of the libaries used in this text editor had an update and there for it does not run

- [Quick start](#quick-start)
- [What's included](#whats-included)
- [Copyright and license](#copyright-and-license)


## Quick start

To use Bozo you first need to download it and configure it manualy, its very easy and i will walk you trough it step for step! DISCLAIMER: This install guide only works on linux and other unix like operating systems

- Start by opening your terminal and clone this repository by typing text show below
```bash
git clone https://github.com/Proxin666/Bozo.git
cd NAME OF THE DIRECTORY YOU JUST CLONED
```
- Then you give the program permision to execute and copy the files to /usr/local/bin to make it executable from everywhere on the system by typing the commands shown below
```bash
chmod a+x bozo
sudo cp bozo bozo_util /usr/local/bin
```
- Now you should be able to run it by typing whats shown below
```bash
bozo somefile.txt
```

## What's included
Here are the features that comes with Bozo

> arrows - move cursor in  a direction\
> ctrl-x - clean exit\
> ctrl-w - write the changes to the file\
> ctrl-j - delete line\
> ctrl-t - go to the top\
> ctrl-y - go to the bottom\
> ctrl-f - move to a specific line\
> ctrl-h  - Syntax highlighting on/off

## Copyright and license

Code released under the [Gpl license](LICENSE).

Enjoy 💻
