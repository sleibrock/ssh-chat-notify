ssh-chat-notify
===============

`ssh-chat-notify` is a wrapper extension for normal `ssh-chat` by [@shazow](https://github.com/shazow).
This forks data from `ssh` into a FIFO, which is then grepped every time you get a BEL alert from 
the `ssh-chat`. This is then converted into a notification action like `notify-send` so you get 
desktop alerts.

![image](https://cloud.githubusercontent.com/assets/15330989/17787795/ab84f9a8-6558-11e6-82f1-826f4304f110.png)

## Requirements

* Git
* openssh
* Linux (or some kind of Unix-like environment)
* Python

## Setup

Git clone it into a repository you'll never see. Then we have to modify some shell dotfiles to 
export the settings so that it works properly.
``` bash
git clone https://github.com/sleibrock/ssh-chat-notify $HOME/.sshome
echo "export $SSHOME=$HOME/.sshome" >> .bashrc
echo "source $SSHOME/ssh_chat.sh" >> .bashrc
```

Replace `.bashrc` with whatever your shell uses to define stuff (`.zshrc`, etc).

After that try logging into the default server with `ssh_chat <your_name>`.

## Credits

Mostly everything is credited to [@shazow](https://github.com/shazow) for helping me put this together. 
He also hosts `ssh-chat` and is cool for doing so.
