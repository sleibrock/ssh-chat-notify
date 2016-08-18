#!/usr/bin/env python
#-*- coding: utf-8 -*-

from sys import argv
from subprocess import call
from collections import namedtuple

# Change this based on options fed to the program
NOTIFY_PROTOCOL = 0

dummy_string = "^[[38;5;95msteve2^[[0m: hello world ^[[38;5;8msteve^[[0m"

# Parsed contents of a message
# From is who the message is from
# Message is the contents
# PM is a bool if it was a PM or not
Pmsg = namedtuple("Pmsg", ["who", "message", "pm"])

# Collections of characters we don't want (\033 -> ^[)
filterables = ["^[[D", "^[[K", "^[[0m", "\n", "^G", "^M"]

def parse_message(string, name):
    s = string
    for fil in filterables: #replace all the filterable crap
        s = s.replace(fil, "")
    if s.endswith("$"): # strip the $ off the end (echo option?)
        s = s[:-1]
    clean, start, end = False, 0, 0
    while not clean: # gee willikers this could be a monad comp
        start = s.find("^[[") # find the start of a ansi seq
        if start >= 0:
            end = s[start:].find("m") # should be an 'm' to end the esc seq
            if end >= 0:
                s = s[:start] + s[start:][end+1:] # remove the sequence
            else:
                clean = True # most likely someone just put in ^[[ for giggles 
        else:
            clean = True
        # print(s) debug trace
    s = s.replace("[{}]".format(name), "").strip() # strip our name from the start
    if "PM" in s: # this means the message received was a PM
        splitted = s.split("[PM from ")[0].split("]")
        who = splitted.pop(0) 
        rest = "]".join(splitted)  #inverse of ] split
        pmsg = Pmsg(who.strip(), rest.strip(), True)
    else:         # otherwise it's just a normal message
        splitted = s.split(" ")
        who = splitted.pop(0)
        msg = " ".join(splitted)
        who = who[:-1] # remove a colon
        pmsg = Pmsg(who.strip(), msg.strip(), False)
    return pmsg

def default_notify(pmsg):
    if pmsg.pm:
        args = ["Message from {}".format(pmsg.who), psmg.message]
    else:
        args = ["Mentioned by {}".format(pmsg.who), pmsg.message]
    return call(["notify-send", "--icon=mail-message-new"] + args)

def termux_notify(message):
    if pmsg.pm:
        args = ["-c", pmsg.message, "-t", "Message from {}".format(pmsg.who)]
    else:
        args = ["-c", pmsg.message, "-t", "Mentioned by {}".format(pmsg.who)]
    return call(["termux-notification", message])

# A list of notify programs supported
supported_nots = [default_notify, termux_notify]

if __name__ == "__main__":
    if len(argv) > 1:
        argv.pop(0) # remove the code filename
        uname = argv.pop(0) # pop off the user's name
        msg_test = argv.pop(0)
        if msg_test == "-t":
            NOTIFY_PROTOCOL = 1 # set it to termux
            msg_test = argv.pop(0) # proceed to the next one
        with open("logger.txt", "w") as f:
            f.write(msg_test)
        msg = parse_message(msg_test, uname) # parse the message into an NT
        supported_nots[NOTIFY_PROTOCOL](msg) # call the notify program
    
