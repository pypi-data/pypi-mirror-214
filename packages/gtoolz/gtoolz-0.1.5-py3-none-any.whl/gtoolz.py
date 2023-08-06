#!/usr/bin/env python3
# vim: set syntax=none nospell:
# #####################
# Script name: gtoolz.py
# Created by: geoff.mcnamara@gmail.com
# Created on: 2018
# Purpose: this is a quick-n-dirty set of tools that might be useful
# ... much room for improvment and lots of danger points - not recommended for anything you care about  # noqa:
# ... use this file in anyway and all your data could be at risk ;)
# ... lots of debugging code still remains and legacy code that should be removed  # noqa:
# ... this file is constantly changing so nothing should depend on it ;)
# ... depends on python3!
# LICENSE = MIT
# WARNING: Use at your own risk!
#          Side effects include but not limited: severe nosebleeds and complete loss of data.
#          This file is subject to frequent change!
# Please contact me anytime. I willingly accept compliments and I tolerate complaints (most of the time).
# Requires: docopt, dbug.py, gftools.py, and others
# #####################################
# To see an overview:
# python3 -m pydoc nicetools
# note: because dbug is pulled in with import you can call it drectly from this module as well, also funcname
# to have access:
# in bash --- export PYTHONPATH="${PYTHONPATH}:/home/geoffm/dev/python/gmodules"
# or
# import sys
# sys.path.append("/home/geoffm/dev/python/gmodules")
# #####################################

# ### IMPORTS ### #
import os
import sys
import shutil
import glob
import re
import subprocess
from datetime import datetime  # , date
from math import ceil
from urllib.request import urlopen
import inspect
from inspect import (getframeinfo, currentframe)
from docopt import docopt
import time
# import requests
import threading
import configparser
import itertools
import pandas as pd


# ### GLOBALS ### #
__version__ = '0.1.5'
dtime = datetime.now().strftime("%Y%m%d-%H%M")
FULL_PATH_SCRIPT = __file__
SCRIPT = os.path.basename(__file__)
styles_d = {'normal': '0', 'bold': '1', 'bright': 1, 'dim': '2', 'italic': '3', 'underline': '4', 'blink': '5', 'fast_blink': '6', 'reverse': '7', 'crossed_out': '9'}
fg_colors_d = {'black': ";30",
        'red': ";31",
        'green': ";32",  # I don't like "their" green, should "my" green (;38) instead or even better is rgb(0,215,0)
        # 'green': ";38",
        'yellow': ';33',
        'blue': ';34',
        'magenta': ';35',
        'cyan': ';36',
        'white': ';37',
        'normal': '38',
        'bold normal': ';39'}
bg_colors_d = {'black': "40",
        'red': "41",
        'green': "42",
        'yellow': "43",
        "blue": "44",
        'magenta': "45",
        "cyan": "46",
        'white': "47",
        'normal': '48',
        'normal1': '49'}


# ############### #
# ### CLASSES ### #
# ############### #

# ############
class Spinner:
    # ########
    """
    purpose: prints a spinner in place
    input: msg="": str style='bar': ellipsis, pipe, box, vbar, growing_bar, missing_box, solid_box,  arrow, clock, bar, balloons, moon, dot, braille, pulse
        prog|progressive|progress: bool
        color: str
        txt_color: str
        elspsed: bool
    requires:
        import sys
        import threading
        import itertools
    return: none
    use:
        with Spinner("Working...", style='bar')
            long_proc()
        with Spinner("Doing long work...", style='vbar', progressive=True,  colors=shades('red'))
               for x in range(100):
                   time. sleep(1)
    """
    def __init__(self, message="", *args, delay=0.2, style="pipe", **kwargs):
        """--== debugging ==--"""
        # dbug(f"class: Spinner {funcname()} style: {style} args: {args} kwargs: {kwargs}")
        # dbug(args)
        # dbug(kwargs)
        """--== config ==--"""
        # color = kvarg_val(["color", "spinner_color", "spinner_clr"], kwargs, dflt="")
        txt_color = kvarg_val(["text_color", "txt_color", "text_clr", "txt_clr"], kwargs, dflt="")
        self.color = kvarg_val(["color", 'spinner_clr', 'spinner_color', 'clr'], kwargs, dflt="")
        # if isinstance(color, list):
        self.colors = kvarg_val(["colors", "color", "spinner_colrs", "spinner_clrs"], kwargs, dflt=[])
        self.COLOR = sub_color(self.color)
        txt_color = kvarg_val(["txt_color", 'txt_clr'], kwargs, dflt="")
        self.TXT_COLOR = sub_color(txt_color)
        self.elapsed = bool_val(['elapsed', 'elapse', "time", "timed"], args, kwargs, dflt=False)
        # dbug(self.elapsed)
        time_color = kvarg_val(["time_color", 'time_clr', 'elapsed_clr', 'elapsed_time_clr', 'elapsed_color', 'elapse_color', 'elapse_clr'], kwargs, dflt=txt_color)
        # dbug(time_color)
        self.time_color = time_color
        self.TIME_COLOR = sub_color(time_color)
        # self.elapsed_time = 0
        self.etime = bool_val(["etime", "show_elapsed", 'elpased_time', 'elapsed', 'time'], args, kwargs, dflt=False)
        self.centered = bool_val(['center', 'centered'], args, kwargs, dflt=False)
        self.RESET = sub_color('reset')
        self.start_time = time.time()
        # dbug(self.etime)
        self.style = style = kvarg_val(["style", 'type'], kwargs, dflt=style)
        # dbug(self.style)
        self.prog = bool_val("prog", args, kwargs, dflt=True)
        self.style_len = kvarg_val(["length", "width"], kwargs, dflt=4)
        """--== set default ==--"""
        if isinstance(self.colors, str):
            # just to make sure it is a list before going forward
            self.colors = [self.colors]
        spinner_chrs = ['.', '.', '.', '.']  # the default will be ellipsis
        # self.prog = True  # the default
        """--== SEP_LINE ==--"""
        if style in ('ellipsis', 'elipsis', 'elipses', 'ellipses'):  # for the spelling challenged like me
            spinner_chrs = ['.', '.', '.', '.']
            # spinner_chrs = ['.' * self.style_len]
            self.style_len = len(spinner_chrs)
            self.prog = True
            # dbug(f"Style: {self.style} prog: {self.prog} style_len: {self.style_len} color: {self.color} time_color: {self.time_color}")
        if style == "pipe":
            spinner_chrs = ['/', '-', '\\', '|']
            self.prog = False
        if style == "arrow":
            # spinner_chrs = ['⬍', '⬈', '⮕', '⬊', '⬍', '⬋', '⬅', '⬉']
            spinner_chrs = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
            self.prog = False
        if style == 'clock':
            spinner_chrs = ['🕛', '🕧', '🕐', '🕜', '🕑', '🕝', '🕒', '🕞', '🕓', '🕟', '🕔', '🕠', '🕕', '🕡', '🕖', '🕢', '🕗', '🕣', '🕘', '🕤', '🕙', '🕥', '🕚', '🕦']
            self.style_len = len(spinner_chrs)
            self.prog = False
        if style == 'moon':
            spinner_chrs = ['🌑', '🌘', '🌗', '🌖', '🌕', '🌔', '🌓', '🌒']
            self.prog = False
        if style == 'vbar':
            spinner_chrs = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█', '▇', '▆', '▅', '▄', '▃', '▂', '▁']  # , '_']
            self.style_len = len(spinner_chrs)
        if style in ('growing_bar', 'pump'):
            spinner_chrs = ['\u258F', '\u258E', '\u258D', '\u258C', '\u258B', '\u258A', '\u2589', '\u2588', '\u2589', '\u258A', '\u258B', '\u258C', '\u258D', '\u258E', '\u258F', ' ']
            self.prog = False
        if style == 'bar':
            spinner_chrs = ['█', '█', '█', '█', '█']
            self.prog = True
            self.style_len = 20
        if style == 'braille':
            spinner_chrs = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
            self.prog = False
        if style == 'dot':
            spinner_chrs = ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈']
            self.prog = False
        if style == 'box' or style == 'boxes':
            spinner_chrs = ['◰', '◳', '◲', '◱']
            self.prog = False
        if style == 'solid_box' or style == 'solid_boxes':
            spinner_chrs = ['\u2598', '\u259D', '\u2597', '\u2596']
            self.prog = False
        if style == 'missing_box' or style == 'hole_boxes':
            spinner_chrs = ['\u259F', '\u2599', '\u259B', '\u259C']
            self.prog = False
        if style == 'balloons':
            spinner_chrs = ['.', 'o', 'O', '@', '*']
            self.prog = False
        if style == 'pulse':
            spinner_chrs = ['.', 'o', 'O', 'o']
            self.prog = False
        if style == 'batball':
            spinner_chrs = ['q', 'p', 'b']
            self.prog = False
        # self.style_len = len(spinner_chrs)
        self.chr_cnt = 1
        self.clr_cnt = 0
        self.spinner = itertools.cycle(spinner_chrs)
        self.delay = kvarg_val("delay", kwargs, dflt=delay)
        self.busy = False
        self.spinner_visible = False
        message = printit(message, "str", 'noprnt', color=txt_color)
        # dbug(type(message))
        if self.centered:
            spinner_len = 1
            if self.prog:
                spinner_len = len(spinner_chrs)
            if self.etime:
                spinner_len += 2
            shift = -(spinner_len)
            message = printit(message, 'centered', prnt=False, rtrn_type="str", color=txt_color, shift=shift)
        sys.stdout.write(message)
    """--== SEP_LINE ==--"""
    def write_next(self):
        # write the next chr in spinner_chrs
        with self._screen_lock:
            if not self.spinner_visible:
                # dbug(self.colors)
                if len(self.colors) > 1:
                    color = self.colors[self.clr_cnt]
                    # dbug(color)
                    self.COLOR = sub_color(color)
                    # dbug(f"color: {color} chr_cnt: {self.clr_cnt} repr(self.COLOR): {repr(self.COLOR)}")
                    self.clr_cnt += 1
                    if self.clr_cnt > len(self.colors) - 1:
                        self.clr_cnt = 0
                spinner_chr = self.COLOR + str(next(self.spinner)) + self.RESET
                if self.style == 'clock':
                    if self.chr_cnt >= self.style_len:
                        self.chr_cnt = 0
                    else:
                        self.chr_cnt += 1
                if self.style == 'clock':
                    if nclen(spinner_chr) > 1:
                        # I have absolutely no idea why this is needed but it is. Believe me I beat this to death - it causes a 'blink'
                        # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len} spinner_chr: {spinner_chr} nclen(spinner_chr)) {nclen(spinner_chr)}")
                        sys.stdout.write('  ')
                    else:
                        # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len} spinner_chr: {spinner_chr} nclen(spinner_chr)) {nclen(spinner_chr)}")
                        sys.stdout.write(spinner_chr)
                else:
                    # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len} spinner_chr: {spinner_chr} nclen(spinner_chr)) {nclen(spinner_chr)}")
                    sys.stdout.write(spinner_chr)
                # sys.stdout.write(spinner_chr)
                self.spinner_visible = True
                sys.stdout.flush()
                """--== SEP_LINE ==--"""
    def spin_backover(self, cleanup=False):
        with self._screen_lock:
            # _self_lock is the thread
            if self.spinner_visible:
                if not self.prog:
                    # backover chr if not prog (progressive)
                    # dbug(f"self.style: {self.style} self.chr_cnt: {self.chr_cnt} self.style_len: {self.style_len}")
                    sys.stdout.write('\b')
                else:
                    # if progressive then ...
                    # clr_cnt = self.chr_cnt % len(self.colors)
                    # self.COLOR = self.colors[clr_cnt]
                    # dbug(self.COLOR)
                    # dbug(f"prog: {self.prog} chr_cnt: {self.chr_cnt} style_len: {self.style_len}")
                    self.chr_cnt += 1
                    if self.chr_cnt > self.style_len:
                        # if we hit the len of style_len... print elapsed time... then...
                        if self.etime:
                            elapsed_time = round(time.time() - self.start_time, 2)
                            elapsed_time = f"{elapsed_time:>6}"  # if we go over 999 seconds we will be in trouble with the length
                            # dbug(elapsed_time)
                            sys.stdout.write(f" {self.TIME_COLOR}{elapsed_time}{self.RESET}")
                            # time.sleep(self.delay)
                            sys.stdout.write("\b" * (len(str(elapsed_time)) + 1))
                            # sys.stdout.write(self.RESET)
                            sys.stdout.flush()
                        while self.chr_cnt > 1:
                            # while chr_cnt is more than 1... back over
                            self.chr_cnt -= 1
                            sys.stdout.write("\b")
                            sys.stdout.write(" ")
                            sys.stdout.write("\b")
                            time.sleep(self.delay)
                            sys.stdout.flush()
                        sys.stdout.write(" ")
                        sys.stdout.write("\b")
                        sys.stdout.flush()
                        time.sleep(self.delay)
                        # self.chr_cnt = 0
                if self.style in ('clock', 'moon'):
                    sys.stdout.write('\b')
                # if self.chr_cnt > self.style_len:
                #     #dbug("how did we get here")  # not sure if this section is needed
                #     if self.etime:
                #         elapsed_time = round(time.time() - self.start_time, 2)
                #         sys.stdout.write(f" {self.TIME_COLOR}{elapsed_time}{self.RESET}")
                sys.stdout.write('\x1b[?25l')  # Hide cursor
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')              # overwrite spinner with blank
                    sys.stdout.write('\r')             # move to next line
                    sys.stdout.write("\x1b[?25h")      # Restore cursor
                sys.stdout.flush()
                """--== SEP_LINE ==--"""
    def spin_proc(self):
        while self.busy:
            self.write_next()
            if self.etime and not self.prog:
                elapsed_time = round(time.time() - self.start_time, 2)
                elapsed_time = f"{elapsed_time:>6}"  # this is to assure proper back over length - if we go over 999 seconds we are in trouble with the length
                sys.stdout.write(f" {self.TIME_COLOR}{elapsed_time}{self.RESET}")
                # dbug(len(elapsed_time))
                # time.sleep(self.delay)
                sys.stdout.write("\b" * (len(elapsed_time) + 1))
            time.sleep(self.delay)
            self.spin_backover()
            """--== SEP_LINE ==--"""
    def __enter__(self):
        try:
            if sys.stdout.isatty():
                self._screen_lock = threading.Lock()
                self.busy = True
                self.thread = threading.Thread(target=self.spin_proc)
                self.thread.start()
        except Exception as Error:
            dbug(Error)
            pass
        """--== SEP_LINE ==--"""
    def __exit__(self, exc_type, exc_val, exc_traceback):
        self.busy = False
        if sys.stdout.isatty():
            # self.busy = False
            # end_time = time.time()
            # self.elapsed_time = (end_time - self.start_time)
            # sys.stdout.write(f"({self.elapsed_time})")
            self.spin_backover(cleanup=True)
            sys.stdout.write('\r')
            sys.stdout.flush()
            print()  # ??? tries to force the cursor to the next line
        else:
            sys.stdout.write("\x1b[?25h")     # Restore cursor
            sys.stdout.write('\r')
            sys.stdout.flush()
            time.sleep(0.2)
            print()  # ??? tries to force the cursor to the next line
    # ### class Spinner: ### #


# ##################
def Spinner_demo():
    # ##############
    """
    purpose: demo of Spinner
    """
    # ith Spinner("[red on black]Working...approx: 5 sec[/] ", 'elapsed', style='vbar', prog=False,
    #             colors=shades('white'), elapsed_clr="yellow! on black", centered=True):
    #    time.sleep(5)
    styles = ["ellipsis", "dot", "bar", "vbar", "moon", "pipe", "arrow", "balloons", 'braille', 'pulse', 'box', 'clock']
    # colors = ["red", "blue", "green", "yellow", "magenta", "white", "cyan"]
    # with Spinner(f"Demo progressive vbar ", 'centered', 'prog', 'elapsed', style='vbar', colors=colors):
    #     time.sleep(5)
    red_shades = ['rgb(20,0,0)', 'rgb(40,0,0)', 'rgb(60,0,0)', 'rgb(80,0,0)', 'rgb(100,0,0)',
                  'rgb(120,0,0)', 'rgb(140,0,0)', 'rgb(160,0,0)', 'rgb(180,0,0)', 'rgb(200,0,0)',
                  '  rgb(220,0,0)', 'rgb(240, 0,0)', 'rgb(254,0,0)', 'rgb(254,0,0)', 'rgb(254,0,0)', 'rgb(254,0,0)']
    while True:
        style = gselect(styles, 'centered', 'quit', rtrn="v")
        # style = gselect(styles, 'centered', rtrn="v", colors=colors)
        if style in ("q", "Q", ""):
            break
        wait_time = cinput("For how many seconds: (default=15) ") or 15
        color = cinput("Input a spinner color Note: if you enter a list (eg ['red', 'green', 'blue']) then the spinner will rotate colors accordingly, default is shades of red: ") or red_shades
        txt_color = cinput("Input a text color, default is normal: ") or 'normal'
        time_color = cinput("Input a time color, default is 'yellow! on black': ") or 'yellow! on black'
        printit("Note: some spinner styles will not use the progressive setting...", 'centered')
        prog = askYN("Should we try progressive?", "n", 'centered')
        # dbug(prog)
        # dbug(color[:4])
        # dbug(txt_color)
        # dbug(time_color)
        printit([f"Demo: Spinner(style: {style}", f"txt_clr: {txt_color}", f"spinner_clr: {color[:4]}...", f"time_clr: {time_color}", f"Progressive: {prog}... "], 'centered')
        with Spinner("Demo: Spinner: working... ): ", 'centered', 'elapsed', color=color, txt_color=txt_color, elapsed_clr=time_color, style=style, prog=prog):
            time.sleep(int(wait_time))  # to simulate a long process


# #########################
class Transcript:
    # #####################
    """
    Transcript - direct print output to a file, in addition to terminal. It appends the file target
    Usage:
        import transcript
        transcript.start('logfile.log')
        print("inside file")
        transcript.stop()
        print("outside file")
    Requires:
        import sys
        class Transcript
        def transcript_start
        def transcript_stop
    """
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "a")
        """--== SEP_LINE ==--"""
    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)
        """--== SEP_LINE ==--"""
    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass
    # ### class Transcript: ### #


def write_file(data, fname, *args, **kwargs):
    """
    purpose: writes data to a file typically as a csv file (or a .dat file) - creates a new file or appends an existing file
    options:
        - colnames: list (adds hdr line if not currently there)
        - comment_lines: str | list
        - bak: bool      # make a backup file
        - indx: bool     # not used yet - future flag for adding an index col (first column) or not
        - prnt: bool     # turns on print
        - ask: bool      # ask before actually writing data to file (before overwriting the file)
        - append: bool   # whether to append data - the default=False whereby submitted data will overwrite the file
        - dat: bool      # this is a special flag to declare that the first line (hdr) is made a comment starting it with "#"
    returns: bool        # true if successful write
    Notes:
        - only use this to write a data file = either csv (or a dat file which is a csv file with the header commented)
        - data should be a list of lists (rows of cols)
        - assumes first line is comma delimited colnames or use colnames option (in a dat file the first line will be commented)
        - all comments will go to/near the top
        - if the file ends with the ".dat" extension it will be treated as a 'dat' file
    """
    """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(data[:3])
    # dbug(args)
    # dbug(kwargs)
    """--== Config ==--"""
    prnt = bool_val(["print", "prnt", "show", "verbose"], args, kwargs, dflt=True)  # True for now TODO
    ask_b = bool_val(["ask"], args, kwargs, dflt=False)
    # id_flag = bool_val(["orig_id_flag", "id_flag", "indx", "idx", "id"], args, kwargs, dflt=False)
    bak = bool_val(["bak"], args, kwargs, dflt=True)
    # comment_lines = kvarg_val(["comment_lines"], kwargs, dflt=[])
    colnames = kvarg_val(["colnames", "col_names", "cols"], kwargs, dflt=[])
    append_b = bool_val(["append", "a"], args, kwargs, dflt=False)
    dat_b = bool_val(["dat", 'dat_file'], args, kwargs, dflt=False)
    """--== Local Import(s) ==--"""
    # import csv
    """--== Init ==--"""
    # writefile = fname
    data_lines = []
    csv_lines = []        # this will become a list of comma delimited strings/lines and will include a header string/line as the first line
    content_lines = []    # lines read from the file (if it exists) - all non-comment lines
    comment_lines = []    # comments lines read from the file if it exists
    # file_type = "csv"   # this will either be a 'csv' or a 'dat' based on file name extension
    """--== Convert ==--"""
    if isinstance(data, str):
        # dbug(f"Converting a data if str into a list... data: {data}")
        data = [data]
    for row in data:
        # dbug(row)
        if isinstance(row, list):
            # dbug("row is a list")
            # if isinstance(row, list):
            row = comma_join(row)
        csv_lines.append([row])
        data = csv_lines
    # """--== Validate ==--"""
    if not isinstance(colnames, list):
        dbug("Colnames must be a list ... colnames: {colnames} ... returning...")
        return
    if islol(data):
        # dbug(data)
        for row in data:
            # row = [elem.replace('\r',"\\n") for elem in row]  # replace 
            # dbug(row)
            new_row = comma_join(row)
            # dbug(new_row, 'ask')
            data_lines.append(new_row)
    else:
        dbug(f"Data is not a list of lists and it should be. data: {data}... returning...")
        return
    if len(data[0]) < 1:  # arbitrary
        dbug(f"Data should have more content: {data[:3]}")
        return
    # """--== Init ==--"""
    if file_exists(fname):
        # content_lines = cat_file(fname, 'lst')
        with open(fname, "r") as f:
            lines = f.readlines()
            for ln in lines:
                ln = ln.rstrip("\n")
                if ln.startswith("#"):
                    comment_lines.append(ln)
                content_lines.append(ln)
    if fname.endswith(".dat") or dat_b:
        # file_type = "dat"
        # hdr_line = content_lines[0].lstrip("#")
        data_lines = data_lines[1:]
    # """--== WIP below ==--"""
    # are we ready to write out the file
    # cp file first
    if bak and file_exists(fname):
        # import shutil
        bak_fname = fname + ".bak"
        if file_exists(bak_fname):
            shutil.copy(bak_fname, fname + ".prev")
        shutil.copy(fname, fname + ".bak")
        printit(f"File: {fname} has been backed up to: {fname}.bak", 'centered')
    if append_b:
        # do_append_file()
        if ask_b:
            if not askYN(f"Do you want to continue with writing to file: {fname}?", 'y'):
                return False
        with open(fname, "a") as f:
            for ln in data:
                if isinstance(ln, list) and len(ln) == 1:
                    ln = ln[0]
                    # dbug(f"ln: {ln} should be a string, istead it appears to be a {type(ln)}... fname: {fname} not written to... returning", 'warn') 
                    # return
                if not ln.endswith("\n"):
                    ln += "\n"
                f.write(ln)
    else:
        # do_write_file()
        # either creates a new file or overwites existing file - above is for appending
        new_lines = []
        for ln in comment_lines:  # obtained above
            new_lines.append(ln)
        for ln in data_lines:
            new_lines.append(ln)
        # """--== SEP_LINE ==--"""
        # dbug(new_lines, 'lst')
        # """--== SEP_LINE ==--"""
        # dbug('ask')
        if ask_b:
            if not askYN(f"Do you want to continue with writing to file: {fname}?", 'y'):
                return False
        with open(fname, "w") as f:
            if not isempty(colnames):
                new_lines.insert(0, ", ".join(colnames))
            for ln in new_lines:
                if isinstance(ln, list):
                    ln = comma_join(ln)
                if not ln.endswith("\n"):
                    ln += "\n"
                f.write(ln)
    if prnt:
        printit(f"The file fname: {fname} has be re-written...", 'centered')
    return True
    # ### EOB def write_file() ### #


# #############################
def transcript_start(filename, *args, **kwargs):
    # ##########################
    """
    Start class Transcript(object=filename),
    appending print output to given filename
    """
    prnt = bool_val(["prnt", 'printit', 'show'], args, kwargs, dflt=False)
    centered_b = bool_val(['centered'], args, kwargs, dflt=False)
    if prnt:
        printit(f"Starting transcript out to {filename}", centered=centered_b)
    sys.stdout = Transcript(filename)


# ########################
def transcript_stop(*args, **kwargs):
    # ###################
    """
    Stop class Transcript() and return print functionality to normal
    """
    prnt = bool_val(["prnt", 'printit', 'show'], args, kwargs, dflt=False)
    centered_b = bool_val(['centered'], args, kwargs, dflt=False)
    sys.stdout.logfile.close()
    sys.stdout = sys.stdout.terminal
    if prnt:
        printit("Stopping transcript out", centered=centered_b)
    return


# ####################
def transcript_demo():
    # ################
    """
    purpose: Quick demo of using transcript (which writes out to the screen and to a file simultaneously - like bash 'script')
    returns: none
    notes: allows capturing screen output to a file for reference later... I use it in financial analysis tools - uses transcript_start() and a transcript_stop() 
    """
    rname = rootname(__file__)
    file = f"./{rname}-transcript-demo.out"
    if file_exists(file):
        printit(f"Removing existing file: {file}", 'centered')
        os.remove(file)
    printit(f"We are now going to write all output to file: {file}", 'centered')
    transcript_start(file, 'prnt', 'centered')
    printit("This output will also be found in file: {file}", 'boxed', 'centered')
    transcript_stop('prnt', 'centered')
    printit(f"Here are the contents of file: {file}", 'centered')
    contents = cat_file(file)
    printit(contents)
    return


# #######################################
class ThreadWithReturn(threading.Thread):
    # ###################################
    """
    requires:
        import threading
    usage:
        run_cmd_threaded(cmd)
        which does this ...
        dbug("Just getting started...")
        cmd = "/home/geoffm/ofrd.sh"
        t1 = ThreadWithReturn(target=run_cmd, args=(cmd,))
        t1.start()
        dbug("Done")
        result = t1.join()
        dbug(result)
    """
    def __init__(self, *init_args, **init_kwargs):
        threading.Thread.__init__(self, *init_args, **init_kwargs)
        self._return = None
        """--== SEP_LINE ==--"""
    def run(self):
        self._return = self._target(*self._args, **self._kwargs)
        """--== SEP_LINE ==--"""
    def join(self):
        threading.Thread.join(self)
        return self._return


# ### FUNCTIONS ### #

# ################
def funcname(n=0):
    # ############
    """
    purpose: returns current function name - primarily used for debugging
    """
    return sys._getframe(n + 1).f_code.co_name


# ###########
def lineno():
    # #######
    """
    purpose: returns current line number - primarily used for debugging
    """
    cf = currentframe()
    return str(cf.f_back.f_lineno)


# ##############################################
def ddbug(msg="", *args, ask=False, exit=False):
    # ##########################################
    """
    purpose: this is for use by dbug only... as dbug can't call itself
    """
    """--== Debugging ==--"""
    # print(f"funcname: {funcname()}")
    # print(f"ask: {ask}")
    """--== SEP_LINE ==--"""
    # dbug = DBUG if DBUG else 1
    # my_centered = True if 'center' in args else False
    # my_centered = True if 'centered' in args else centered
    ask = True if 'ask' in args else False
    exit_b = True if 'exit' in args else False
    # dbug(f"ask:  {ask} exit_b: {exit_b}")
    # cf = currentframe()
    filename = str(inspect.getfile(currentframe().f_back))
    filename = os.path.basename(filename)
    fname = str(getframeinfo(currentframe().f_back).function)
    fname = os.path.basename(fname)
    lineno = str(inspect.currentframe().f_back.f_lineno)
    # msg = "DEBUG: [" + {fname} + ":" + {lineno} + "] " + {msg}
    # if file:
    #     msg = "DEBUG: [" + filename + ";" + fname + "(..):" + lineno + "] " + msg
    # else:
    #     msg = "DEBUG: [ " + str(fname) + "():" + str(lineno) + " ] " + str(msg)
    msg = f"*** DDBUG ***: [{filename}; {fname} (..): {lineno} ] {msg}"
    try:
        print(msg)
    except Exception as e:
        print(f"print({msg}) failed Error: {e}")
        print(msg)
    if ask:
        askYN()  # this will ask "Continue:" ... should exit with 'n'
        # ans = input("Do you want to exit? ")
        # # ddbug(f"we got here ~679 with and: {ans}")
        # if ans.lower().strip() in ("y", "yes"):
        #     print("Exiting as requested...")
        #     sys.exit(99)
    if exit_b:
        sys.exit()
    return msg
    # ### EOB def ddbug(msg="", *args, ask=False, exit=False): ### #


# ############
def dbug(xvar="", *args, exit=False, ask=False, prnt=True, **kwargs):
    # ########
    """
    purpose: display DEBUG file, function, linenumber and your msg of local variable content
    required: xvar: str ... can be a local variable, a python statement, a string, a list
    options:
        -ask: bool        # forces a breakpoint, stops execution ans asks the user before continuing
        -here: bool       # will only return the DEBUG info (file, function. linenumber) as a string without printing - typically used like this boxed("my box", footer=dbug('here'))
        -boxed: bool      # boxes debug output
        -box_color: str   # declares box_color default is 'red! on grey40'
        -color: str       # declares text output color
        -nocolor: bool
        -centered: bool   # centers the debug output
        -lst: bool        # forces printing the variable contents as a list (like printit()) - allows displaying ansii codes properly
        -titled: bool     # only works when 'boxed'... puts the DEBUG info into the title of a box  This should probably be the default...
        -footerred: bool  # only works when 'boxed'... puts the DEBUG info into footer of a box
    returns: prints out debug info (unless 'here' option invoked)
    notes: Enjoy!
    To test:
        run: python3 -m doctest -v dbug.py
    # >>> a = "xyz"
    # >>> dbug_var(a)
    DEBUG: [dbug.py; <module>:1] a:xyz
    '1'
    """
    """--== Imports ==--"""
    """--== Config ==--"""
    center = bool_val(['center', 'centered'], args, kwargs)
    box = bool_val(['box', 'boxed'], args, kwargs, dflt=False)
    color = kvarg_val('color', kwargs, dflt='')
    nocolor = bool_val(['nocolor', 'noclr'], args, kwargs, dflt=False)
    # box_color = kvarg_val('box_color', kwargs, dflt="red! on black")
    box_color = kvarg_val(['box_color', 'box_clr', 'bxclr'], kwargs, dflt="red! on grey40")
    # if 'center' in args or 'centered' in args:
    #     center = True
    DBUG = kvarg_val(['dbug', 'DBUG'], kwargs, dflt=True)  # True unless specified as False
    if not DBUG:
        # the idea here is if dbug looks like this: {where DBUG is True or >0) dbug(..., dbug=DBUG) then this func will honor the value of DBUG (ie True or False)
        # this should ease the pain for change ... now you can do this
        # DBUG = bool_val('dbug', args)
        # and then dbug(f"whatever here", dbug=DBUG)
        # ddbug(f"DBUG: {DBUG} therefore I am returning [empty handed sort of speak]")
        # further... you could put DBUG = 0 (or False) in GLOBAL vars and use docopts to turn on or off DBUG
        return
    EXIT = bool_val('exit', args, kwargs, dflt=False)
    ask_b = bool_val('ask', args, kwargs, dflt=False)
    warn_b = bool_val(["warn", "warning"], args, kwargs, dflt=False)
    info_b = bool_val(["info"], args, kwargs, dflt=False)
    error_b = bool_val(['err', 'error'], args, kwargs, dflt=False)
    lineno_b = bool_val(['lineno_b', 'lineno', 'line_no', 'line_number'], args, kwargs, dflt=False)
    here_b = bool_val('here', args, kwargs, dflt=False)
    title = kvarg_val("title", kwargs, dflt="")
    footer = kvarg_val("footer", kwargs, dflt="")
    list_b = bool_val(["lst", "list"], args, kwargs, dflt=False)  # print the list in lines if xvar contains a list (like printit for dbug)
    titled = bool_val("titled", args, kwargs, dflt=True)  # consider making this the default - this adds the debug_info to the box title
    footered = bool_val(["footered", "footerred"], args, kwargs, dflt=False)  # yes, this is footerred <-- TODO probably need to change or eliminate this
    """--== Init ==--"""
    # if footered or titled:
        # box = True
    """--== SEP_LINE ==--"""
    # ddbug(f"xvar: {xvar}")
    if str(xvar) == 'lineno':
        lineno_b = True
    if str(xvar) == 'here':
        here_b = True
    if str(xvar) == 'ask':
        ask_b = True
        # see below where msg_literal gets changed when it is == 'ask'
    # fullpath filename
    i_filename = str(inspect.getfile(currentframe().f_back))
    # filename without path
    filename = os.path.basename(i_filename)
    # fname = function name
    fname = str(getframeinfo(currentframe().f_back).function)
    lineno = str(inspect.currentframe().f_back.f_lineno)
    if lineno_b:
        return lineno
    if here_b:
        # if 'only' in str(xvar).lower():
        #    return f"{filename}:{fname}:{lineno}"
        # if 'now' in str(xvar).lower():
        #    return f"DEBUG: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} [{filename}:{fname}:{lineno}]"
        return f"DEBUG: [{filename}:{fname}:{lineno}]"
    # this inconsistently holds what we want for the most part ...just wrong format
    # you would have to put this directly into your code and include a msg
    # ie eg:  <frame at 0x7f4d6e4b25e0, file '/home/geoffm/././t.py', line 3000, code tdbug>
    frame = inspect.currentframe().f_back
    # ddbug(f"footer: {footer}")
    def do_prnt(rtrn_msg, *args, ask=ask_b, footer=footer, **kwargs):  # , ask=ask_b, centered=centered):
        # ddbug(f"title: {title}")
        # ddbug(f"footer: {footer}")
        # titled = bool_val("titled", args, kwargs, dflt=True)
        # footered = bool_val("footered", args, kwargs, dflt=False)
        # title = kvarg_val("title", kwargs, dflt="")
        # footer = kvarg_val("footer", kwargs, dflt="")
        to_prnt = f"{rtrn_msg}"
        # ddbug(rtrn_msg)
        if "\n" in to_prnt:
            # ddbug(f"to_prnt: {to_prnt}")
            to_prnt = "\n" + to_prnt
        COLOR_CODE = rgb(250,0,0, prfx=True)
        LVL = "DEBUG"
        if warn_b:
            COLOR_CODE = rgb(250,250,0, prfx=True)
            LVL = "WARN"
        if info_b:
            COLOR_CODE = rgb(250,250,250, prfx=True)
            LVL = "INFO"
        if error_b:
            COLOR_CODE = rgb(250,0,0, prfx=True)
            LVL = "ERR"
        if nocolor:
            COLOR_CODE = ""
        to_prnt = f"{COLOR_CODE + LVL + RESET}: [{filename}:{fname}:{lineno}] {rtrn_msg}"
        # to_prnt = f"DEBUG: [{filename}:{fname}:{lineno}] {rtrn_msg} {msg_literal}:"
        # ddbug(f"to_prnt: {to_prnt}")
        if box:
            my_title = ""
            my_footer = ""
            if not isempty(title):
                my_title = "title: " + title
            if not isempty(footer):
                my_footer = "footer: " + footer
            # dbug(f"titled: {titled}")
            if titled or footered:
                phrases = to_prnt.split(']')
                # ddbug(f"phrases: {phrases}")
                if titled:
                    # ddbug(titled)
                    my_title += " " + phrases[0] + "]"
                    # ddbug(f"phrases: {phrases}")
                    # ddbug(f"phrases[0]: {phrases[0]}")
                    # ddbug(f"my_title: {my_title}")
                    to_prnt = phrases[1]
                    # ddbug(f"to_prnt: {to_prnt}")
                    # this is such a kludge ... arghhh TODO !!!!!
                    work_l = phrases[1].split("\n")
                    # ddbug(f"work_l[0]: {work_l[0]}")
                    # ddbug(f"msg_literal: {msg_literal}")
                    tst_first_line = work_l[0].strip()
                    tst_first_line = tst_first_line.rstrip(":")
                    # ddbug(f"tst_first_line: {tst_first_line}")
                    if tst_first_line == msg_literal.strip():
                        # ddbug("bingo-bongo")
                        # ddbug(f"work_l[1:]: {work_l[1:]}")
                        to_prnt = "\n".join(work_l[1:])
                if footered:
                    if not isempty(footer):
                        footer = f"footer: {footer} "
                    my_footer = footer + " " + phrases[0] + "] " + footer
                    to_prnt = phrases[1]
            to_prnt = boxed(to_prnt, color=color, box_color=box_color, title=my_title, footer=my_footer)
        if center:
            # num_rows, columns = os.popen("stty size", "r").read().split()
            # lfill = (int(columns) - len(to_prnt)) // 2
            # to_prnt = " " * lfill + to_prnt
            to_prnt = centered(to_prnt)
        # ddbug(to_prnt)
        printit(to_prnt)
        # if isinstance(to_prnt, list):
        #     # dbug(center)
        #     # ddbug(to_prnt)
        #     for ln in to_prnt:
        #         # ddbug(ln)
        #         # print(phrases[1] + "?: " + ln)
        #         print(ln)
        # else:
        #     print(f"{to_prnt}")
        if ask_b:
            # ddbug(f"ask_b: {ask_b}")
            if not askYN("Continue?: ", "y", centered=center, exit=True):  # exit=True?????
                sys.exit()
            # ddbug('ask')
        if EXIT:
            sys.exit()
        # title = kvarg_val('title', kvargs, "")
        # ### EOB def do_prnt(rtrn_msg, *args, ask=ask_b, **kwargs):  # , ask=ask_b, centered=centered): ### #
    line_literal = inspect.getframeinfo(frame).code_context[0].strip()  # the literal string including dbug(...)
    # ddbug(f"line_literal: {line_literal}")
    msg_literal = re.search(r"\((.*)?\).*", line_literal).group(1)  # ?non-greedy search
    # ddbug(f"msg_literal: {msg_literal}")
    # ddbug(f"msg_literal: {msg_literal}")
    if msg_literal.replace("'", "") == 'ask' or msg_literal.replace('"', '') == "ask":
        # ddbug(f"msg_literal: {msg_literal} args: {args}")
        ask_b = True
        # rtrn_msg = "Enter or 'y' to continue... anything else to exit... "
        rtrn_msg = ""
        to_prnt = f"DEBUG: [{filename}:{fname}:{lineno}] {rtrn_msg}\nContinue: "
        if not askYN(to_prnt):
            sys.exit()
        return
    # try:
    #     ddbug(f"msg_literal: {msg_literal}")
    #     # import pyparsing as pp
    #     all_args = pp.commaSeparatedList.parseString(msg_literal).asList()
    #     msg_literal = all_args[0]
    #     ddbug(f"msg_literal: {msg_literal} all_args: {all_args}")
    #     # import abracadabra
    # except Exception as Error:
    all_args = msg_literal.split(",")
    msg_literal = all_args[0]
    """--== SEP_LINE ==--"""
    lvars = inspect.currentframe().f_back.f_locals
    # ddbug(f"msg_literal: {msg_literal}")
    if msg_literal.startswith('f"') or msg_literal.startswith("f'"):
        do_prnt(xvar, args, ask=ask_b, footered=footered, title=titled)
        return
    if msg_literal.startswith('"') or msg_literal.startswith("'"):
        # ddbug(f"msg_literal: {msg_literal}")
        msg_literal = msg_literal[1:-1]
    # ddbug(f"msg_literal: {msg_literal} lvas: {lvars}")
    found = False
    if msg_literal in lvars:
        # ddbug(f"Looks like this msg_literal: {msg_literal} is in lvars")
        found = True
    # ddbug(f"found: {found}")
    for k, v in lvars.items():
        # ddbug(f"lvars: {lvars}")
        # ddbug(f"testing msg_literal: {msg_literal} against k: {k}")
        if msg_literal == k or found:  # in loop below we might break out and miss testing if in lvars hence the found value
            # ddbug(f"looks like msg_literal: {msg_literal} == k: {k}")
            try:
                if "\n" in str(xvar) and list_b:
                    xvar = xvar.split("\n")
                    xvar = [x for x in xvar if x != ""]
            except Exception as Error:
                ddbug(f"Error: {Error}")
                pass
            # so this is in the local vars so lets build it as a string
            # ddbug(f"msg_literal: {msg_literal} xvar: {xvar}")
            if isinstance(xvar, list) and list_b:
                # contents of msg_literal (xvar) will be treated like printit as best we can
                # ddbug(f"xvar: {xvar} islol(xvar): {islol(xvar)} islos(xvar): {islos(xvar)}")
                # orig_xvar = xvar
                if islol(xvar):
                    lines1 = []
                    # ddbug("here now")
                    if islos(xvar):
                        for elem in xvar:
                            lines1.append("\n".join(elem))
                        xvar = lines1
                        # ddbug(xvar)
                    else:
                        lines = xvar
                        xvar = "You used 'lst' with dbug. Too many levels deep. Using printit with a box."
                        # printit("You used 'lst' with dbug. Too many levels deep. Using printit with a box.")
                        my_prnt = f"DEBUG: [{filename}:{fname}:{lineno}] {msg_literal}"
                        printit(lines, 'boxed', title="Too many layers deep for dbug to handle. Just using printit (boxed)", footer=f"{my_prnt}", box_color="red on white")
                        return
                        list_b = False
                        # ddbug(lines)
                    if list_b:
                        # ddbug(xvar)
                        xvar = "\n" + "\n".join(xvar)
                        # ddbug(xvar)
                # ddbug(f"type(orig_xvar): {type(orig_xvar)} islos(orig_xvar): {islos(orig_xvar)} type(xvar): {type(xvar)} islos(xvar): {islos(xvar)}")
                if islos(xvar):
                    # ddbug(f"hmmm this looks like xvar: {xvar} islos", 'ask')
                    lines0 = []
                    for ln in xvar:
                        lines0.append(ln)
                    xvar = lines0
                    # ddbug(f"xvar: {xvar}")
                    # for ln in xvar:
                    #     ddbug(f"ln: {ln}")
                    if list_b:
                        xvar = "\n" + "\n".join(xvar)
                    # ddbug(xvar)
            rtrn_msg = f"{msg_literal}: {xvar}"
            # ddbug(f"rtrn_msg: {rtrn_msg}")
            # ddbug(f"args: {args}")
            # ddbug(f"msg_literal: {msg_literal} xvar: {xvar}")
            do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
            return
        else:
            # not match to a local var
            # ddbug(f" ---- xvar: {xvar} is not in lvars")
            if isinstance(xvar, list) and list_b:
                # ddbug(f"mmmm looks like this is a list xvar: {xvar}")
                if islol(xvar):
                    lines1 = []
                    for elem in xvar:
                        # ddbug(f"type(elem): {type(elem)}")
                        if isinstance(elem, str):
                            # ddbug(f"elem: {elem} is a string")
                            lines1.append("\n".join(elem))
                        """--== SEP_LINE ==--"""
                        if islos(elem):
                            for ln in elem:
                                # ddbug(f"ln: {ln} is a string")
                                # lines1.append("\n".join(ln))
                                lines1.append(ln)
                    xvar = lines1
                    # ddbug(f"xvar: {xvar}")
                xvar = "\n" + "\n".join(xvar)
                # ddbug(f"xvar: {xvar}")
                # print(xvar)
                # for ln in xvar:
                #    for my_ln in ln:
                #        printit(xvar
                # askYN("HHHHHHHHHAAAAAAAA")
            # ddbug(f"msg_literal: {msg_literal} k: {k}")
        # rtrn_msg = f"{msg_literal}: {xvar}"
        rtrn_msg = f"{xvar}"
        # ddbug(f"rtrn_msg: {rtrn_msg}")
        # ddbug(f"doing do_prnt now with msg_literal: {msg_literal} xvar: {xvar}")
        # these next 2 lines killed a dbug that has msg_literal like dbug(len(msg))
        # do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
        # return
    # ddbug(f"msg_literal: {msg_literal}")
    try:
        import pandas as pd
        if isinstance(xvar, pd.DataFrame) or isinstance(xvar, pd.core.series.Series):
            rtrn_msg = f"{msg_literal}: {xvar}"
            do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
            return  # yes, this return is needed otherwise bool prnts 2x
    except Exception as e:
        ddbug(f"Error: {e}")
    # ddbug(f"msg_literal: {msg_literal}")
    if msg_literal != xvar or not isinstance(msg_literal, str):
        # ddbug(f"msg_literal: {msg_literal}")
        if isinstance(xvar, type):
            rtrn_msg = f"{msg_literal}: {xvar}"
            do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
            return  # yes, this return is needed otherwise bool prnts 2x
        try:
            if re.search(r'^f["].*"$', msg_literal) or re.search("^'.*'$", msg_literal):
                # catches an f-strg (assumes that it is an f-str
                rtrn_msg = xvar  # default to this
                do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
                return
            else:
                # ddbug(f"msg_literal: {msg_literal} xvar: {xvar}")
                # if msg_literal == 'ask':
                if msg_literal.replace("'", "") == 'ask' or msg_literal.replace('"', '') == "ask":
                    rtrn_msg = ""
                    ddbug(f"rtrn_msg: {rtrn_msg}")
                else:
                    rtrn_msg = f"{msg_literal}: {xvar}"
                do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
                return
        except Exception as Error:
            rtrn_msg = f"{msg_literal}: {xvar}"
            ddbug(f"rtrn_msg: {rtrn_msg} Error: {Error}")
            do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
            return
        return
    rtrn_msg = f"{msg_literal}"
    do_prnt(rtrn_msg, args, ask=ask_b, footered=footered, titled=titled)
    return
    # ### EOB def dbug(): ### #


def dbug_demo():
    """
    purpose: A quick-n-dirty demo of using dbug()
    """
    my_var = "Just a simple msg"
    dbug(my_var)
    dbug(len(my_var), 'ask')
    """--== SEP_LINE ==--"""
    dbug(len(my_var))
    msg3 = gclr("[red on black]my msg3 in color[/]")
    msgs = ["my msg1", "my msg 2", msg3]
    dbug(msgs, 'ask', 'lst')
    msg = "This will use: dbug(f'msg: {msg} msg_len: {len(msg)}"
    print(f"NOTE: msg = {msg}")
    dbug(f"msg: {msg} msg_len: {len(msg)}")
    print("-" * 40)
    msg = "This will use: dbug(msg)"
    print(f"NOTE: msg = {msg}")
    dbug(msg)
    print("-" * 40)
    msg = "This will use: dbug(f'msg: {msg}')"
    print(f"NOTE: msg = {msg}")
    dbug(f"msg: {msg}")
    print("-" * 40)
    msg = "This will use dbug(len(msg))"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg))
    print("-" * 40)
    msg = "This will use dbug(len(msg), 'boxed')"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg), 'boxed')
    print("-" * 40)
    msg = "This will use dbug(len(msg), 'boxed', 'centered')"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg), 'boxed', 'centered')
    print("-" * 40)
    msg = "This will use dbug(len(msg), 'boxed', 'centered', box_color='red! on black')"
    print(f"NOTE: msg = {msg}")
    dbug(len(msg), 'boxed', 'centered', box_color="red! on black")
    print("-" * 40)
    msg = "This will use dbug(type(['one', 'two', 'three']), 'boxed')"
    print(f"NOTE: msg = {msg}")
    dbug(type(['one', 'two', 'three']), 'boxed')
    print("-" * 40)
    msg = "This will use dbug(type(['one', 'two', 'three']), 'ask')"
    print(f"NOTE: msg = {msg}")
    dbug(type(['one', 'two', 'three']), 'ask')
    print("-" * 40)


# # #################
# def funcname(n=0):
#     # #############
#     """
#     Use: eg:
#     from dbug import dbug, fname
#     def myfunc():
#         dbug(f"This is function name: {funcname()}")
#         pass
#     """
#     # using this sys method is faster than inspect methods
#     return sys._getframe(n + 1).f_code.co_name


# #######################################
def gselect(selections, *args, **kwargs):
    # ###################################
    """
    purpose: menu type box for selecting by index, key, or value
    required:
    - selections: list or dictionary
    options:
        - prompt: str # no need to include ": "
    - rtrn=''     # can be 'k|key' or 'v|val|value' or "i" | "int" <-- tells gselect whether you want it to return a key or a value from a supplied list or dictionary or just user input (default)
                  # if "i"|"int" is invoked then the value of the key will return as an integer (as opposed to a string)
            This is an important option and allows control over what gets returned. See the Notes below.
    - show: str   # "k|key" or 'v|val|value' <-- tells gselect whether to display a list of keys or a list of values
    - indx: bool  # whether to index (place a number before) each selection shown
    - quit: bool <-- add "q)uit" to the prompt and will do a sys.exit() if ans in ("q","Q","exit")
    - multi <-- allows multiple selections and returns them as a list
    - default|dflt='':   # allows you to /declare a default if enter is hit
    - sep: str     # separation chars between cols default=" | "
    - cols: int    # default is 1 column for displaying selections
    - quit
    - title
    - footer
    - color
    - box_color
    - width: int|str   # if this is an integer it will provide the width in columns for the gselect. 
                       # If it is a string it *must* have a "%" sign in it. The width will then become the percentage of the available screen columns 
    returns: str | list  -- either key(s) or value(s) as a *string* <---IMPORTANT  or list (if multiple), your choice
    Notes:
        - to understand this function know first that everything is turned into a dictionary first. A list would become a dictionary with  the keys being 1,2,3...
        while the original list would become the keys - this understanding will help with determining the rtrn and show options (key | val)
        - a dictionary remains as keys and values
        - with a simple list by default it will return the value in the list - if you want the menu number then use rtrn='k' option!!!
    examples:
    > tsts = [{1: "one", 2: "two", 3: "three"},["one", "two", "three"], {"file1": "path/to/file1", "file2": "path/to/file2"} ]
    > for tst in tsts:
    ...     ans = gselect(tst, rtrn="v")
    ...     ans = gselect(tst, rtrn="k")
    -----------
    To run a function using gselect - write code similar to this:
        selections = {"Clean up files": 'clean', "Copy file": 'copyfile'}
        ans = gselect(selections, rtrn="v", quit=True)
        globals()[ans]()  # this will run the function name returned .. eg: clean() or copyfile() obviously you can do a lot with this
    """
    """--== dbug ==--"""
    # dbug(funcname())
    # dbug(selections)
    # dbug(args)
    # dbug(kwargs)
    """--== Config ==--"""
    prompt = kvarg_val("prompt", kwargs, dflt="Please select")
    centered_b = bool_val(["center", "centered"], args, kwargs, dflt=False)
    # dbug(centered_b)
    shift = kvarg_val(["shift", "shft"], kwargs, dflt=0)  # only works with centered option
    title = kvarg_val("title", kwargs, dflt=" Selections ")
    footer = kvarg_val("footer", kwargs, dflt="")
    # dbug(footer)
    default = kvarg_val(["dflt", "default"], kwargs, dflt="")
    # dbug(default)
    width = kvarg_val(["width", "w", "length", "len", "l"], kwargs, dflt=0)
    # dbug(width)
    box_color = kvarg_val(["box_color"], kwargs, dflt="bold white on rgb(60,60,60)")
    cols = kvarg_val(["cols", "columns"], kwargs, dflt=1)
    sep = kvarg_val(["sep"], kwargs, dflt=" | ")
    color = kvarg_val(["color"], kwargs, dflt="white on rgb(20,20,30)")
    quit = bool_val(["quit", "exit"], args, kwargs, dflt=False)
    # dbug(kwargs)
    rtrn = kvarg_val(["rtrn"], kwargs, dflt="v")  # can be key|k or value|v|val or ''
    show = kvarg_val(['show', 'show_type', 'shw', 'shw_type'], kwargs, dflt="k")
    indx = bool_val(["indx", "idx", "index", "indexes"], args, kwargs, dflt=True)
    # index = bool_val(['index', 'idx'], args, kwargs, dflt=True)
    multi = bool_val(["choose", "choices", "multi"], args, kwargs, dflt=False)
    # dbug(quit)
    """--== Validate ==--"""
    if selections is None:
        dbug(f"Please provide valid selections: {selections}")
        return None
    if len(selections) == 0:
        dbug("Nothing to process...")
        return None
    if isinstance(selections, str):
        dbug("Selections can not be a string. They must be either a list or dictionay")
        return None
    """--== Init ==--"""
    selections_d = {}
    lines = []
    rtrn_ans = ""
    keys = []
    vals = []
    dict_submitted = False
    """--== Convert ... Type Mngmt ==--"""
    " we will turn a list into a dict "
    # if isinstance(selections, str):
    #     if selections.startswith("[") and selections.endswith("]"):
    #         dbug("OMG")
    if isinstance(selections, list):
        # dbug(selections)
        for n, elem in enumerate(selections, start=1):
            num_len = len(str(len(selections)))
            # max_elem_len = maxof(selections)
            selections_d[f"{str(n):>{num_len}} {elem}"] = elem
            keys.append(str(n))
            vals.append(elem)
    if isinstance(selections, dict):
        # dbug(selections)
        dict_submitted = True
        n = 1
        for k, v in selections.items():
            # dbug(f"n: {n} k: {k} v: {v} show: {show} rtrn: {rtrn}")
            if show in ("v", "val", "value", "values"):
                # dbug(show)
                # dbug(selections)
                selections_d[k] = v
            else:
                if rtrn in ("v", "val", "value", "values"):
                    # dbug(indx)
                    if indx:
                        selections_d[f"{n:>3}). {k}"] = k
                    else:
                        selections_d[f"{k}"] = k

                    show = "k"
                elif rtrn in ("k", "key", "keys"):
                    selections_d[f"{n:>3}). {k}"] = n
                    show = "k"
                else:
                    # selections_d[str(n)] = k
                    selections_d[k] = v
                    show = "k"
            keys.append(k)
            vals.append(v)
            n += 1
    # dbug(selections_d)
    """--== Process ==--"""
    for k, v in selections_d.items():
        # lines is choices
        if show in ("v", "val", "value", "values"):
            lines.append(v)
        else:
            lines.append(k)
    # dbug(lines)
    if cols > 0:
        # dbug(cols)
        # dbug(sep)
        lines = gcolumnize(lines, cols=cols, color=color, sep=sep)
    if "%" in str(width):
        scr_cols = get_columns()
        width = width.replace("%", "")
        width = int(scr_cols * (int(width)/100))
    if int(width) > 0:
        # dbug(width)
        lines = gcolumnize(lines, width=width, color=color, sep=sep)
        # dbug(lines, 'lst')
    # dbug(lines)
    # dbug(width)
    """--== SEP_LINE ==--"""
    if quit:
        prompt = prompt + " or q)uit"
    if default != "":
        prompt += f" default: [{default}] "
    if prompt.endswith(":") or prompt.endswith(": "):
        prompt = prompt.rstrip()
        prompt = prompt.rstrip(":")
    prompt += ": "
    """--== SEP_LINE ==--"""
    # dbug(f"multi: {multi} default: {default}")
    # dbug(lines)
    if multi:
        selected_l = []
        footer_l = []
        ans = "none"
        while ans not in ("q", "Q"):
            # dbug(rtrn)
            if footer == "":
                footer = " Please add selections one at a time. "
            # display_selections(lines)
            # printit(lines, 'boxed', center=centered_b, box_color=box_color, color=color, title=title, footer=prompt + dbug('here'))
            # dbug(centered_b)
            printit(lines, 'boxed', center=centered_b, box_color=box_color, color=color, title=title, footer=footer)
            printit(f"Selected: {selected_l}", centered=centered_b, color=color)
            if centered_b:
                # dbug(centered_b)
                ans = cinput(prompt, center=centered_b, shift=shift, quit=quit)
            else:
                ans = input(prompt)
                if ans in ("q", "Q", "exit", ""):
                    sys.exit()
            if ans in ("q", "Q", ""):
                if ans == "":
                    ans = default
                break
            # dbug(ans)
            if rtrn in ("k", "K", "keys"):
                # dbug(ans)
                ans = keys[int(ans)]
                # dbug(ans)
            # else:
            #     ans = vals[int(ans)]
            footer_l.append(int(ans))
            footer = f" Selected: {footer_l} "
            ans = vals[int(ans) - 1]
            # dbug(ans)
            selected_l.append(ans)
        # dbug(f"Returning: {selected_l}")
        return selected_l
        """--== EOB while ... multi ... ==--"""
    else:
        """--== not multi selection ==--"""
        # dbug(lines)
        # dbug(centered_b)
        printit(lines, 'boxed', centered=centered_b, box_color=box_color, color=color, title=title, footer=footer)
        # now get input with prompt
        if centered_b:
            # dbug(centered_b)
            ans = cinput(prompt, shift=shift, quit=quit) or default
        else:
            # dbug(centered_b)
            ans = input(prompt) or default
        orig_ans = ans
    # dbug(f"ans: {ans} rtrn: {rtrn} selections_d: {selections_d} keys: {keys} vals: {vals}")
    rtrn_ans = ans
    # dbug(repr(ans))
    if quit and ans in ("q", "Q", "quit", "Quit", "exit"):
        sys.exit()
    if (not isnumber(ans) and rtrn == "v") or (ans not in keys and ans not in vals):
        if not indx:
            # dbug(f"ans: {ans} rtrn: {rtrn}\nselections_d: {selections_d}\nkeys: {keys}\nvals: {vals}")
            # this allows a pass-through for what might be considered an invaldid ans - developer can use this feature or code for it
            # dbug(f"Returning ans: {ans}")
            return ans
    # dbug(f"ans: {ans} rtrn: {rtrn}" )
    # dbug(vals)
    # dbug(keys)
    if str(ans) not in keys and not dict_submitted:
        # dbug(f"Returning ans: {ans}")
        return ans
    if isnumber(ans):
        ans = int(ans) - 1
    # dbug(ans)
    if rtrn in ("k", "key", "keys"):
        # dbug(ans)
        rtrn_ans = keys[ans]
    if rtrn in ("v", "val", "vals", "values", "value"):
        # dbug(vals)
        # dbug(keys)
        # dbug(ans)
        if isnumber(ans) and (str(ans+1) not in keys and str(ans) not in vals):
            # dbug(f"ans: {ans} keys[ans]: {keys[ans]}")
            if isnumber(keys[ans]):
                # dbug(vals[ans])
                # dbug(orig_ans)
                rtrn_ans = orig_ans
            else:
                rtrn_ans = vals[ans]
        else:
            # dbug(vals[ans])
            if isnumber(ans):
                rtrn_ans = vals[ans]
            else:
                rtrn_ans = ans
    # dbug(f"Returning rtrn_ans: {rtrn_ans}")
    if rtrn in ("i", "int"):
        if isnumber(rtrn_ans):
            rtrn_ans = int(rtrn_ans)
    # dbug(f"Returning {rtrn_ans}")
    return rtrn_ans
    # ### EOB def gselect(selections, *args, **kwargs): ### #


# ################################
def gselect_demo(*args, **kwargs):
    # ############################
    """
    purpose: demo of using gselect
    returns: none
    """
    cls()
    """--== SEP_LINE ==--"""
    mrkt_syms_d = {'S&P': '^GSPC', 'DOW': '^DJI', 'NASDAQ': '^IXIC', 'Russel2k': '^RUT', "Crude": 'CL=F', 'Gold': 'GC=F',
                   'Silver': 'SI=F', 'EURUSD': 'EURUSD=X', '10yr': '^TNX', 'GBP/USD': 'GBPUSD=X', 'USD/JPY': 'JPY=X'}
    ans = gselect(mrkt_syms_d, 'centered', 'quit', rtrn="v", cols=4, title="rtrn='v' ie value", footer=dbug('here'))
    dbug(ans, 'ask', 'center')
    """--== SEP_LINE ==--"""
    simple_list = ["Select me", "No, please select me", "Select me and I will bring you happiness!"]
    ans = gselect(simple_list, title="Vertical Listing")
    dbug(f"You selected this: {ans}", 'ask')
    """--== SEP_LINE ==--"""
    simple_list = ["Select me", "No, please select me", "Select me and I will bring you happiness!"]
    ans = gselect(simple_list, cols=len(simple_list), title="Horizontal Listing")
    dbug(f"You selected ans: {ans}", 'ask')
    """--== SEP_LINE ==--"""
    my_d = {"o)ne": "o", "t)wo": "t", "t)hree": "t"}
    msg = f"my_d: {my_d}"
    printit(f"Using {msg}", 'boxed')
    ans = gselect(my_d, length=100)
    dbug(f"Your ans: {ans}", 'boxed')
    """--== SEP_LINE ==--"""
    my2_d = {"one": "o", "two": "t", "three": "t"}
    msg = f"my2_d: {my2_d} rtrn='v'"
    printit(f"Using {msg}", 'boxed')
    ans = gselect(my_d, length=100, rtrn="v")
    dbug(f"Your ans: {ans}", 'boxed')
    """--== SEP_LINE ==--"""
    msg = f"my2_d: {my2_d} rtrn='k'"
    printit(f"Using {msg}", 'boxed')
    ans = gselect(my_d, length=100, rtrn="k")
    dbug(f"Your ans: {ans}", 'boxed')
    """--== SEP_LINE ==--"""
    my_l = list_files("./", "*.*")
    my_l = my_l[:3]
    msg = f"my_l: {my_l} rtrn='k' length=220"
    printit("Using " + msg)
    ans = gselect(my_l, length=220, title=msg, footer=dbug('here'), quit=True, rtrn='k')
    dbug(f"Your ans: {ans}", 'boxed')
    """--== SEP_LINE ==--"""
    msg = f"my_l: {my_l} rtrn='v' (default) width=40"
    printit("Using " + msg)
    printit(f"Using a simple list: {my_l[:3]} for gselect; center the display and offer q)uit as part of the prompt", 'centered')
    ans = gselect(my_l, 'centered', 'quit', rtrn="v", title="Example of gselect using a simple list", footer=dbug('here'))
    dbug(f"Your ans: {ans}", 'boxed')
    """--== SEP_LINE ==--"""
    ans = gselect(my_l, 'centered', 'quit', rtrn="v", width=40, title=msg, footer=dbug('here'))
    dbug(f"Your ans: {ans}", 'boxed')
    dbug("Now lets show what can be done with a dictionary", 'centered')
    printit(f"Using a dictionary: {my_d} for gselect; center the display and offer q)uit as part of the prompt", 'centered')
    ans = gselect(my_d, 'centered', 'quit', rtrn="v", title="Example of gselect using a dictionary", footer=dbug('here'))
    dbug(f"Your ans: {ans}", 'boxed')
    printit("Now lets use a dictionary but allow multiple selections")
    selected_l = gselect(my_d, 'centered', 'multi', 'quit')
    dbug(f"You selected: {selected_l}")
    my2_l = ["S&P", "DOW", "BuffetIndicator", "VIX", "NASDAQ", "EUR", "USD", "GOLD", "JPN", "PE", "ShillerPE"]
    selected_l = gselect(my2_l, 'multi', 'centered', width=100)
    dbug(f"You selected: {selected_l}")
    return
    # ### EOB def gselect_demo(): ### #


# This is here as an example of how to use gselect as a menu to make function calls
# if you want a menu of selections of functions to run put this in your code
# I couldn't keep this in this file because of scope issues - this file can't "see" the functions you built in another file
# def gmenu(selections_d, *args, **kwargs):
#     """"
#     purpose:  given a dictionary of selection keys: function() it will run the selected function until "q"uit is called
#     options:
#         - cols: int   # default is to display selection keys in 1 column
#     returns: None
#     usage:
#       selections_d = {"Calendar 1 week": "cal('w'), "Calendar 1 month": "cal('m')"}"
#       gmenu(selections_d, cols=2)
#     """
#     """--== Config ==--"""
#     cols = kvarg_val(["cols", "columns"], kwargs, dflt=1)
#     """--== Init ==--"""
#     keys = list(selections_d.keys())
#     """--== Process ==--"""
#     while True:
#         ans = gselect(keys, rtrn="v", cols=cols)
#         if ans in ("q", "Q"):
#             return None
#         eval_this = selections_d[ans]
#         eval(eval_this)

# # ##############
# def changelog(file=__file__):
#     # ##########
#     """
#     prints out the global CHANGELOG string with dbug centered
#     this is for fun - shows off Live too
#     """
#     from rich.table import Table
#     from rich.live import Live
#     from rich.align import Align
#     try:
#         dbug(CHANGELOG, 'centered')
#     except Exception as Error:
#         dbug(Error, 'centered')
#     table = Table(header_style="on rgb(50,50,50)", title="Functions", border_style="bold white on rgb(50,50,60)", row_styles=["on black", "on rgb(20,20,20)"])
#     # table = rtable([], 'header', 'center", title="funcs", prnt=False)
#     table_centered = Align.center(table)
#     table.add_column("funcname", style="bold cyan on black")
#     table.add_column("funcname.__doc__", style="yellow")
#     funcs = []
#     with open(file) as f:
#         lines = f.readlines()
#         with Live(table_centered, refresh_per_second=4) as live:
#             for l in lines:
#                 if l.startswith("def"):
#                     funcs.append(l)
#                     l = l.rstrip("\n")
#                     funcname = re.search(r"def (.*?)\(.*", l).group(1)
#                     if funcname in ("handleOPTS", 'changelog', "main", "docvars"):
#                         continue
#                     fdoc = eval(f"{funcname}.__doc__")
#                     table.add_row(funcname, fdoc)
#                     time.sleep(0.25)
#


# #######################################
def kvarg_val(key, kwargs_d={}, *args, **kwargs):
    # ###################################
    """
    purpose: returns a value when the key in a key=value pair matches any key given
    NOTE: key can be a string or a list of strings
    option: dflt="Whatever default value you want"
    use: used in function to get a value from a kwargs ky=value pair
    - eg:
        def my_function(*args, **kwargs):
            txt_center = kvarg_val(["text_center", "txt_cntr", "txtcntr"], kwargs, dflt=1)
    - so if you call my_function(txt_center=99) then txt_center will be set to 99
    ---
    If any key in the list is set = to a value, that value is returned
    see: bool_val which process both args and kvargs and returns bool_val
    input key(string), kvargs_d(dictionary of key,vals), default(string; optional)
    purpose: return a value given by a key=value pair using a matching key (in key list if desired)
    options:
    -  key provided can be a string or a list of strings
    -  dflt="Whatever default value you want - can be a string, list, int, float... whatever" <-- this is optional, if not declared "" is returned
    if key in kvargs:
        return val
    else:
        return default
    returns str(key_val) or default_val(which is "" if none is provided)
    """
    """--== Debugging ==--"""
    # print(f"funcname: {funcname()}")
    # print(f"args: {args}")
    # print(f"kwargs: {kwargs}")
    # print(f"key: {key}")
    # print(f"kwargs_d: {kwargs_d}")
    """--== Init ==--"""
    required = False
    if "required" in args:
        required = True
    if 'required' in list(kwargs.keys()):
        required = True
    mydflt = ""
    if 'dflt' in kwargs:
        mydflt = kwargs['dflt']
        # ddbug(f"dflt: {mydflt}")
        # print(f"dflt: {mydflt} this is in kvarg_val()")
    """--== Validate ==--"""
    # ### required option ### #
    if required:
        # dbug(key)
        # dbug(kwargs_d)
        found_flag = False
        for my_k in kwargs_d.keys():
            dbug("checking my_k: {my_k}")
            if my_k in key:
                found_flag = True
                ddbug(f"Found on key: {key} my_k: {my_k}")
        if not found_flag:
            dbug(f"Note: A value for a key: {key} was declared required: [{required}] for this operation. No value was provided")
            # dbug(f"Required: [{required}] is experimental but was apparently not included")
            # dbug(f"A value for a key: {key} is required for this operation.", 'ask', 'boxed')
    # if 'rtrn' in key:
        # ddbug(f"kwargs_d: {kwargs_d}")
    """--== Init ==--"""
    # my_val = ""
    my_val = mydflt
    # my_default = ""
    if not isinstance(kwargs_d, dict):
        dbug(f"Supplied kwargs_d: {kwargs_d} MUST be a dictionary! Returning...")
        return
    """--== Convert ==--"""
    if isinstance(key, list):
        keys = key
    else:
        keys = [key]
    """--== Process ==--"""
    for k in keys:
        # dbug(keys)
        # dbug(k)
        # test each key in list
        if k in kwargs_d:
            # dbug(type(k))
            # dbug(f"k: {k} is in kvargs_d: {kvargs_d}")
            my_val = kwargs_d[k]
            # convert a string into a boolean when needed
            if my_val == "False":
                # dbug(f"Converting my_val: {my_val} to False")
                my_val = False
            if my_val == "True":
                # dbug(f"Converting my_val: {my_val} to True")
                my_val = True
    # print(f"Returning my_val: {my_val}")
    # ans = input("Hit anything this is the end of lvarg_val()")
    return my_val
    # ### EOB def kvarg_val(key, kwargs_d={}): ### #


def kvarg_val_demo(*args, **kwargs):
    """
    WIP
    """
    print("We are starting kvarg_val_demo...")
    kwargs = {'tst': "False"}
    keys = ["tst", "test"]
    my_tst = kvarg_val(keys, kwargs, dflt="")
    dbug(type(my_tst))
    # dbug(my_tst, 'ask')
    kwargs = {'tst': "This is a test"}
    dflt = "this is mydefault"
    print(f"Sending keys: {keys}, kwargs: {kwargs}, and dflt={dflt}")
    my_tst = kvarg_val(keys, kwargs, dflt="")
    # dbug(f"my_tst: {my_tst}")
    print("-" * 40)
    """--== SEP_LINE ==--"""
    kwargs = {'xtst': "This is a test"}
    keys = ["tst", "test"]
    dflt = ""
    print(f"Sending keys: {keys}, kwargs: {kwargs}, and dflt={dflt}")
    my_tst = kvarg_val(keys, kwargs, dflt=dflt)
    dbug(f"my_tst: {my_tst}")
    print("-" * 40)
    """--== SEP_LINE ==--"""
    kwargs = {'xtst': "This is a test"}
    kwargs = {'xtst': "This is a test"}
    keys = ["tst", "test"]
    dflt = "The default here"
    print(f"Sending keys: {keys}, kwargs: {kwargs}, and dflt={dflt}")
    my_tst = kvarg_val(keys, kwargs, dflt=dflt)
    dbug(f"my_tst: {my_tst}")
    print("-" * 40)


# ###########################################
def bool_val(key_l, args_l, kvargs={}, **kwargs):
    # #######################################
    """
    purpose: look at args and kwargs with a list of possible option strings and return the default True or False
    requires:
        - key_l: str | list  # this is the string or list of strings to check args and kwargs against
    options:
        - default | dflt: bool  # the default value to return
        - opposite | opposites: str | list  # a list of opposites
            eg: prnt = bool_val(["print", "prnt"], args, kwargs, dflt=True, opposites=['noprnt', 'no_prnt', 'no_print'])
    return True or False
    Notes:
        key_l can be a str or list
        args_l must be provided
        kvargs is optional
        used to see if a string or a list of stings might be declared true
            by being in args or seeing it has a bool value set in kvargs
    use:
        DBUG = bool_val('dbug', args, kvargs)
        or
        DBUG = bool_val(['dbug', 'DBUG'], args, kvargs)
    """
    """--== Debugging ==--"""
    # ddbug(f"funcname: {funcname()}")
    # ddbug(f"args_l: {args_l}")
    # ddbug(f"kvargs: {kvargs}")
    # ddbug(f"kwargs: {kwargs}")
    """--== Config ==--"""
    bool_v = kvarg_val(["default", "dflt"], kwargs, dflt=False)
    opposite_words = kvarg_val(['opposite', 'opposites'], kwargs, dflt=[])
    # ddbug(opposite_words, 'ask')
    """--== Validate ==--"""
    if not isinstance(opposite_words, list) and opposite_words != []:
        # ddbug(f"opposite_words: {opposite_words} needs to be a list")
        opposite_words = [opposite_words]
    """--== Convert ==--"""
    if isinstance(key_l, str):
        key_l = [key_l]  # make it a list
    for k, val in kvargs.items():
        # convert strings to boolean when needed
        if kvargs[k] == "False":
            kvargs[k] = False
        if kvargs[k] == "True":
            kvargs[k] = True
    """--== Init ==--"""
    opposite_b = False
    """--== Process ==--"""
    for key in key_l:
        # dbug(f"s: {s} args_l: {args_l} kvargs: {kvargs}")
        if key in args_l:
            bool_v = True
        if key in kvargs:
            bool_v = kvargs[key]
    for word in opposite_words:
        # ddbug(f"word: {word} args_l: {args_l}")
        if word in args_l:
            # ddbug(f"word: {word}")
            opposite_b = True
        if word in kvargs:
            # convert strings to boolean when needed
            if kvargs[word] == "False":
                kvargs[word] = False
            if kvargs[word] == "True":
                kvargs[word] = True
            if isinstance(kvargs[word], bool):
                opposite_b = kvargs[word]
    if opposite_b:
        # ddbug(f"opposite_b: {opposite_b}")
        bool_v = False
    # dbug(f"Returning bool_v: {bool_v}")
    return bool_v


def bool_val_demo():
    def my_function(*args, **kwargs):
        print(f"args: {args}    kwargs: {kwargs}")
        prnt = bool_val(["prnt", "print", "show", "verbose"], args, kwargs, dflt=False, opposites=["no_prnt", 'noprnt', 'no_print', 'noprint'])
        dflt_true_prnt = bool_val(["prnt", "print", "show", "verbose"], args, kwargs, dflt=True, opposites=["no_prnt", 'noprnt', 'noprint'])
        print(f"prnt={prnt}")
        centered_b = bool_val(["center", "centered"], args, kwargs, dflt=False)
        print(f"centered_b: {centered_b}")
        print(f"dflt_true_print: {dflt_true_prnt}")
        
    msg = """
    The purpose of this function is to allow easy configuration to a function.
    All that is needed for a function is *args and **kwargs ... eg:
    -    def my_function(*args, **kwargs):
    -        my_bool_val = bool_val(["bool", 'bool_val', 'bval'], args,kwargs)
    -        centered = bool_val(["center", 'centered', 'cntr', 'cntrd'], args,kwargs)
    Now if the function is called in any of the following ways my_bool_val will be True and as written here centered will be True
    Keep in mind python insists the quoted single arguments must preceed key=value pairs.
    - my_function('bval', 'centered')
    - my_function('cntr', bval=True, 'cntr')
    - my_function('bool_val', center=True)
    - my_function('centered', bool_val=True)
    - my_function('bool', centered=True, my_other_args)
    .  etc...
    Within a function use this to determine True or False in arguments provided: boo_val(['arg1', 'arg2', ...], args, kwargs, dflt='Your Default')
    """
    printit(msg, 'boxed', 'centered')
    printit("Calling my_function():")
    my_function()
    print("-" * 40)
    printit("Calling my_function('print'):")
    my_function('print')
    print("-" * 40)
    printit("Calling my_function('show', 'centered'):")
    my_function('show', 'centered')
    print("-" * 40)
    printit("Calling my_function('prnt)', centered=False):")
    my_function('print', centered=False)
    print("-" * 40)
    printit("Calling my_function('noprnt)', centered=False):")
    my_function('noprnt', centered=False)
    # ### EOB def bool_val_demo(): ### #


# #########################################
def cfg_val(keys, section, cfg_d, dflt=""):
    # #####################################
    """
    purpose: to retrieve cfg val from a config_dictionary (section, key-value pair) while allowing different key name requests to get a specific key
    options: 
        - if section == "" or section not found then section 'default' will be used
        - dflt: str|int|bool|whatever  # allows a fall-back value if none found in cfg_d (see notes below) 
    returns: value
    notes: if section == 'DEFAULT' | 'Default' | 'default' | 'dflt' | "" then it will be processed as 'default' section;
            This might seem like it defeats the purpose of the dflt option but it allows a cfg_d['default'] value to take precedent and allow a return even if no
                matching key(s) can be found
    use:
        cfg_d = handleCFG("/path/to/api.cfg")
        api_key = cfg_val(["api", "key", "api_key"], 'testpypi', cfg_d, dflt="1234")
        # above will find the api_key if it is defined in the file with any of the names in the list for section='testpypi'
        # or
        theme = cfg_val(["theme", "style"], 'default', cfg_d, dflt="1234")
    """
    # TODO: this needs serious refactoring
def cfg_val(keys, section, cfg_d, dflt=""):
    """--== Config ==--"""
    my_section = section
    if my_section not in cfg_d:
        my_section = 'default'
    if str(section).lower() in ("", 'default', 'dflt'):
        # dbug("force section to be 'default' as it appears to be the section requested")
        my_section = 'default'
    """--== Convert ==--"""
    if isinstance(keys, str):
        # dbug(f"turn a string keys: {keys} into a list")
        keys = [keys]
    """--== SEP_LINE ==--"""
    rtrn = ""
    new_cfg_d = {}
    for my_section, vals in cfg_d.items():
        # dbug(f"Make sure my_section: {my_section} is 'default' if needed")
        if str(my_section).lower() in ("", 'default', 'Default', 'dflt'):
            # dbug("Grabbing vals for key: default")
            new_cfg_d["default"] = vals
        else:
            # dbug(f"Grabbing vals for key: {my_section}")
            new_cfg_d[my_section] = vals
    cfg_d = new_cfg_d
    """--== Process ==--"""
    for key in keys:
        try:
            # grab the actual key value from user declared section if present
            rtrn = cfg_d[section][key]
            break
        except:
            try:
                # dbug(f"grab the default 'key': {key} if present")
                rtrn = cfg_d['default'][key]
                break
            except:
                rtrn = dflt
    if isinstance(rtrn, str):
        if "," in str(rtrn):
            rtrn = rtrn.split(",")  # rtrn becomes a list
            rtrn = [x.strip() for x in rtrn]  # clean each elem up
    # dbug(f"Returning rtrn: {rtrn}")
    return rtrn
    # ### EOB def cfg_val(keys, section, cfg_d, dflt=""): ### #


# ###########################
def docvars(*args, **kvargs):
    # #######################
    """
    purpose: wrapper for function to allow variable substitution within its doc
    I use this in front on a function I call handleOPTS(args)
    which works with the module docopts
    Thank you to stackoverflow.com: answered Apr 25 '12 at 1:54 senderle
    this is a very useful way to allow variables in your __doc__ strings
    wrap a function with this and use if this way
    eg:
    @docvars(os.path.basename(__file__), anotherarg, myarg="abcd")
    def myfunc():
        \"""
        Usage: {0} [-hijk]\"

        Notes:
             anotherarg: {1}
             myarg: {myarg}
        \"""
        return \"Done\"
    """
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kvargs)
        return obj
    return dec
    # ### EOB def docvars(*args, **kvargs): ### #


# def fstring(s):
#     """
#     purpose: alternative to f-strings
#     use: fsting(s)
#     returns: formated s string
#     use: not currently used but it was used in the early versions of python3 that lacked f-strings
#     """
#     # alternate to f-strings
#     # requires: from inspect import currentframe
#     # this is an alternative to f-string
#     # use: [instead of f"my string contains {myvar}"]
#     # f("my string contains {myvar}")
#     frame = currentframe().f_back
#     return eval(f"f'{s}'", frame.f_locals, frame.f_globals)


def fix_msgs(msgs, *args, **kwargs):
    """
    purpose: 'fix' an internal multiline msg = \"""  line1\n    line2\n   etc\"""  to remove preceding spaces - only works if spaces are used and not tabs (TODO)
    options:
        - lst: bool  # option to force return msg to be a list (default is str)
    returns: msgs as a string if 'lst' not invoked without the preceding 4x" " 
    """
    lst = bool_val(["lst", "list"], args, kwargs, dflt=False)
    if isinstance(msgs, str):
        lines = msgs.split("\n")
    msgs = [re.sub("^    ", "", ln) for ln in lines]
    if not lst:
        msgs = "\n".join(msgs)
    return msgs
    # ### EOB def fix_msgs(msgs, *args, **kwargs): ### #


# #########################
def handleCFG(cfg_file="", *args, **kwargs):
    # #####################
    """
    purpose:  if no cfg_file given it will find the default and return cfg_d (dictionary of dictioanries: cfg.sections; cfg.elem:vals)
    input: cfg_file: str
    options:
        - section: str
        - key: str
    defaults: cfg_file if it exists is: {myappname.basename}.cfg
    returns: cfg_d: dict (dictionary of dictionaries - cfg.sections with key, val pairs)
    use:
        cfg_d = handleCFG("/my/path/to/myapp.cfg")
        try:
            title = cfg_d['menu']['title']
        except:
            title = ""
    """
    # TODO add global section that over-rides all of similar values
    # dbug(funcname())
    # dbug(cfg_file)
    # dbug(args)
    # dbug(kwargs)
    """--== Imports ==--"""
    import dynaconf
    """--== Config ==--"""
    my_section = kvarg_val('section', kwargs, dflt="")
    my_key = kvarg_val(['key'], kwargs, dflt="")
    dflt = kvarg_val(['dflt'], kwargs, dflt=None)
    # dbug(f"my_section: {my_section} my_key: {my_key}")
    """--== Init ==--"""
    type = "ini"
    cfg_d = {}
    """--== Convert ==--"""
    if isinstance(cfg_file, dict):
        dbug(f"cfg_file: {cfg_file} is probably already a dictionary so assume the user wants the section: {my_section} and key: {my_key}")
        cfg_d = cfg_file
        # dbug(cfg_d)
        # dbug(args)
        # dbug(kwargs)
        # user passed the cfg_d back probably with a section and key
        if len(my_key) > 0:
            try:
                if isinstance(my_key, str):
                    key = [my_key]
                for k in key:
                    # dbug(f"Chkg k: {k}")
                    rtrn = cfg_d[my_section][k]
                # rtrn = cfg_d[section][key]
                dbug(f"Returning {rtrn}")
                return rtrn
            except Exception as Error:
                # dbug(cfg_d)
                # dbug(f"Exception Error: {repr(Error)}")
                dbug(f"Returning {dflt}")
                return dflt
    if isinstance(cfg_file, str):
        # dbug(f"force cfg_file to be a list")
        cfg_file = os.path.expanduser(cfg_file)
        # bname = os.path.splitext(cfg_file)[0]
        ext = cfg_file.split(".")[-1]
        type = ext
    if isinstance(cfg_file, list):
        # dbug(f"cfg_file: {cfg_file} is apparently a list...")
        cfg_files = cfg_file
        cfg_d = {}
        for f in cfg_files:
            # dbug(f"processing file: {f} type: {type} cfg_d: {cfg_d}")
            # dbug(f)
            ext = os.path.splitext(f)[1]
            type = ext.lstrip(".")
            my_cfg = handleCFG(f)
            # dbug(my_cfg)
            cfg_d.update(my_cfg)
        # dbug(f"Returning cfg_d: {cfg_d}", 'ask')
        return cfg_d
    # dbug(cfg_file)
    # dbug(cfg_files)
    """--== Validate ==--"""
    if not file_exists(cfg_file):
        dbug(f"Failed to find cfg_file: {cfg_file} ... please investigate...")
        return
    if cfg_file == "":
        inspect_filename = str(inspect.getfile(currentframe().f_back))
        inspect_filename = inspect_filename.replace("/./", "/")
        bname = inspect_filename.split(".")[0]
        # dbug(bname)
        types = ['env', 'ini', 'cfg', 'conf', 'toml', 'json', 'yaml']
        cfg_file = []
        for type in types:
            cfg_file.append(bname + "." + type)
        # dbug(cfg_file)
        # dbug(f"No cfg_filename provided cfg_file: [{cfg_file}]")
        cfg_files = []
        for f in cfg_file:
            # dbug("Test each file to see if it exists...")
            if file_exists(f):
                f = f.replace("/./", "/")
                cfg_files.append(f)
        # dbug(cfg_files)
        # cfg_file = cfg_files
        if all([file_exists(f) for f in cfg_file]):
            dbug(f"cfg_file not found (cfg_file: {cfg_file})... returning None ...")
        # cfg_file = os.path.splitext(__file__)[0]
        # cfg_file += ".cfg"
        # dbug("Returning None")
        # return None
        if len(cfg_files) == 0:
            dbug("No cfg_file(s)... returning...")
            if askYN(f"Would you like to edit one: {bname}.toml", "y", 'centered'):
                do_edit(bname + ".toml")
            return None
        else:
            # dbug("Begin handleCFG(cfg_files) ... one or more cfg_files")
            cfg_d = handleCFG(cfg_files)
            # dbug(cfg_d)
            return cfg_d
    # https://hackersandslackers.com/simplify-your-python-projects-configuration/
    # if type.lower() == 'env':
    #     from  dotenv import load_dotenv
    #     dbug("do_env")
    # dbug(type, 'ask')
    if type.lower() == 'env':
        content_l = purify(cfg_file, 'lst')
        cfg_d = {}
        for ln in content_l:
            if "=" in ln:
                var, value = ln.split("=")
                cfg_d[var] = value
                # dbug(cfg_d, 'ask')
    if type.lower() in ("ini", "cfg", "conf"):
        # dbug(f"type: {type} cfg_file: cfg_file")
        config = configparser.ConfigParser()
        try:
            config.read(cfg_file, encoding='utf-8')
            config.read(cfg_file)
        except Exception as Error:
            dbug(f"Problem with cfg_file: {cfg_file} Error: {Error}")
        # dbug(config.sections())
        if len(config['DEFAULT']) > 0:
            # DEFAULT is treated differently by configparser... got me why
            # I don't suggest using it as values don't seem to be parsed the same way (needs quoting??)
            # lowercase 'default' will work fine - use it instead?
            default_d = dict(config.items('DEFAULT'))
            cfg_d['DEFAULT'] = {}
            for key, val in default_d.items():
                cfg_d['DEFAULT'][key] = val
        for section in config.sections():
            cfg_d[section] = {}
            for key in config[section]:
                val = config[section][key]
                cfg_d[section][key] = val
    if type.lower() == 'json':
        import json
        # dbug("begin to do json")
        json_content = cat_file(cfg_file)
        # dbug(json_content)
        cfg_d = json.loads(json_content)
        # dbug(f"do_json cfg_d: {cfg_d}")
    if type.lower() == 'yaml':
        import yaml
        # dbug(cfg_file)
        yaml_content = cat_file(cfg_file)
        cfg_d = yaml.safe_load(yaml_content)
        # dbug("do yaml")
        # dbug(f"do_yaml cfg_d: {cfg_d}")
    if type.lower() == 'toml':
        import toml
        cfg_d = toml.load(cfg_file)  # , _dict=dict) #  f=f|[f,f,...]
        # or toml.loads(s, _dict=dict) s=string  _dict specifies return class
        # dbug(f"do_toml cfg_d: {cfg_d}")
    """--== attempt dynaconf ==--"""
    # dbug(f"Running dynaconf with cfg_files: {cfg_files}")
    # cfg_o = dynaconf.Dynaconf(settings_files=cfg_files)
    # dbug(cfg_o)
    # cfg_d = cfg_o.as_dict()
    # dbug(cfg_d, 'ask')
    """--== SEP_LINE ==--"""
    # dbug(cfg_d)
    if my_section != "":
        cfg_d = cfg_d[my_section]
    if my_key != "":
        # kv_cols(cfg_d, 4, 'prnt', title="debugging", footer=dbug('here'))
        cfg_d = cfg_d[my_key]  # assumes section done above
    # dbug(f"Returning: {cfg_d} using file: {cfg_file} type: {type} EOB")
    return cfg_d
    # ### EOB def handleCFG(cfg_file=""): ### #


def handleCFG_tst(*args, **kwargs):
    """
    purpose: to demo use of handleCFG function
    returns: none
    """
    # """--== Debugging ==--"""
    # dbug(args)
    # dbug(kwargs)
    # calling_funcname = str(getframeinfo(currentframe().f_back).function)
    # dbug(calling_funcname)
    # """--== Init ==--"""
    calling_filename = str(inspect.getfile(currentframe().f_back))
    # dbug(calling_filename)
    bname = os.path.splitext(calling_filename)[0] 
    bdir = os.path.dirname(calling_filename)
    # dbug(bdir)
    # dbug(bname)
    """--==  write out some config files ==--"""
    env_cfg = """
    MYVAR="this is a dotenv variable contained in .env file"
    """
    env_cfg = fix_msgs(env_cfg)
    """--== SEP_LINE ==--"""
    ini_cfg = """
    [default]
    name = "Ralph (cfg) Ublanowitz"
    type_file = ini
    cfg_job: blogger

    [section1]
    name = ini Section1 Name
    width = 10
    height = 15
    """
    ini_cfg = fix_msgs(ini_cfg)
    # """--== SEP_LINE ==--"""
    """--== toml ==--"""
    toml_cfg = """
    [default]
        name = "R (toml) Ublanowitz"
        tonl_job = 'blogger'
        type_file = "toml"
    [section1]
        name = "toml Section1 Name"
        width = 70
        height = 25
        tonl_date = 20230420
    """
    toml_cfg = fix_msgs(toml_cfg)
    # """--== SEP_LINE ==--"""
    """--== json ==--"""
    json_cfg = """
    {
      "name": "Ralph (json) Ublanowitz",
      "type_file": "json",
      "date": "2023-04-19",
      "json_job": "vocational pastor"
    }
    """
    json_cfg = fix_msgs(json_cfg)
    # """--== SEP_LINE ==--"""
    """--== yaml ==--"""
    yaml_cfg = """
    type_file: yaml
    section:
        section_name: section1
    default:
      name: Ralph (yaml) Ublanowitz
      job: "brick layer extrodinaire"
    """
    yaml_cfg = fix_msgs(yaml_cfg)
    # """--== Process ==--"""
    env_filename = bdir + "/.env"
    # dbug(env_filename)
    cfg_filename = bname + ".cfg"
    toml_filename = bname + ".toml"
    json_filename = bname + ".json"
    yaml_filename = bname + ".yaml"
    cfg_files = [env_filename, cfg_filename, toml_filename, json_filename, yaml_filename]
    # dbug(cfg_files)
    for file in cfg_files:
        # dbug(file)
        with open(file, 'w') as f:
            # dbug(f"We open file: {file} for writing")
            ext = file.split(".")[-1]
            type = ext
            # ext = os.path.splitext(file)[1]
            # type = ext.lstrip(".")
            # dbug(type)
            printit(f"======== Writing and handling file type: {ext} file type: {type} =========", 'centered')
            if type == "env":
                msg = env_cfg
            elif type == "cfg":
                msg = ini_cfg
            elif type == "toml":
                msg = toml_cfg
            elif type == "json":
                msg = json_cfg
            elif type == "yaml":
                msg = yaml_cfg
            else:
                dbug(f"I don't know how to handle this file type {type}...")
                return
            f.write(msg)
        printit(cat_file(cfg_filename), 'boxed', 'centered', title=f"cat_file({cfg_filename}) type: {type}", footer=dbug('here'))
        cfg_d = handleCFG(cfg_filename)
        gtable(cfg_d, 'prnt', 'hdr', 'centered', colnames=["Key", "Value"], title=f"cfg_d file: {file} type: {type}", footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    # cfg_d = handleCFG(toml_filename)
    # dbug(cfg_d, 'ask')
    # dbug(cfg_d['default']['name'], 'ask')
    printit("==================", 'centered')
    boxes = []
    for f in cfg_files:
        my_box = boxed(cat_file(f), title=f"{os.path.basename(f)}", footer=dbug('here'), box_clr="yellow on black")
        # dbug('ask')
        boxes.append(boxed(cat_file(f), title=f"{os.path.basename(f)}", footer=dbug('here'), box_clr="yellow on black"))
    gcolumnize(boxes, 'prnt', 'centered', cols=3)
    cfg_d = handleCFG(cfg_files)
    gtable(cfg_d, 'prnt', 'hdr', 'centered', colnames=["Key", "Value"], title=f"cfg_d all the types", footer=dbug('here'))
    """--== final test with no arguments - check all possible default cofnig files ==--"""
    cfg_d = handleCFG()
    # dbug(cfg_d, 'ask')
    return
    # ### EOB def handleCFG_tst(*args, **kwargs): ### #


def browseit(url="http://localhost/", *args, **kwargs):
    """
    purpose: opens the url in your browser
    requires: url: str
    returns: none
    """
    # """--== Imports ==--"""
    import webbrowser
    # """--== Debugging ==--"""
    # dbug(funcname())
    # """--== Process ==--"""
    # webbrowser.open_new(url)
    if not file_exists(url) and "://" not in url:
        # dbug("treat as html text")
        with open("tmp.html", 'w') as f:
            f.write(url)
        # cat_file('tmp.html', 'prnt')
        webbrowser.open('tmp.html', new=0)
        return
    else:
        # dbug("url is either a file or a real url")
        webbrowser.open(url, new=0)
    return


def browseit_tst(*args, **kwargs):
    """
    purpose: simple demo of browseit
    returns: none
    """
    browseit()


@docvars(os.path.basename(__file__))
def handleOPTS(args):
    """
    Usage:
        {0} -h
        {0} -T <func> [<fargs>]
        {0} -E
        {0} --version
        {0} --demos
        {0} --docs
        {0} <cmd> [<fargs>...]

    Options
        -h, --help             Help
        -v, --version          Prints version
        -T <func> [<fargs>]    runs specified func with optional args=fargs, primarily for development
        -E                     edit this file
        --demos                allows user to select a demo
        --docs                 allows to user to display the doc for selected function
        <cmd> [farg farg] ...] function arg, arg, arg ... (when used at command line, ie: {0}-cli, prnt is always assumed to be true)

    Examples for {0}-cli:
        {0}-cli "This is in a red box" boxed centered box_color=red
        {0}-cli printit "Message in a white on black box" boxed box_color='white on black'
    """
    # dbug(args)
    # def get_args(arg_s):
    #     if arg_s is None:
    #         arg_s = ""
    #     args_l = arg_s.split(",")
    #     new_args_l = []
    #     new_kwargs_d = {}
    #     for arg in args_l:
    #         if "=" in arg:
    #             # dbug(arg)
    #             key, val = arg.split("=")
    #             # dbug(key)
    #             # dbug(val)
    #             new_kwargs_d[key.strip()] = val
    #         else:
    #             new_args_l.append(arg)
    #     rtrn_d = {'args': new_args_l, 'kwargs': new_kwargs_d}
    #     # dbug(f"Returning rtrn_d: {rtrn_d}")
    #     return rtrn_d
    # if args["-t"]:
    #     try:
    #         import doctest
    #     except Exception as Error:
    #         dbug(f"Error: {Error}")
    #         return
    #     # dbug()
    #     if args['<func>']:
    #         func = args['<func>']
    #         name = f"{os.path.basename(__file__)}.{func}()"
    #         gb = globals()
    #         # don't lose this next line --- iC<Plug>ocRefresht took time to find it!
    #         doctest.run_docstring_examples(globals()[func], gb, verbose=True, name=name, optionflags=doctest.ELLIPSIS)
    #         do_close()
    #     else:
    #         doctest.testmod(verbose=True, report=False, raise_on_error=False, exclude_empty=False)
    #     do_close()
    if args['-T']:
        """
        this is to test a single function
        Put this in Usage section:
          {0} -T <funcname> [<fargs>]
        """
        # dbug(args['-T'])
        # if isinstance(args['-T'], str):
        #     funcname = args['-T']
        #     dbug(funcname)
        if isinstance(args['-T'], bool):
            funcname = args['<func>']
        else:
            funcname = args['-T']
        # dbug(funcname)
        fargs = args['<fargs>']
        # dbug(fargs)
        args_d = get_args(fargs)
        # dbug(args_d)
        # dbug(args_d)
        if args_d is None:
            dbug(funcname)
            globals()[funcname]()
        else:
            if args_d['kwargs'] is None:
                dbug(args_d['args'])
                dbug(args_d['kwargs'])
                globals()[funcname](*args_d['args'])
            else:
                # dbug(funcname)
                # dbug(args_d['args'])
                # dbug(args_d['kwargs'])
                args = args_d['args']
                kwargs = args_d['kwargs']
                # dbug(args)
                # dbug(kwargs)
                # dbug(f"full cmd: {funcname}({args}, {kwargs}")
                if isempty(args) and isempty(kwargs):
                    # this is in case the funcname lacks any arguments ie funcname(*args, **kwargs)
                    globals()[funcname]()
                else:
                    globals()[funcname](*args_d['args'], **args_d['kwargs'])
        return
        """--== SEP_LINE ==--"""
        args_d = get_args(fargs)
        if args_d is None:
            globals()[funcname]()
        else:
            if args_d['kwargs'] is None:
                globals()[funcname](*args_d['args'])
            else:
                globals()[funcname](*args_d['args'], **args_d['kwargs'])
        do_close("", 'center')
        return
    # """--== SEP_LINE ==--"""
    if args['<cmd>'] and args['<fargs>']:
        # this handles do_cli situations
        cmd = args['<cmd>']
        args_l = args['<fargs>']
        args_s = ", ".join(args_l)
        # dbug(args['<fargs>'])
        # dbug(args_s)
        if 'prnt' not in args_s:
            args_s = args_s + ", prnt=True"
        out = str(do_cli(cmd, args_s))  # out currently is not used
        # sys.stdout.flush(out)
        # print(out, flush=True)
        # dbug(f"Done... out: {out}")
        sys.exit()
    # """--== SEP_LINE ==--"""
    # if args["--dir"]:
    #     # import sys
    #     sys.path.append("/home/geoffm/dev/python/gmodules")
    #     # import __file__
    #     print(f"dir({__file__}): " + "\n".join(dir(__file__)))
    #     print("file: " + __file__)
    #     return
    # """--== SEP_LINE ==--"""
    if "-E" in sys.argv:
        do_edit(FULL_PATH_SCRIPT)  # I do not know why but in this module __file__ get lost... ???
        do_close()
    return None
    # ### EOB def handleOPTS(args): ### #


def get_args(arg_s):
    """
    purpose: parses string into *args and **kwargs
    notes: called by do_cli()
    """
    if isempty(arg_s):
        arg_s = ""
    if not isinstance(arg_s, str):
        dbug(f"args_s: {arg_s} should be a string")
        return
    args_l = arg_s.split(",")
    new_args_l = []
    new_kwargs_d = {}
    for arg in args_l:
        if "=" in arg:
            # dbug(arg)
            key, val = arg.split("=")
            key = key.strip()
            # if key.endswith("'") and key.startswih("'"):
            #     key = key.strip("'")
            if val.startswith('"') and val.endswith('"'):
                val = val.strip('""')
            # dbug(val)
            if val.startswith("'") and val.endswith("'"):
                val = val.strip("'")
            # dbug(key)
            # dbug(val)
            new_kwargs_d[key] = val
        else:
            # dbug(arg)
            arg = arg.strip()
            # dbug(arg)
            if arg.startswith('"') and arg.endswith('"'):
                arg = arg.strip('""')
            # dbug(arg)
            if arg.startswith("'") and arg.endswith("'"):
                arg = arg.strip("'")
            # dbug(arg)
            arg = arg.strip()
            # """--== deal with a possible list ==--"""
            if arg.startswith('['):
                arg_l = [arg.lstrip("[")]
                continue
            if arg.endswith("]"):
                arg_l.append(arg.rstrip("]"))
                # dbug(arg_l)
                arg = arg_l
            # dbug(arg)
            # """--== EOB ==--"""
            new_args_l.append(arg)
    rtrn_d = {'args': new_args_l, 'kwargs': new_kwargs_d}
    # dbug(f"Returning rtrn_d: {rtrn_d}")
    return rtrn_d
    # ### EOB def get_args(arg_s): ### #




# def run_func(fname, func_args, *args, **kwargs):
#     """
#     purpose: runs a func with declared arguments and returns result
#     options:
#     returns: result from function
#     notes: no need to quote variable argument values
#     experimental: this is way to fragile 20230210
#     """
#     # """--= Config ==--"""
#     doc_b = bool_val(["doc", "docs"], args, kwargs, dflt=False)
#     # """--== Process ==--"""
#     rslt = None
#     fargs = func_args
#     dbug(type(fname))
#     if doc_b:
#         if isinstance(fname, str):
#             my_msg = globals()[fname].__doc__
#         else:
#             my_msg = fname.__doc__
#         if my_msg is None:
#             my_msg = "No doc available..."
#         printit(f"Function: {fname}({fargs}) doc: " + my_msg, 'centered', 'boxed',
#                 title=f"Calling function {fname}() for testing purposes", footer=dbug('here'))
#     def get_args(arg_s):
#         if arg_s is None:
#             arg_s = ""
#         if isinstance(arg_s, str):
#             args_l = arg_s.split(",")
#         if isinstance(arg_s, list):
#             args_l = arg_s
#         new_args_l = []
#         new_kwargs_d = {}
#         for arg in args_l:
#             if "=" in arg:
#                 key, val = arg.split("=")
#                 new_kwargs_d[key.strip()] = val
#             else:
#                 new_args_l.append(arg)
#         return {'args': new_args_l, 'kwargs': new_kwargs_d}
#     args_d = get_args(fargs)
#     if isinstance(fname, str):
#         if fname in locals():
#             dbug("Found in locals")
#             if args_d is None:
#                 rslt = locals()[fname]()
#             else:
#                 if args_d['kwargs'] is None:
#                     rslt = locals()[fname](*args_d['args'])
#                 else:
#                     rslt = locals()[fname](*args_d['args'], **args_d['kwargs'])
#         if fname in globals():
#             dbug("Found in globals")
#             if args_d is None:
#                 rslt = globals()[fname]()
#             else:
#                 if args_d['kwargs'] is None:
#                     rslt = globals()[fname](*args_d['args'])
#                 else:
#                     rslt = globals()[fname](*args_d['args'], **args_d['kwargs'])
#     else:
#         dbug("Using type(fname): {type(fname)}")
#         try:
#             fname(*args_d['args'], **args_d['kwargs'])
#         except Exception as Error:
#             dbug(Error)
#     dbug(f"Did it work? Returning rslt: {rslt}")
#     return rslt
#     # ### EOB def run_func(func, func_args, *args, **kwargs): ### #


# # #####################
# def path_to(app):
#     # #################
#     """Check whether `name` is on PATH and marked as executable."""
#     from shutil import which
#     full_path = which(app)
#     # print("full_path: " + full_path)
#     # returns None type if it fails?
#     if full_path is not None:
#         return full_path
#     return None
    if args_d is None:
        rslt = globals()[fname]()
    else:
        if args_d['kwargs'] is None:
            rslt = globals()[fname](*args_d['args'])
        else:
            rslt =globals()[fname](*args_d['args'], **args_d['kwargs'])
    do_close("", 'center')
    return rslt
    # ### EOB def run_func(func, func_args, *args, **kwargs): ### #


# # #####################
# def path_to(app):
#     # #################
#     """Check whether `name` is on PATH and marked as executable."""
#     from shutil import which
#     full_path = which(app)
#     # print("full_path: " + full_path)
#     # returns None type if it fails?
#     if full_path is not None:
#         return full_path
#     return None


# ############################
def centered(msgs, *args, **kwargs):
    # ########################
    """
    purpose: calculates screen placement for msgs: list|str
    options:
        length=columns: int
        shift=0: int
        'str'|'string'=False: bool
        'lst'|'list'=True: bool
    returns: line|lines
    note: replaces deprecated centerit()
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(msgs)
    # """--== SEP_LINE ==--"""
    # try:
    #    # sometimes there is no stty... like with wsgi
    #     rows, columns = os.popen("stty size", "r").read().split()
    # finally:
    #     rows = 0
    #     columnns = 0
    # """--== Config ==--"""
    shift = kvarg_val('shift', kwargs, dflt=0)
    length = kvarg_val(['length'], kwargs, dflt=0)  # canvas columns instead of screen columns
    # dbug(length)
    width = kvarg_val(["width"], kwargs, dflt=0)  # rarely used; different from length which is for canvas instead of screen columns
    lst = bool_val(['lst', 'list'], args, kwargs, dflt=True)
    string_b = bool_val(['str', 'string'], args, kwargs, dflt=False)
    pad = kvarg_val(["pad"], kwargs, dflt=" ")
    prnt = bool_val(["prnt", "print", "show", "verbose"], args, kwargs, dflt=False)
    # margin = 0
    # """--== Validation ==--"""
    if msgs is None:
        dbug(f"msgs: {msgs} appear to be empty... returning")
        return None
    if not isinstance(shift, int):
        shift = 0
    if not isinstance(length, int):
        length = 0
    # """--== Init ==--"""
    # reset = sub_color("reset")
    if length == 0:
        # dbug(shift)
        # scr_columns = get_columns(shift=shift)
        scr_columns = get_columns()
        # dbug(scr_columns)
        # scr_columns = get_columns(shift=0)
        # dbug(scr_columns)
        length = scr_columns
    l_pad_len = 0
    # """--== Process ==--"""
    if isinstance(msgs, str):
        msgs = [msgs]
    msgs_max_len = maxof(msgs)
    # dbug(msgs_max_len)
    if msgs_max_len > int(width) and int(width) > 10:  # arbitrary
        msgs = wrapit(msgs, length=int(width))
    lines = []
    for ln in msgs:
        # dbug(ln)
        if isinstance(ln, list) and len(ln) == 1:
            # looks like printit will center a title  and footer line and it will be a single elem in a list???
            # so this fixes it but it really should be fixed in printit... TODO
            # hmmm tried doing this in printit and it breaks things
            ln = ln[0]
            lines.append(ln)
            # dbug(f"Just appended ln: [{ln}]")
        else:
            # dbug(length)
            l_pad_len = (length - nclen(ln)) // 2
            # dbug(f"l_pad_len: {l_pad_len} before shift: {shift} nclen(ln): {nclen(ln)}")
            l_pad_len += shift  # remember that shift will most likely be a negative value
            # dbug(f"l_pad_len: {l_pad_len} after shift: {shift}")
            l_pad = pad * l_pad_len
            lines.append(l_pad + ln)
    if not lst or string_b:
        rtrn = "".join(lines)
    else:
        rtrn = lines
    # dbug(lines)
    if prnt:
        printit(rtrn)
    return rtrn
    # ### EOB def centered(msgs): ### #


# #################################
def centered_demo(*args, **kwargs):
    # #############################
    """
    purpose: demo of using centered()
    returns: None
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # """--== Init ==--"""
    shifts = [0, -10, -20, -30, -40, -50, -60]
    # """--== Process ==--"""
    for shift in shifts:
        msg = f"msg here with shift: {shift}"
        centered(msg, 'prnt', shift=shift)
    ruleit(center=True)
    # ### EOB def centered_demo(*args, **kwargs): ### #


# #############
def ruleit(*args, **kwargs):
    # #########
    """
    purpose: This is for development purposes
        It draws a rule across the screen and that is all it does
        It fails to prepare your meals or schedule your week\'s agenda, sorry.
    options:
        - width: int     # default=0     - truncates at this len otherwise it is screen length
        - cntr: bool     # default=False - provide center info
        - prnt: bool     # default=True  -  whether to print
    returns: printed ruler line with tick marks and marker numbers below
    """
    # """--== Config ==--"""
    width = kvarg_val(["width", "w", "length", "l"], kwargs, dflt=0)
    cntr = bool_val(["cntr", "center"], args, kwargs, dflt=False)
    prnt = bool_val(["prnt", "print"], args, kwargs, dflt=True)
    # """--== Init ==--"""
    line = ""
    tick_line = ""
    mark_line = ""
    # lines = []
    new_lines = []
    if width == 0:
        columns = get_columns()
        cols = int(columns)
    else:
        cols = int(width)
    cntr = cols / 2
    # iters = int(floor(int(cols)) / 10)
    my_iters = cols // 10
    # dbug(my_iters)
    markers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    # """--== Process ==--"""
    # diff = int(columns) % 10
    diff = int(cols) % 10
    for i in range(0, my_iters):
        for x in range(0, 10):
            actual_num = (i * 10) + x + 1
            # dbug(f"i: {i} x: {x} actual number: {actual_num}")
            if prnt:
                marker = markers[x]
                if actual_num == cntr:
                    marker = gclr("red", text=marker, reset=True)
                print(marker, end="")
            line += str(markers[x])
    for i in range(0, diff):
        # dbug(i)
        if prnt:
            print(markers[i], end="")
        line += str(markers[i])
    if prnt:
        print()
    for i in range(0, my_iters):
        for x in range(0, 10):
            # dbug(x)
            if x == 9:
                if prnt:
                    print("|", end="")
                tick_line += "|"
            else:
                if prnt:
                    print(" ", end="")
                tick_line += " "
    if prnt:
        print()
    cnt = 10
    new_lines.append(line)
    new_lines.append(tick_line)
    for i in range(0, my_iters):
        for x in range(0, 10):
            if x == 0:
                pad = " "
                # dbug(cnt)
                # dbug(str(cnt))
                padding = 10 - len(str(cnt))
                # dbug(padding)
                fill = padding * pad
                # dbug(f"fill: [{fill}]")
                if prnt:
                    print(fill + str(cnt), end="")
                mark_line += fill + str(cnt)
                cnt += 10
                if cnt > width:
                    break
    # dbug(mark_line)
    new_lines.append(mark_line)
    if prnt:
        print()
    if cntr:
        # cntr = cols / 2
        printit(f"cols/length: {cols} The center is: {cntr} marked in red", 'centered', width=width)
        return cntr
    return new_lines
    # ### EOB def ruleit(): ### #


def ruleit_demo(*args, **kwargs):
    """
    purpose: demo of using ruleit()
    returns: None
    """
    ruleit(5)
    ruleit(12)
    ruleit(16)
    ruleit(20)
    ruleit(26)
    # printit(ruleit(36, prnt=False), 'boxed', footer=dbug('here'))


# ######################################
def do_close(msg="", *args, hchr="=", color="", rc=0, **kwargs):
    # ##################################
    """
    purpose: to provide a boxed closing message default msg is below
    options:
        - box_clr: str           # color of main box
        - quote: str             # should a random quote from filename provided be included
        - quoote_box_color: str  # box color for quote default="White! on black"
        - centered: bool         # center the output on the screen
        - shadowed: bool         # should the box(es) be shadowed
        - figlet: bool           # use figlet to decorate msg
    returns: None
    # dflt_msg = "Enjoy!"
    input msg or it uses dflt_msg
    options: 'center' | 'centered' color='red' rc=return code to exit with
    >>> do_close()
        ======
        Enjoy!
        ======
    """
    # """--== Config ==--"""
    quote = kvarg_val('quote', kwargs, dflt="")
    quote_box_color = kvarg_val(["qbox_clr", "quote_box_color", "quote_box_clr"], kwargs, dflt="white! on black")
    centered = bool_val(['center', 'centered'], args, kwargs, dflt=True)
    txt_center = kvarg_val(['txt_center', 'text_center', 'cntr_txt', 'txt_centered'], kwargs, dflt=0)
    shadowed = bool_val(['shadow', 'shadowed'], args, kwargs)
    box_color = kvarg_val(["box_clr", 'box_color', "bx_clr", "bxclr"], kwargs, dflt="")
    figlet = bool_val(['figlet'], args, kwargs)
    # """--== Init ==--"""
    dflt_msg = "Wanted: Software Developer. Python experience is a plus. Pay commensurate with skill set. Apply within."
    # dflt_msg = "All is well that ends well!"
    # """--== Process ==--"""
    if msg == "":
        msg = dflt_msg
    if figlet:
        from pyfiglet import figlet_format
        msg = figlet_format(msg, width=1000)
    printit(msg, 'box', footer=f"{datetime.now().strftime('%Y-%m-%d %H:%M')}", center=centered, shadow=shadowed, box_color=box_color, color=color, txt_center=txt_center)
    if quote != "":
        # quote needs to be a path/filename -- path can include "~/" for $HOME
        # dbug(quote)
        if isinstance(quote, str):
            file = os.path.expanduser(quote)
        else:
            dbug(f"quote: {quote} must be a valid filename: str containing quote lines", 'centered')
            return None
        quote_msg = get_random_line(file)
        if isempty(quote_msg):
            quote_msg = f"No quote found from quote: {quote}"
        quote_msg = wrapit(quote_msg, length=80)
        printit(quote_msg, 'boxed', title=" Quote ", box_color=quote_box_color, centered=centered, shadow=shadowed, color=color)
    sys.exit(rc)
    # ### EOB def do_close(msg="", *args, hchr="=", color="", box_color="", rc=0, **kwargs): ### #


# ###################################
def convert_temp(temp, convert2="f"):
    # ###############################
    """
    purpose: convert from Celsius to Fahrenheit or vice versa
    expects: a string with either an ending.lower() of "f" or "c" to declare what to return
    returns: rounded(converted_temp)
        always returns a string with 2 places (including 0s)
    """
    temp = str(temp)
    if convert2.lower() == "f":
        # this seems counter intuitive but it tells the func that the float(temp) is currently Celcius so convert it
        temp = temp + "c"
    if convert2.lower() == "c":
        # this seems counter intuitive but it tells the func that the float(temp) is currently Fahrenheit so convert it
        temp = temp + "f"
    if temp.lower().endswith("f"):
        # convert to Celcius
        temp = float(temp[:-1])
        temp_C = (temp - 32) / 1.8
        converted_temp = temp_C
        temp_C = round(float(converted_temp), 2)
        return(f"{converted_temp:.2f}")
    if temp.lower().endswith("c"):
        # convert to Fahrenheit
        temp = float(temp[:-1])
        temp_F = (temp * 1.8) + 32
        converted_temp = temp_F
        converted_temp = round(float(converted_temp), 2)
        return(f"{converted_temp:.2f}")
    else:
        dbug("temp must end with [CcFf] or declare ForC=[FfCc]")
        return None
    # ### EOB def convert_temp(temp, convert2="f"): ### #


# #############################################
def do_logo(content="", *args, hchr="-", prnt=True, figlet=False, center=True, shadow=False, **kwargs):
    # #########################################
    """
    purpose: presents a boxed logo for the begining of a program
    requires: nothing but you should provide some default content: str|list
    options: 
        - content: str|list, 
        - prnt: bool, 
        - figlet: bool, 
        - center: bool, 
        - shadow: bool, 
        - box_color: str, 
        - color: str, 
        - fotune: bool <-- requires the fortune app
        . quote: str   <-- requires a filename with quote lines within it - one will be randomly selected
    if content = "" and /usr/local/etc/logo.nts does not exist then we use "Your Organization Name"
    if content == "" then open default file: /usr/local/etc/logo.nts
    if content is a filename then use the lines in that file
    if content is a str and not a file then use pyfiglet to turn it into ascii letters of print lines
    """
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # dbug(center)
    # """--== Config ==--"""
    shadow = bool_val(['shadow', 'shadowed'], args, kwargs, dflt=shadow)
    quote = kvarg_val('quote', kwargs, dflt="")
    fortune = bool_val('fortune', args, kwargs)
    color = kvarg_val('color', kwargs)
    box_color = kvarg_val(['box_color', 'box_clr'], kwargs)
    prnt = bool_val('prnt', args, kwargs, dflt=True)
    title = kvarg_val('title', kwargs, dflt="")
    footer = kvarg_val('footer', kwargs, dflt="")
    figlet = bool_val('figlet', args, kwargs, dflt=figlet)
    # """--== Convert ==--"""
    if "\n" in content:
        content = content.split('\n')
    if isinstance(content, list):
        lines = content
    else:
        lines = [content]
    # dbug(lines)
    if isinstance(content, str) and content == "":
        filename = "/usr/local/etc/logo.nts"
        if file_exists(filename):
            with open(filename) as f:
                lines = [line.rstrip() for line in f]
        else:
            lines = ["Your Organization Name", dtime]
    else:
        if isinstance(content, str) and file_exists(content):
            with open(content) as f:
                lines = [line.rstrip() for line in f]
        else:
            # dbug(lines)
            if figlet:
                # dbug("found pyfiglet")
                from pyfiglet import figlet_format
                lines = figlet_format(content, width=1000)
            # else:
            #     lines.append(content)
    if len(lines) < 1:
        dbug(f"Problem: nothing to print lines: {lines}")
    if isinstance(lines, str):
        lines = lines.split("\n")
    # """--== Process ==--"""
    lines = printit(lines, 'boxed', box_color=box_color, title=title, footer=footer, color=color, shadow=shadow, prnt=False)
    if fortune:
        cmd = "fortune -s"
        out = run_cmd(cmd)
        if isempty(out):
            out = f"Nothing returned fron cmd: {cmd}... please check."
        f_box = printit(out, "boxed", title=" Fortune ", prnt=False, box_color=box_color, color=color, shadow=shadow)
    if quote != "":
        # quote needs to be a path/filename -- path can include "~/" for $HOME
        if isinstance(quote, str):
            file = os.path.expanduser(quote)
        else:
            dbug(f"quote: {quote} must be a valid filename: str containing quote lines", 'centered')
            return None
        quote_msg = get_random_line(file)
        quote_msg = wrapit(quote_msg, length=80)
        if isempty(quote_msg):
            quote_msg = f"Nothing returned from quote: {quote}"
        q_box = printit(quote_msg, 'boxed', title=" Quote ", prnt=False, shadow=shadow, box_color=box_color, color=color)
    if quote or fortune:
        lines.append("   ")
    if quote and fortune:
        columns = [f_box, q_box]
        boxes_l = gcolumnize(columns, color=color)  # color affects the 'fill color'
        boxes = boxed(boxes_l, box_color=box_color, color=color, shadow=shadow, top_pad=1, bottom_pad=1)
        # dbug(lines)
        # printit(boxes)
        # dbug('ask')
        lines.extend(boxes)
    else:
        if fortune:
            lines.extend(f_box)
        if quote:
            lines.extend(q_box)
    if prnt:
        printit(lines, center=center)
    return lines
    # ### EOB def do_logo(content="", *args, hchr="-", prnt=True, figlet=False, center=True, box=True, shadow=False, color='red', **kwargs): ### #


def do_logo_demo():
    """
    purpose: demo of using do_logo()
    returns: None
    """
    file = "~/data/lines.dat"
    quote = askYN("Do you want to include a quote from file: {file} <-- must exist ", "n", 'centered')
    fortune = askYN("Do you want to include a  fortune from the script fortune <-- must be installed ", "n", 'centered')
    if quote:
        do_logo("Do Logo Demo", color="White! on rgb(20,20,50)", box_color="red!", fortune=fortune, quote=file)  # , rgb(20,20,50)")
    else:
        do_logo("Do Logo Demo", 'figlet', color="White! on rgb(20,20,50)", box_color="red!", fortune=fortune)  # , rgb(20,20,50)")
    # dbug("EOB do_logo_demo", 'ask')


# #########
def cls():
    # #####
    """
    purpose: Clears the terminal screen.
    returns: None
    """
    import platform
    # Clear command as function of OS
    command = "-cls" if platform.system().lower() == "windows" else "clear"
    # Action
    os.system(command)
    # print(ansi.clear_screen()) # this works but puts it at the same cursor position
    # location


# # #######################
# def sudoit(user='root'):
#     # ##################
#     """
#     user='root'
#     forces this app to run as root
#     this should be right at the top of the script
#     keep in mind that the PYTHONPATH will be root's (probably empty)
#     so you may have to sys.path.append() before importing needed personal modules
#     eg
#         sys.path.append('/home/geoffm/dev/python/gmodules')
#     This function is like my (gwm) bash chkID function
#     aka force_super
#     """
#     import subprocess
#     import shlex
#     import getpass
#     current_user = getpass.getuser()
#     # dbug(user)
#     if current_user != user:
#         # sys.path.append('/home/geoffm/dev/python/gmodules')
#         # print(f"Running this app as {user} using sudo...")
#         cmd = "sudo --preserve-env=HOME,PYTHONPATH -u " + user + " " + " ".join(sys.argv)
#         subprocess.call(shlex.split(cmd))
#         sys.exit()
#     # print("This script was called by: " + current_user)
#     return


# ########################
def askYN(msg="Continue", *args, dflt="y", auto=False, **kwargs):
    # ####################
    """
    purpose: using msg as a prompt, this will ask for a simple Yes or No response and return a bool
        Typically used with an "if " statement but can simply be used as: askYN()
    options:
        - centered: bool
        - boxed: bool          # puts only the prompt in a box with a reply prompt centered under it
        - timeout: int=0: int  # how long to wait in seconds
        - auto: bool
        - exit: bool
        - quit: bool           # if response is in  ("q". "Q") an sys.exit() is executed
        - dflt: str="y"        # the default is "y"
        - auto: bool           #  var can be used to automatically invoke the default
        - shift: int           # will shift prompt left (neg) or right (pos)
    returns: bool  # True or False
    useage: 
        askYN()
         Continue [y]: True
    or
    if askYN("Do you want to save this file?", "n"):
        do_save_file()
    """
    # """--== Debugging ==--"""
    # dbug(f"funcname(): {funcname}")
    # dbug(f"msg: {msg}")
    # dbug(f"args: {args}")
    # dbug(f"kwargs: {kwargs}")
    # """--== Config ==--"""
    dflt = kvarg_val(["default", "dflt"], kwargs, dflt=dflt)
    if len(args) > 0:
        if args[0] in ["n", "N", "Y", "y"]:
            dflt = args[0]
    color = kvarg_val(['color', 'clr'], kwargs, kwargs, dflt="")
    center_b = bool_val(['center', 'centered'], args, kwargs, dflt=False)
    shadow_b = bool_val(['shadow', 'shadowed'], args, kwargs, dflt=False)
    boxed_b = bool_val(['box', 'boxed'], args, kwargs, dflt=False)
    # dbug(center)
    auto = True if 'auto' in args else auto
    # dbug(auto)
    quit_b = kvarg_val('quit', kwargs)
    exit_b = kvarg_val('exit', kwargs, dflt=False)
    timeout = kvarg_val("timeout", kwargs, dflt=0)
    # dbug(timeout)
    shift = kvarg_val(["shift"], kwargs, dflt=10)  # dflt is arbitrary
    # """--== Init ==--"""
    shift = int(shift)
    # """--== Validate ==--"""
    if not isinstance(timeout, int):
        timeout = 0
    # """--== Process ==--"""
    # dbug(repr(msg))
    # dbug(RESET)
    if dflt.upper() == "Y" or dflt.upper() == "YES":
        dflt_msg = " [Y]/n "
    else:
        dflt_msg = " y/[N] "
    if center_b:
        # dbug(msg)
        # dbug(center)
        # dbug(auto)
        if auto:
            ans = dflt
            # dbug(f"setting ans: {ans}")
        else:
            # dbug(RESET)
            # prompt = RESET + msg + dflt_msg  # <--- this is just weird how it acts... sometimes prints out \x1b[0
            prompt = msg + dflt_msg
            # dbug(prompt)
            if boxed_b:
                printit(prompt, 'centered', 'boxed')
                ans = cinput(dflt_msg + " -> ", shift=-shift)
            else:
                # dbug(repr(prompt))
                ans = cinput(prompt)
    else:
        # dbug(msg)
        if auto:
            ans = dflt
            # dbug(f"setting ans: {ans}")
        else:
            # ddbug(f"timeout: {timeout}", 'ask')
            if timeout > 0:
                from threading import Timer
                t = Timer(timeout, print, ['Sorry, time is up... '])
                t.start()
                ans = input(msg + dflt_msg)
                t.cancel()
            else:
                if isinstance(msg, list):
                    msg = "".join(msg)
                if isinstance(dflt_msg, list):
                    dflt_msg = "".join(dflt_msg)
                # dbug(RESET)
                prompt = RESET + msg + dflt_msg
                # dbug(prompt)
                if boxed_b:
                    # dbug(prompt)
                    ans = input(boxed(prompt))
                else:
                    # dbug(prompt)
                    ans = input(prompt)
    if ans.upper() == "":
        ans = dflt
    if msg != "":
        # dbug(msg)
        if msg == "Continue" and ans.lower() == "n":
            printit("Exiting at user request...")
            sys.exit()
        if quit_b or exit_b:
            # if quit is true and user hits 'q' then exit out as requested
            printit("Exiting as requested", shadow=shadow_b, center=center_b, box_color="red on black", color=color)
            if ans.lower() in ('q', 'quit'):
                sys.exit()
        if ans.upper() == "Y":
            return True
    return False
    # ### EOB def askYN(msg="Continue", dflt="y", *args, center=False, auto=False, timeout=0):  ### #


def askYN_demo(*args, **kwargs):
    """
    purpose: demo of using askYN() function
    returns: None
    """
    new_line = "This is a sample new line..."
    dbug(f"new_line: {new_line}", 'centered')
    if askYN("Do you want to add this new_line: ", 'y', 'centered'):
        printit(f"Here we would call a function to add the new line: {new_line}", 'boxed', 'centered', box_color="yellow!")
    if not askYN("(centered and boxed) Do you want to continue", 'centered', 'boxed'):
        printit("User does not want to continue... we would have responded appropriately...", 'centered')
        return
    dbug("Testing dbug with ask and centered", 'ask', 'centered')
    rtrn = askYN("Test of using askYN() ", 'centered')
    print(f"The result was: {rtrn}")
    print("Using just 'Continue' as the msg will allow sys.exit when it is not a 'y' or 'Y'")
    printit("This next one is perhaps useful for developing creating a forced breakpoint... it is just 'askYN()' with no arguments anything but 'Y' will exit", 'centered', 'boxed')
    askYN()
    if askYN("Here I am asking if you like birds", 'centered', 'boxed'):
        printit("You like birds...", 'centered')
    else:
        printit("You do not like birds...", 'centered')
    return None


def get_dtime_format(s_date):  # date_fmt
    """
    purpose: returns the format of a date-time stamp string
        useful for date series in dataframes
    options: none
    returns date patters in strftime format
    """
    if isinstance(s_date, float):
        s_date = int(s_date)
    if isinstance(s_date, int):
        s_date = str(s_date)
    # in case it is still numpy int or whatever...
    add_this = ""
    if str(s_date).endswith(","):
        add_this = ","
        s_date = s_date.strip(",")
    s_date = str(s_date)
    date_patterns = ["%Y%m%d", "%d-%m-%Y", "%Y-%m-%d", "%Y%m%d-%H%M", "%Y-%m-%d %H:%M", "%Y%m%d-%H:%M", "%Y-%m-%d %H:%M:%S"]
    for pattern in date_patterns:
        try:
            # r = datetime.strptime(s_date, pattern).date()
            # dbug(f"r: {r} pattern: {pattern}")
            return pattern + add_this
        except Exception as Error:
            dbug(f"pattern: {pattern}\nFailed against\ns_date: {s_date} Error: {Error}")
    # if we got here something went wrong...
    dbug(f"Date: [{s_date}] is not in expected format. Searched date_patterns: {date_patterns}")
    return None
    # ### EOB def get_dtime_format(s_date): ### #

# alias
# get_date_format = dtfmt


# ########################
def cat_file(fname, *args, prnt=False, lst=False, **kwargs):
    # ####################
    """
    purpose: reads a file and return lines or rows_lol (list of list) or as a df (dataframe)
    options:
    -    prnt: bool,  # prints out the file contents
    -    lst: bool,   # returns a list of lines or you could use: txt.split('\n') to make it a list
    -    csv: bool,   # treat the file as a csv (or for me, a dat file)
    -    dat: bool,   # this one will seem strange, it treats the first line as a commented out header line
    -    xlsx: bool,  # returns df of a spreadsheet file
    -    hdr: bool,   # whether to include header line or header data in the return
    -    df: bool,    # return a df
    -    delimiter: str # delimiter to use for a csv, or dat file
    -    rtrn: str, (can be "str", "string", "lst", "list", "df"
    -    nums: bool   # forces all numbers to be returned as floats instead of str - useful for plotting
    -    index: bool  # adds id numbers to csv data
    -    purify: bool # default=True - strips off all comments (except first line on a ".dat" file)
    returns the text of a file as a str or rows_lol (if it is a cvs: bool file) or returns a df if requested
    Note: if the result df has the header/colnames repeated in row[0] then make sure you included 'hdr' or hdr=True
    #>>> t = cat_file("/etc/timezone")
    #>>> print(t)
    America/New_York
    <BLANKLINE>
    """
    # """--== debugging ==--"""
    # dbug(funcname())
    # dbug(fname)
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    csv_b = bool_val(['csv', 'csv_file', 'csvfile'], args, kwargs, dflt=False)
    dat_b = bool_val(['dat', 'datfile', 'dat_file'], args, kwargs, dflt=False)
    lst = bool_val(['lst', 'list', 'lol'], args, kwargs, dflt=lst)
    xlsx = bool_val('xlsx', args, kwargs, dflt=False)
    prnt = bool_val('prnt', args, kwargs, dflt=prnt)
    # hdr_b = bool_val('hdr', args, kwargs, dflt=False)
    # dbug(hdr_b)
    df_b = bool_val('df', args, kwargs, dflt=False)  # rtrn as df?
    # dbug(df_b)
    rtrn = kvarg_val('rtrn', kwargs, dflt='')  # rtrn value is  df or str  same as above, just another way to do it
    purify_b = bool_val(['purify', 'decomment', 'pure', 'uncomment'], args, kwargs, dflt=True)
    # dbug(purify_b)
    nums_b = bool_val(["nums", "numbers", 'num', 'number'], args, kwargs, dflt=False)
    delimiter = kvarg_val(["delim", "delimiter"], kwargs, dflt=",")
    index_b = bool_val(["index", "indexes", "idx", "indx"], args, kwargs, dflt=False)
    # dbug(index_b)
    # dbug(nums_b)
    # dbug(f"fname: {fname} csv: {csv} df_b: {df_b} hdr_b: {hdr_b} rtrn: {rtrn} purify_b: {purify_b}")
    # """--== Local Functions ==--"""
    # this is only here to show an example of using yield in this (or similar) process
    # def decomment(csvfile):
    #     # purify
    #     for row in csvfile:
    #         raw = row.split('#')[0].strip()
    #         if raw:
    #             yield raw
    # """--== Validation ==--"""
    if isempty(fname):
        dbug(f"fname: {fname} appears to be empty... returning")
        return
    # """ Process  """
    # dbug(fname)
    fname = os.path.expanduser(fname)
    if not file_exists(fname):
        dbug(f"Ooops... fname: {fname} not found... returning None ...")
        return
    # dbug(f"fname: {fname} rtrn: {rtrn}")
    # if (csv_b or fname.endswith(".csv") or fname.endswith(".dat")) and rtrn not in ("str", "string") or dat_b:
    # dbug(df_b)
    if (csv_b or fname.endswith(".csv") and rtrn not in ("str", "string")) or dat_b or df_b:
        # dbug(df_b)
        # dbug(csv_b)
        # dbug(dat_b)
        # if it is a csv or ".dat" file return rows_lol (list of lists) unless df_b
        lines = []
        rows_lol = []
        lines = purify(fname, dat=dat_b, purify=purify_b)
        # dbug(lines[:3])
        if len(lines) > 0:
            rows_lol = get_elems(lines, delimiter=delimiter)
        # """--== fix numbers ==--"""
        new_rows = []
        # dbug(rows_lol[:3])
        for row in rows_lol:
            new_row = []
            for num, elem in enumerate(row):
                elem = elem.strip()
                if num == 0:
                    new_row.append(elem)
                else:
                    # dbug(f"elem: {elem}")
                    tmp_elem = elem.replace(",", "")  # if the "number has commas eg: 1,024 - remove them"
                    if isnumber(tmp_elem, 'float') and nums_b:
                        # dbug(f"Converting elem: {tmp_elem} to float", 'ask')
                        new_row.append(float(tmp_elem))
                    else:
                        new_row.append(elem)
                # if "AVGO" in new_row:  # debugging
                    # dbug(new_row)
            new_rows.append(new_row)
        rows_lol = new_rows
        # dbug(rows_lol[:2])
        # """--== if rtrn df ==--"""
        # dbug(df_b)
        if rtrn == "df" or df_b:
            # dbug(rows_lol[:2])
            df = pd.DataFrame(rows_lol)
            if index_b:
                df = df.reset_index()
                # dbug(df.head())
                # dbug(df.index.name)
            # dbug(f"Returning df: {df[:2]}")
            # df.columns = df.iloc[0]
            # df = df[1:]
            df = df.rename(columns=df.iloc[0]).drop(df.index[0])
            df = df.set_index(list(df)[0])
            # dbug(f"Returning df: {df[:2]}", 'ask')
            return df
        else:
            # dbug("do not return a df")
            if index_b:
                dbug(rows_lol[:4])
                if dat_b:
                    rows_lol = [[n] + row for n, row in enumerate(rows_lol, start=0)]
                    rows_lol[0][0] = 'id'
                    # row1_l.insert(0, 'id')
                    # dbug(new_lol)
                    # # rows_lol = [[n] + row for n, row in enumerate(rows_lol[1:], start=1)]
                    # new_lol.extend([[n] + row for n, row in enumerate(rows_lol, start=1)])
                    # rows_lol = new_lol
                else:
                    rows_lol = [[n] + row for n, row in enumerate(rows_lol, start=1)]
                dbug(rows_lol[:4])
            # dbug("Returning rows_lol[:2: {roes_lol[:2]}", 'ask')
            return rows_lol
    if xlsx:
        df = pd.read_excel(fname)
        # dbug(f"Returning df[:2]: {df[:2]}")
        return df
    # """--== treat this as just a text file ==--"""
    with open(fname, "r") as file:
        text = file.read()
    if prnt:
        print(f" ---- cat_file({fname}) ---- ")
        printit(text)
        print(f" ---- end cat_file({fname}) ---- ")
    if lst:
        # dbug(f"text): [{text}]")
        text_l = text.splitlines()
        # dbug(f"Returning text_l: {text_l}", 'ask')
        return text_l
    # dbug(f"Returning text: {text}", 'ask')
    return text
    # ### EOB def cat_file(fname, *args, prnt=False, lst=False, **kwargs): ### #


# ###############################
def file_exists(file, type="file", *args, **kwargs):
    # ###########################
    """
    purpose: returns bool if the file (or directory - see options) exists or is it executable
    options:
        type: str  # Note: type can be "file" or "dir" (if it isn't file the assumption is dir)
                    if type == "x" or "X" then the return bool will depend on if the file is executable
    returns: bool
    usage:
        file_exists('/etc/hosts')
        True
    """
    if type == "file":
        try:
            os.path.isfile(file)
        except Exception as e:
            print("Exception: " + str(e))
            return False
        return os.path.isfile(file)
    if type in ('X', 'x', 'executable'):
        try:
            os.path.isfile(file)  # , X_OK)
        except Exception as e:
            print("Exception: " + str(e))
            return False
    if type == 'dir':
        # check file or dir
        return os.path.exists(file)
    # to move a file use: os.rename(source, target)
    # or shutil.move(source, target)
    return True


# # #####################
# def do_list(lst, *args, mode="", prnt=True, center=False, title="", **kwargs):
#     # ##############o#
#     """
#     purpose: quick-n-dirty display of a list in a gtable
#     # >>> lst = ['one','two','three']
#     # >>> do_list(lst, "nc")
#     # ===========
#     # || one   ||
#     # || two   ||
#     # || three ||
#     # ===========
#     """
#     # """--== Config ==--"""
#     prnt = bool_val(['prnt', 'show'], args, kwargs, dflt=prnt)
#     center = bool_val(['centered', 'center'], args, kwargs, dflt=prnt)
#     title = kvarg_val('title', kwargs, dflt=title)
#     # footer = kvarg_val('footer', kwargs, dflt=title)
#     # """--== SEP_LINE ==--"""
#     if mode == "v":
#         lst_d = {}
#         for n, elem in enumerate(lst):
#             lst_d[n] = elem
#         lst = lst_d
#     lines = gtable([lst], prnt=prnt, centered=center)
#     return lines


# ####################
def purify(content, *args, **kwargs):
    # ################
    """
    purpose: de-comments a file, aka removes all comments denoted by "#" ...
    input: 
        content: list | filename | str   # content can be a line (string), a list of lines (strings), of a filename
    options:
        - dat_b: bool   # converts first (commented line) into a non-commented line rather than eliminating it as a comment
    return lines: list (de-commented lines/purified)
    """
    # DONE make this simply purify() and accept, filename, lines: list, or line: str for "purifying" (decommenting)
    # """--== Config ==--"""
    dat_b = bool_val(["dat", "dat_file", "datfile"], args, kwargs, dflt=False)
    purify_b = bool_val(["purify", "purify_b", "decomment"], args, kwargs, dflt=True)  # this might seem strange but there is an occasion
                                                                                       # where I need for this to NOT strip comments (except first line of a '.dat' file)
                                                                                       # This is not defined int the function doc above because it is probably never needed
    # this dat_b option is primarily for me (the author) - I have legacy ".dat" files that have a commented first line which has column names for a csv type file
    # this dat_b option will preserve that first line but decomment it - it is not listed above because it simply for me
    """--== function(s) ==--"""
    def purify_line(line):
        # purified_line = line.split('#')[0].strip()  # TODO make this an re.split(r'(?<!\\)#', str)
        line = line.strip()
        purified_line = re.split(r'(?<!\\)#', line)[0]  # TODO make this an re.split(r'(?<!\\)#', str)
        return purified_line
    # """--== Process ==--"""
    purified_lines = []
    if isinstance(content, str):
        file = content  # renamed just for clarity
        if file_exists(file):
            with open(file, "r") as myfile:
                for num, line in enumerate(myfile):
                    # dbug(f"processing line: {line}")
                    if num == 0 and dat_b:
                        if line.startswith("#"):
                            # remove the '^#\s'  but leave the line
                            # dbug(line)
                            line = re.sub(r"^#\s", "", line)
                            # dbug(line)
                        purified_lines.append(line)
                        line = line.rstrip('\n')
                        continue
                    line = line.rstrip('\n')
                    # if num == 0:
                    #     line = line.lstrip("#")
                    if purify_b:  # this default is to purify but in the case of gtable data(lol) this may be False
                        purified_line = purify_line(line)
                    else:
                        # dbug(line)
                        purified_line = line
                    # dbug(purified_line)
                    if purified_line.isspace() or purified_line == '':
                        # skip a blank line - this is part of purify # TODO, ??? make this an option???
                        continue
                    purified_lines.append(purified_line)
        else:
            # assuming this is a simple string or line
            line = purify_line(content)
    # dbug(purify_b)
    # dbug(purified_lines[:3])
    if isinstance(content, list):
        for line in content:
            if purify_b:
                purified_lines.append(purified_line(line))
            else:
                purified_lines.append(line)
    return purified_lines
    # ### EOB def purify() ### #


# alias purify
purify_file = purify


# # ####################
# def purify_line(line):
#     # ################
#     """
#     purpose: strips off and comments from a line
#     returns: line
#     """
#     line = str(line).rstrip('\n')
#     m = re.match(r'^([^#]*)#(.*)$', line)
#     # note: m.group(0) is the orig line
#     if m:  # The line contains a hash ie comment
#         stripped_line = m.group(1)
#         # note: m.group(2) is the comment
#         return stripped_line.strip()
#     else:
#         return line.strip()


# # #######################
# def pretty_array(array):
#     # ##################
#     """
#     prints out nested arrays into readable format using yaml
#     """
#     import yaml
#     print(yaml.dump(array, default_flow_style=False))


# ###################################
def ireplace(s, indices=[], char="|"):
    # ###############################
    """
    purpose: index replace
    To get indices use eg:
        iter = re.finditer(rf"{c}", s)
        indices = [m.start(0) for m in iter]
        # next line removes first two and last two indices - just an example
        indices = indices[2:-2]
    then use this func with:
        s: is the string to do the replacements
        indices: list of indexed positions
        char: is the char to replace with
    """
    # if replace != "":
    #     iter = re.finditer(rf"\{replace}", s)
    #     indices = [m.start(0) for m in iter]
    s_l = list(s)
    # dbug(f"indices: {indices} chr: {chr} len(s): {len(s)} s: {s}")
    if len(indices) > 0:
        # dbug(len(s_l))
        for i in indices:
            # dbug(f"i: {i}")
            # dbug(s_l[i])
            s_l[i] = char
        s = "".join(s_l)
    return s


# ########################################
def first_matched_line(filename, pattern, upto=1):
    # ####################################
    """
    purpose: return: just the first matched line(s) from a filename using pattern
    required:
        - filename: str
        - pattern: str
    options:
        - upto: int default=1  # How many matching lines to return
    returns: matching lines
    """
    # """--== SEP_LINE ==--"""
    # dbug(funcname())
    # dbug(filename)
    # dbug(pattern)
    # """--== SEP_LINE ==--"""
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    matched_l = []
    line_n = 1
    for line in lines:
        # dbug(f"Processing line: {line_n} of {len(lines)}")
        r = re.match(pattern, line)
        if r:
            matched_l.append(line.rstrip("\n"))
            if len(matched_l) >= upto:
                return matched_l
        line_n += 1
    return matched_l
    # ### EOB def first_matched_line(filename, pattern, upto=1): ### #


# # ###################################
# def pp_d(d, between=" ", kv_s=": "):
#     # ###############################
#     """
#     purpose: pretty print a dictionary
#     deprecated as gtable does this
#     with between (str) placed between elems
#     and kv_s (str) between k and v
#     >>> d = {"one": 1, "two": 2, "three": 3}
#     >>> print(pp_d(d))
#     one: 1  two: 2  three: 3
#     """
#     dbug("Who uses this? ")
#     s = between.join([f'{k}{kv_s}{v}' for (k, v) in d.items()])
#     return s


# ######################################
def x_items(my_d, x=2, *args, **kwargs):
    # ##################################
    """
    purpose: returns a limited number of dictionary items - primarily used for development (debugging)
    options:
        -x: int     # default=2 number of items (pairs of key/value) to return 
    returns: dict
    """
    # TODO this needs a better name
    return {k: my_d[k] for k in list(my_d)[:x]}


# ###########################################
def kv_cols(my_d, cols=3, *args, **kwargs):
    # #######################################
    """
    input: my_d: dict cols:default=3 <-- both args ie: dict and cols are required!
    options:
        - title, header, pad, box_style, box_color: str, color: str, neg: bool,
        - prnt: bool,  footer,title: str, rjust_cols: list, sep,pad: str, max_col_width: int,
        - centered: bool, box_style: str, human: bool, rnd: bool, box_title: bool (requires title), sep: str
        - hdr: bool default=True
        - no_hdr: bool        # removes hdr/colnames from tables
        - box_color: str      # affects all "internal" (columnized) boxes
        - boxed: bool         # if true a master box is created surrounding the internal/columnized boxes
        - mstr_box_clr: str   # master box color
    returns: lines tabalized key-value pairs
    """
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # dbug(cols)
    # dbug(my_d)
    # """--== Config ==--"""
    cols = kvarg_val("cols", kwargs, dflt=cols)
    title = kvarg_val("title", kwargs, dflt="")
    # dbug(title)
    # footer = kvarg_val("footer", kwargs, dflt=funcname() + "()")
    footer = kvarg_val("footer", kwargs, dflt="")
    header_b = bool_val(['header', 'hdr'], args, kwargs, dflt=True)
    nohdr_b = bool_val(['no_header', 'nohdr', "no_hdr"], args, kwargs, dflt=False)
    # dbug(header_b)
    # pad = kvarg_val("pad", kwargs, dflt=2)
    box_style = kvarg_val("box_style", kwargs, dflt="single")
    box_color = kvarg_val(["box_color", "box_clr"], kwargs, dflt="")
    mstr_box_color = kvarg_val(["mstr_box_color", "mstr_box_clr", 'main_box_color', 'main_box_clr', "mstrclr", 'mstr_clr'], kwargs, dflt="")
    color = kvarg_val(["color"], kwargs)
    neg = bool_val("neg", args, kwargs, dflt=False)
    prnt = bool_val(["prnt", "print"], args, kwargs, dflt=False)
    boxed_b = bool_val(['box', 'boxed'], args, kwargs, dflt=False)
    center = bool_val(["centered", "center"], args, kwargs, dflt=False)
    # dbug(f"prnt: {prnt} centered: {center}", 'ask')
    sep = kvarg_val("sep", kwargs, dflt=" ")
    rjust_cols = kvarg_val(["rjust_cols", "rjust", "rjust_values", 'rjust_vals'], kwargs, dflt=[])
    box_title = bool_val(["box_title", "boxed_title", "title_boxed"], args, kwargs)
    max_width = kvarg_val(["max_col_width", "col_width", "maxwidth", "max_width", "colwidth", "max", 'col_limit', 'width'], kwargs, dflt=30)
    rnd = kvarg_val(['rnd', 'round'], kwargs, dflt="")
    human = bool_val(['h', 'human', "H"], args, kwargs, dflt=False)
    # """--== Validation ==--"""
    if my_d is None:
        dbug("Submitted dict is None... returning...")
        return None
    # dbug(my_d)
    if len(str(my_d)) == 0:
        dbug("Nothing submitted... returning...")
        return None
    if not isinstance(my_d, dict):
        dbug(f"Submission must be a dict type(my_d): {type(my_d)}... returniing...")
        return None
    # """--== Init ==--"""
    if mstr_box_color != "":
        boxed_b = True
    # RESET = sub_color('reset')
    myd_len = len(my_d)
    # dbug(myd_len)
    # dbug(x_items(my_d, 5))
    num_rows = ceil(myd_len / int(cols))
    if neg and rjust_cols == []:
        rjust_cols = [1]  # if neg numbers are to be processed then it is highly likely that the values should all be rjustified
    myd = []  # new dict for columned my_d
    lines = []
    for n in range(cols + 1):
        # dbug(n)
        myd.append({})
    # cnt = 0
    row_num = 1
    # """--== Convert list k, v elems  with proper widths ==--"""
    if isinstance(my_d, list):
        dbug(f"Input: my_d: {my_d} appears to be a list. This function: {funcname()} requires a dict.")
        return
    # TODO: clean this up, maybe sep max_width into k_width and v_width
    # dbug(max_col_width)
    # dbug(x_items(my_d, 5))
    new_d = {}
    for k, v in my_d.items():
        # dbug(f"k: {k} repr(v): {repr(v)}")
        key = escape_ansi(k)
        pat = str(key) + "(?!;)(?!m)"
        # codes = k.split(key)
        codes = re.split(pat, str(k))
        if len(codes) == 2:
            prefix_code = codes[0]
            postfix_code = codes[1]
        new_k = k
        if len(key) > max_width:
            new_k = str(key)[:max_width]
            new_k = prefix_code + new_k + postfix_code
        if isinstance(v, list):
            v = ",".join(str(v))
        val = escape_ansi(v)
        # prefix_code = postfix_code = ""
        if len(val) > 0 and len(val) < 30:
            # dbug(f"k: {k} v: {v} val: {val}")
            if val.startswith("^"):
                val = val.replace("^", "")
            if val.startswith("+"):
                val = val.replace("+", "")
            val = val.replace("?", "?")
            v = str(v).replace("^", "")
            codes = split_codes(v)
            prefix_code = codes[0]
            if len(codes) > 1:
                postfix_code = codes[1]
        else:
            v = " "
        new_v = v
        if len(val) > max_width:
            new_v = str(val)[:max_width]
            new_v = prefix_code + new_v + postfix_code
        # dbug(f"repr(k): {repr(k)}, repr(key): {repr(new_k)} repr(v): {repr(v)} repr(val): {repr(val)} repr(new_v): {repr(new_v)}")
        new_d[new_k] = new_v
    my_d = new_d
    # dbug(x_items(my_d, 5))
    # myd = new_d
    # """--== Process ==--"""
    # dbug(my_d)
    col = 0
    for k, v in my_d.items():
        # builds my_d which is a list of dicts
        # dbug(k)
        if len(str(k)) < 1:
            # skip a bogus (k)ey
            continue
        # dbug(f"col: {col} k: {k} v: {v}")
        myd[col][k] = v
        # dbug(myd)
        if row_num >= num_rows:
            row_num = 1
            col += 1
            # dbug("continuing...")
            continue
        row_num += 1
    # dbug(myd)
    # dbug(x_items(my_d, 5))
    tables = []
    col = 0
    for col in range(cols):
        if len(myd[col]) < 1:
            continue
        if len(myd[col]) < num_rows:
            diff = (num_rows) - len(myd[col])
            for n in range(diff):
                # dbug("adding a new ... row")
                myd[col]["." * (n + 1)] = "..."
        # dbug(f"myd[{col}]: {myd[col]}")
        # dbug(header_b)
        # dbug(rnd)
        DEBUG = False
        # DEBUG = True  # debugging only
        table = gtable(
            myd[col],
            prnt=DEBUG,
            header=header_b,
            no_hdr=nohdr_b,
            box_style=box_style,
            neg=neg,
            rnd=rnd,
            col_limit=max_width,
            human=human,
            box_color=box_color,
            color=color,
            rjust_cols=rjust_cols,)
        tables.append(table)
    columns_l = gcolumnize(tables, sep=sep)
    width = nclen(columns_l[0])
    if title != "" and not boxed_b:
        # dbug(width)
        if box_title:
            # titlebox = boxed(title, box_color=box_color, color=color, width=width)
            titlebox = boxed(title, box_color=box_color, color=color)
            lines = titlebox 
            # lines = centered(titlebox, width=width, box_color=box_color, color=color)
        else:
            gline_title = gline(width, msg=title, just='center')
            lines.insert(0, gline_title)
    lines.extend(columns_l)
    if footer != "" and not boxed_b:
        # dbug(footer)
        # dbug(width)
        line = gline(width, msg=footer, just='center')
        lines.append(line)
    if boxed_b:
        lines = boxed(lines, title=title, footer=footer, box_color=mstr_box_color)
    if center:
        lines = centered(lines)
    if prnt:
        printit(lines)
    return lines
    # ### EOB def kv_cols(my_d, cols=3, *args, **kvargs): ### #


def kv_cols_demo(*args, **kwargs):
    """
    purpose: demo of using kv_cols()
    returns: None
    """
    large_d = {}
    for x in range(30):
        v = (x * 1000) / 3
        large_d[f'key_{x}'] = f'{v}'
    cols = 2
    x = 6
    small_d = x_items(large_d, x)
    kv_cols(small_d, cols, prnt=True)
    dbug('ask')
    kv_cols(large_d, cols, 'prnt', title=f"{funcname()} Demo: {cols} no header ", footer=dbug('here'))
    dbug('ask')
    kv_cols(large_d, cols, 'prnt', title=f"{funcname()} Demo: {cols} no header rnd=2", footer=dbug('here'), rnd=2)
    kv_cols(large_d, cols, 'prnt', title=f"{funcname()} Demo: {cols} no header rnd=2 and human=True", footer=dbug('here'), rnd=2, human=True)
    dbug('ask')
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'hdr', title=f"{funcname()} Demo: {cols} w/header ", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'centered', title=f"{funcname()} Demo: {cols} centered", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'hdr', 'centered', title=f"{funcname()} Demo: {cols} w/header and centered ", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'centered', 'boxed', title=f"{funcname()} Demo: {cols} no header cntered and boxed ", mstr_box_clr="red! on black", footer=dbug('here'))
    cols += 1
    print()
    kv_cols(large_d, cols, 'prnt', 'hdr', 'centered', 'boxed', title=f"{funcname()} Demo: {cols} w/header cntered and boxed ", mstr_box_clr="yellow! on black", footer=dbug('here'))


def rowscols_cols(lol, cols, *args, **kwargs):
    """
    purpose: this takes a longish lol - namely, rows of columns and allows
        you to split those rows into X columns. This is most likely used to split
        up rows of columns for gtables so an option include colnames to add to the
        top of each new column of rows cols:
        This is an experiment but I think it could be useful
    Here is a simple visual
    row_of_cols
    +------+-----+----+
    |      |     |    |
    +------+-----+----+
    |      |     |    |
    +------+-----+----+
    |      |     |    |
    +------+-----+----+
    |      |     |    |
    +------+-----+----+
    |      |     |    |
    +------+-----+----+
    |      |     |    |
    +------+-----+----+
    |      |     |    |
    +------+-----+----+
   split_tables = rowscols_cols(row_of_cols, 2)
    +------+-----+----+ +------+-----+----+
    |      |     |    | |      |     |    |
    +------+-----+----+ +------+-----+----+
    |      |     |    | |      |     |    |
    +------+-----+----+ +------+-----+----+
    |      |     |    | |      |     |    |
    +------+-----+----+ +------+-----+----+
    |      |     |    |
    +------+-----+----+
    TODO? - having seconds thoughts that this should be part of gtables...
    """
    import math
    colnames = ["IP", "Hostname", "Status", "Ports"]
    rows_len = len(lol)
    dbug(rows_len)
    half = math.ceil(rows_len / cols)
    dbug(half)
    chunks = chunkit(lol, half)
    dbug(len(chunks))
    boxes = []
    for chunk in chunks:
        box = gtable(chunk, 'hdr', colnames=colnames)
        boxes.append(box)
        printit(box)
    dbug(len(boxes))
    col_blocks = gcolumnize(boxes)
    return(col_blocks)
    # ### EOB def rowscols_cols(lol, cols, *args, **kwargs): ### #


# #################################
def key_swap(orig_key, new_key, d):
    # #############################
    """
    purpose: switch or change the keyname (a single key)  on an element in a dictionary
    args:
        orig_key  # original key name
        new_keyA  # new key name
        d         # dictionay to change
    returns: the altered dictionary
    """
    # dbug(f"orig_key: {orig_key} new_key: {new_key}")
    d[new_key] = d.pop(orig_key)
    return d
    # END def keys_swap(orig_key, new_key, d):


# ########################################################
def gcolumnize(msg_l, *args, **kwargs):
    # ####################################################
    """
    purpose: This will columnize (vertically) a list or a list of blocks or strings
    input: msg_l: list|lol
    options:
        - width|length=0: int              # max width or use cols below
        - cols: int                        # number of desired columns
        - sep|sep_chrs|sepchrs=' | ': str  # string or character to use between columns
        - prnt|print|show = False: bool
        - boxed: bool                      # box the output
        - box_color: str                   # color to use for box border
        - centered = False: bool  # only invoked if prnt == True
        - title = "": str   # only invoked if prnt == True
        - color: str
        - footer = "": str  # only invoked if prnt == True
        - positions: list   # list of either triplets or lists with 3 values, (row, col, position)
                --- position can easily be declared as 1-9 -> see gblock().__doc__
    returns: lines: list # suitable for printit()
    notes:
    - handles simple lists or a list of blocks/boxes (a list of lines)
    - If it is a list of lists (like several boxes made up of lines ) then
    it will list them next to each other
    Further is it is a list or rows with a list of boxes for each row then this will try to accomodate
    eg
    box1 = +------+
           | box1 |
           +------+
    box2 = +------+
           | box2 |
           +------+
    boxes = box1 + box2
    lines = gcolumnize(boxes)
    printit(lines)
        +------+  +------+
        | box1 |  | box2 |
        +------+  +------+
              or
    box1 = +------+
           | box1 |
           +------+
    box2 = +------+
           | box2 |
           | box2 |
           +------+
    box3 = +----------------+
           | box3 box3 box3 |
           +----------------+
    box4 = +------+
           | box4 |
           | box4 |
           | box4 |
           | box4 |
           +------+
    row1 = [box1, box2]
    row2 = [box3, box4]
    lines = gcolumnize([row1, row2]
    printit(lines)
      or
    mylist = ["One potato", "Two potato", "Three potato", "Four", "Now close the door"]
    lines = gcolumnize(mylist, width=40)
    printit(lines)
    One potato    Four
    Two potato    Now close the door
    Three potato
    """
    """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(msg_l)
    # dbug(args)
    # dbug(kwargs)
    # for box in msg_l:
    #     printit(box)
    nlvl = nestlvl(msg_l)
    # dbug(nlvl)
    # """--== Config ==--"""
    pad = kvarg_val("pad", kwargs, dflt=" ")
    sep_chrs = kvarg_val(['sep', 'sepchr', 'sepchrs', 'sep_chr', 'sep_chrs'], kwargs, dflt=" ")
    # dbug(sep_chrs)
    cntr_cols = kvarg_val(["cntr_cols", "center_cols", "cols_cntr", "cols_center"], kwargs, dflt=[])
    # my_lol = msg_l
    prnt = bool_val(['prnt', 'print', 'show'], args, kwargs, dflt=False)
    boxed_b = bool_val(['boxed', 'box'], args, kwargs, dflt=False)
    # dbug(boxed_b)
    # boxed = boxed_b
    # dbug(boxed)
    box_color = kvarg_val(['box_color', 'box_clr', 'border_color', 'border_style'], kwargs, dflt="")  # white! on grey(50)?
    color = kvarg_val(["color", "clr", "txt_clr"], kwargs, dflt="")                                   # white! ?
    centered_b = bool_val(['center', 'centered', 'cntr', 'cntrd'], args, kwargs, dflt=False)
    # dbug(centered_b)
    title = kvarg_val(['title'], kwargs, dflt="")
    footer = kvarg_val(['footer'], kwargs, dflt="")
    # aligned = bool_val(["cols", 'aligned', "evencols"], args, kwargs, dflt=False)
    width = kvarg_val(["width", "length"], kwargs, dflt=0)
    # dbug(width)
    cols = kvarg_val(["cols"], kwargs, dflt=0)  # TODO this is WIP and is only used now to stack blocks of lines when it equals 1
    # dbug(cols)
    height = kvarg_val(["height", "rows"], kwargs, dflt=0)
    positions = kvarg_val(["positions"], kwargs, dflt=[])
    # dbug(my_lol, 'ask')
    # dbug(color)
    # """--== Init ==--"""
    scr_col_len = get_columns()  # get the number of columns on the terminal screen
    if str(width).endswith("%"):
        amnt = width.rstrip("%")
        pamnt = int(amnt)/100
        width = int(int(scr_col_len) * pamnt)
    # """--== Convert ==--"""
    if all([islos(elem) for elem in msg_l]):
        # dbug(f"This is clearly a list of blocks made up with lines(strings)")
        if cols > 0:
            # rows = []
            # row = []
            # """--== SEP_LINE ==--"""
            msg_l = chunkit(msg_l, cols, 'full')
    # """--== EOB if all([islos(elem) for elem in msg_l]): ==--"""
    # if not islol(my_lol):
    if not islol(msg_l):
        # dbug("Simple list")
        # dbug(msg_l, 'lst')
        # dbug(cols)
        # lines = columned(msg_l, width=width, cols=cols, footer=dbug('here'), box_color="white! on grey50", color="white!", centered=centered)
        # dbug(width)
        # lines = columned(msg_l, width=width, cols=cols, footer=dbug('here'), box_color=box_color, color=color, centered=centered_b, sep=sep_chrs)
        lines = columned(msg_l, width=width, cols=cols, box_color=box_color, color=color, centered=centered_b, sep=sep_chrs)
        # dbug("Returning lines")
        printit(lines, prnt=prnt, boxed=boxed_b, centered=centered_b, box_color=box_color, color=color, title=title, footer=footer)
        # dbug(f"Returning lines: {lines}")
        return lines
    # """--== is this an lol of an lol ie: rows of boxes of lines ==--"""
    # dbug("This may be a list of lists of lists... ie: rows of boxes of lines so let's test for it")
    # islol = any(isinstance(elem, str) for elem in my_lol[0])  # True or False... is this a list of lists - a list of boxes
    islolol = all([islol(elem) for elem in msg_l])   # True or False... is this a list of lists within an lol
    # if above is true it is probably a list of boxes
    rows_cols_of_boxes = False
    # dbug(nlvl)
    if nlvl == 3:
        lines = []
        for row in msg_l:
            gb_row = gblock(gcolumnize(row))
            for lnum, line in enumerate(gb_row):
                lines.append(line)
                # dbug(f"lnum: {lnum} line nclen: {nclen(line)}")
        printit(lines)
        # dbug("Returning lines")
        return lines
    # """--== SEP_LINE ==--"""
    if islolol:
        for elem in msg_l:  # for box in list of boxes
            # possible a list of boxes
            for item in elem:
                # possibly a box with lines
                for each in item:
                    # test to see if it really is line strings
                    if isinstance(each, str):
                        rows_cols_of_boxes = True
        # if all([islos(elem) for elem in msg_l]):
        if rows_cols_of_boxes:
            # dbug(f"Must be an lolos msg_l: {msg_l[:10]}")
            # dbug("This is a lol within an lol - it is likely a list of boxes/blocks")
            # """--== SEP_LINE ==--"""
            # assumption here is that [mtrx] is an lol list of rows with columns for a dashboard type display
            mtrx = msg_l
            rows = len(mtrx)
            cols = len(mtrx[0])
            cols = maxof(mtrx, 'elems')
            max_col_lens = [0] * cols
            max_row_h = [0] * rows  # init max_row_h
            """--== SEP_LINE ==--"""
            mtrx = fixlol(mtrx, dflt=gblock(" "))
            pvt_mtrx = fixlol(mtrx, 'pivot')
            nlvl = nestlvl(mtrx)
            # dbug(nlvl)
            """--== SEP_LINE ==--"""
            col_boxes = []
            num_rows = rows - 1
            num_cols = cols - 1
            # dbug("Lets begin...")
            for col_num, col in enumerate(pvt_mtrx):
                pvt_nlvl = nestlvl(pvt_mtrx)
                # dbug(pvt_nlvl)
                # dbug(col_num)
                max_col_lens[col_num] = maxof(col)
                # dbug(max_col_lens[col_num])
                for box in col:
                    # dbug(box[0])
                    if nclen(box[0]) > max_col_lens[col_num]:
                        max_col_lens[col_num] = nclen(box[0])
                my_col = []
                for row_num, box in enumerate(col):
                    # establish default positions
                    pos_str = ""
                    if row_num == 0:             # "top"
                        pos_str += "top "
                    if row_num > 0 and row_num < num_rows:
                        pos_str += "middle "
                    if row_num == num_rows:      # "bottom"
                        pos_str += "bottom "
                    if col_num == 0:             # "left"
                        pos_str += "left "
                    if col_num > 0 and col_num < num_cols:
                        pos_str += "center "
                    if col_num == num_cols:      # "right"
                        pos_str += "right "
                    my_col += gblock(box, height=max_row_h[row_num], width=max_col_lens[col_num], position=pos_str)
                col_boxes.append(gblock(my_col))
                col_len = maxof(col, "length")
                if col_len > max_col_lens[col_num]:
                    max_col_lens[col_num] = col_len
            # """--== SEP_LINE ==--"""
            # dbug("We got here...")
            # prnt = True  # debugging
            # my_cols = gcolumnize(col_boxes, prnt=prnt, boxed=boxed_b, centered=centered_b, box_clr=box_color, title=title, footer=footer)  # , footer=dbug('here'))
            my_cols = gcolumnize(col_boxes, prnt=prnt, boxed=boxed_b, centered=centered_b, box_clr=box_color, title=title, footer=footer)
            # dbug("Returning my_cols")
            return  my_cols
            # """--== SEP_LINE ==--"""
        # dbug(cols)
        row_col_len_lol = []   # this will hold the max len for each col in each row
        rows = len(msg_l)     # this is the number of rows
        for row_num, row in enumerate(msg_l):
            row_col_len_lol.append([])  # initialize an empty list to col lens for this row
            for col in row:
                col_len = maxof(col)
                row_col_len_lol[row_num].append(col_len)  # each col len is appended
        max_cols = 0
        if cols > 0:
            max_cols = cols
        max_allcols_len = 0
        for row_num, row in enumerate(row_col_len_lol):
            if len(row) > max_cols:
                max_cols = len(row)
            max_row_len = 0
            for col_num, col in enumerate(row):
                max_row_len += row_col_len_lol[row_num][col_num]
                if max_row_len > max_allcols_len:
                    max_allcols_len = max_row_len
            # dbug(f"For row_num: {row_num} max_row_len: {max_row_len}")
        # dbug(max_cols)
        # dbug(max_allcols_len)
        rows = []
        # for row_num, row in enumerate(my_lol):
        for row_num, row in enumerate(msg_l):
            # dbug(boxed_b)
            # dbug(f"calling gcolumnize(row: {row}) ")
            # row_lines = gcolumnize(row, boxed=boxed_b, length=max_allcols_len, positions=[[1, 2, 5]])
            # dbug(max_allcols_len)
            row_lines = gcolumnize(row, length=max_allcols_len)  # , positions=[[1, 2, 5]])
            rows.append(row_lines)
        lines = []
        for n, row in enumerate(rows, start=1):  # debugging
            lines.extend(row)
        lines = printit(lines, boxed=boxed_b, centered=centered_b, title=title, footer=footer, box_color=box_color, color=color, prnt=prnt)
        # dbug("Returning lines")
        return lines
    # """--== not a list of lists of lists ==--"""
    # dbug("ok so it is not rows of boxes - it is a single row with boxes (or lines)")
    # dbug(centered_b)
    # """--== Init Vars ==--"""
    lines = []
    line_num = 0
    boxes_len = []
    boxes_height = []
    max_box_lines = 0
    color = sub_color(color)
    pad_char = gclr(color, " ")  # used to position 'boxes' properly when one has more lines than the other
    # """--== Process ==--"""
    # """--== Calculate box widths(boxes_len: list) and max box num of lines (max_box_lines: int) ==--"""
    # width = 140
    # dbug(f" forced width: {width}")
    for box_num, box in enumerate(msg_l):
        # max_col_len = maxof(box, 'len')
        # sum_len += maxof(box, 'len')
        # assumes 1 row of x boxes (lines of same lengthed text)
        boxes_height.append(len(box))  # set box height for each box in the row
        # dbug(f"Just set boxes_height: {len(box)}")
        if len(box) > max_box_lines:  # height/rows
            # set the max_box_len with the greatest box "height"
            max_box_lines = len(box)  # height
            # printit(box)
            # dbug(f"Just set max_box_lines: {max_box_lines} based on len(box): {len(box)}")
        # must be the first line
        """--== SEP_LINE ==--"""
        this_box_width = 0
        for n, line in enumerate(box, start=1):
            if nclen(line) > this_box_width:
                this_box_width = nclen(line)
        # dbug(this_box_width)
        boxes_len.append(this_box_width)  # legths of boxes
        # boxes_height.append(n)
    # dbug(boxes_len)
    # max_len = max(boxes_len)
    # dbug(boxes_height)
    max_height = max(boxes_height)
    # dbug(max_height)
    # dbug(max_box_lines)
    sum_len = sum(boxes_len)
    # dbug(max_len)
    # dbug(sum_len)
    num_boxes = len(boxes_len)
    num_cols = num_boxes
    """--== develop each line ==--"""
    # this only columnizes one row - understand that one row can have many lines
    # full_length = sum_len + (nclen(sep_chrs) * (num_cols - 1))
    while True:
        line = ""
        num_boxes = len(msg_l)  # aka num of cols?
        for box_num, box in enumerate(msg_l):
            # assumes each box is a column in one row
            just = 'left'  # the default?
            if box_num in cntr_cols:
                just = 'center'
            # dbug(len(msg_l))  # num 0f cols?
            # dbug(sep_chrs)
            full_length = sum_len + (nclen(sep_chrs) * (num_cols - 1))
            """--== SEP_LINE ==--"""
            new_col_len = maxof(box, 'len')
            new_height = max_height
            if width > full_length:
                just = 'center'
                diff_len = width - full_length
                new_col_len = new_col_len + (diff_len // num_cols)
                # dbug(f'Changing col_len: {maxof(box, "len")} to new_col_len: {new_col_len}')
            # if height > max_height:
                # just = 'middle'
                # new_height = height
                # dbug(f'Changing boxes height: {max_height} to height: {height}')
            """--== SEP_LINE ==--"""
            box = gblock(box, justify=just, pad=pad, length=new_col_len, height=new_height)  # maximizes each string len  for this box (ie this column)
            # dbug(f"Just used gblock with just: {just}")
            # max_box_len
            if line_num > len(box) - 1:
                # each box that is not the last in a row
                pad_len = boxes_len[box_num]
                # dbug(f"box_num: {box_num} line_len: {nclen(line)} pad_len: {pad_len}")
                col_padding = pad_char * pad_len
                # dbug(f"adding col_padding: {col_padding} [len(box): {len(box)}] for box_num: {box_num} boxes_len: {boxes_len}")
                line += col_padding
            else:
                # this is the last box in a row???
                line += box[line_num]
            if box_num < num_boxes - 1:
                # dbug(f"box_num: {box_num} num_boxes: {num_boxes} line_num: {line_num}")
                # dbug(sep_chrs)
                line += sep_chrs
            # dbug(width)
            if width > scr_col_len:
                dbug(f"Houston, we have a problem... width: {width} exceeds col_len: {scr_col_len}")
                return
        line_num += 1
        lines.append(line)
        if line_num > max_box_lines - 1:
            # dbug("Done!!!")
            break
    lines = printit(lines, boxed=boxed_b, centered=centered_b, title=title, footer=footer, box_color=box_color, color=color, prnt=prnt)
    # dbug("Returning lines")
    return lines
    # ### EOB def gcolumnize(boxes, width=0): ### #


# for now, create and alias (TODO)
# gcolumnized = gcolumnize


def gcolumnize_demo(*args, **kwargs):
    """
    purpose: A demo of using gcolumnize
        Great for build quick dashboards
    """
    my_l = ["line one", "second line", "my longer line three", "line four", "line five", "line six", "seventh line"]
    my_cols = gcolumnize(my_l, cols=2, sep=" | ")
    printit(my_cols, 'boxed', footer=dbug('here'))
    my_cols = gcolumnize(my_l, cols=3, sep=" | ", prnt=True, boxed=True, footer=dbug('here'))
    dbug('ask')
    # dbug(funcname())
    # """--== Config ==--"""
    # ask_b = bool_val(["ask"], args, kwargs, dflt=True)
    # """--== SEP_LINE ==--"""
    prnt = False
    block1 = gblock("[one]", width=20, height=6, fill="1", pos=1, prnt=prnt)
    block2 = gblock("[two]", width=20, height=6, fill="2", pos=2, prnt=prnt)
    block3 = gblock("[three]", width=20, height=6, fill="3", pos=3, prnt=prnt)
    block4 = gblock(boxed("[four]"), 'boxed', width=20, height=6, fill="4", pos=4, prnt=prnt)
    block5 = gblock("[five]", 'boxed', width=20, height=6, fill="5", pos=5, prnt=prnt)
    block6 = gblock("[six]", 'boxed', width=20, height=6, fill="6", pos=6, prnt=prnt)
    block7 = gblock("[seven]", width=20, height=6, fill="7", pos=7, prnt=prnt)
    block8 = gblock("[eight]", width=20, height=6, fill="8", pos=8, prnt=prnt)
    block9 = gblock("[nine]", width=20, height=6, fill="9", pos=9, prnt=prnt)
    print("="*50)
    simple_l = [block1, block2, block3, block4, block5, block6, block7, block8, block9]
    gcolumnize(simple_l, 'prnt', 'boxed', cols=3, title="list of blocks 3 columns")
    # """--== SEP_LINE ==--"""
    dbug("Launcing a list of boxes")
    boxes = [boxed("one"), boxed("two"), boxed("three"), boxed("four"), boxed("five"), boxed("six")]
    gcolumnize(boxes, 'prnt', 'boxed', 'centered', box_clr="white on blue", footer=dbug('here'), title=" one list of boxes - 2 cols", cols=2)
    # """--== SEP_LINE ==--"""
    dbug("Launching test boxes - ie a list  boxes (one combined with +)")
    tst_boxes = [boxed("one", title="Stacked1") + boxed("two", title="stacked2"),
            boxed("three", title="col2"),
            boxed("four", title="col3-stacked1") + boxed("five", title="col3-stacked2") + boxed("six", title="col3-stacke3")]
    gcolumnize(tst_boxes, 'prnt', 'boxed', 'centered', box_clr="yellow! on black", footer=dbug('here'), title="tst_boxes: [1+2, 3, 4+5] type=list")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    dbug("Launching roc_boxes - ie rows of cols of boxes")
    roc_boxes = [[boxed("one", title="row1,1"), boxed("two", title="row1,2")],
                 [boxed("three", title="row2,1"), boxed("four\nfour\nfour\nfour", title="row2,2")],
                 [boxed("five", title="row3-stacked1") + boxed("six", title="row3-stacked2")]]
    gcolumnize(roc_boxes, 'prnt', 'boxed', 'centered', box_clr="yellow! on black", footer=dbug('here'), title="roc_boxes: [[1, 2], [3, 4], [5 + 6]] type=list")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    tst_boxes = [boxed("one"), boxed("two"), boxed("three")]
    gcolumnize(tst_boxes, 'prnt', 'boxed', footer=dbug('here'))
    gcolumnize(tst_boxes, 'prnt', 'boxed', footer=dbug('here'), cols=2)
    dbug('ask')
    # """--== SEP_LINE ==--"""
    my_l = ["one", "two", "three", "four"]
    lines = gcolumnize(my_l, 'prnt', 'boxed', title="boxed")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    my_l = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
            "eighteen", "nineteen", "twenty", "twenty one", "twenty two", "twenty three", "twenty four"]
    lines = gcolumnize(my_l, 'prnt', 'boxed', title="boxed - no args - avoiding screen overrun", sep=" | ", footer=dbug('here'))
    # lines = columned(my_l, 'prnt', title=" - no args - avoiding screen overrun", sep=" | ", footer=dbug('here'))
    # maxof_lines = maxof(lines)
    # dbug(maxof_lines)
    # printit(lines, 'boxed', title="Boxed lines from columned()", footer=dbug('here'))
    dbug('ask')
    gcolumnize(my_l, 'boxed', title="no args", sep=" | ", order='pivot', prnt=True, footer=dbug('here'))
    width = 50
    gcolumnize(my_l, 'boxed', width=width, sep=" | ", title=f"width={width} order='h' (horizontal)", order="h", prnt=True, footer=dbug('here'))
    width = 70
    gcolumnize(my_l, 'boxed', width=width, sep=" | ", title=f"width={width} but order='v' (vertical)", order='v', prnt=True, footer=dbug('here'))
    cols = 4
    gcolumnize(my_l, 'boxed', cols=cols, sep=" | ", title=f"cols={cols} order is (default vertical)", prnt=True, footer=dbug('here'))
    cols = 5
    gcolumnize(my_l, 'boxed', cols=cols, sep=" | ", title=f"cols={cols} order='h' (horizontal)", order="h", prnt=True, footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    box1 = ["+------+", "| box1 |", "+------+"]
    box2 = boxed(["This is", "box2", "Enjoy!"], txt_center=99, box_color="white! on yellow")
    # dbug(f"box2: {box2}")
    boxes = [box1, box2]
    lines = gcolumnize(boxes)
    printit(lines, 'boxed', footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    box1 = boxed(["+------+", "| box1 |", "+------+"], box_color="white! on black")
    box2 = boxed(["+--------------+", "| this is box2 |", "| box2         |", "| box2         |", "+--------------+"], box_color="white! on rgb(100, 60, 120)")
    box3 = boxed(["+----------------+", "| box3 box3 box3 |", "+----------------+"], box_color="white! on blue")
    box4 = boxed(["box4 adding some length to this box just for grins", "box4", "box4", "box4"], box_color="white! on cyan")
    boxes.append(box1)
    boxes.append(box2)
    boxes.append(box3)
    boxes.append(box4)
    gcolumnize(boxes, 'prnt', 'boxed', title="boxes, all boxed")
    dbug('ask')
    gcolumnize(boxes, 'prnt', 'boxed', cols=1, title="boxes cols=1", footer=dbug('here'))
    dbug('ask')
    gcolumnize(boxes, 'prnt', 'boxed', cols=3, title="boxes cols=3", footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    row1 = [box1, box2]
    gcolumnize(row1, 'prnt', 'boxed', title="row1", footer=dbug('here'))
    dbug("Above is row1", 'ask')
    row2 = [box3, box4]
    gcolumnize(row2, 'prnt', 'boxed', title="row2", footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    boxes = [[box1, box2], [box3, box4]]
    # boxes = [box1, box2] + [box3, box4]  # this puts everything on one line
    lines = gcolumnize(boxes)
    print("--------------------------------")
    printit(lines, title="boxes=[[box1,box2],[box3,box4]]", footer=dbug('here'))
    print("--------------------------------")
    dbug("Above printit with title and footer but not boxed", 'ask')
    top_box = boxed("This is the top box - one line boxed", 'prnt')
    lines = gcolumnize([row1, row2], 'prnt', 'boxed', title="row1, row2 boxed")
    dbug('ask')
    lines = gcolumnize(row1 + row2, 'prnt', 'boxed', title="row1 + row2 boxed")
    dbug('ask')
    lines = gcolumnize([row1, row2], title="row1, row2 boxed")
    printit(lines, 'boxeed', title="row1, row2 boxed by printit", footer=dbug('here'))
    dbug('ask')
    big_box1 = boxed(gcolumnize([row1, row2], 'prnt', positions=[[0, 0, 4]]), title="big_box1 positions: [[0, 0, 4]]")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    printit("For reeference positions is a triplet with (row, column, and position 1-9:")
    gtable([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 'prnt', title="Position")
    # """--== SEP_LINE ==--"""
    big_box2 = gcolumnize([row1, row2], 'prnt', 'boxed', title="big_box2 positions=[[0,0,5],[1,0,9]]", positions=[[0, 0, 5], [1, 0, 9]])
    dbug('big_box2 = gcolumnize([row1, row2], "prnt", "boxed", title="big_box2", positions=[[0, 0, 5], [1, 0, 9]])', '')
    print("="*50)
    # dbug("now going to run gcolumnize with prnt and boxed")
    lines = gcolumnize([big_box1, big_box2])
    printit(lines, 'boxed', box_color="white! on red", title="[ All boxed up with no place to go ]", footer=dbug('here'))
    dbug('printit(lines, "boxed", box_color="white! on red", title="[ All boxed up with no place to go ]", footer=dbug("here"))')
    dbug('ask')
    # """--== SEP_LINE ==--"""
    rows = 3
    cols = 2
    rc_a = [[None for c in range(cols)] for r in range(rows)]
    dbug(rc_a)
    box1_1 = boxed(["This is", "my message"],
            title="box1_1",
            color="blue",
            box_color="white! on black")
    gcolumnize([box1_1], 'prnt', 'centered', width=190, title="box1_1", box_color="yellow! on black")
    box1_2 = boxed(["As long as the day is known as today",
        "Encourage one another",
        "To be better to one another"],
        title="[white! on black]box1_2[/]",
        box_color="white! on red",
        color="red!")
    gcolumnize([box1_2], 'prnt', 'centered', width=190, title="box1_2", box_color="yellow! on black")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    gcolumnize([box1_1, box1_2], 'prnt', 'centered', width=190, title="One row of boxes centered on screen", box_color="yellow! on black")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    box2_1 = boxed(["What a piece of work is man",
        "How noble in reason, how infinite in faculty,",
        "In form and moving, how express and admirable",
        "In action how like an angel, in apprehension, how like a god",
        "The beauty of the world!, The paragon of animals!"],
        title="[white! on black]box2_1[/]",
        box_color="white! on blue",
        color="yellow")
    gcolumnize([box2_1], 'prnt', 'centered', width=190, title="box2_1", box_color="white! on black")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    box2_2 = boxed(["And yet, to me", "What is this quintessence of dust?"],
            title="[white! on black]box2_2[/]",
            box_color="white! on red",
            color="white!")
    gcolumnize([box2_2], 'prnt', 'centered', width=190, title="box2_2", box_color="white! on black")
    dbug('ask')
    """--== SEP_LINE ==--"""
    text_lines = printit(["This is just a group", "of lines", "thrown", "together for a demo"], 'noprnt')
    text_lines2 = printit(["All I want to do", "is bang on the drum", "all day."], 'noprnt')
    gcolumnize([text_lines, text_lines2], 'prnt', 'centered', sepchrs="  |  ", title="Two columns of lines of text", footer="sepchrs: [  |  ]")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    row3 = [text_lines, text_lines2]
    gcolumnize(row3, 'prnt', title="row3: [text_lines, text_lines2]", sep=" | ")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    rows_lol = [[box1_1, box1_2], [box2_1, box2_2], row3]
    gcolumnize([box1_1, box1_2], 'prnt', 'boxed', title="[box1_1, box1_2]")
    dbug('ask')
    # dbug("3 rows, 2 cols box1_1 is ~ 10 heigh")
    gcolumnize(rows_lol, 'prnt', 'centered', 'boxed', title="Non-aligned 3 rows of boxes - boxed positions[[0, 1, 5]]", footer=dbug('here'), positions=[[0, 1, 5]])
    dbug('ask')
    # """--== SEP_LINE ==--"""
    row4 = [boxed("This is row four with one line boxed"), [""]]
    rows_lol.append(row4)
    gcolumnize(rows_lol, 'prnt', 'aligned', 'centered', title="aligned rows or boxes", footer=f"These colors are just for demo purposes {dbug('here')}")
    # """--== SEP_LINE ==--"""
    printit("-"*80)
    row1 = gcolumnize([box1_1, box1_2], 'boxed', 'prnt', title="[box1_1,box1_2]", width=150, positions=[(0, 1, 5)], footer=dbug('here'))
    printit("-"*80, 'ask')
    # """--== SEP_LINE ==--"""
    row2 = gcolumnize([box2_1, box2_2], 'prnt', 'boxed', title="[box2_1, box2_2]", footer=dbug('here'), width=150, positions=[(0, 1, 5)])
    dbug('ask')
    # """--== SEP_LINE ==--"""
    box1 = boxed("1234box189012")
    box2 = boxed(["box2", "box2"])
    box3 = boxed(["12345678901", "12345678901", "123456789012345678901"])
    box4 = boxed("box4")
    box5 = boxed("box5")
    box6 = boxed("box6")
    box6 = boxed(gblock(box6, length=50, height=10, position=5))
    # gcolumnize([[box1, box2], [box3, box4], [box5, box6]], 'prnt', positions=[[0, 1, 5], (1, 1, 5), (2, 0, 9)])
    gcolumnize([[box1, box2], [box3, ["Nothing"]], [box5, box6]], 'prnt', 'boxed', title="[[box1,box2],[box3,box4],[box5,box6]]", footer=dbug('here'))
    return


def matrix(rows, cols, *args, **kwargs):
    """
    purpose: initialize a matirx (ie array)
    required: rows/dim1: int, cols/dim2: int
    options:
        - dflt_val=None: anything  # default "value" to initialize each "cell" to
    returns: 2 dim initialized array/matrix
    aka: init_arr | initarray | init_arr
    """
    # """--== Config ==--"""
    dflt_val = kvarg_val(['dflt', 'dflt_val'], kwargs, dflt=None)
    # """--== SEP_LINE ==--"""
    # row col array
    rc_arr = [[dflt_val for c in range(cols)] for r in range(rows)]
    return rc_arr


# #################################
def sayit(msg, *args, prnt=True, **kwargs):
    # #############################
    """
    purpose: This will use computer voice (espeak) to "say" the msg
    options
    - prnt: will print as well  # this is very limited
    - gender: str               # m | f
    - volume: float             # 0 - 1
    - rate: int                 # default = 150
    - tone: int                 # 1 - 5  <-- this does not seem to do anything???
    returns: None
    notes:
    # use espeak --voices to see them all then add +m|f1-?
    # genders = ["m", "f"]
    # tonals = ["1", "2", "3", "4", "5"]
    # for gender in genders:
    #    for tone in tonals:
    #        voice =  f"'english-us+{gender}{tone}'"
    #        engine.setProperty('voice', voice)
    #        msg = f"The time is {date.today().strftime('%B %d %Y')}. My voice is {voice}"
    #        print(msg)
    #        engine.say(msg)
    """
    # """--== Imports ==--"""
    import pyttsx3
    # """--== Config ==--"""
    prnt = bool_val(["prnt", "print"], args, kwargs)
    rate = kvarg_val(['rate'], kwargs, dflt=150)
    volume = kvarg_val(['vol', 'volume'], kwargs, dflt=0.8)
    gender = kvarg_val(['gender'], kwargs, dflt="m")
    tone = kvarg_val(['tone', 'tonal'], kwargs, dflt=3)
    # """--== Init ==--"""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)   # rate is w/m
    engine.setProperty('volume', volume)
    engine.setProperty('voice', f'english-us+{gender}{tone}')
    # """--== Debugging ==--"""
    # voices = engine.getProperty('voices')
    # for n, voice in enumerate(voices):
    #     dbug(msg + f"index-> {n} voice name is: {voice.name}")
    #     if 'rench' in voice.name:
    #         engine.setProperty('voice', voices[28].id)
    # """--== Process ==--"""
    engine.say(msg)
    engine.runAndWait()
    if prnt:
        printit(msg)
    # """--== Alternative ==--"""
    # google text to speach - sounds more realistic but only one voice (now) per language
    # CMI = gtts-cli | mpg123 -
    # from gtts import gTTS
    # import playsound
    # tts = gTTS(msg)
    # filename = "output.mp3"
    # tts.save(filename)
    # """--== SEP_LINE ==--"""
    # playsound.playsound(filename)
    return
    # ### EOB def sayit(msg, *args, prnt=True, **kwargs): ### #


# ##############################
def sayit_demo(*args, **kwargs):
    # ##########################
    """
    purpose: demo of using sayit()
    returns: None
    """
    sayit("Testing sayit")
    sayit("Testing sayit with female voice", gender="f")
    rate = 200
    for gender in ["f", "m"]:
        sayit(f"Testing sayit with gender = {gender} and rate={rate}", gender=gender, rate=rate)
    sayit("Testing sayit with print", 'prnt')
    return
    # ### EOB def sayit_demo(*args, **kwargs): ### #


# ################################
def printit(msg, *args, **kwargs):
    # ############################
    """
   purpose: prepares and prints (option) msg: str|list and can put in unicode color box, centered in terminal and with color
   required: msg: str|list (can contain color codes (see below)
   options:
        "boxed" | boxed=False  # prepares a box around msg
        "centered" | centered=False  # centers horizontally msg on a termial screen
        "shadowed" | shadowed=True  # adds a shadow typically around a box
        "prnt" | prnt=True  # print line(s) or just return them as a str
           (useful for input(printit("What do you want? ", 'centered', prnt=False, rtrn_type="str")))
        txt_center: int  # tells how many lines from the top to center within a list of lines
        txt_right: int  # tells how many lines from the top to justify to the right within a list of lines
        box_color: str  # eg "blink red on black"
        color: str  # eg "bold yellow on rgb(40,40,40)"
        title: str  # puts a title at top of a box
        footer: str  # puts a footer at the bottom of a box
           style: str  # to select box style - not fully functional yet
        shift: int  # how far to the left (neg) or to right (pos) to shift a centered msg
        width: int  # forces msg to fit in this width using text wrap
        rtrn_type: "list" | "str"  # default is list
        function is pretty extensive...
        color coding: activates decoding using color tag(s)
            eg msg = "my  message[blink red on black]whatever goes here[/]. The end or close tag will reset color")
    returns: msgs  # list [default] or str depending on rtrn_type
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # ddbug(f"msg: {msg}")
    # dbug(type(msg))
    # ddbug(f"args: {args}")
    # ddbug(f"kwargs: {kwargs}")
    # """--== Config ==--"""
    centered_b = bool_val(['centered', 'center'], args, kwargs, dflt=False)
    # ddbug(f"centered_b: {centered_b}")
    txt_center = kvarg_val(['text_center', 'txt_center', 'txt_centered', 'txt_cntr', 'lines_centered', 'center_txt', 'cntr_txt'], kwargs, dflt=0)
    txt_right = kvarg_val(['txt_right'], kwargs, dflt=0)
    # ddbug(f"txt_center: {txt_center}")
    # if not isinstance(mycentered, bool):
    #     txt_center = mycentered
    prnt = bool_val('prnt', args, kwargs, dflt=True, opposites=['noprnt', 'no_prnt', 'no_print'])
    boxed_b = bool_val(['box', 'boxed'], args, kwargs, dflt=False)
    # dbug(boxed_b)
    box_color = kvarg_val(['box_color', 'box_clr', 'border_color', 'border_style'], kwargs, dflt="")
    # dbug(box_color)
    title = kvarg_val(['title'], kwargs, dflt="")
    footer = kvarg_val(['footer'], kwargs, dflt="")
    color = kvarg_val(['color', 'txt_color', 'text_style'], kwargs, dflt="")
    # dbug(color)
    # color_coded = bool_val(['clr_coded', 'colorized', 'color_coded', 'colored', 'coded'], args, kwargs, dflt=False)
    shadow = bool_val(['shadow', 'shadowed'], args, kwargs, dflt=False)
    style = kvarg_val(['style', 'box_style'], kwargs, dflt="round")
    width = kvarg_val(['width', 'length'], kwargs, dflt=0)
    columnize = bool_val(['columnize', 'columns'], args, kwargs, dflt=False)
    pad = kvarg_val(['pad'], kwargs, dflt=" ")
    shift = kvarg_val('shift', kwargs, dflt=0)
    # dbug(shift)
    rtrn_type = kvarg_val(['rtrn_type', 'rtrn'], kwargs, dflt='list')
    str_b = bool_val(["str", "string"], args, kwargs, dflt=False)
    if str_b:
        rtrn_type = "str"
    # end = kvarg_val('end', kwargs, dflt="\n")
    # """--== Validate ==--"""
    if isempty(msg):
        dbug(f"Nothing to print msg: {msg}")
        return
    if not isinstance(columnize, bool):
        columnize = False
    if not isinstance(width, int):
        width = 0
    # """--== Convert to list (msgs) ==--"""
    # dbug(color)
    if 'pandas' in str(type(msg)):
        # dbug("pandas")
        msg = str(msg)
    if isinstance(msg, tuple):
        msgs = list(msg)
    if msg is None or len(str(msg)) == 0:
        # dbug(f"Nothing to do, msg is empty? ... msg: {msg}")
        return None
    if isinstance(msg, list):
        msgs = msg
    if isinstance(msg, float) or isinstance(msg, int):
        msg = str(msg)
    # dbug(type(msg))
    if isinstance(msg, str):
        # dbug(msg)
        if "\n" in msg or "\\n" in msg:
            # dbug(msg)
            # dbug("Splitting up msg on \n")
            msgs = msg.split("\n")
            # dbug(len(msgs))
            # dbug(msgs, 'ask')
            # mymsgs = msg.splitlines()
            # dbug(mymsgs, 'ask')
        else:
            # dbug(msg)
            msgs = [msg]
        # ddbug(f"columnize: {columnize}")
        # ddbug(f"width: {width}", 'ask')
        if not columnize and width > 0:
            msgs = wrapit(msgs, width-2)
        # dbug(msgs)
    if isinstance(msg, dict):
        # wip?
        msgs = []
        for k, v in msg.items():
            msgs.append(f"k: {k} v: {v}")
    if not isinstance(msgs, list):
        dbug(f"Failed to convert msg to list ...: type(msg): {type(msg)}... returning")
        return
    # """--== Process ==--"""
    color_coded = False  # init color_coded before test
    for msg in msgs:
        # this is not fully tested, but seems to work... until we curl wttr....
        if re.search(r"\[.+?\].+\[/]", str(msg)):
            # dbug(f"msg: {msg} appears to be color_coded")
            color_coded = True
    # dbug(color_coded)
    if color_coded:
        # from gcolors import clr_coded
        # dbug(f"Using color_coded")
        msgs = [clr_coded(msg) for msg in msgs]
    # for m in msgs:  # for debugging only
        # dbug(m)
    if columnize:
        # if width < 1:
        #    scr_len = get_columns(rows=False)
        #    scr_len = get_columns()
        #   width = ceil(scr_len * 0.8)
        # dbug(f"gcolumnize(msgs: {msgs} width: {width})")
        msgs = gcolumnize(msg, width=width)
        # dbug(f"gcolumnized msgs: {msgs}")
    if boxed_b:
        # dbug(boxed_b)
        # dbug(msgs)
        # dbug(txt_center)
        # dbug(color)
        # dbug(box_color)
        # dbug(footer)
        # dbug(boxed_b)
        title = str(title)
        # dbug(pad)
        # dbug(width)
        # dbug('ask')
        msgs = boxed(msgs, title=title, footer=footer, color=color, box_color=box_color, txt_center=txt_center, txt_right=txt_right, width=width, style=style, pad=pad)
    else:
        COLOR = sub_color(color)  # TODO fix this so that it is not needed
        msgs = [COLOR + str(m) for m in msgs]
        # dbug(boxed_b)
        if nclen(title) > 0:
            msgs.insert(0, title)
            # dbug(f"Just inserted title: {title}")
        # dbug(color)
        if nclen(footer) > 0:
            if centered_b:
                # msgs_len = maxof(msgs)
                # dbug(footer)
                footer = centered(footer, width=width)  # , length=msgs_len)[0]
                # dbug(footer)
            msgs.append(footer)
            # dbug(f"Just appended footer: {footer} to msgs")
        # dbug(f"This is a test of color: {color} using repr(COLOR): {repr(COLOR)} " + COLOR + " testing color " + RESET)
    if shadow:
        msgs = shadowed(msgs)
    if centered_b:
        # dbug(centered_b)
        # dbug(repr(msgs))
        # dbug(shift)
        # dbug(width)
        msgs = centered(msgs, shift=shift, width=width)
        # dbug(repr(msgs))
    # dbug(prnt)
    # prnt = True
    if prnt:
        # dbug(boxed_b)
        # dbug(prnt)
        [print(ln) for ln in msgs]
    # dbug(rtrn_type)
    if rtrn_type in ('str', 'string', 's'):
        # NOTE: If you made this invisible (not prnt) then you may want to add this option as well rtrn_type="str"
        # there are times when you want no prnt but still return lines (like in gcolumnize) so these two options need to be used carefully
        msgs = "\n".join(msgs)  # cinput() needs this to be a str
    # dbug(boxed_b)
    return msgs
    # #### EOB def printit(msg, *args, **kwargs): ### #


def printit_demo(*args, **kwargs):
    """
    purpose: demo of using printit()
    returns: None
    """
    msg = "This is a msg:\none\ntwo\nthree"
    printit(msg)
    boxed_msg = printit(msg, 'boxed', title="msg boxed", footer=dbug('here'))
    print()
    printit(boxed_msg, 'boxed', title=" [red on white]And now we box the previous box...[/] ", footer=dbug('here'), box_color="white on blue")
    print()
    printit(msg, 'boxed', 'centered', title="msg boxed centered", footer=dbug('here'))
    printit(msg, 'boxed', 'centered', title="msg boxed centered txt_center=99", footer=dbug('here'), txt_center=99)
    printit(msg, 'boxed', 'centered', title="msg boxed centered txt_right=99", footer=dbug('here'), txt_right=99)
    # box2 = boxed(["one", "two", "three"])
    # printit(box2, 'boxed', title='box2', footer=dbug('here'))
    # row = gcolumnize([box1, box2])
    # printit(row, 'boxed', title='row', footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    msgs = []
    out = run_cmd('date')
    msgs.append(out.rstrip('\n'))
    out = run_cmd('uname -a')
    msgs.append(out.rstrip('\n'))
    cmd = 'ls | tail -5'
    out = run_cmd(cmd, 'lst')
    # dbug(out)
    out = [ln.rstrip('\n') for ln in out if ln != '']
    msgs += out
    # """--== SEP_LINE ==--"""
    orig_msgs = gblock(msgs)
    title = f"gblock output from cmd: {cmd}"
    printit(orig_msgs, title=title)
    printit(orig_msgs, 'boxed', title=title + " boxed")
    # msgs = []
    print()
    printit(orig_msgs, 'centered', title="Centered but Not Boxed", footer=dbug('here'))
    print()
    # dbug('ask')
    printit("[red! on yellow!]Done[/][white! on black!] Enjoy your day! [/]", 'centered')
    return


def clr_coded(msg_s):
    """
    purpose: takes any msg string containing tags for colors and decodes them into a colorized string
    requires: msg_s: str
    returnd: colorized string
    decode a string - replace \[color\].*[\/] with code and reset
    requires a space before the first bracket
    """
    # """--== Debug ==--"""
    # dbug(funcname())
    # dbug(msg_s)
    # """--== Process ==--"""
    rgx = True
    # this loop algorythm seems lame to me but it works
    while rgx:
        # dbug(msg_s)
        msg_s = msg_s.replace("[/]", gclr('reset'))
        # dbug(msg_s)
        pattern = r'\[([^\[]+?)\]'  # works! unless another bracket???
        # pattern = r'\[([^\[]+?)\[\]'  # fails
        # dbug(pattern)
        rgx = re.search(pattern, msg_s)
        if rgx:
            color = rgx.group(1)
            # dbug(f"color: {color} rgx.group(1): {rgx.group(1)}")
            color = color.strip()
            # dbug(f"sending color: {color} to gclr()" + RESET)
            try:
                clr_code = gclr(color)
            except:
                break
            # dbug(f"Got this back from gclr({color}) repr(color_code): {repr(clr_code)} clr_code: {clr_code}" + RESET)
            bracketed_color = f'\[\s*{color}\s*?\]'
            # dbug(bracketed_color)
            msg_s = re.sub(bracketed_color, clr_code, msg_s)
    # dbug(f"returning: {repr(msg_s)}")  # may have RESET appended to it already
    return msg_s
    # ### EOB def clr_coded(msg_s): ### #


def clr_coded_demo(*args, **kwargs):
    """
    purpose: demo of using clr_coded()
    returns: None
    """
    s = "print [red]this as red[/] done"
    print(s)
    printit(s)
    print(s)
    s = "[now try this with [red]this as red[/] done]"
    printit(s)
    s = "[now try this with [red]this as red[/]] done]"
    print(s)
    printit(s)


def gclr(color='normal', text="", **kwargs):
    """
    Purpose: to return color code + text (if any) NOTE: sub_color() uses this!
    input:
        text: str = ""         # if "" then the color code alone is returned
        color: str = 'normal'  # examples: 'red on black', 'bold green on normal', 'bold yellow on red', 'blink red on black' etc
        reset: bool            # adds a color reset after the text
    Notes:
        color is the first argument because you may just want to return the color code only
        run gcolors.demo() to see all color combinations
    returns: color coded [and text]
    """
    """--== Debug ==--"""
    # ddbug(f"funcname(): {funcname()}")

    # """--== Config ==--"""
    reset_b = kvarg_val('reset', kwargs, dflt=False)  # add a RESET to the end of text
    # """--== Init ==--"""
    color = color.lower()
    PRFX = "\x1b["
    PRFX2 = "\033["
    RESET = PRFX + "0m"
    fg = bg = ''
    STYLE_CODES = ""
    color = color.strip()
    # ddbug(color)
    text = str(text)
    # """--== Convert ==--"""
    # this is not fully tested, but seems to work... until we curl wttr....
    if re.search(r"\[.+?\].+\[/]", str(color)):
        # dbug(f"text: {text} appears to be color_coded")
        text = color
        color = ""
    if re.search(r"\[.+?\].+\[/]", str(text)):
        # dbug(f"text: {text} appears to be color_coded")
        text = clr_coded(text)
    # """--== Process ==--"""
    if color == "":
        return "" + text
    if color == 'reset':
        return RESET + text
    if PRFX in color or PRFX2 in color:
        # dbug(f"Found either PRFX or PRFX2 in color: {repr(color)}")
        return color + text
    # ddbug(f"color: {color}")
    # """--== Pull out and Xlate STYLE ==--"""
    if "fast_blink" in color:
        # we have to do this special case first - otherwise "blink" will get pulled out incorrectly from "fast_blink"
        STYLE_CODES += f"{PRFX}{styles_d['fast_blink']}m"
        color = fg.replace("fast_blink", "")
    # ddbug(f"color: {color}")
    for s in styles_d:
        # ddbug(f"chkg for style: {s} in fg_color: {color}...")
        if s in color:
            if s == "bold":
                continue
            fg = fg.replace(s, "").strip()
            # print(f"s: {s}")
            if s != 'normal':
                STYLE_CODES += f"{PRFX}{styles_d[s]}m"
            color = color.replace(s, "")  # pull out style
            # ddbug(f"STYLE_CODES: {repr(STYLE_CODES)}")
    # ddbug(f"color: {color}")
    # """--== Process split fg from bg ==--"""
    if color.startswith("on "):
        color = 'normal ' + color  # make fg = normal
        # print(f"myDBUG: funcname: {funcname()} lineno: {lineno()} color is now: {color}")
    # """--== Split color into fgbg_l ==--"""
    fg_color = bg_color = ""  # init these first
    fgbg_color = color.split(" on ")  # create a fgbg list split on " on "
    # ddbug(f"color: {color} splits into fgbg_color: {fgbg_color}", 'ask')
    fg_color = fgbg_color[0]
    if len(fgbg_color) > 1:
        bg_color = fgbg_color[1]
    # ddbug(f"fgbg_color: {fgbg_color} repr(fg_color): {repr(fg_color)}" + RESET + f" repr(bg_color): {repr(bg_color)}" + RESET)
    # """--== Process FG_CODE ==--"""
    if fg_color.strip() == "" or fg_color.strip() == 'normal':
        # ddbug(f"fg_color: [{fg_color}]")
        FG_CODE = ""
    else:
        fg_color = xlate_clr(fg_color)
        # ddbug(fg_color)
        # ddbug(f"fg_color: [{fg_color}]")
        FG_CODE = ""
        fg_rgb_substring = re.search(r".*rgb\((.*?)\).*", fg_color)
        if fg_rgb_substring:
            # found an rgb(...) inclusion
            rgb_color = fg_rgb_substring.group(1)
            r, g, b = rgb_color.split(",")
            FG_RGB_CODE = rgb(r, g, b, prfx=False)  # returns with "m" on it
            # ddbug(f"FG_RGB_CODE: {FG_RGB_CODE}")
            FG_CODE = PRFX + "38" + FG_RGB_CODE  # has "m" on it already
            # ddbug(f"repr(FG_CODE): {repr(FG_CODE)}")
        else:
            # ddbug(f"fg_color: [{fg_color}]")
            # if PRFX in fg_color or PRFX2 in fg_color or fg_color == "":
            if PRFX in fg_color or PRFX2 in fg_color:
                FG_CODE = fg_color
            else:
                # ddbug(f"fg_color: [{fg_color}]")
                if " on" in fg_color:
                    # ddbug("this is should never happen right?")
                    fg_color = fg.replace(" on", "")
                # ddbug(f"fg_color: [{fg_color}]")
                fg_color = fg_color.strip()
                # dbug(f"fg_color: [{fg_color}]")
                # dbug(f"fg_colors_d[fg_color]: {repr(fg_colors_d[fg_color])}")
                FG_CODE = PRFX + fg_colors_d[fg_color] + "m"  # fg_colors do not need "38"
    # ddbug(f"Test fg_color: [{fg_color}] {RESET}{FG_CODE}This should be in assigned fg_color {RESET}Here is the repr(FG_CODE): {repr(FG_CODE)}")
    # """--== Process BG ==--"""
    # ddbug(f"bg_color: {bg_color}")
    if bg_color.strip() == "":
        BG_CODE = ""
    else:
        # bg_color is not blank
        bg_color = xlate_clr(bg_color)
        # ddbug(bg_color)
        bg_rgb_substring = re.search(r".*rgb\((.*?)\).*", bg_color)
        if bg_rgb_substring:
            rgb_color = bg_rgb_substring.group(1)
            r, g, b = rgb_color.split(",")
            BG_RGB_CODE = rgb(r, g, b, bg=False, prfx=False)  # returns with "m" on it
            # ddbug(f"repr(BG_RGB_CODE): {repr(BG_RGB_CODE)}")
            BG_CODE = PRFX + "48" + BG_RGB_CODE  # has "m" on it already
            # ddbug(f"repr(BG_CODE): {repr(BG_CODE)}")
        else:
            # bg_color is not an rgb color
            # ddbug(f"bg_color: {bg_color}")
            if PRFX in bg_color or PRFX2 in bg_color or bg_color == "":
                BG_CODE = bg
            else:
                # bg_color is not pre-CODED
                # dbug(bg)
                if bg == "dim black":
                    # hey, it's ugly, but it works the way I want
                    BG_RGB_CODE = rgb(0, 0, 0, bg=True, prfx=False)
                    BG_CODE = PRFX + "48" + BG_RGB_CODE  # has "m" on it already
                else:
                    # bg_color is not == dim black
                    bg_color = bg_color.strip()
                    # dbug(bg_color, 'ask')
                    BG_CODE = bg_colors_d[bg_color]
                    # ddbug(f"repr(BG_CODE): {repr(BG_CODE)}")
                    BG_CODE = PRFX + BG_CODE + "m"  # understood to be BG so "48" not needed
                    # ddbug(f"Testing repr(BG_CODE): {repr(BG_CODE)} {BG_CODE} TEST TEXT {RESET}")
                    # dbug('ask')
    # ddbug(f"Test bg_color: [{bg_color}] {RESET}{BG_CODE}This should be in assigned bg_color {RESET}Here is the repr(BG_CODE): {repr(BG_CODE)}" + RESET)
    # """--== SEP_LINE ==--"""
    CODE = STYLE_CODES + FG_CODE + BG_CODE
    # clr_tst(CODE, color=color)
    rtrn = CODE + text
    if " " in STYLE_CODES + FG_CODE + BG_CODE:
        ddbug("WWWWWWWWWWWWHHHHHHHHHHHHAAAAAAAAAAAATTTTTTTTTTT")
        rtrn = STYLE_CODES.replace(" ", "")
        rtrn = FG_CODE.replace(" ", "")
        rtrn = BG_CODE.replace(" ", "")
    if "on" in rtrn:
        dbug("Problem: found 'on' in rtrn", 'ask')
    if reset_b:
        # dbug(reset_b)
        rtrn = rtrn + RESET
    # ddbug(f"color: {color} repr(rtrn)): {repr(rtrn)} rtrn: {rtrn} This should be in rtrn color" + RESET)
    return rtrn
    # ### EOB def gclr(color='normal', text=""): ### #


def gclr_demo(*args, **kwarg):
    """
    purpose: brief demo of using gclr()
    options: none
    returns: None
    notes:   none
    """
    print("There are several ways to print color ....\n")
    """--== SEP_LINE ==--"""
    color = "red"
    msg = f"This is: [{color}] color here [/]"
    print("  =============== This:")
    print(msg)
    print(f"  --------------- using printit({msg}) this prints out as: ")
    printit(msg)
    """--== SEP_LINE ==--"""
    color = "red!"
    msg = f"This is: [{color}] color here [/]"
    print("  =============== This:")
    print(msg)
    print(f"  --------------- using printit({msg}) this prints out as: ")
    printit(msg)
    """--== SEP_LINE ==--"""
    color = "red on yellow"
    msg = f"This is: [{color}] color here [/]"
    print("  =============== This:")
    print(msg)
    print(f"  --------------- using printit({msg}) this prints out as: ")
    printit(msg)
    """--== SEP_LINE ==--"""
    color = "bold red on bold yellow"
    msg = f"This is: [{color}] color here [/]"
    print("  =============== This:")
    print(msg)
    print(f"  --------------- using printit({msg}) this prints out as: ")
    printit(msg)
    # dbug('ask')
    """--== SEP_LINE ==--"""
    color = "white! on red!"
    msg = f"This is: [{color}] color here [/]"
    print("  =============== This:")
    print(msg)
    print(f"  --------------- using printit({msg}) this prints out as: ")
    printit(msg)
    """--== SEP_LINE ==--"""
    print("  =============== This:")
    r = 180
    g = 40
    b = 220
    print(f'"my"  + gclr("rgb({r}, {g}, {b})") +  "msg is rgb({r}, {g}, {b})" + gclr("reset") + " and back to normal"')
    print("  --------------- prints out as: ")
    print("my " + gclr(f'rgb({r}, {g}, {b})') + f"msg is rgb({r}, {g}, {b})" + gclr("reset") + " and back to normal")
    """--== SEP_LINE ==--"""


def clr_tst(CODE, color="unknown"):
    """
    purpose: This is strictly for developer testing
        strickly for developer use - given an ansi color CODE will display it in a way to see if it works as expected
        displays COLOR_TEST: This should be displayed using CODE
    returns: None
    """
    if not CODE.startswith(PRFX):
        dbug(f"clr_tst(CODE, color='unknown') - apprently CODE does not seem like a color CODE... returning...")
        return
    from inspect import (getframeinfo, currentframe, getouterframes)
    cf = currentframe()
    fname = str(getframeinfo(currentframe().f_back).function)
    msg = " called from line: ["+str(cf.f_back.f_lineno) + " Func:" + fname + "] "
    SAMPLE_CODE = '\x1b[38;2;0;0;255m\x1b[47m'
    sample_txt = f"{RESET}COLOR TEST: {repr(SAMPLE_CODE)}{SAMPLE_CODE}    This should be displayed using SAMPLE_COLOR    {RESET}{repr(RESET)}"
    print(sample_txt)
    print("-----------------------------------")
    sample_txt = f"{RESET}COLOR TEST: {repr(CODE)}{CODE}    This should be displayed in color: {color}    {RESET}{repr(RESET)}"
    print(sample_txt)
    print(f"------{msg}-------")
    # ### EOB def clr_tst(CODE, color="unknown"): ### #


def shades(color, num=16):
    """
    purpose: returns a list of increasing intensity color shades
    requires = color: str
    options:
    -   num=16  <-- number to divide into 255 ~ the number of color intensities
    -   rtrn???  TODO return codes or text... CODES | strings/text/txt
    returns list # of ncreasing colors
    """
    fg_color = color
    bg_color = ""
    if " on " in color:
        fg_color = color.split()[0]
        bg_color = color.split()[2]
    colors = []
    start  = 40
    step = (255 - start) // num
    for shade in range(start, 255, step):
        if fg_color.lower() == 'red':
            my_color = f'rgb({shade}, 0, 0)'
        if fg_color.lower() == 'green':
            my_color = f'rgb(0, {shade}, 0)'
        if fg_color.lower() == 'blue':
            my_color = f'rgb(0, 0, {shade})'
        if fg_color.lower() == 'yellow':
            my_color = f'rgb({shade}, {shade}, 0)'
        if fg_color.lower() in ('cyan', 'green-blue', 'blue-green'):
            my_color = f'rgb(0, {shade}, {shade})'
        if fg_color.lower() in ('violet', 'magenta'):
            my_color = f'rgb({shade},0,{shade})'
        if fg_color.lower() in ('white', 'magenta'):
            my_color = f'rgb({shade},{shade},{shade})'
        if bg_color != "":
            my_color += " on " + bg_color
        colors.append(my_color)
    return colors


def rgb(r=80, g=80, b=140, text="", fg=False, bg=False, prfx=False, reset=False):
    """
    purpose: translated rgb(r,g,b) text into ansi color CODE
    input: r, g, b, text
        prfx: bool = False
        bg: bool = False # if set to true the color is applied to bg
    returns: rgb color coded text
    """
    # ddbug(f"r: {r} g: {g} b: {b}")
    # PRFX = "\033["
    PRFX = "\x1b["
    RESET = PRFX + "0m"
    # global PRFX
    # number = 16 + 36 * r + 6 * g + b
    # dbug(f"{PRFX}{number}m{number}")
    rtrn = ""
    fgbg_num = ""
    if fg and not bg:
        fgbg_num = 38
    if prfx and not fg and not bg:
        fgbg_num = 38
    r = int(r)
    g = int(g)
    b = int(b)
    if bg:
        fgbg_num = 48
    if prfx:
        rtrn += f"{PRFX}{fgbg_num};2;{r};{g};{b}m"
        # ddbug(f"adding proper prefix rtrn={rtrn}")
    else:
        # user will probably want to prefix this with a ";"
        if fgbg_num == "":
            rtrn += f";2;{r};{g};{b}m"
        else:
            rtrn += f"{fgbg_num};2;{r};{g};{b}m"
    # dbug(f"my color {rtrn} is this and my text: {text}")
    if not reset:
        RESET = ""
    if len(text) > 0:
        rtrn += text + RESET
    # dbug(f"rtrn: {rtrn}")
    # ddbug(f"Returning repr(rtrn): {repr(rtrn)}")
    return rtrn
    # ### EOB def rgb(r=80, g=80, b=140, text="", fg=False, bg=False, prfx=False, reset=False): ### #


def xlate_clr(color, *args, **kwargs):
    """
    purpose: translates special color names to rgb(r,g,b) for processing
    requires: special color eg:
    - greyXX | grayXX  # where XX is a precent gradient of gray from 0,0,0 for black! to 255,255,255 white
    - white!           # solid 255,255,255 white
    - black!           # solid 0,0,0 black
    - red!             # solid bright 255,0,0 red
    - green!           # solid bright 0,255,0 green
    - blue!            # solid bright 0,0,255 blue
    - blue!            # solid bright 0,0,255 blue
    - blue!            # solid bright 0,0,255 blue
    - yellow!          # solid bright 255,255,0 yellow
    - magenta!         # solid bright 255,0,255 magenta
    - cyan!            # solid bright 0,255,255 cyan
    returns: rgb(r,g,b) text string instead of supplied color
    """
    # """--== Debugging ==--"""
    # dbug(color)
    # """--== Config ==--"""
    rgb_b = bool_val(["all", "rgb"], args, kwargs, dflt=False)
    # --== Xlate special colors to rgb() ==--
    grey_tone = re.search(r"(gr[ea]y)(\d+)", color)
    if grey_tone:
        grey_word = grey_tone[1]
        grey_tone = grey_tone.group(2)
        # ddbug(f"grey_word: {grey_word} grey_tone: {grey_tone}")
        # grey = f"rgb({grey_tone}, {grey_tone}, {grey_tone})"
        # dbug(f"Found grey in color: {color}")
        # color = re.sub(r"gr[ea]y(\d+)", grey, color)
        r = g = b = int(grey_tone)
        grey_color = f"rgb({r}, {g}, {b})"
        color = re.sub(f"{grey_word}{grey_tone}", grey_color, color)
        # ddbug(f"grey_color: {grey_color} TEST {RESET} repr(grey_color): [{repr(grey_color)}] {RESET} repr(color): {repr(color)} {RESET}")
    # """--== SEP_LINE ==--"""
    rgx = re.search(r"gr[ea]y", color)
    # If it is just "grey" or "gray"
    if rgx:
        # dbug(f"color: {color}")
        r = g = b = 100
        rgb_color = f"rgb({r},{g},{b})"
        color = re.sub(r"gr[ea]y", rgb_color, color)
        # dbug(f"repr(color): {repr(color)}")
    # dbug(f"color: {color} repr(color): {repr(color)} text: {text}")
    if 'bold' in color:
        color = color.replace("bold", "").strip() + "!"
    if 'white!' in color:
        r = g = b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('black!', myrgb)
    if 'black!' in color:
        r = g = b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('black!', myrgb)
    if 'red!' in color:
        r = 255
        g = 0
        b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('red!', myrgb)
    if 'green' in color:
        # doing this because the defailt green is more of a washed out brown
        r = 0
        g = 215
        b = 0
    if 'green!' in color:
        r = 0
        g = 255
        b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('green!', myrgb)
    if 'blue!' in color:
        r = 0
        g = 0
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('blue!', myrgb)
    if 'yellow!' in color or 'bold yellow' in color:
        r = 255
        g = 255
        b = 0
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('yellow!', myrgb)
    if 'magenta!' in color:
        r = 255
        g = 0
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('magenta!', myrgb)
    if 'cyan!' in color:
        r = 0
        g = 255
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('cyan!', myrgb)
    if 'white!' in color:
        r = 255
        g = 255
        b = 255
        myrgb = f"rgb({r},{g},{b})"
        color = color.replace('white!', myrgb)
    if rgb_b:
        if "white" == color:
            r = 255
            g = 255
            b = 255
            myrgb = f"rgb({r},{g},{b})"
            color = color.replace('white!', myrgb)
        if "black" == color:
            r = 40
            g = 40
            b = 40
            myrgb = f"rgb({r},{g},{b})"
            color = color.replace('white!', myrgb)
        if "red" == color:
            r = 205
            g = 0
            b = 0
            myrgb = f"rgb({r},{g},{b})"
            color = color.replace('white!', myrgb)
        if "green" == color:
            r = 0
            g = 205
            b = 0
            myrgb = f"rgb({r},{g},{b})"
            color = color.replace('white!', myrgb)
        if "blue" == color:
            r = 0
            g = 0
            b = 205
            myrgb = f"rgb({r},{g},{b})"
            color = color.replace('white!', myrgb)
        if "cyan" == color:
            r = 0
            g = 255
            b = 255
            myrgb = f"rgb({r},{g},{b})"
            color = color.replace('white!', myrgb)
        if "magenta" == color:
            r = 255
            g = 0
            b = 255
            myrgb = f"rgb({r},{g},{b})"
            color = color.replace('white!', myrgb)
    return color



# #################
def sub_color(clr, *args, **kwargs):
    # #############
    """
    purpose: substiture ansi color CODE for given color
    returns ansi-CODE
    """
    # dbug(funcname())
    # dbug(f"clr: {clr} repr(clr): {repr(clr)}")
    rset_b = bool_val(['reset', 'rst', 'rset'], args, kwargs, dflt=False)
    PRFX = "\x1b["
    # PRFX2 = "\033["
    if isinstance(clr, list):
        # dbug(f"Submitted clr: {clr} should be a string... returning...")
        new_clr_l = []
        for my_clr in clr:
            my_clr_code = sub_color(my_clr)
            # dbug(repr(my_clr_code))
            new_clr_l.append(my_clr_code)
        # dbug(repr(new_clr_l))
        return new_clr_l
    if clr.startswith(PRFX):
    # dbug("clr starts with PRFX")
        return clr
    RESET = PRFX + "0m"
    if rset_b and clr == "":
        return RESET
    # if PRFX in clr or PRFX2 in clr or clr == "":
    #     dbug(clr)
    #     return clr
    clr = escape_ansi(clr)
    # dbug(clr)
    if clr.upper() == "RESET" or clr.upper() == "NORMAL":
        # dbug(clr)
        return RESET
    # dbug(clr)
    COLOR_CODE = gclr(text="", color=clr)
    # dbug(f"clr: {clr} COLOR_CODE [test]: {COLOR_CODE}[test] {repr(COLOR_CODE)}{RESET}")
    return COLOR_CODE


RESET = gclr("reset")
BLACK = gclr("rgb(0,0,0)")


# ###############################
def wrapit(sentence, length=20, *args, **kwargs):
    # ###########################
    """
    purpose: turns line(s) into a list of strings with full words less than or equal to length
    input is sentence which can be a string or list
    returns lines from a list text wrapped using specified length and colorize text if stipulated
    NOTE: all color codes will get stripped out text before processing
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(f"sentence: [{sentence}] length: {length}")
    # dbug(length)
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    length = kvarg_val(["width", "w", "length", "l"], kwargs, dflt=length)
    color = kvarg_val(["color", "clr"], kwargs, dflt="")
    # """--== Init ==--"""
    if length < 1:
        dbug(f"length: {length} is a problem")
    # """--== Convert ==--"""
    if isinstance(sentence, str):
        # dbug("string")
        if "\n" in sentence:
            sentence_l = sentence.split("\n")
        else:
            sentence_l = [sentence]
    # dbug(sentence_l)
    if isinstance(sentence, list):
        new_lines = []
        for line in sentence:
            line = line.rstrip()
            line = line.rstrip("\n")
            if "\n" in line:
                my_lines = line.split("\n")
                new_lines.extend(my_lines)
            else:
                new_lines.append(line)
        sentence_l = new_lines
    # """--== Process ==--"""
    # dbug(length)
    # maxof_sentence = maxof(sentence, 'len')  # debugging
    # dbug(maxof_sentence)
    # dbug(type(sentence))
    # dbug(sentence)
    sentence = escape_ansi(sentence)
    RESET = COLOR = ""
    if color != "":
        COLOR = sub_color(color)
        RESET = sub_color('reset')
    import textwrap
    wrapper = textwrap.TextWrapper(width=length)
    lines = []
    for line in sentence_l:
        maxof_line = maxof(line)
        if maxof_line > length:
            lines.extend(wrapper.wrap(text=line))
        else:
            lines.append(line)
    if color != "":
        lines = [f"{COLOR}{line}{RESET}" for line in lines]
    # maxof_lines = maxof(lines)  # debugging
    # dbug(maxof_lines)
    # dbug(lines)
    return lines
    # ###      s1 = [      s1 = [ EOB def wrapit(sentence, length=20, color="", *args, **kwargs): ### #


def wrapit_demo(*args, **kwargs):
    """
    purpose: demo of using wrapit
    returns: None
    """
    s1 = ["This is line one and it is small"]
    s = "This is line one and it is small"
    boxed(s1, 'prnt', length=20)
    ruleit(20)
    # boxed(s, 'prnt', length=20)
    # ruleit(20)


def get_columns(*args, **kwargs):
    """
    gets screen/terminal cols OR rows
    returns int(columns)| int(rows: bool) | int(cols), int(rows) both: bool
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    shift = kvarg_val("shift", kwargs, dflt=0)
    rows_b = bool_val("rows", args, kwargs, dflt=False)
    both_b = bool_val("both", args, kwargs, dflt=False)
    # """--== Init ==--"""
    columns = 80
    # rows = 40
    # """--== Validate ==--"""
    if not isinstance(shift, int):
        shift = 0
    # """--== Process ==--"""
    try:
        num_rows, columns = os.popen("stty size", "r").read().split()
    except Exception as e:
        print(f"Error: {e}")
    # print(f"returning columns: {columns}")
    if rows_b:
        return int(num_rows)
    if both_b:
        return int(columns), int(num_rows)
    columns = int(columns)
    # dbug(columns)
    # dbug(shift)
    columns = columns + int(shift)
    # dbug(f"Returning columns: {columns}", 'ask')
    return int(columns)
    # ### EOB def get_columns(*args, **kwargs): ### #


def replace_all(msg, with_d):
    """
    purpose: replaces every string in a dict key with dict value in a string
        with_d eg: {'\t', '  ', 'foo', 'bar'}
    example use could be to replace foul words with less offensive terms
    returns: str 
    TODO need more doc info here
    """
    for i, j in with_d.iteritems():
        msg = msg.replace(i, j)
    return msg


# ##############################################################################
def boxed(msgs, *args, cornerchr="+", hchr="=", vchr="|", padmin=1, color="", title="", footer="", style="single", shadow=False, **kwargs):
    # ##########################################################################
    """
    purpose: draw a unicode box around msgs
    args: msgs
    options:
        centered | center: bool  # centers box on the screen
        prnt: bool
        txt_center: int | list | tuple  # num of lines from top to center in the box - if list or tuple lines between first int and second int (inclusive) will be centered
        txt_right: int | list | tuple   # num of lines from top to justify to the right within the box- if list or tuple lines between first int and second int (inclusive) will be right justified
        color: str  # text color
        box_color: str  # color of border
        title, footer: str # goes in topline or bottom line centered of box
        width forces the width size defaults to # screen columns
        shadowed | shadow: bool # adds a shadow right and bottom
        ... some other options; see below
    returns boxed lines: list
    NOTES: this function does not print - it returns the box lines
    """
    # dbug(funcname())
    # dbug(msgs)
    # dbug(args)
    # dbug(kwargs)
    # reset = "\x1b[0m"
    # from math import ceil
    # dbug(footer)
    # """--== Config ==--"""
    # center = kvarg_val('center', kwargs, dflt=False)
    centered_b = bool_val(["centered"], args, kwargs, dflt=False)
    prnt = bool_val(['prnt', 'print'], args, kwargs, dflt=False)
    shadowed_b = bool_val(["shadow", "shadowed"], args, kwargs, dflt=False)
    txt_center = kvarg_val(["txt_center", "text_center", 'center_txt', 'cntr_txt'], kwargs, dflt=0)
    txt_right = kvarg_val(["txt_right", "text_right", 'right_txt', 'rght_txt'], kwargs, dflt=0)
    # dbug(txt_center)
    # if isinstance(center, int) and center > 0:
        # txt_center = center
    # dbug(txt_center)
    title = kvarg_val(['title'], kwargs, dflt=title)
    box_color = kvarg_val(['bclr', 'box_color', 'border_color', 'box_clr', 'border_clr'], kwargs, dflt="")
    # dbug(box_color)
    shadow = kvarg_val(['shadow', 'shadowed'], kwargs, dflt=shadow)
    pad = kvarg_val(['pad'], kwargs, dflt=" ")
    # dbug(pad)
    top_pad = kvarg_val("top_pad", kwargs, dflt=0)  # "semi" (ie " ") blank lines to add at top
    bottom_pad = kvarg_val(["bottom_pad", "bot_pad", "botpad"], kwargs, dflt=0)  # "semi" (ie " ") blank lines to add to the bottom
    width = kvarg_val(["width", "w", "length", "l"], kwargs, dflt=0)
    # """--== Init ==--"""
    if "%" in str(width):
        width = width.replace("%", "")
        scr_cols = get_columns()
        # dbug(scr_cols)
        width = int(scr_cols * (int(width)/100))
        # dbug(width)
    lines = []
    PRFX = "\x1b["
    box_chrs = get_boxchrs(box_style=style)
    # tl = top left         = box_chrs[0]
    # hc = horz char        = box_chrs[1]
    # tr = top right        = box_chrs[2]
    # vc = vert char        = box_chrs[3]
    # rs = right separator  = box_chrs[4]
    # ms = mid sep          = box_chrs[5]
    # bl = bot left         = box_chrs[6]
    # bs = bot sep          = box_chrs[7]
    # br = bot right = box_chrs[0
    tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br = box_chrs
    pad = gclr(color) + str(pad)
    # """--== Validate ==--"""
    if isempty(msgs):
        dbug(f"msgs appears to be None or empty... msgs: {msgs}")
        return None
    # if not isinstance(top_pad, int):
    #    top_pad = 0
    # if not isinstance(bottom_pad, int):
        # bottom_pad = 0
    # """--== Convert ==--"""
    if isinstance(msgs, pd.DataFrame):
        msgs = printit(msgs, 'noprnt')
    if isinstance(msgs, list):
        new_msgs = []
        for msg in msgs:
            # Get rid of completely blank lines - leave it if it has even a space in it
            # dbug(f"\n[msg]")
            # ruleit()
            # dbug(nclen(msg))
            if nclen(msg) == 0:
                continue
            new_msgs.append(msg)
        msgs = new_msgs
    if len(msgs) < 1:
        # dbug(f"msgs: {msgs} appears empty... returning...")
        return
    if isinstance(msgs, int) or isinstance(msgs, float):
        msgs = str(msgs)
    if "\n" in str(msgs):
        msgs = msgs.splitlines()
        # dbug(f"msgs: {msgs}")
    if isinstance(msgs, str):
        if '\t' in msgs:
            msgs = msgs.replace('\t', '  ')
        # dbug(f"msgs: {msgs} type(msgs): {type(msgs)}")
        if '\n' in msgs:
            msgs = msgs.split('\n')
            # dbug(msgs)
        else:
            # cast it to list
            msgs = [msgs]
            # dbug(msgs)
    if isinstance(msgs, list):
        msgs = [str(x) for x in msgs]
        msgs = [msg.replace('\t', '  ') for msg in msgs if msg != ""]  # this took a while to figure out!
        # for msg in msgs:
        #     dbug(f"[{msg}]")
    # """--== Process ==--"""
    max_msg_len = 0
    maxof_msgs = maxof(msgs)
    # dbug(maxof_msgs)
    max_msg_len = maxof_msgs
    # for msg in msgs:
        # # dbug(msg)
        # if nclen(msg) > max_msg_len:
            # max_msg_len = nclen(msg)
    if nclen(title) > max_msg_len:
        # if len(title) is longer than max_msg_len...
        max_msg_len = nclen(title)
    if nclen(footer) > max_msg_len:
        # if len(footer) is longer than max_msg_len...
        max_msg_len = nclen(footer)
    # dbug(max_msg_len)
    columns = get_columns()
    # dbug(width)
    if width == 0:
        # dbug(width)
        reduce_by = 6
        if shadow:
            reduce_by += 2
        if max_msg_len >= int(columns):
            max_msg_len = int(columns) - reduce_by
        width = (max_msg_len + 2 + (2 * padmin))  # or declared which makes max_msg_len = width - 2 - (2 * padmin)
        if width >= int(columns):
            width = int(columns) - reduce_by
    msg = title
    # dbug(width)
    topline = gline(width, lc=tl, rc=tr, fc=hc, title=title, center=True, box_color=box_color, color=color)
    # dbug(topline)
    lines.append(topline)
    new_lines = []
    # """--== SEP LINE ==--"""
    for m in msgs:
        # dbug(nclen(m))
        # dbug(width)
        working_width = (width - 4)
        # dbug(working_width)
        if nclen(m) > (width - 4) and m is not None:
            # dbug(width)
            wrapped_lines = wrapit(m, length=int(working_width), color=color)  # I discovered that the -x is needed for extra measure
            # maxof_wrapped_lines = maxof(wrapped_lines)
            # dbug(maxof_wrapped_lines)
            # dbug(wrapped_lines)
            if wrapped_lines is not None:
                for line in wrapped_lines:
                    if line is not None:
                        new_lines.append(line)
        else:
            # dbug(f"m: [{m}]")
            new_lines.append(m)
    # """--== SEP LINE ==--"""
    # dbug(lines)
    if top_pad > 0:
        for n in range(top_pad):
            # adds semi blank lines at the top... spaces are needed because other functions will drop completely blank lines
            # this can be useful if you gcolumize boxes and then want to combine them into another 'parent' box
            # dbug(f"top line pad requested top_pad: {top_pad}")
            new_lines.insert(0, "   ")
    if bottom_pad > 0:
        for n in range(bottom_pad):
            new_lines.append("    ")
    for cnt, msg in enumerate(new_lines):
        just = 'left'
        # if txt_center:
            # center = 99
        if txt_center != 0:
            # if isinstance(txt_center, int) and cnt < txt_center:
                # if center is a number then center every line less than int(center)
                # doline_center = True
            cntr_start = 0
            if isinstance(txt_center, int):
                cntr_end = txt_center
            if isinstance(txt_right, (list, tuple)):
                cntr_start = txt_center[0]
                cntr_end = txt_center[1]
            if cnt >= cntr_start and cnt <= cntr_end:
                just = 'center'
                msg = msg.strip()
        # else:
            # doline_center = False
        if txt_right != 0:
            rght_start = 0
            if isinstance(txt_right, int):
                rght_end = txt_right
            if isinstance(txt_right, (list, tuple)):
                rght_start = txt_right[0]
                rght_end = txt_right[1]
            if cnt >= rght_start and cnt <= rght_end:
                just = 'right'
                msg = msg.strip()
        if msg.startswith(PRFX) and not msg.endswith(RESET):
            # dbug(repr(RESET))
            msg = msg + RESET
        # dbug(repr(msg))
        # dbug(f"msg: {msg}")
        # dbug(pad)
        # line = gline(width, lc=vc, rc=vc, fc=" ", pad=pad, msg=msg.replace("\n", ""), box_color=box_color, center=doline_center, color=color)
        line = gline(width, lc=vc, rc=vc, fc=" ", pad=pad, msg=msg.replace("\n", ""), box_color=box_color, just=just, color=color)
        # dbug(line)
        # dbug(repr(line))
        lines.append(line)
    # bottomline = doline(width, echrs=[bl, br], hchr=hc, footer=footer, box_color=box_color, color=color, center=True)
    bottomline = gline(width, lc=bl, rc=br, fc=hc, footer=footer, box_color=box_color, color=color, center=True)
    lines.append(bottomline)
    # dbug(lines)
        # lines = shadowed(lines)
    # dbug(centered_b)
    lines = printit(lines, 'noprnt', centered=centered_b, shadowed=shadowed_b)
    if prnt:
        printit(lines)
    return lines
    # ### EOB def boxed(msgs, *args, ..., **kvargs): ### #


def boxed_demo(*args, **kwargs):
    """
    purpose: boxed function test
    options: none
    return None
    """
    print()
    options_msg = "\noptions include = 'prnt', 'centered', box_clr='red on black'"
    boxed("This is just a test of the boxed function" + options_msg, 'prnt', 'centered', box_clr="red on black", title=options_msg.replace("\n", ""), footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    cmd = "lsb_release -a"
    out = run_cmd(cmd)
    options_msg = "\noptions include: 'prnt', 'centered',box_clr='yellow! on black'"
    my_box = boxed(out + options_msg, 'prnt', 'centered', title=f"output from run_cmd({cmd})", footer=dbug('here'), box_clr="yellow on black")
    options_msg += ", txt_center=99, shadowed=True"
    my_box = boxed(out + options_msg, 'prnt', 'centered', txt_center=99, title=options_msg.replace("\n", ""), footer=dbug('here'), box_clr="yellow! on black", shadowed=True)
    options_msg += ", txt_center=(0,1), shadowed=True, txt_right=(3,99)"
    my_box = boxed(out + options_msg, 'prnt', 'centered', txt_center=(0,1), txt_right=(3,99), title=options_msg.replace("\n", ""), footer=dbug('here'), box_clr="yellow! on black", shadowed=True)


# ##################################
def gline(width=0, *args, **kwargs):
    # ##############################
    """
    purpose: prints a line with msg with lots of options 
    options:
        - width: int,     # first argument
        - msg|title: str  # default=""  msg has to be a key=val pair! eg: gline(60, msg="My Message", just='center')
        - fc: str         # default=" " fill string/character (char(s) used to fill all surrounding space default: lc=rc=fc)
        - lc: str         # default=fc  left/edge/corner (char(s) for left corner ie first charater(s))
        - rc: str         # default=lc  right/edge/corner (char(s) for right corner ie last charcter(s))
        - pad: str        # default=""  string/character(s) on each side of msg
        - lpad: str       # default=pad
        - rpad: str       # default=lpad
        - box_color: str
        - color: str
        - lfill_color: str
        - rfill_color: str
        - just: str       # default = "left"|"l" but can be declared "center"|"c" or 'right'|"r"
        - prnt: bool      # prints the output
    returns: line: str
    notes: this is used in boxed and other functions
    """
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # if "TEST" in msg:
    # dbug(f"msg: [{msg}]")
    # """--== Config ==--"""
    msg = kvarg_val(['msg', 'title', 'footer'], kwargs, dflt="")
    # dbug(repr(msg))
    # dbug(width)
    width = kvarg_val(['width', 'length'], kwargs, dflt=width)
    # dbug(width)
    fc = kvarg_val(['fc', 'fill_chr', 'hc', 'fill'], kwargs, dflt=" ")
    lc = kvarg_val(['lc', 'ec', 'echr'], kwargs, dflt=fc)
    rc = kvarg_val(['rc', 'tr', 'br', 're'], kwargs, dflt=lc)
    box_color = kvarg_val(['box_color'], kwargs, dflt="")
    # color = kvarg_val(['color'], kwargs, dflt="reset")
    color = kvarg_val(['color'], kwargs, dflt="")
    # dbug(f"Config... color: [{color}color_coded]{sub_color('reset')})")
    pad = kvarg_val(['pad'], kwargs, dflt="")
    lpad = kvarg_val(['lpad'], kwargs, dflt=pad)
    lfill_color = kvarg_val(['lfill_color'], kwargs, dflt=color)
    rpad = kvarg_val(['rpad'], kwargs, dflt=pad)
    rfill_color = kvarg_val(['rfill_color'], kwargs, dflt=color)
    # the order here for just is important
    just = kvarg_val(["just", "justification"], kwargs, dflt='ljust')
    # dbug(f"msg: {msg} just: {just}")
    centered = bool_val(["centered", "center"], args, kwargs, dflt=False)
    if centered:
        # change just to 'center' - the bool val centered get ignored after this
        just = 'c'
    just = kvarg_val(['ljust'], kwargs, dflt=just)
    just = kvarg_val(['rjust'], kwargs, dflt=just)
    prnt = bool_val(["print", "prnt", "show", "verbose"], args, kwargs, dflt=False)
    # """--== Validate ==--"""
    # if not isinstance(width, int):
    #     width = 0
    # """--== Init ==--"""
    if "%" in str(width):
        width = width.replace("%", "")
        scr_cols = get_columns()
        # dbug(scr_cols)
        width = int(scr_cols * (int(width)/100))
        # dbug(width)
    RESET = sub_color('reset')
    msg = str(msg)  # deals with int, floats, bool, etc
    llen = 0
    rlen = 0
    # """--== Process ==--"""
    if color == "":
        color = 'reset'
    COLOR = sub_color(color)
    if box_color == "":
        box_color = 'reset'
    BOX_COLOR = sub_color(box_color)
    LFILL_COLOR = sub_color(lfill_color)
    RFILL_COLOR = sub_color(rfill_color)
    # """--== color_coded??? ==--"""
    # color_coded = False
    # if re.search(r"\[.+?\].+\[/]", str(msg)):
    #     # dbug(f"msg: {msg} appears to be color_coded")
    #     color_coded = True
    # if color_coded:
    msg = clr_coded(msg)
    # """--== EOB ==--"""
    if nclen(msg) > 0:
        # nc_msg = escape_ansi(msg)
        msg = lpad + msg + RFILL_COLOR + rpad
        # dbug(f"msg: [{msg}]")
    msg_len = nclen(msg)
    flen = width - msg_len - len(rc) - len(lc)
    # dbug(f"msg: {msg} just: {just}")
    if just in ('center', "c"):
        llen = rlen = (flen // 2)
        diff = flen - (llen + rlen)
        rlen += diff
        # dbug(f"just: {just} width: {width} msg_len: {msg_len} diff: {diff} =  flen: {flen} - ( llen: {llen} - rlen: {rlen} )")
    if just in ('ljust', 'left', 'l'):
        # llen = len(lpad)
        llen = 0  # lpad has already been applied
        rlen = flen  # - len(rpad)  # ???? not sure about this.... 20220803
        # dbug(f"just: {just} width: {width} msg_len: {msg_len}  llen: {llen} = len(lpad): {len(lpad)}  rlen: {rlen} = flen: {flen} - len(lpad): {len(lpad)} len(rpad): {len(rpad)}")
    if just in ('rjust', 'right', 'r'):
        rlen = 0
        llen = flen
    if nclen(msg) > 0:
        # dbug(repr(msg))
        if fc == ' ':  # then treat it as a pad... use COLOR instead of BOX_COLOR
            # dbug(f"{RESET}repr(BOX_COLOR): [{repr(BOX_COLOR)}] repr(COLOR): [{repr(COLOR)}] fc: [{fc}] rc: [{rc}] msg: [{msg}] repr(LFILL_COLOR): [{repr(LFILL_COLOR)}] rlen: {rlen} repr(RFILL_COLOR): [{repr(RFILL_COLOR)}]")
            #     dbug(f"msg: [{msg}]")
            line = RESET + BOX_COLOR + lc + RESET + LFILL_COLOR + (fc * llen) + msg + RFILL_COLOR + (fc * rlen) + RESET + BOX_COLOR + rc + RESET
            # dbug(f"line: [{line}]")
        else:
            # dbug(f"{RESET}BOX_COLOR: " + BOX_COLOR + "box color " + RESET + "COLOR: " + COLOR + f"color fc: [{fc}] msg: [{msg}]")
            # line = BOX_COLOR + COLOR + lc + (fc * llen) + msg + BOX_COLOR + (fc * rlen) +  RESET + rc + RESET
            line = RESET + BOX_COLOR + lc + (fc * llen) + COLOR + msg + BOX_COLOR + (fc * rlen) + rc + RESET
        # dbug(repr(line))
    else:
        line = RESET + BOX_COLOR + lc + (fc * llen) + (fc * rlen) + rc + RESET
    if prnt:
        print(line)
    # dbug(f"repr(color): {repr(color)} repr(box_color): {repr(box_color)}  line: [{line}]")
    return line
    # ### EOB def gline(width=0, *args, **kwargs): ### #


def gtitle(width=40, msg="", fc="=", *args, **kwargs):
    """
    purpose: quick-n-dirty Title/Separation Line - I use this just to separate sections
    required:
    options:
        - centered: bool
        - boxed: bool
    returns: prints a line with "=" fill character and msg in the middle (centered) with width=width
    see: gline_demo
    """
    # """--== Config ==--"""
    centered_b = bool_val(["centered", "center", "cntr"], args, kwargs, dflt=False)
    boxed_b = bool_val(["boxed", "box"], args, kwargs, dflt=False)
    # """--== Process ==--"""
    line = gline(width, msg=msg, just="c", fc=fc, *args, prnt=False, **kwargs)
    printit(line, centered=centered_b, boxed=boxed_b)
    # ### EOB def gtitle(width, msg, fc="=", *args, **kwargs): ### #


def gline_demo(*args, **kwargs):
    """
    purpose: demo of using gline()
    returns: None
    """
    # """--== Init ==--"""
    width = 80
    msg = "gline test message"
    box_color = "white on black"
    color = 'cyan!'
    sepline = lambda width, msg: gline(width, msg=msg, just="c", fc="=", prnt=True)
    # """--== Process ==--"""
    sepline(80, " sep line - all will be width=80 ")
    print(gline(80, msg=" simple title line ", just="c", fc="="))
    print(gline(80, msg, fc="*", just="c", lc="[", rc="]"))
    print(gline(80, msg, lfill="-", rfill="-", just="r", pad="_pad_", lc="[", rc="]"))
    print(gline(80, msg=msg+" w/lc and rc declared", lc="(--", rc="--)"))
    print(gline(80, msg=msg+" w/lc and rc declared just=center", lc="(--", rc="--)", just="c"))
    print(gline(80, lc="|", msg=msg + " w/colors", pad="", rc="|", box_color='red', color='black', lfill_color='blue', rfill_color="yellow"))
    sepline(80, " sep line ")
    # """--== SEP_LINE ==--"""
    lines = []
    lines.append(gline(width, lc="+", rc="+", fc="-", title=" [white! on black]top line quick-n-dirty DIY box[/] ", center=True, box_color=box_color, color=color))
    lines.append(gline(width, lc="|", rc="|", fc=" ", title=msg, just='c', box_color=box_color, color=color))
    lines.append(gline(width, lc="+", rc="+", fc="-", title=" [white! on black]my bottom line[/] ", center=True, box_color=box_color, color=color))
    printit(lines)
    sepline(80, " sep line ")
    # """--== SEP_LINE ==--"""
    ruleit(width=80)
    sepline(80, " sep line ")
    # """--== SEP_LINE ==--"""
    printit("gline is used to create boxes", 'boxed', footer=dbug('here'), txt_center=99, title="End of gline demo", box_clr="white! on black")


# #############
class MenuBox:
    # #########
    """
    purpose:
        sets up a menu selection box
        executes selected function and arguments
        quits (returns) on "Enter" "Q" or "q"
    arguments:
        bclr: box color eg "reb" "blue" "green"
        clines: number of lines to center in the box
        center: center menu default is True
    methods:
        add_selection(["selection_name", func, arg1, arg2,...])  # needs an entry for arg(s) even if it is ''
        show()
    useage:
        mainmenu = Menu("Main")
        mainmenu.add_selection(["get statistics", get_stats, f"{symbol}"])
        mainmenu.add_selection(["display_chart", do_chart, f"{symbol}"])
        mainmenu.add_selection(["display_chart", run_fun, ""])
        ans = ""
        while ans is not None:
            ans = mainmenu.show()
    notes: consider using gselect() instead of this. Your choice.
    """
    def __init__(self, name):
        self.name = name
        self.title = ""  # default: f"Menu: {self.name}"
        self.selections = {}
        self.msgs = []
        self.cnt = 0
        self.clines = 2
        self.bclr = ""
        self.center = True
    # """--== SEP_LINE ==--"""
    def add_selection(self, selection):
        # selection should be [ "title", func, arg1, arg2, arg3, ... ]
        # dbug(f"selection: {selection}")
        # dbug(f"selection[0]: {selection[0]}")
        # self.selections[selection[0]] = selection[1]
        if isinstance(selection, str):
            selection = selection.split(",")
        if not isinstance(selection, list):
            dbug(f"Selection submission must be a list with ['name', func, 'arg1', 'arg2', ..] selection: {selection}")  # noqa:
            sys.exit()
        else:
            if len(selection) < 3:
                dbug(f"Too few items in selection - must be > 2 you submitted [{len(selection,)}] selection: {selection}")  # noqa:
                sys.exit()
        self.cnt += 1
        self.selections[str(self.cnt)] = selection
    # """--== SEP_LINE ==--"""
    def show(self):
        self.title = f"Menu: {self.name}"
        msgs = []
        msgs.append(f"{self.title}")
        msgs.append("=" * nclen(self.title))
        # dbug(f"self.selections: {self.selections}")
        cnt = 0
        for selection in self.selections:
            cnt += 1
            # dbug(f"selection: {selection}")
            item = self.selections[selection][0]
            # dbug(f"item: {item} type(item): {type(item)}")
            # dbug(f"type(self.selections[selection][2:],): {type(self.selections[selection][2:],)}: {self.selections[selection][2:]}",)  # noqa:
            cmd = self.selections[selection][1]
            arguments = self.selections[selection][2:]
            # if len(arguments) == 1:
            #     dbug(f"cmd: {cmd} arguments: {arguments}")
            # dbug(f"cmd: {cmd} arguments: {arguments}")
            msgs.append(f"{cnt}. {item}")
            # cmd(*arguments)
        printit(centered(boxed(msgs, center=2, bclr=self.bclr)))
        # if center:
        #     printit(centered(boxed(msgs, center=2, bclr="red")))
        # else:
        #     printit(boxed(msgs, center=2, bclr="red"))
        ans = input(printit("Please select:  ", center=True, prnt=False))
        if ans.upper() == "Q" or ans == "":
            return None
        item = self.selections[ans][0]
        cmd = self.selections[ans][1]
        arguments = self.selections[ans][2:]
        # dbug(arguments)
        # dbug(arguments)
        # dbug(*arguments)
        if arguments[0] == '':
            cmd()
        else:
            if "ask" in arguments[0]:
                arguments = input("Please enter arguments: ")
            # dbug(arguments)
            # dbug(*arguments)
            cmd(*arguments)
        return ans


def isnumber(x, *args, **kwargs):
    """
    purpose: determines if x is a number even if it is a percent, or negative, or is 2k or 4b or 10M etc
             or test for stricktly float
    options:
        - float:  bool  # is this a float
        - human:  test the submission after stripping off "human" symbols like "M" or "G" or "%" etc
    input: x: str|float|int
    returns: True|False
    notes: tests... pos, neg, floats, int, scientific, B(illion), T(trillions), G(ig.*) Kb(ytes|its), Mb(ytes)
        Can be used on financial data which often includes M(illions) or B(illions) if human option included
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # dbug(repr(x))
    # dbug(type(x))
    # """--== Config ==--"""
    float_b = bool_val(["flt", "float"], args, kwargs, dflt=False)
    human = bool_val(["human", "H", "h"], args, kwargs, dfault=False)
    # """--== Validate ==--"""
    if x is None:
        # dbug(x)
        return False
    # """--== Process ==--"""
    x = escape_ansi(x)  # strip off any ansi codes/color codes
    if human:
        x = re.sub("[GMK%e]", "", str(x))
    if float_b:
        try:
            float(x)
            return True
        except ValueError:
            return False
    x = escape_ansi(x).strip()
    # dbug(x)
    x = str(x).strip()
    if x.startswith(("-", "+")):
        x = x.lstrip(r"[+-]")
    x = x.replace('.', '', 1).replace(",", "").replace("e-", "", 1)  # .replace("%", "", 1)
    # dbug(repr(x))
    r = x.isdigit()
    # dbug(f"Returning: {r}")
    return r
    # ### EOB def isnumber(x, *args, **kwargs): ### #


def isnumber_demo(*args, **kwargs):
    """
    purpose: test/demo of using isnamber()
    returns: None
    """
    numbers = [-1.003456, -0.3456, "44,56", "22%", "4,56G", "-", "four"]
    for num in numbers:
        dbug(f"num: {num} isnumber(num): {isnumber(num)}")
        # num = re.sub("[MGK%]", "", str(num))
        dbug(f"num: {num} isnumber(num): {isnumber(num, 'human')} with 'human' option")


# ###################################################
def get_boxchrs(box_style="single", *args, **kwargs):
    # ###############################################
    """
    purpose: given a box_style (ansi, single, solid, double) will return a set of chars for creating a box
    input: box_style: str
    return:
        [tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br]  as a list in the order shown
    Note: boxed() uses this
        tl = top_left, hc=horizontal_char, ts=top_separator, tr=top_right, vc=vertical_char,
        ls=left_separator, rs=right_separator, ms=middle_separator
        bl=bottom_left, bs=bottom_sep, br=bottom_right
    """
    box_color = kvarg_val("box_color", kwargs, dflt="")
    reset = sub_color('reset')
    box_chrs = [9484, 9472, 9516, 9488, 9474, 9500, 9508, 9532, 9492, 9524, 9496]
    if box_style == 'none':
        box_chrs = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
    if box_style == 'ascii':
        box_chrs = ["+", "=", "=", "+", "|", "|", "|", "|", "+", "=", "+"]
    if box_style == "single":
        # box_chrs = [tl, hc, ts, tr, vc, le, re, ms, bl, bs, br]
        box_chrs = [9484, 9472, 9516, 9488, 9474, 9500, 9508, 9532, 9492, 9524, 9496]
    if box_style == "solid":
        box_chrs = [9487, 9473, 9523, 9491, 9475, 9507, 9515, 9547, 9495, 9531, 9499]
    if box_style == "double":
        box_chrs = [9556, 9552, 9574, 9559, 9553, 9568, 9571, 9580, 9562, 9577, 9565]
    box_chrs = [chr(n) for n in box_chrs]
    if box_color != "":
        # you should avoid this becuase every char gets wrapped with color codes
        box_chrs = [box_color + c + reset for c in box_chrs]
    # tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br = box_chrs
    return box_chrs


def flattenit(my_l):
    """
    purpose: "flattens nested lists
    options: none
    returns: list
    """
    flatlist = []
    for elem in my_l:
        # dbug(f"Working on elem: {elem}")
        if type(elem) == list:
            # dbug(f"flattening elem: {elem}")
            flatlist += flattenit(elem)
        else:
            flatlist.append(elem)
        # dbug(f"Now flatlist: {flatlist}", 'ask')
    # dbug(flatlist)
    return flatlist
    # ### EOB def flattenit(my_l): ### #


# #####################################
def fixlol(my_lol=[], *args, **kwargs):
    # #################################
    """
    purpose: makes the length or every "row" in a list of lists the same number of elements (length)
    options:
        - length: int        # defaults to the length of the first row ie len(my_lol[0])
        - blank: str|None    # defaults to None but can be any string eg blank="..."
        - transpose|pivot: bool   # default=False - if set true the lol will be transposed or pivoted before returning
    returns: fixed lol with all rows the same length (number of elements)
    used by gtable with option "fix"
    """
    length = len(my_lol[0])  # or what is declared
    length = kvarg_val(["len", "length"], kwargs, dflt=length)
    length = int(length)
    blanks = kvarg_val(["blank", "blanks", "pad"], kwargs, dflt=None)
    pivot = bool_val(["pivot", "transpose", "pvt"], args, kwargs, dflt=False)
    # """--== Process ==--"""
    my_lol = [row[:length] for row in my_lol]  # truncate first
    # now pad each row with None
    for num, row in enumerate(my_lol):
        while len(row) < length:
            my_lol[num].append(blanks)
    if pivot:
        # list(map(list, zip(*msg_l))  # to pivot??? need to research this TODO
        transposed = list()
        for i in range(len(my_lol[0])):
            row = list()
            for sublist in my_lol:
                row.append(sublist[i])
            transposed.append(row)
        my_lol = transposed
    return my_lol
    # ### EOB def fixlol(my_lol=[], *args, **kwargs): ### #


# ###################################
def cnvrt2lol(data, *args, **kwargs):
    # ###############################
    """
    purpose: accepts any type of "data" (ie str|list|pandas|list of dictionaries|csv_file_name etc) and converts to a list of lists (ie lol)
    options:
        - colnames: list|str  # list of colnames or string eg: "firstline"|"firstrow" declares that the firstrow is already the colnames
        - delimeter: char     #  if a filename is supplied (assumes a csv type file) this delimiter will be used to separate column values
        - fix: bool           # will "fix" all the rows of an lol to the length of the first row (be careful with this)
        - blanks: str|None    # default=None blanks sets the string for elements added in row when fix option is used
        - index: bool         # default=False
        - purify: bool        # default=True - strips off comments (purifies based on the '#' symbol) before processing
        - selected: list      # list of colnames to include
        - sortby: str         # colname to sort on
        - filterby: dict      # dictionary with {'colname': 'pattern'}
        - cols_limit: int      # sets max column size
    returns: a list of lists (rows of columns) with the first row having colnames
    notes: problem if a "#" is in a line, it will truncate it as it thinks the ramaining is a comment # TODO need to fix this
    """
    # TODO add filterby (dict {colname: pattern}) and sortby|orderby
    # """--== SEP_LINE ==--"""
    # dbug(funcname())
    # dbug(type(data))
    # if isinstance(data, dict): dbug(x_items(data, 5))
    # dbug(data)
    # if isinstance(data, list): dbug(data[:2])
    # dbug(args)
    # dbug(kwargs)
    # """--== Import ==--"""
    # import pandas as pd
    # """--== Config ==--"""
    colnames = kvarg_val(["colnames"], kwargs, dflt=[])
    # idx_b = kvarg_val(["colnames"], kwargs, dflt=[])  # TODO
    # hdr_b = kvarg_val(["hdr"], kwargs, dflt=[])
    delimiter = kvarg_val(["delim", "delimiter"], kwargs, dflt=",")
    fix_b = bool_val("fix", args, kwargs, dflt=False)
    blanks = kvarg_val(["blank", "blanks"], kwargs, dflt=None)
    index_b = bool_val(["indx", 'index', "indexes"], args, kwargs, dflt=False)
    # dbug(index_b)
    purify_b = bool_val(["purify", "purify_b", "decomment"], args, kwargs, dflt=True)
    selected_cols = kvarg_val(["selected_cols", "selected", "fields", "cols", 'select'], kwargs, dflt=[])  # TODO
    filterby = kvarg_val(["filterby"], kwargs, dflt={})  # TODO
    sortby = kvarg_val(["sortby", "orderby"], kwargs, dflt="")  # TODO
    col_limit = kvarg_val(["col_limit", 'col_size', 'col_max', "collimit", "colmax"], kwargs, dflt=0)
    ci_b = bool_val(["case_insensitive", "ci", "ignore_case", "ic"], args, kwargs, dflt=False)
    # """--== Init ==--"""
    lol = []
    # lol = data
    # add_colnames_flag = False
    """--== Validate ==--"""
    if isempty(data):
        dbug("data: {data} appears to be empty... returning...")
        return
    # """--== Convert ==--"""
    if isinstance(data, pd.DataFrame):
        # dbug(f"This is a DataFrame data: {data.head(3)}")
        df = data  # now df = data I really don't like this TODO
        indexname = df.index.name
        if not isempty(indexname) and "date" in indexname.lower():
            df.reset_index(inplace=True)  # turn the index into first column
        # dbug(indexname)
        if isempty(indexname):
            df.index.name = "id"
            indexname = df.index.name
            if index_b:
                df = df.reset_index()
        # dbug(indexname)
        if len(colnames) == 0:
            colnames = list(df.columns)
            colnames.insert(0, indexname)
        else:
            df.columns = colnames
        # dbug(df, 'boxed')
        if index_b:
            df = df.reset_index()
            df.columns = colnames
            # dbug(df)
            colnames.insert(0, indexname)
        else:
            df = df.reset_index(drop=True)  # avoid using inplace=True
        # """--== rubber hits the road here ==--"""
        lol = df.values.tolist()  # rubber hits the road
        # dbug(lol[:3])
        """--== add colnames ==--"""
        if colnames != "done":
            # dbug(colnames)
            colnames = list(df.columns)
            # dbug(colnames)
            lol.insert(0, colnames)
            colnames = "done"
            # dbug(lol[:2])
    # dbug(colnames)
    # dbug(type(lol))
    # dbug(lol)
    # """--== deal with dict ==--"""
    if isinstance(data, dict):
        # dbug("data is a dictionary")
        if isinstance(colnames, str) and colnames in ("keys"):
            colnames = list(lol.keys())
        my_vals = list(data.values())
        if not isinstance(my_vals[0], dict) and not isinstance(my_vals[0], list):
            # we tested val[0] to makes sure this is not a dictionary (dol) of lists or of dictionaries (dod)
            # dbug(f"so this must be a simple dictionary. colnames: {colnames}")
            # dbug(lol)
            if len(colnames) == len(data):
                # dbug("looks like user wants to add a row for colnames: {colnames}")
                # lol = [colnames, my_vals]
                data = [my_vals]  # colnames will get added as row one later
                # dbug(lol)
            else:
                # dictionary and we probably want to list the keys in column 1 and the values in col 2
                my_lol = []
                if colnames == []:
                    my_lol = [["Key", "Value"]]
                n = 0
                for k, v in data.items():
                    if n == 0 and isinstance(colnames, str) and colnames in ("firstrow", "firstline", "first_row", "first_line"):
                        colnames = [k, v]
                    else:
                        my_lol.append([k, v])
                    n += 1
                # lol = [list(lol.keys()), list(lol.values())]
                lol = my_lol
        if isinstance(lol, dict):
            # if we still have a dictionary (ie it did not get changed to an lol above)
            mylol = []
            for k, v in lol.items():
                mylol.append([k, v])
            # lol = list(lol.items())
            lol = mylol
    # dbug(lol[:3])
    # """--== deal with str ==--"""
    if isinstance(data, str):
        # dbug(data)
        # dbug(type(data))
        # dbug(delimiter)
        # dbug(purify_b)
        rows_lol = cat_file(data, delim=delimiter, purify=purify_b)
        # dbug(rows_lol[:3])
        # dbug('ask')
        if len(colnames) == 0:
            colnames = rows_lol[0]
        lol = rows_lol
    # dbug(lol[:3])
    if isempty(lol):
        lol = data
    # dbug(lol[:2])  
    # """--== deal with simple list ==--"""
    if isinstance(lol[0], str) or isinstance(lol[0], int) or isinstance(lol[0], float):
        lol = [(lol)]  # lol maybe a simple list so turn it into an lol with one row
    # """--== deal with numpy's ==--"""
    if 'ndarray' in str(type(lol)):
        # import numpy as np
        lol = lol.tolist()
    # """--== make sure we have colnames ==--"""
    if len(colnames) > 0 and colnames != "done":
        if colnames != lol[0]:
            if isinstance(colnames, list):
                lol.insert(0, colnames)
                colnames = "done"
    # dbug(f"Returning lol: {lol[:3]}")
    if fix_b:
        lol = fixlol(lol, blanks=blanks)
    if filterby != {}:
        if not isinstance(filterby, dict) or len(filterby) != 1:
            dbug(f"filterby: {filterby} must be a dictionary of (one key: value pair) " + "{colname: pattern\} ... returning")
            return None
        for k, v in filterby.items():
            filterby_col = k
            filterby_pattern = v
        if not filterby_col in lol[0]:
            dbug(f"filterby_col: {filterby_col} not found in colnames ie lol[0]: {lol[0]}")
        else:
            filterby_i = lol[0].index(filterby_col)  # filterby col index number
            if filterby_i is None:
                dbug(f"Failed to find filterby_col: {filterby_col} in hrd: {lol[0]}")
            # filterby_pattern = list(filterby_d.values())[0]
            pat = ""  # default: non-regex
            # """--== convert filterby ==--"""
            pat = filterby_pattern  # now we have a regex search
            # """--== process ==--"""
            new_lol = []
            # filterby_str = filterby_str.lower()
            for row in lol:
                elem = str(row[filterby_i])
                # dbug(f"chkg searching elem: {elem} for pat: {pat}")
                match_results = re.search(pat, elem,)
                if ci_b:
                    match_results = re.search(pat, elem, re.IGNORECASE)
                # if re.search(pat, elem):
                if match_results:
                    new_lol.append(row)
                    continue
            if len(new_lol) == 0:
                dbug(f"No matching records found using pattern: {filterby_pattern} on column: {filterby_col}", centered=centered)
                return None
            new_lol.insert(0, lol[0])
            lol = new_lol
    # dbug(lol[:2])
    if selected_cols != []:
        # dbug("do selected cols only and add them in order specified")
        new_lol = [[ln[lol[0].index(i)] for i in selected_cols] for ln in lol]
        # dbug(new_lol)
        lol = new_lol
    #     dbug("do filterby must be a dictionary of {colname: pattern}")
    #     dbug("fo sortby - string, colname to sortby should ideally allow ascending and decending")
    # """--== sortby ==--"""
    if sortby != '':  #  or sortby_n != "":
        # this was first in gtable because it may sort on a colname that will get removed in next blocks
        # if sortby_n != "":
            # sortby = sortby_n
        sortby_i = lol[0].index(sortby)
        # dbug(len(lol[0]))
        # dbug(sortby_i)
        hdr = lol[0]
        my_lol = lol[1:]
        if isinstance(sortby, int):
            sortby_i = int(sortby)
            # dbug(sortby_i)
        if isinstance(sortby, str):
            # dbug(hdr)
            sortby_i = hdr.index(sortby)
            # dbug(f"sortby: {sortby} sortby_i: {sortby_i}")
            # dbug(sortby_i)
        else:
            sortby_i = int(sortby)
            # dbug(sortby_i)
        # if sortby_n != "":
            # # dbug(rows)
            # rows = sorted(rows, key=lambda x: float(x[sortby_i]))
        # else:
        # dbug(my_lol[:2])  # hdr has been pulled above
        # gtable(lol[:3], 'prnt', title="debugging", footer=dbug('here'))
        # dbug(sortby)
        # dbug(sortby_i)
        if isnumber(my_lol[0][sortby_i]):
            my_lol = sorted(my_lol, key=lambda x: x[sortby_i])
        else:
            my_lol = sorted(my_lol, key=lambda x: str(x[sortby_i]).lower())
        lol = [hdr] + my_lol
        # """--== EOB ==--"""
    if int(col_limit) > 0:
        new_lol = []
        for row in lol:
            new_row = [col[:int(col_limit)] for col in row]
            new_lol.append(new_row)
        lol = new_lol
    # dbug(f"Returning lol[:3]: {lol[:3]}")
    return lol
    # ### EOB def cnvrt2lol(data, *args, **kwargs): # ###


def cnvrt2lol_demo(*args, **kwargs):
    """
    purpose: demo cnvrt2lol
    returns: None
    """
    # dbug(funcname())
    # """--== SEP_LINE ==--"""
    import pandas as pd
    # import pandas.testing
    # """--== SEP_LINE ==--"""
    #
    this_lol = [
               ['Ralph', 22, 183, 'M'],
               ['Jane', 53, 126, 'F'],
               ['John', 37, 158, 'yes'],
               ['Jackson', 50, 185, 'no']]
    # dbug(this_lol)
    df = pd.DataFrame(this_lol)
    # dbug(df, 'boxed', title="df contents")
    # dbug(df.head(), 'boxed', title="df contents")
    """--== TEST ==--"""
    " filterby "
    raw_data_box = boxed(df, title=f"raw data type: {type(df)}", box_clr="white on black")
    # printit(df, 'boxed', title="df contents")
    # printit(f"cnvrt2lol options: {options}", 'boxed', footer=dbug('here'))
    colnames = ["col0", "col1", "col2", "col3"]
    selected = ["col0", "col2"]
    filterby = {'col0': "Jane|Ral"}
    cnvrt2lol_options = f"colnames={colnames}, selected={selected}, filterby: {filterby}"
    lol = cnvrt2lol(df, colnames=colnames, selected_cols=["col0", "col2"], filterby=filterby)
    cnvrted_box = boxed(lol, title="cnvrt2lol data", box_clr="white on black")
    gtable_options = "'hdr', 'boxed',..."
    gbox = gtable(lol, 'hdr', 'noprnt', title=f"gtable options: {gtable_options}", footer=dbug('here'))
    gcolumnize([raw_data_box, cnvrted_box, gbox], 'prnt', 'boxed', title=f"cnvrt2lol_options: {cnvrt2lol_options}", footer=dbug('here'))
    dbug('ask')
    gtitle(80, "--== SEP_LINE ==--", fc="-")
    # """--== SEP_LINE ==--"""
    """--== SEP_LINE ==--"""
    raw_data_box = boxed(df, title=f"raw data type: {type(df)}", box_clr="white on black")
    # printit(df, 'boxed', title="df contents")
    options = "none"
    # printit(f"cnvrt2lol options: {options}", 'boxed', footer=dbug('here'))
    lol = cnvrt2lol(df)
    cnvrted_box = boxed(lol, title="cnvrt2lol data", box_clr="white on black")
    gbox = gtable(lol, 'noprnt', title="gtable options: ", footer=dbug('here'))
    gcolumnize([raw_data_box, cnvrted_box, gbox], 'prnt', 'boxed', title=f"cnvrt2lol options: {options}", footer=dbug('here'))
    dbug('ask')
    gtitle(80, "--== SEP_LINE ==--", fc="-")
    # """--== SEP_LINE ==--"""
    colnames = ["col0", "col1", "col2", "col3"]
    options = f"colnames={colnames}"
    # printit(f"cnvrt2lol options: colnames={colnames}", 'boxed', footer=dbug('here'), box_clr="white! on black")
    lol = cnvrt2lol(df, colnames=colnames)
    cnvrted_box = boxed(lol, title="cnvrt2lol data", box_clr="white on black")
    gbox = gtable(lol, 'noprnt', 'hdr', title="gtable options: hdr", footer=dbug('here'))
    gcolumnize([raw_data_box, cnvrted_box, gbox], 'prnt', 'boxed', title=f"cnvrt2lol options: {options}", footer=dbug('here'))
    dbug('ask')
    gtitle(80, "--== SEP_LINE ==--", fc="-")
    # """--== SEP_LINE ==--"""
    index = True
    df_box = boxed(df)
    options = f"index={index}"
    # printit(f"cnvrt2lol options: index={index}", 'boxed', footer=dbug('here'))
    lol = cnvrt2lol(df, index=index)
    gbox = gtable(lol, 'noprnt', 'hdr', title="gtable options: hdr", footer=dbug('here'))
    gcolumnize([raw_data_box, cnvrted_box, gbox], 'prnt', 'boxed', title=f"cnvrt2lol options: {options}", footer=dbug('here'))
    dbug('ask')
    gtitle(80, "--== SEP_LINE ==--", fc="-")
    # """--== SEP_LINE ==--"""
    df_colnames = ['name', 'age', 'weight', 'gender']
    options = f"colnames={df_colnames}"
    # lines = printit(df, 'noprnt')
    raw_data_box = boxed(df, title=f"raw data type: {type(df)} ", footer=dbug('here'), box_clr="white on black")
    lol = cnvrt2lol(df, colnames=df_colnames)
    cnvrted_data_box = boxed(lol, title="cnrt2lol data")
    gbox = gtable(lol, 'noprnt', 'hdr', title="tablized cnvrt2lol data", footer=dbug('here'))
    gcolumnize([raw_data_box, cnvrted_box, gbox], 'prnt', 'boxed', title=f"cnvrt2lol options: {options}", footer=dbug('here'))
    dbug('ask')
    gtitle(80, "--== SEP_LINE ==--", fc="-")
    # """--== SEP_LINE ==--"""
    """--== selected_cols ==--"""
    raw_data_box = boxed(df, title=f"raw data type: {type(df)}", box_clr="white on black")
    # printit(df, 'boxed', title="df contents")
    # printit(f"cnvrt2lol options: {options}", 'boxed', footer=dbug('here'))
    colnames = ["col0", "col1", "col2", "col3"]
    selected = ["col0", "col2"]
    cnvrt2lol_options = f"colnames={colnames}, selected={selected}"
    lol = cnvrt2lol(df, colnames=colnames, selected_cols=["col0", "col2"])
    cnvrted_box = boxed(lol, title="cnvrt2lol data", box_clr="white on black")
    gtable_options = "'hdr', 'boxed',..."
    gbox = gtable(lol, 'hdr', 'noprnt', title=f"gtable options: {gtable_options}", footer=dbug('here'))
    gcolumnize([raw_data_box, cnvrted_box, gbox], 'prnt', 'boxed', title=f"cnvrt2lol_options: {cnvrt2lol_options}", footer=dbug('here'))
    dbug('ask')
    gtitle(80, "--== SEP_LINE ==--", fc="-")
    # """--== SEP_LINE ==--"""
    dbug(f"Done {funcname()}")
    do_close()


# #########################################################################
def gtable(lol, *args, **kwargs):
    # #####################################################################
    """
    purpose: returns lines or displays a colorized table from a list_of_lists, df, or dictionary
    required:
        - lol: list_of_lists | pandas_data_frame | str: csv_filename # this gives lots of flexibility
    input: rows: str|list|dict|list_of_lists|list_of_dicts|dataframe
    options:
        - color: str,
        - box_style: 'single', 'double', 'solid',
        - box_color: str,
        - header|hdr: bool,  # header | hdr   # highlights the colnames
        - end_hdr: bool      # adds highlighted hdr/colnames to the bottom of the table
        - colnames: list | str,  'firstrow' | 'firstline' | 'keys'
        - col_colors: list,   # gtable will use this list of colors to set each column, repeats if more cols than colors
        - neg: bool | list,
        - nan: str,
        - alt: bool_val,
        - alt_color: str,
        - title: str,
        - footer: str,
        - index: bool,         # default=False
        - box_style: str,
        - max_col_len|col_limit|col_len...: int,  default=100
        - human: bool| list,   # if bool all numbers will get "humanized", if list syntax = [colname, colname...] and ony those colnames will get "humanized"
        - rnd: int | dict,     # if int all numbers will be rounded to rnd value,  if dict syntax is {colname, round_val, colname, round_val}
                                keep in mind if round_val = 0 it will turn that colname into all integers
                                if round > 0 then all the column values will have that many decimal places
        - sortby: str,
        - filterby: dict {'field': 'pattern'}  # Note: the default is to search the column for matches of rows
                                               # where the column "contains" the string/pattern
                                               # NOTE: max_col_len WILL affect this pattern search
        - ci|ic: bool             # will make filterby case insensitive (ci) or ignore case (ic) default=False
        - select_cols: list    # specify which columns to include - table will be in same order
        - excluded_cols: list  # specify which columns to exclude
        - write_csv: str,
        - skip: bool           # tells gtable to skip lines of the wrong length - be careful w/this
        - cell_pad=' ': str    # you can set the padding char(s)
        - strip: bool          # strip all white space off of ever element in every row
        - blanks: str          # you can declare how blank cells (blank elements in a row) should appear
        - fix: bool            # default=False - if true then everry row of the data will be made the length of the first row
        - ignore: bool         # default=False builds the table even if the number of columns is different on the rows - makes it easier to troublshoot
        - cols: int            # split a table into several tables or columns (aka chunks) - very useful with long tables
        - sep: str             # default=" "  this is the string between columns (only effective with the cols option > 1)
        - lol: bool            # default=False - will return the conditioned lol (rows of columns) instead of the default printable lines
        - no_hdr: bool         # removes header/colnames row from the table
        - purify: bool         # default=False - assumes provided data (lol) has all ready been purified
    returns lines: list
    Notes:
        - if colnames="firstrow" then the firstrow will be extracted and used for the header
        - if colnames="keys" and we are passed a dictionary then the colnames will be the dictionary keys
        - TODO: add head: int and tail: in
        - I frequenly use this function for financial data analysis or csv files
    """
    """--== debugging ==--"""
    # dbug(funcname())
    # dbug(lol[:2])
    # dbug(args)
    # dbug(kwargs)
    # dbug(type(lol))
    # dbug(type(lol))
    # """--== Config ==--"""
    color = kvarg_val('color', kwargs, dflt="")
    lfill_color = kvarg_val("lfill_color", kwargs, dflt=color)
    # rfill_color = kvarg_val("rfill_color", kwargs, dflt=color)
    box_color = kvarg_val(['box_color', 'border_color'], kwargs, dflt="bold white on rgb(40,40,40)")
    header = bool_val(['header', 'headers', 'hdr'], args, kwargs, dflt=False)
    end_hdr = bool_val(['end_hdr', "endhdr", 'hdr_last'], args, kwargs, dflt=False)
    # dbug(header)
    # header_color
    header_color = kvarg_val(['header_color', 'hdr_color'], kwargs, dflt="white! on grey40")
    colnames = kvarg_val(["col_names", "colnames"], kwargs, dflt=[])
    # dbug(colnames)
    # NOTE: if colnames (str) in ("firstrow", "first_row", "firstline", "first_line" then use firstline as colnames
    # NOTE: if colnames (str) in ("keys") then use dictionary keys as colnames
    selected_cols = kvarg_val(['selected_cols', 'selectedcols', 'slctd_cols', 'slctdcols', 'select', 'selected'], kwargs, dflt=[])
    # dbug(selected_cols, 'lst')
    # dbug(type(selected_cols))
    # dbug(selected_cols)
    # dbug('ask')
    excluded_cols = kvarg_val(['excluded_cols', 'excludedcols', 'xcld_cols', 'excdcols', 'exclude', 'excluded'], kwargs, dflt=[])
    # dbug(excluded_cols)
    centered = bool_val(['center', 'centered'], args, kwargs, dflt=False)
    shadowed = bool_val(['shadow', 'shadowed'], args, kwargs, dflt=False)
    prnt = bool_val(['prnt', 'print', 'prn'], args, kwargs, dflt=False)
    rjust_cols = kvarg_val(['rjust_cols'], kwargs, dflt=[])
    col_colors = kvarg_val(['col_colors', 'colors', "col_color"], kwargs, dflt=["white!", "cyan", "red", "green", "blue", "red!", "green!", "yellow!"])
    # col_colors = kvarg_val(['col_colors', "col_color"], kwargs, dflt=[])
    title = kvarg_val('title', kwargs, dflt="")
    footer = kvarg_val('footer', kwargs, dflt="")
    index_b = bool_val(['indexes', 'index', 'idx', 'id', 'indx'], args, kwargs, dflt=False)
    box_style = kvarg_val(['style', 'box_style'], kwargs, dflt='single')
    alt_color = kvarg_val(['alt_color', 'alt_clr', "altclr"], kwargs, dflt="on rgb(30,30,30)")
    # alt_color = kvarg_val(['alt_color', 'alt_clr', "altclr"], kwargs, dflt="on rgb(55,25,55)")
    if len(alt_color) > 2 and not alt_color.strip().startswith("on"):
        alt_color = "on " + alt_color
    alt = bool_val('alt', args, kwargs, dflt=False)
    max_col_len = kvarg_val(['max_col', 'max_col_len', 'width', 'col_limit', 'max_limit', 'max_len', 'col_len'], kwargs, dflt=100)
    # dbug(max_col_len)
    wrap_b = bool_val(["wrap", "wrapit"], args, kwargs, dflt=False)
    neg = bool_val('neg', args, kwargs, dflt=False)  # if a list is supplied here the syntax is [colname, colname, colanme...]
    # dbug(neg)
    rnd = kvarg_val(['rnd', 'round'], kwargs, dflt="")
    # dbug(rnd)
    human = bool_val(['h', 'human', "H"], args, kwargs, dflt=False)
    # dbug(human)
    # nan = kvarg_val(['nan'], kwargs, dflt="")
    sortby = kvarg_val(["sortby", "sort_by", "sorton", "sort_on", "sort", 'sorted_by', 'sortedby'], kwargs, dflt='')
    # sortby_n = kvarg_val(["sortbyn", "sort_byn", "sortby_n", "sortby_n", "sort_n"], kwargs, dflt='')
    filterby_d = kvarg_val(['filterby', 'filter_by'], kwargs, dflt={})  # column_to_search: pattern
    ci_b = bool_val(["case_insensitive", "ci", "ignorecase", "ignore_case", "ic"], args, kwargs, dflt=True)
    # ci_b = bool_val(["case_insensitive", "ci"], args, kwargs, dflt=False)
    # rgx_b = bool_val(["rgx", "regex", "exact", 'rgex'], args, kwargs, dflt=False)  # forces a regex search using supplied filterby pattern
    write_csv = kvarg_val(["write_csv", 'csv_file'], kwargs, dflt='')  # write a csv file with gtable data
    write_out = kvarg_val(["write_out", 'out_file'], kwargs, dflt='')  # write table out to file
    cell_pad = kvarg_val(['cell_pad', 'cellpad', 'pad'], kwargs, dflt=' ')
    strip_b = bool_val(['strip'], args, kwargs, dflt=False)
    # delimiter = kvarg_val(["delimiter", "delim"], kwargs, dflt=",")  # only needed if lol is a filename and not the default
    blanks = kvarg_val(["blank", "blanks"], kwargs, dflt="")
    skip = bool_val(['skip'], args, kwargs, dflt=False)  # skip non-compliant lines/rows?
    ignore_b = bool_val(['ignore'], args, kwargs, dflt=False)  # skip non-compliant lines/rows?
    cols = kvarg_val(["cols", "columns", "chunks", "splits"], kwargs, dflt=1)
    sep = kvarg_val(["sep", "separation"], kwargs, dflt="")
    cols_limit = kvarg_val(["cols_limit", "max_cols"], kwargs, dflt=0)
    lol_b = bool_val(["lol", 'data'], args, kwargs, dflt=False)
    rtrn = kvarg_val(["rtrn", "return", "rtrn_type"], kwargs, dflt="")
    if rtrn in ("lol", 'data'):
        lol_b = True
    # reverse_b = bool_val(["rev", "rvsd", "reverse", "reversed"], args, kwargs, dflt=False)  # TODO - ie lol.reverse()
    nohdr_b = bool_val(["nohdr", "no_hdr", "nocolnames"], args, kwargs, dflt=False)  # removes first line (hdr/colnames) from table
    fix_b = bool_val(['fix'], args, kwargs, dflt=False)  # make all rows same number of columns as first row
    # dbug(fix_b)
    purify_b = bool_val(["purify", "purify_b", "decomment"], args, kwargs=False)  # assumes that provided data has already been "purified" ie decommented
    # """--== Validate ==--"""
    if not isinstance(selected_cols, list):
        dbug(f"selected_cols: {selected_cols} must be a list ... please investigate... returning...")
        return
    if not isinstance(filterby_d, dict):
        dbug("filterby must be a dictionary")
        return None
    # dbug(lol[:2])
    if isempty(lol):
        dbug("Submission is empty... returning...")
        return None
    # """--== Init ==--"""
    cell_pad = str(cell_pad)
    RESET = sub_color('reset')
    COLOR = sub_color(color)
    if box_color == "":
        box_color = 'reset'
    BOX_COLOR = sub_color(box_color)
    HEADER_COLOR = sub_color(header_color)
    box_chrs = get_boxchrs(box_style)
    tl, hc, ts, tr, vc, ls, rs, ms, bl, bs, br = box_chrs
    lines = []
    max_elem_len = []  # init... will hold max len for each col
    # cell_pad = " "  # add before and after @ elem - this has to come after sub_color(color)
    max_width = 0
    rnd_l = []
    # """--== Convert to lol ==--"""
    # dbug(f"launching cnvrt2lol with lol: {lol}")
    lol = cnvrt2lol(lol, colnames=colnames, fix=fix_b, indx=index_b, blanks=blanks, purify=purify_b, filterby=filterby_d, ci_b=ci_b, sortby=sortby)
    # dbug(lol[:2])
    if int(cols_limit) > 0:
        lol = [row[:int(cols_limit)] for row in lol]
    if isempty(lol):
        dbug("lol is empty... returning...")
        return None
    hdr = lol[0]  # needed in case end_hdr is called for but not hdr
    # """--== End of Convert ==--"""
    # """--== no header ==--"""
    if nohdr_b:
        lol = lol[1:]
    # """--== ignore lengths of row ==--"""
    if ignore_b:
        # ignore different lengths (num of elems) in rows
        max_num_elems = maxof(lol, 'elems')
        new_lol = []
        for row in lol:
            new_row = []
            for n in range(max_num_elems):
                new_row.append(blanks)
            for n, elem in enumerate(row):
                new_row[n] = elem
            # dbug(new_row)
            # dbug(row)
            new_lol.append(new_row)
        lol = new_lol
    # now lol[0] will be the header names (colnames)
    # """--== Init ==--"""
    max_row_lines = []
    for row in lol:
        max_row_lines.append(1)  # initializes a max_row_lines number for each row default=1
    # """--== change out blanks if desired ==--"""
    if blanks != "":
        new_rows = []
        for row in lol:
            new_row = []
            new_row = [x.replace("", blanks) if x == "" else x for x in row]
            new_rows.append(new_row)
        lol = new_rows
    # """--== get rid of blank rows and condition any elems in each row ==--"""
    new_lol = []
    for row in lol:
        if len(row) == 0:
            continue
        else:
            new_lol.append(row)
        lol = new_lol
    # dbug(lol)
    # """--== Test row lengths ... do columns = num or elems throughout ==--"""
    if isinstance(lol[0], list):
        firstrow_len = len(lol[0])  # this will be the number of columns
        firstrow = lol[0]
        # dbug(f"firstrow_len: {firstrow_len}, lol[0]: {lol[0]}")
    err_cnt = 0
    # dbug([row for row in lol if 'PNC' in row])  # debugging only!
    # """--== Test row lengths (ie num of elems or cols) ... do cols = num or elems throughout ==--"""
    # let's test lol rows to make sure number of col matches
    # dbug(lol[:2])
    for n, row in enumerate(lol, start=1):
        # DO NOT Try to use n as an index for lol[n] <--weird stuff happens!
        if not isinstance(row, list):
            dbug(f"Problem... row: [{row}] is not a list! and it should be")
        # firstrow_len = len(lol[0])  # set above
        # dbug(row)
        # dbug(len(row))
        # dbug(type(lol[n]))
        # dbug(lol[n])
        thisrow_len = len(row)
        if thisrow_len != firstrow_len:  # row_len was set above using the first row
            if skip:
                err_cnt += 1
                dbug(f"Error cnt: {err_cnt}")
                continue
            else:
                # dbug(lol[:2])
                # dbug(row)
                msg = [f"Returning as it looks like row (row num: {n}) has the wrong number of items."]
                msg.append(f"firstrow_len (first row length which all other rows should match): {firstrow_len} len(row) (this row): {thisrow_len}")
                diff = thisrow_len - firstrow_len
                # dbug(diff)
                over_under = "over"
                if diff < 0:
                    over_under = "under"
                msg.append(f"Row number: {n} is {over_under} by: {diff}")
                msg.append("For reference:")
                msg2 = [f"First Row: {firstrow}"]
                msg2.append(f"Row {n}:     {row}")
                msg2_box = boxed(msg2)
                # dbug(msg2)
                msg_box = msg + msg2 + ["Returning .... You might want to consider the 'skip' option "]
                dbug(msg_box, 'boxed', 'centered', 'lst', title=title, footer=footer)
                # dbug('ask')
                # new_d = dict(zip(firstrow, row))
                # gtable(new_d, 'prnt', 'index', title="Zipped lists", footer=dbug('here'))
                # dbug([firstrow_len, thisrow_len])
                max_len = max([firstrow_len, thisrow_len])
                # dbug(max_len)
                # row1_table = gtable(lol[0], 'prnt')
                # rowX_table = gtable(lol[n], 'prnt')
                row_nums = [str(x) for x in range(1, max_len+1)]
                # dbug(row_nums)
                # dbug(firstrow)
                # dbug(row)
                screen_cols = get_columns()
                # dbug(screen_cols)
                firstrow_max_len = maxof(lol[0])
                if maxof(row) > screen_cols - (firstrow_max_len + 15):
                    row_max = screen_cols - (firstrow_max_len + 15)
                    row = [str(elem)[:row_max]+" ..." if nclen(elem) > screen_cols else str(elem) for elem in row]
                gcolumnize([row_nums, firstrow, row], 'prnt', 'centered', 'boxed',
                           cols=3, title="Col#, Firstrow, This Row",
                           footer=dbug('here'), box_clr="red on black!")
                err_table = ["Row#", "Firstrow", "This Row"]
                for num, x in enumerate(row_nums):
                    try:
                        firstrow_elem = firstrow[num]
                    except Exception as Error:
                        firstrow_elem = "..."
                        # dbug(Error)
                    try:
                        row_elem = row[num]
                    except Exception as Error:
                        row_elem = "..."
                        # dbug(Error)
                    my_row = [x, firstrow_elem, row_elem]
                    err_table.append(my_row)
                # dbug(err_table)
                # gtable(err_table, 'prnt', 'hdr', 'centered', title=f"Row with wrong number of elems: {n}", footer=dbug('here'))
                # gcolumnize([len(lol[0]), len(lol[n])], 'prnt', 'centered', cols=2,  footer=dbug('here'))
                # dbug('ask')
                # if diff < 0:
                #     for n in range(diff):
                #         dbug("adding a col='---'")
                #         row.append("---")
                # if diff > 0:
                #     dbug(f"truncating row: {row}")
                #     row = row[:firstrow_len]
                #     dbug(f"Now row: {row}")
                # continue  # TODO debugging only
                # dbug("Problem with len or rows(s_. Returning None...")
                return None
    # dbug(selected_cols)
    # dbug([row for row in lol if 'PNC' in row])
    if err_cnt > 0 and skip:
        dbug(f"Found length issues in {err_cnt} rows")
    # """--== limit length of each elem to max_col_len ==--"""
    new_lol = []
    # dbug(max_col_len)
    for row in lol:
        # truncate elems in each row if needed
        new_row = []
        for elem in row:
            # dbug(f"Working of row: {row}")
            if strip_b:
                # stip off all whitespace
                elem = str(elem).strip()
            if wrap_b:
                # wrap if needed
                if isinstance(elem, str):
                    if max_col_len == 0:
                        max_col_len = 99
                    if nclen(str(elem)) > max_col_len - 5:  # for padding
                        elem = wrapit(elem, length=int(max_col_len - 5))
            if isinstance(elem, dict):
                elem = str(elem)
            if isinstance(elem, list):
                elem = flattenit(elem)  # just in case elem is a nested list
            if isinstance(elem, list):
                # this is a multi_line elem
                new_elem = []
                for item in elem:
                    # should test len(item) here? and wrapit if  needed
                    item = str(item).replace("\n", "")
                    if len(str(item)) > max_col_len:
                        # dbug(max_col_len)
                        item = str(item)[:max_col_len]  # trim it if it is too long
                    new_elem.append(item)
                if len(new_elem) == 1:
                    new_elem = new_elem[0]
                elem = new_elem
            else:
                # elem is not a list type
                if nclen(elem) > max_col_len:
                    if not isnumber(elem) and not isinstance(elem, dict):
                        elem = elem[:max_col_len]  # trim it if necessary
            new_row.append(elem)
        new_lol.append(new_row)
        # End of loop for adding elems to this row
    lol = new_lol
    # dbug(lol[:3])
    # """--== deal with first row being None ,1 ,2, 3, etc ==--"""
    if lol[0][0] is None:
        # not sure about this yet ... was a df maybe??
        lol = lol[1:]  # drop that first row - assumes second row is colnames
        # Removing element from list of lists
        del_col = 0
        [j.pop(del_col) for j in lol]  # does the drop "in-place"
    # dbug(lol)
    # """--== Local Functions ==--"""
    def bld_row_line(row):
        lfill_color = color
        for col_num, elem in enumerate(row):
            if col_num == 0:
                msg = ""
            mycolor = color  # the default passed as a Config option above
            if col_colors != []:
                # now change mycolor to appropriate col_colors
                color_num = col_num % len(col_colors)
                col_color = col_colors[color_num]
                mycolor = col_color
                myCOLOR = sub_color(col_color)
            if alt:
                # now add in alt color
                line_num = row_num
                if header:
                    line_num = row_num + 1
                if line_num % 2:
                    mycolor = mycolor + " " + alt_color
                    myCOLOR = sub_color(mycolor)
            fill_len = max_elem_len[col_num] - nclen(elem)
            fill = " " * fill_len
            myfill = fill
            mypad = cell_pad
            elem = str(elem)
            if col_num in rjust_cols or isnumber(elem, 'human'):
                # right justify this elem
                justified_elem = myfill + str(elem)
            else:
                # left justify this elem
                justified_elem = str(elem) + myfill
            if col_num + 1 == len(row):
                # last column
                add_this = mypad + justified_elem + mypad
                msg += myCOLOR + add_this
                # marker_line += hc * nclen(add_this)
                rfill_color = mycolor
            else:
                # not the last column
                add_this = mypad + justified_elem + mypad
                msg += myCOLOR + add_this + BOX_COLOR + vc + RESET
                if col_num == 0:
                    lfill_color = mycolor
            if col_num == len(row) - 1:
                # this is the last col_num (column)
                rfill_color = mycolor
                # dbug(f"mycolor: {mycolor} lfill_color: {lfill_color} rfill_color: {rfill_color}")
                line = gline(max_width, lc=vc, msg=msg, pad="", rc=vc, box_color=box_color, color=mycolor, lfill_color=lfill_color, rfill_color=rfill_color)
                lines.append(line)
        return msg
        # ### EOB def bld_row_line(row): ### #
    # """--== Process ==--"""
    if colnames == []:
        colnames = lol[0]
    # dbug(colnames)
    missing_items_l = [item for item in selected_cols if item not in colnames]
    if len(missing_items_l) > 0:
        dbug(f"It appears at least one of the selected_cols: {missing_items_l}\nis not in colnames: {colnames}... please investigate.")
    if len(selected_cols) > 1:
        # dbug(selected_cols, 'ask')
        new_lol = []
        hdr = lol[0]
        hdr_indxs_l = []
        # if index_b:
            # hdr_indxs_l = [0]
            # lol[0][0] = "id"
        for col in selected_cols:
            # uses the order given in selected_cols
            if col in hdr:
                hdr_i = hdr.index(col)
                hdr_indxs_l.append(hdr_i)
                # dbug(f"col: {col} hdr: {hdr} hdr_i: {hdr_i} lol[0][hdr_i]: {lol[0][hdr_i]}")
        for n, row in enumerate(lol):
            # new_row = []
            # dbug(hdr_indxs_l)
            new_row = [row[x] for x in hdr_indxs_l]
            new_lol.append(new_row)
        if len(new_lol) == 0:
            # this is probably because no colnames were supplied and we need to know them
            dbug("Unable to determine colnames for this data: please provide colnames and try again...", 'boxed', 'centered')
            return None
        lol = new_lol
    num_cols = len(lol[0])
    # dbug(len(selected_cols))
    # dbug(num_cols)
    # dbug(lol[:3])
    # dbug(len(lol))
    # """--== excluded_cols ==--"""
    if len(excluded_cols) > 0:
        new_lol = []
        hdr = lol[0]
        hdr_indxs_l = []
        for col in hdr:
            if col not in excluded_cols:
                hdr_i = hdr.index(col)
                hdr_indxs_l.append(hdr_i)
        for row in lol:
            new_row = []
            new_row = [row[x] for x in hdr_indxs_l]
            new_lol.append(new_row)
        lol = new_lol
    num_cols = len(lol[0])
    # dbug(lol[:3])
    new_lol = []
    mycolnames = lol[0]
    # for row in lol[:3]:  # for debugging
    for row in lol:
        # dbug(row)
        new_row = []
        for n, elem in enumerate(row):
            # elem_PRFX = elem_SFX = ""  # init PRFX and SFX
            # dbug(repr(elem))
            elem_CODES = split_codes(elem)  # respect given elem color is provided
            # dbug(f"elem: {elem} elem_CODES: {elem_CODES}")
            elem_PRFX = elem_CODES[0]
            elem_SFX = elem_CODES[1]
            # dbug(repr(elem_PRFX))
            elem = escape_ansi(elem)
            # dbug(f"n: {n} mycolnames[{n}]: {mycolnames[n]}")
            suffix = ""
            if str(elem).endswith("%"):
                elem = elem.strip("%")
                suffix = "%"
            new_elem = elem_PRFX + elem + elem_SFX
            # dbug(new_elem)
            if isnumber(new_elem, 'human'):  # is it a number either human or not
                # dbug(f"new_elem is a number: {new_elem}")
                if 'numpy' in str(type(elem)):
                    import numpy
                    elem = str(elem.item())
                myrnd = ""
                myhuman = ""
                myneg = ""
                """--== rnd? ==--"""
                # dbug(f"elem: {elem} isnumber...")
                if isinstance(rnd, dict):
                    rnd_d = rnd
                    # rnd_l = list(rnd.keys())
                    # dbug(mycolnames[n])
                    if mycolnames[n] in rnd_d:
                        # dbug(f"mycolnames[n]: {mycolnames[n]} is in rnd_l: {rnd_l} with val rnd[mycolnames[n]]: {rnd[mycolnames[n]]}")
                        # elem = cond_num(elem, rnd=rnd[mycolnames[n]])
                        myrnd = int(rnd_d[mycolnames[n]])
                        # elem = round(float(elem), myrnd))
                    else:
                        # dbug(f"Oooops mycolnames[n]: {mycolnames[n]} is not in rnd_l: {rnd_l}")
                        myrnd = ""
                if isinstance(rnd, int):
                    # dbug(rnd)
                    myrnd = rnd
                """--== human? ==--"""
                if isinstance(human, list):
                    # dbug(f"chkg mycolnames[n]: {mycolnames[n]} in human: {human}")
                    if mycolnames[n] in human:
                        myhuman = True
                        # dbug(f"Making myhuman: {myhuman} mycolnames[n]: {mycolnames[n]} n: {n}")
                    else:
                        myhuman = ""
                if isinstance(human, bool) and human:
                    if isnumber(elem):
                        elem = str(elem).replace(",", "")
                        if float(elem) > 1000:
                            myhuman = True
                """--== neg? ==--"""
                if isinstance(neg, list):
                    if mycolnames[n] in neg:
                        myneg = True
                        # dbug(f"neg: {neg} myneg: {myneg} elem: {elem} mycolnames[n]: {mycolnames[n]}")
                    else:
                        myneg = False
                        # dbug(f"neg: {neg} myneg: {myneg} elem: {elem} mycolnames[n]: {mycolnames[n]}")
                if isinstance(neg, bool) and neg:
                    myneg = True
                """--== new_elem ==--"""
                # dbug(f"elem: {elem} myneg: {myneg} mycolnames[n]: {mycolnames[n]} neg: {neg} new_elem: {new_elem}")
                new_elem = cond_num(str(new_elem) + suffix, rnd=myrnd, human=myhuman, neg=myneg)
                # dbug(f"myrnd: {myrnd} myhuman: {myhuman} mycolnames[n: {n}]: {mycolnames[n]} elem: {elem} rnd_l: {rnd_l} human: {human} new_elem: {new_elem}")
            new_row.append(new_elem)
        new_lol.append(new_row)
    lol = new_lol
    # dbug(lol[:6])
    # """--== At this point lol is fully ready??!! ==--"""
    # """--== Recurse if needed ==--"""
    if cols > 1:
        # user wants multiple cols
        # need to break this lol into "chunks" and feed each chunk into gtables - then gcolumnize them TODO
        # a header for each column/table will be assumed here
        hdr = lol[0]  # this is needed for each call to gtable
        lol_no_hdr = lol[1:]
        size = len(lol) // cols
        lols_l = chunkit(lol_no_hdr, size)
        tbls = []
        for lol in lols_l:
            # dbug(hdr)
            # dbug(colnames)
            tbls.append(gtable(lol, 'hdr', colnames=hdr, title=title, footer=footer, neg=neg, human=human, rnd=rnd))
        lines = gcolumnize(tbls, sep=sep)
        scr_cols = int(get_columns())
        max_ln_len = maxof(lines)  # they all should be the same length
        if max_ln_len > scr_cols:
            dbug(f"The length of lines: {max_ln_len} is greater than the available screen columns: {scr_cols}... returning")
            return None
        # printit(lines, 'boxed', title="debugging", footer=dbug('here'))
        # dbug("Returning lines...")
        if prnt:
            printit(lines, centered=centered)
        return lines
    # """--== get max_elem_len[col] length for each col ==--"""
    # Now get max length for each column - in a series of steps using lol[0]
    num_cols = len(lol[0])
    for idx in range(num_cols):
        if not isinstance(lol[0][idx], str):
            hdr_elem = str(lol[0][idx])
        hdr_elem = lol[0][idx]
        # initializes a max_elem_len for each col using row one (lol[0])
        if isinstance(hdr_elem, list):
            hdr_elem = hdr_elem[0]
        else:
            hdr_elem = str(lol[0][idx])
        hdr_elem_len = nclen(hdr_elem)
        max_elem_len.append(hdr_elem_len)
    # dbug(lol[:3])
    new_lol = []
    for row_num, row in enumerate(lol):
        new_row = []
        # for each row in lol... get length
        # calc max_elem_len for each col
        if row == []:
            # skip a blank or empty row
            continue
        for col_num, elem in enumerate(row):
            # for each elem in row
            my_elem = elem
            if not isinstance(elem, list):
                if "\n" in str(my_elem):
                    my_elem = str(elem).split("\n")
            # dbug(elem)
            """--== Is this a muti_line row? ==--"""
            if isinstance(my_elem, list):
                # for measuring length purposes only
                if len(my_elem) > 1:
                    max_row_lines[row_num - 1] = len(elem)  # sets the max_row_lines number to len of my_elem list - makes it multi_line
                    my_elem = max(my_elem, key=len)  # this makes my_elem the longest str in the list
                    if nclen(my_elem) > max_elem_len[col_num]:
                        max_elem_len[col_num] = nclen(my_elem) + 2  # adding some padding
            # now set max_elem_len[col_num] for each elem
            # dbug(f"max_elem_len[{col_num}]: {max_elem_len[col_num]} nclen(str(my_elem)): {nclen(str(my_elem))}")
            # dbug(f"col_num: {col_num} len(lol[0]: {len(lol[0])})")
            if col_num >= len(lol[0]) and skip:
                continue
            if nclen(str(my_elem)) > max_elem_len[col_num]:
                max_elem_len[col_num] = nclen(str(my_elem))  # set max col width
                # dbug(f"elem: {my_elem} len(my_elem): {len(str(my_elem))} max_elem_len[{col_num}]: {max_elem_len[col_num]}")
            new_row.append(elem)
        new_lol.append(new_row)
    lol = new_lol
    # dbug(lol[:3])
    if nclen(title) + 4 > max_width:
        max_width = nclen(title) + 4
    if nclen(footer) + 4 > max_width:
        max_width = nclen(footer) + 4
    # """--== Build Table ==--"""
    for row_num, row in enumerate(lol):
        # line = vc
        # dbug(row)
        msg = ""
        # """--== is this a multi_line row, if so then make it multi_line ==--"""
        if max_row_lines[row_num - 1] > 1:
            # dbug(f"this is a multi_line row... row_num: {row_num} row: {row}")
            # now add needed rows
            elem_line_num = 0  # init
            for add_row_num in range(max_row_lines[row_num - 1]):
                # add new_line rows
                new_row = []  # init
                for elem_num, elem in enumerate(row):
                    # for each elem in row - is it a list type ?
                    if isinstance(elem, list):  # muti-line
                        # start adding multi_line rows...  this is a multi_line elem (it is of list type)
                        # this is a multi_line elem so use the first item in that elem and increment elem_line_num
                        # elem_num_lines[elem_num] = len(elem)
                        # dbug(f"This is a multi_line elem as it is a list. elem: {elem} len(elem): {len(elem)} add_row_num: {add_row_num}")
                        if add_row_num < len(elem):
                            new_elem = elem[add_row_num]
                    else:
                        # elem is not multi_line (ie not a list)
                        if add_row_num > 0:
                            # elem is not type list  and we are past the first row so just add the blank elem
                            new_elem = " "
                        else:
                            elem = str(elem)
                            new_elem = elem[:max_elem_len[elem_num]]
                            elem_line_num = 0
                    new_row.append(new_elem)
                # this is one of the multi_line rows to add - there will be max_row_lines added
                elem_line_num += 1
                last_msg = bld_row_line(new_row)
                # dbug(last_msg)
            # dbug(f"End loop for adding multi_line rows last_msg: {last_msg}")
        # """--== SEP_LINE ==--"""
        if row_num == 0 and header:
            # dbug(f"Working on header row: {row} header: {header}")
            hdr_line = vc
            for col_num, elem in enumerate(row):
                if isinstance(elem, list):
                    msg_len = nclen(max(elem, key=len))  # uses the longes str in a list
                else:
                    msg_len = nclen(elem)
                fill_len = max_elem_len[col_num] - msg_len
                # fill = " " * fill_len
                """--== SEP_LINE ==--"""
                if header:
                    # First row and header is true
                    COLOR = HEADER_COLOR
                    rfill = lfill = " " * ((max_elem_len[col_num] - nclen(elem)) // 2)
                    elem = str(elem)
                    justified_elem = rfill + elem + lfill
                    if nclen(rfill) + nclen(lfill) < fill_len:
                        diff = (fill_len) - (nclen(lfill) + nclen(rfill))
                        diff_fill = " " * diff
                        justified_elem += diff_fill
                    if col_num == len(row) - 1:
                        # column, not the last
                        msg += COLOR + cell_pad + justified_elem + cell_pad
                    else:
                        # last column
                        msg += COLOR + cell_pad + justified_elem + cell_pad + BOX_COLOR + vc
            hdr_line = gline(max_width, lc=vc, msg=msg, pad="", rc=vc, box_color=box_color, color=COLOR, lfill_color=lfill_color)
            lines.append(hdr_line)
            last_msg = msg
            # dbug(last_msg)
        else:
            # not the first row and not header
            msg = ""
            """--== is this a multi_line row, if so then make it multi_line ==--"""
            if max_row_lines[row_num - 1] == 1:
                for col_num, elem in enumerate(row):
                    if col_num == 0:
                        msg = ""
                    mycolor = color  # the default passed as a Config above
                    if col_colors != []:
                        # now change mycolor to appropriate col_colors
                        color_num = col_num % len(col_colors)
                        col_color = col_colors[color_num]
                        mycolor = col_color
                        myCOLOR = sub_color(col_color)
                    else:
                        mycolor = ""
                        myCOLOR = sub_color("")
                    if alt:
                        # now add in alt color
                        line_num = row_num
                        if header:
                            line_num = row_num + 1
                        if line_num % 2:
                            mycolor = mycolor + " " + alt_color
                            myCOLOR = sub_color(mycolor)
                            # dbug(repr(myCOLOR), 'ask')
                    fill_len = max_elem_len[col_num] - nclen(elem)
                    fill = " " * fill_len
                    myfill = fill
                    mypad = cell_pad
                    elem = str(elem)
                    if col_num in rjust_cols or isnumber(elem.strip("%BGMK+-")):
                        # right justify this elem
                        # dbug(f"Right justify elem: {elem}")
                        justified_elem = myfill + str(elem)
                    else:
                        # left justify this elem
                        justified_elem = str(elem) + myfill
                    if col_num + 1 == len(row):
                        # last column
                        add_this = mypad + justified_elem + mypad
                        # dbug(add_this)
                        # dbug(msg)
                        msg += myCOLOR + add_this
                        # dbug(msg)
                        # marker_line += hc * nclen(add_this)
                        rfill_color = mycolor
                        # dbug(msg)
                    else:
                        # not the last column
                        add_this = mypad + justified_elem + mypad
                        # dbug(split_codes(str(elem)))
                        if isnumber(elem, 'human') and 0 :
                            if len(split_codes(elem)[0]) > 0:
                                # is the first_code/prefix_code not empty ie ''
                                # dbug(len(split_codes(elem)[0]))
                                myCOLOR = ""
                        # dbug(f"elem: {elem} myCOLOR: {repr(myCOLOR)} add_this: {add_this} split_codes(elem): {split_codes(elem)}")
                        msg += myCOLOR + add_this + BOX_COLOR + vc + RESET
                        # dbug(msg)
                        if col_num == 0:
                            lfill_color = mycolor
                        # dbug(msg)
                    if col_num == len(row) - 1:
                        # this is the last col_num (column)
                        # dbug(msg)
                        rfill_color = mycolor
                        if len(str(msg)) > 1:
                            last_msg = msg
                        line = gline(max_width, lc=vc, msg=msg, pad="", rc=vc, box_color=box_color, color=mycolor, lfill_color=lfill_color, rfill_color=rfill_color)
                        lines.append(line)
    # """--== marker line ==--"""
    if end_hdr and header:
        lines.append(hdr_line)
    # add a sep_line after this header line
    marker_line = ""
    last_msg = escape_ansi(last_msg)
    for ch in last_msg:
        # we are changing every ch to a hc except vc will get a "@" marker. result eg: -----@---@-------@------
        if ch == vc:
            c = "@"  # This is just an arbitrary marker for proper positioning
        else:
            c = hc
        marker_line += c
    # marker_line = gline(max_width, lc=ls, msg=marker_line, hc=hc, rc=rs, box_color=box_color, color=box_color)  # color=box_color because the msg is part of the box
    marker_line = escape_ansi(gline(max_width, msg=marker_line, fc=hc, lc=tl, rc=tr))
    marker_line = marker_line[1:-1]  # strip off beginning and ending vc
    # """--== sep_line ==--"""
    sep_line = marker_line.replace("@", ms)
    sep_line = gline(max_width, lc=ls, msg=sep_line, hc=hc, rc=rs, box_color=box_color, color=box_color)  # color=box_color because the msg is part of the box
    if header:
        # insert the sep_line right under the hdr_line
        lines.insert(1, sep_line)
    if end_hdr:
        lines.insert(-1, sep_line)
    # """--== marker_line ==--"""
    # """--== top_line ==--"""
    top_line = ""
    msg = title
    msg_len = nclen(msg)
    my_marker_line = marker_line.replace("@", ts)
    my_marker_line = tl + my_marker_line + tr
    if msg_len > 0:
        my_marker_line_len = nclen(my_marker_line)
        non_title_len = my_marker_line_len - msg_len
        lside_len = rside_len = non_title_len // 2
        lside = my_marker_line[:lside_len]
        diff = my_marker_line_len - (lside_len + msg_len + rside_len)
        rside_len = rside_len + diff
        rside = my_marker_line[(my_marker_line_len - rside_len):]
        top_line = BOX_COLOR + lside + COLOR + msg + BOX_COLOR + rside + RESET
    else:
        top_line = BOX_COLOR + my_marker_line + RESET
    # lines[0] = top_line
    lines.insert(0, top_line)
    # """--== bot_line ==--"""
    bot_line = ""
    msg = footer
    msg_len = nclen(msg)
    my_marker_line = marker_line.replace("@", bs)
    my_marker_line = bl + my_marker_line + br
    my_marker_line_len = nclen(my_marker_line)
    if msg_len > 0:
        non_title_len = my_marker_line_len - msg_len
        side_len = non_title_len // 2
        lside = my_marker_line[:side_len]
        diff = my_marker_line_len - ((side_len * 2) + msg_len)
        side_len = side_len + diff
        rside = my_marker_line[my_marker_line_len-side_len:]
        bot_line = BOX_COLOR + lside + COLOR + msg + BOX_COLOR + rside + RESET
        # dbug(bot_line)
    else:
        bot_line = BOX_COLOR + my_marker_line + RESET
    lines.append(bot_line)
    new_lines = lines
    # printit(new_lines)
    if prnt:
        printit(lines, centered=centered, shadowed=shadowed)
    if write_csv != "":
        CSV_FILE = write_csv
        with open(CSV_FILE, 'w', newline='\n') as f:
            # if we used import csv then use next 2 lines
            # writer = csv.writer(f)
            # writer.writerows(rows)
            for row in lol:
                f.write(",".join(row))
                f.write("\n")
            f.write(f'\n# This file was written out: {dtime} \n')
        # printit(f"Done writing csv file: {CSV_FILE}")
    if len(new_lines) == 0:
        # dbug("Returning None")
        return None
    if write_out != "":
        with open(write_out, 'w', newline='\n') as f:
            for line in new_lines:
                f.write(line + "\n")
    # dbug(lol[:2])
    if lol_b:
        # dbug(f"Returning lol[:3]: {lol[:3]}"
        return lol
    # dbug("Returning new_lines")
    return new_lines
    # ### EOB def gtable( ... ) ### #


def gtable_demo(*args, **kwargs):
    """
    purpose: test/demo using gtable()
    returns: None
    """
    ans_d = {RESET + str(30.0): gclr('rgb(250,0,250)') + str(50.0), gclr('white!', '--------', reset=True): gclr('white!', '--------', reset=True), gclr('cyan') + '10.0': '\x1b[38;2;255;0;0m16.67\x1b[0m', 'nnormal': 1}
    # printit(ans_d, 'boxed', title="It should turnout with these colors", footer=dbug('here'))
    gtable(ans_d, 'prnt', 'hdr', title="Respecting preset colors", footer=dbug('here'))
    # dbug('ask')
    # """--== SEP_LINE ==--"""
    line_5_val = gclr("[red!]this elem value was set to red using gclr()[/]")
    # dbug(line_5_val)
    tst_d = {"simple": "table", "goes": "here", "line three": "this is a very very long exstensive and verbose line or string", "line four": "If you thought that last line was long it was only because you had not come across this very long, exstensively verbose, long line.", "line five": line_5_val}
    gtable(tst_d, 'prnt', 'centered', 'wrap', 'hdr', 'index', colnames=["col1", "col2"], title="tst_d dict w/wrap default col_limit=60", col_limit=60, footer=dbug('here'))
    dbug('ask')
    gtable(tst_d, 'prnt', 'centered', 'hdr', colname=["col1", "col2"], title="tst_d dict no wrap default col_limit=60", col_limit=60, footer=dbug('here'))
    dbug('ask')
    gtable(tst_d, 'prnt', 'centered', title="tst_d dict no wrap col_limit=140", col_limit=140, footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap", footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap and col_limit=30", footer=dbug('here'), col_limit=30)
    dbug('ask', 'centered')
    printit("Now run gtable with: tst_d dict w/hdr & end_hdr, wrap, alt, index and clolimit=30", 'centered')
    box1 = gtable(tst_d, 'header', 'wrap', title="Short title w/wrap", footer=dbug('here'), end_hdr=True, col_limit=30)
    box2 = gtable(tst_d, 'header', 'index', 'alt', 'wrap', title="Short title w/wrap, alt, and w/index", footer=dbug('here'), end_hdr=True, col_limit=30)
    gcolumnize([box1, box2], 'prnt', 'centered', 'boxed', title="Two gtables boxed and centered", box_color="yellow! on black", footer=dbug('here'))
    # dbug('ask', 'centered')
    # """--== SEP_LINE ==--"""
    my_lol = [["name", "value", "make", "model"], ["two", "2", "foo", "bar"], ["twenty_two", "22", "bing", "bang"],
            ["one", "1", "boom", "bam"], ["five", "5", "tik", "tok"], ["three", "3", "string", "strum"], ["four", "4", "ping", "pong"]]
    title = "with hdr and alt"
    gtable(my_lol, 'prnt', 'centered', 'hdr', 'alt', alt_clr="rgb(50,50,50)", title=title, footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    my_d = {"col1": 1, "col2": 2, "col3": 3, "col4": 4, "col5": "col5 with a very very long winded line that has man many chacters in it. Do not be alarmed by it's length", "col6": ["This is six", "another line"], "col7": 7}
    colnames = ["col1", "col2", "col3", "col4", "col5", "col6"]
    gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/colnames and now with header and colnames", footer=dbug('here'), colnames=colnames)
    print()
    title = "with hdr and sortby=1"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortby=1, title=title, footer=dbug('here'))
    dbug('ask')
    title = "with hdr and sortby=value"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortby="value", title=title, footer=dbug('here'))
    title = "with hdr and sortby_n=value"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortbyn="value", title=title, footer=dbug('here'))
    dbug('ask')
    title = "with hdr and sortby_n=value filterby value: 2"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortbyn="value", filterby={'value': '2'}, title=title, footer=dbug('here'))
    title = "with hdr and sortby_n=value filterby value: 2 select_cols=[name, value, make]"
    gtable(my_lol, 'prnt', 'hdr', 'centered', sortbyn="value", filterby={'value': '2'}, select=['name', 'value', 'make'], title=title, footer=dbug('here'))
    dbug('ask')
    gtable(my_lol, 'prnt', 'hdr', 'centered', 'end_hdr', sortbyn="value", filterby={'value': '2'}, select=['name', 'value', 'make'], title=title, footer="with end_hdr" + dbug('here'))
    # """--== SEP_LINE ==--"""
    printit(gtable.__doc__, 'boxed', 'centered', title=" gtable() doc ", footer=dbug('here'), box_color="yellow! on black!")
    askYN("Continue: ", 'centered')
    csv_lines = """
    sym,lpr,chg,pchg,trgt,ask,iv,pom,cp,date,blks,pc,pp,sr,pe,fpe,div,roe,rl,rh,fv,mv,peg,shrs,acnt,misc,misc2,status,score,rng_pcnt,avg,mcap,ps,pb,cps,cr,dr,beta,eps,div5yr,pinst,pinsdr,ma200,ma50,notes,rundate
AVGO,  520.86,  -29.27,  -5.32,  450.0,  70,  31.0,  95,  535.48,  20220730,  1,  P,  __,  A+,  25,  12,  15.9,  39,  463,  678,  302,  624,  1.09,  xxx,  1510,  ,  ,  ,  80.0,  26.91,  76.5,  210936823808,  7.03,  10,  22.3,  2,  188.02,  1.1,  20.19,  2.96,  82.11,  2.35,  570.38,  517.43,  *t,  20220827
ALSN,  37.14,  -1.24,  -3.23,  30.0,  045,  50.0,  82,  35.30,  20220412,  2,  P,  __,  C_,  08,  06,  0.8,  62,  32,  42,  69,  ___,  0.55,  xxx,  1510,  ,  ,  ,  60.0,  51.4,  54.0,  3574528256,  1.4,  5,  1.28,  2,  336.98,  0.92,  4.62,  1.62,  102.23,  0.84,  38.2,  38.49,  *t,  20220827
AMAT,  98.80,  -6.2,  -5.9,  85.0,  60,  47.0,  87,  98.80,  20220828,  1,  P,  __,  B+,  13,  12,  1,  55,  82,  168,  112,  142,  1.1,  xxx,  1510,  22sep85in@60,  , ofrd22sep_P:NO,  80.0,  19.53,  80.0,  85950767104,  3.42,  7,  4.11,  2,  45.2,  1.51,  7.47,  1.18,  78.48,  0.35,  124.2,  99.13,  ,  20220828
BABA,  98.00,  -1.89,  -1.89,  75.0,  129,  73.0,  80,  89.37,  20220730,  1,  P,  ___,  _+,  45,  11,  0,  02,  73,  183,  32,  100,  316.17,  xxx,  1510,  audit_probs_SEC,  ,  ,  30.0,  22.73,  53.5,  260032233472,  0.3,  0,  174.82,  2,  16.91,  0.58,  2.16,  None,  16.44,  0.01,  109.8,  102.31,  *t,  20220827
BAC,  34.03,  -1.11,  -3.16,  28.0,  11,  35.0,  92,  33.05,  20220727,  1,  P,  __,  C+,  10,  09,  0.84,  10,  29,  51,  48,  41,  1.58,  xxx,  1510,  ,  ,  ,  60.0,  22.86,  68.5,  273439211520,  2.99,  1,  88.88,  0.0,  0.0,  1.4,  3.2,  2,  70.88,  0.12,  39.99,  33.29,  *t,  20220827
    """
    csv_l = csv_lines.split("\n")
    csv_l = [line for line in csv_l if line != '' and not line.isspace()]  # get rid of empty lines
    csv_lol = []
    for row in csv_l:
        elems = row.split(",")
        elems = [str(elem).strip() for elem in elems]
        csv_lol.append(elems)
    selected = csv_lol[0][:20]
    selected.append('div5yr')
    gtable(csv_lol, 'hdr', 'prnt', 'centered', 'alt', title="Selected data from a csv file and selected columns w/alt", footer="alt_color: default " + dbug('here'), selected=selected)
    print()
    gtable(csv_lol, 'hdr', 'prnt', 'centered', 'alt', alt_color="on rgb(60,60,100)", pad='', title="Selected columns, alt and w/o padding", footer="alt_color: 'on rgb(60,60,100)' " + dbug('here'), selected=selected)
    print()
    gtable(csv_lol, 'prnt', 'hdr', 'centered', pad='', col_colors=[], title="Selected columns and w/o padding no column_colors", footer=dbug('here'), selected=selected)
    dbug('ask')
    # """--== SEP_LINE ==--"""
    my_d = {"one": 1, "two": 2, "three": 3, "four": 4, "One thousand": 1000, "One million": 1000000, "col 7": "    this has lots of white space    "}
    gtable(my_d, 'prnt', 'centered', title="Simple Dictionary", footer=dbug('here'))
    print()
    box1 = gtable(my_d, 'prnt', 'centered', 'strip', pad='', title="cell_pad=''")
    dbug('ask')
    box2 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header", footer=dbug('here'))
    print()
    box3 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header colnames=keys", footer=dbug('here'), colnames="keys")
    print()
    gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header colnames=keys exclude=['three']", exclude=['three'], footer=dbug('here'), colnames="keys")
    print()
    gtable(my_d, 'prnt', title="Simple Dictionary colnames=keys", footer=dbug('here'), colnames="keys")
    print()
    printit(gcolumnize([box1, box2]), 'boxed', box_color="red! on black", title="Two Boxes", footer=dbug('here'))
    print()
    printit(gcolumnize([box1, box2]), 'boxed', 'centered', box_color="red! on black", title="Two Boxes centered", footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    my_d = {"one": 1, "two": 2, "three": 3, "four": 4, "One thousand": 1000, "One million": 1000000, "col 7": "    this has lots of white space    "}
    colnames = ["column one", "column two", "column three", "column four", "column five", "column six", "column seven"]
    box1 = gtable(my_d, 'prnt', title="Simple Dictionary", footer=dbug('here'))
    print()
    box2 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header", footer=dbug('here'))
    print()
    printit(gcolumnize([box1, box2]), 'centered')
    print()
    dbug('ask')
    box3 = gtable(my_d, 'prnt', title="Simple Dictionary", footer=dbug('here'))
    box4 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/header", footer=dbug('here'))
    box5 = gtable(my_d, 'prnt', title="Simple Dictionary w/colnames='keys'", footer=dbug('here'), colnames="keys")
    box6 = gtable(my_d, 'prnt', title="Simple Dictionary w/colnames", footer=dbug('here'), colnames=colnames)
    dbug("GOing to box7...", 'ask')
    dbug(my_d)
    box7 = gtable(my_d, 'prnt', 'hdr', title="Simple Dictionary w/colnames w/header", footer=dbug('here'), colnames=colnames)
    dbug("Stop",'ask', 'boxed', box_color="red! on rgb(80,30,80)")
    print()
    printit(gcolumnize([box1, box2]) + box3, 'centered', 'boxed', title="Two boxes in one row and another box in the next", footer=dbug('here'))
    print()
    gtable(my_d, 'prnt', 'centered', 'hdr', title="Simple dictionary w/header", footer=dbug('here'))
    dbug('ask', 'centered')
    my_l = list(my_d.values())
    my_l.append(12345)
    my_l.append(123.45)
    # dbug(my_l)
    colnames = ["column one", "column two", "column three", "column four", "column five", "column six", "big column", "Integer", "Float"]
    # dbug(colnames)
    # dbug(my_l)
    gtable(my_l, 'prnt', 'centered', title="Simple list of values", footer=dbug('here'))
    print()
    gtable(my_l, 'prnt', 'centered', 'hdr', title="Simple list of values w/header and colnames", footer=dbug('here'), colnames=colnames)
    print()
    colnames = []
    for x in range(len(my_l)):
        colnames.append(x)
    # dbug(colnames)
    # dbug(my_l)
    gtable(my_l, 'prnt', 'centered', 'hdr', title="Simple list of values w/header and colnames", footer=dbug('here'), colnames=colnames)
    print()
    # dbug(list(my_d.values()))
    dbug('ask', 'centered')
    # """--== SEP_LINE ==--"""
    my_lol = [
            ["col1", "col2", "col3", "col4", "col5", "col6", "col7"],
            [1, 2, 3,4 , 5, 6, 7],
            ["11", "22", "33", "44", "55", "66", "77"],
            ["111", "222", "333", "444", "555", "666", "777"],
            ["1111", "2222", "3333", "4444", "5555", "6666", "7777"]
            ]
    gtable(my_lol, title="Simple list of lists (lol)", footer=dbug('here'))
    print()
    gtable(my_lol, 'prnt', 'hdr', title="Simple list of lists (lol) w/header", footer=dbug('here'))
    selected_cols = ["col2", "col4", "col6"]
    printit(f"Simple list of lists (lol) w/header & selected_cols: {selected_cols}")
    gtable(my_lol, 'prnt', 'hdr', selected_cols=selected_cols)
    dbug('ask', 'centered')
    # """--== SEP_LINE ==--"""
    tst_d = {"simple": "table", "goes": "here", "line three": "this is a very very long exstensive and verbose line or string", "line four": "If you thought that last line was long it was only becuse you had not come across this very long, exstensively verbose, long line."}
    gtable(tst_d, 'prnt', 'centered', title="tst_d dict no wrap", footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap", footer=dbug('here'))
    gtable(tst_d, 'prnt', 'centered', 'wrap', title="tst_d dict w/wrap and col_limit=30", footer=dbug('here'), col_limit=30)
    printit("Now run gtable with: tst_d dict w/hdr & end_hdr, wrap, alt, index and clolimit=30")
    gtable(tst_d, 'prnt', 'header', 'index', 'alt', 'wrap', alt_color='on rgb(25,25,25)', title="Short title", footer=dbug('here'), end_hdr=True, col_limit=30)
    print()
    dbug('ask', 'centered')
    # """--== SEP_LINE ==--"""
    tst_d = {"first": ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line '], "one": 1, "two": [2, 2], "three": 3, "four": ['pupose: re-writes a file with an added line (after or before a pattern) or   replace a line, or append a line', '-    I wrote this because I am constantly building csv files with a header line ']}
    gtable(tst_d, 'prnt', 'centered' 'wrap', footer=dbug('here'))
    tst_d = {'add_content': ['pupose: re-writes a file with an added line (after or before a pattern) or replace a line, or append a line', '-    I wrote this because I a  m constantly building csv files with a header line '], "next": 4}
    gtable(tst_d, 'prnt', 'wrap', 'centered')
    dbug('ask', 'centered')
    # """--== SEP_LINE ==--"""
    my_d = {"col1": 1, "col2": 2, "col3": 3, "col4": 4, "col5": 5, "col6": [6, "This is six", "another line"]}
    gtable(my_d, "prnt", 'centered', title="testing", footer=dbug('here'))
    my_d = {"col1": 1, "col2": 2, "col3": 3, "col4": 4, "col5": "col5 with a very very long winded line that has man many chacters in it. Do not be alarmed by it's length", "col6": ["This is six", "another line"], "col7": 7}
    gtable(my_d, "prnt", 'centered', 'wrap', title="testing", footer=dbug('here'))
    # dbug('ask')
    kv_cols(my_d, 2, 'prnt','centered',  title="kv_cols 2 columns", footer=dbug('here'))
    kv_cols(my_d, 2, 'prnt', 'centered', 'boxed', title="kv_cols 2 columns boxed ", footer=dbug('here'), mstr_box_color="blue! on white")
    dbug('ask')
    # nums = [1, 20, 40, 3, 33, 55, 11, "21"]
    # dbug(nums)
    # dbug(sorted(nums, key=lambda x: float(x)))
    # """--== SEP_LINE ==--"""
    import pandas as pd
    my_df = pd.DataFrame(my_lol)
    # my_df.rename(columns=my_df.iloc[0]).drop(my_df.index[0])  # uses the first row as colnames and uses the rest of the rows for the df
    gtable(my_df, 'prnt', 'centered', 'end_hdr', colnames="firstrow", title="Using a df", footer="with end_hdr")
    my_d = {"col1": 1, "col2": 2, "col3": 3}
    gtable(my_d, 'prnt', 'hdr', 'centered', 'shadowed', 'human', title=dbug('here'), footer="gtable demo", colnames=["Key", "Value"])
    dbug('ask')
    sym = "CVS"
    with Spinner(f"Working on getting info for Ticker: {sym} then gtable(sym.info...): ", 'elapsed', 'centered'):
        try:
            import yfinance as yf
            sym = yf.Ticker(sym)
            my_d = sym.info
            # dbug(my_d)
            # dbug(type(my_d))
            # dbug(len(my_d))
            # dbug(type(my_d[0]))
            print()
            gtable(my_d, 'prnt', 'centered', 'hdr', 'shadowed', title=dbug('here'), footer=" gtable demo ")
            # if r is None:
            #    dbug('ask')
        except Exception as Error:
            dbug(Error)
            dbug('ask')
    print()
    kv_cols(my_d, 2, 'prnt', 'centered', title="kv_cols(my_d)", footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    my_lol = [["Asset", "type", "value", "age"],
            ["house", "cape cod", "120,000", "55yrs"],
            ["car", "CX5", 3000, 7],
            ["Vermeer", "The Girl with a Pearl Earing", 30000000, 357],
            ["Magic Kit", "With case", 300.4657, 82],
            ["coin", "kugarand", "[1600]", 45]]
    # """--== SEP_LINE ==--"""
    title = "  Need a very long, desparately long, and  wider than usaual title " + dbug('here')
    gtable(my_lol, 'prnt', 'hdr', 'centered', 'human', title=title, footer=" gtable demo " + dbug('here'))
    """--== SEP_LINE ==--"""
    # dbug(f"Now run gtable for my_lol[0]: {my_lol}")
    gtable(my_lol[0], 'prnt', 'centered', title="keys only ", footer=dbug('here'))
    # dbug(my_lol[0])
    dbug('ask')
    # """--== SEP_LINE ==--"""
    title = "list-of-lists"
    gtable(my_lol, 'prnt', 'hdr', 'centered', 'human', rnd=2, title=title, footer=" gtable demo ")
    # gtable(my_lol, 'prnt', 'hdr', 'human', rnd=2,  title=title, footer=" gtable demo " + dbug{'here'})
    # """--== SEP_LINE ==--"""
    my_d = {"one": 1, "two": 2, "three": 3, "four": 4, "One thousand": 1000, "One million": 1000000}
    kv_cols(my_d, 2, 'prnt', 'centered', title="kv_cols(my_dictionary, cols=2)", footer=dbug('here'))
    kv_cols(my_d, 2, 'prnt', 'centered', 'boxed', box_color="red!", mstr_box_clr="yellow!", title="kv_cols(my_dictionary, cols=2) boxed", footer=dbug('here'))
    # ### EOB def gtable_demo(): ### #


def nestlvl(lst, *args, **kwargs):
    """
    purpose: gets the level of nested lists
    requires: lst
    options:
        - verbose: bool    # returns a string providing the possible nature of the provided list (lst)
    returns: int
    notes: used by htmltable and gcolumnize (TODO)
        This helps determine rows and columns of boxes (cell dimension=1) or tables (cell dimension=2)
    """
    """--== Config ==--"""
    verbose = bool_val(["verbose"], args, kwargs, dflt=False)
    # """--== SEP_LINE ==--"""
    # rocs is row(s) of cols ... ie data table
    # box is a simple list of strings
    # for reference:
    add_this = 1
    if not isinstance(lst, list) and not isinstance(lst, dict):
        return 0
    if isinstance(lst, dict):
        # dbug("We found a dictionary")
        add_this += 1
    if isempty(lst):
        return
    if not lst:
        dbug(f"Nothing to process... lst: {lst}... returning...")
        return 1
    # dbug(my_max)
    # dbug(last_type)
    rtrn = max(nestlvl(item) for item in lst) + add_this
    if verbose:
        nestlvl_types = ['blank', 'box', 'a table or row of boxes', 'a row of tables or multi-row of boxes', 'multirow of tables', '???']
        rtrn = nestlvl_types[rtrn] + f" nestlvl: {rtrn}"
    return rtrn
    # ### EOB def nestlvl(lst, *args, **kwargs): ### #


def nestlvl_tst(*args, **kwargs):
    s = "my string"
    nlvl = nestlvl(s)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    box = boxed(["This is a box", "with two lines"])
    printit(box)
    nlvl = nestlvl(box)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    row = [box, box]
    gcolumnize(row, 'prnt')
    nlvl = nestlvl(row)
    # nlevel = nest_level(row)
    dbug(nlvl)
    # dbug(nlevel)
    gtitle(msg="""--== SEP_LINE ==--""")
    rows = [row, row]
    gcolumnize(rows, 'prnt')
    nlvl = nestlvl(rows)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    lol = [["col1", "col2"], ['val1', 'val2']]
    gtable(lol, 'prnt', title='debugging', footer=dbug('here'))
    nlvl = nestlvl(lol)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    row = [lol, lol]
    gcolumnize(row, 'prnt')
    nlvl = nestlvl(row)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    rows = [row, row]
    gcolumnize(rows, 'prnt', cols=2)
    nlvl = nestlvl(rows)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    my_d = {'one': 1, "two": 2}
    gtable(my_d, 'prnt', title=f"my_d: {my_d}", footer=dbug('here'))
    nlvl = nestlvl(my_d)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    row = [my_d, my_d]
    gcolumnize(row, 'prnt')
    nlvl = nestlvl(row)
    dbug(nlvl)
    gtitle(msg="""--== SEP_LINE ==--""")
    rows = [row, row]
    gcolumnize(rows, 'prnt')
    nlvl = nestlvl(rows)
    dbug(nlvl)
    # ### EOB def nestlvl_tst(*args, **kwargs): ### #



# ###################################
def htmltable(data, *args, **kwargs):
    # ###############################
    """
    purpose: create code returning data as an html table
    required: data: list of lists | df    # expects the first line/row to be the header elements 
    options: 
        - title: str
        - footer: str
        - width: int|str   # provides width of holding box - can be a percent eg: width=80%
        - col_colors: list # default (see code)
        - page_cntr: bool  # if true the box with the table will be centered on the web page
        - show: bool       # primarily for debugging; open the returning html code in a browser
    returns: str  # html code with a box (which is a single table cell or rows of tables) holding a table or tables of all the data provided
    notes: this is still limited in features but seems to be useful
        You can also submit rows and or cols of tables(ie list-of-lists) or further do something like this
        Syntax:
            - htmltable(lol1)                      # a single table
            - htmltable([lol1, lol2])              # a single row with two tables
            - htmltable([[lol1, lol2], [lol3]])    # one row with two tables, and a second row with one table
            - htmltable([[lol1], [lol2], [lol3]])  # three rows with one tables in each row
        html_code = htmltable([{'table': my_lol, 'options': {'title': 'Title for my_lol'}}, {'table': my_lol2, 'options': {'title': "Title my_lol2"}}],
                            [{'table': my_lol3}, 'options': {'title': "Title for my_lol3", 'footer': dbug('here')}]
                        ])
        browseit(html_code)
    """
    """--== Config ==--"""
    end_hdr = bool_val(["end_hdr"], args, kwargs, dflt=False)
    col_colors = kvarg_val(['col_colors', 'colors', "col_color"], kwargs, dflt=["white!", "cyan", "red", "green!", "rgb(100,100,255)", "red!", "green!", "yellow!"])
    width = kvarg_val(['width'], kwargs, dflt="")
    title = kvarg_val(["title"], kwargs, dflt="")
    # dbug(title)
    footer = kvarg_val(["footer"], kwargs, dflt="")
    # dbug(footer)
    page_cntr = bool_val(["pg_cntr", 'page_cntr', 'page_center', 'centered'], args, kwargs, dflt=False)
    show = bool_val(["show", "debug"], args, kwargs, dflt=False)
    styles_b = bool_val(["styles", "style"], args, kwargs, dflt=True)
    """--== Convert ==--"""
    if not isinstance(data, dict):
        data = cnvrt2lol(data)
    # new_data = []
    # for row in data:
    #     new_row = []
    #     for elem in row:
    #         new_row.append(str(elem))
    #     new_data.append(new_row)
    # data = new_data
    """--== Init ==--"""
    multitable_flag = False
    multirow_flag = False
    nlvl = nestlvl(data)
    if nlvl > 2:
        multitable_flag = True
    if nlvl > 3:
        multirow_flag = True
    # dbug(f"nlvl: {nlvl} multitable_flag: {multitable_flag} multirow_flag: {multirow_flag}")
    """--== SEP_LINE ==--"""
    # or include <link href="./htmltable.css" ref="stylesheet">
    styles = """
    <style>
        .mycanvass {
            background-color: #000;
        }
        table {
          color: white;
          border-collapse: collapse;
          border-top: 1px solid white;
          border-bottom: 1px solid white;
          border-right: 1px solid white;
          border-left: 1px solid white;
          //width: 100%;
        }
        td {
          padding: 8px;
          padding-top: 1px;
          padding-bottom: 1px;
          //text-align: left;
          border-left: 1px solid white;
          border-right: 1px solid white;
          // border-bottom: 1px solid #DDD;
        }
        .hdr_row {
            border-top: 1px solid white;
            background-color: #444;
        }
        .first_row {
              border-top: 1px solid white;
        }
        .bottom_row {
                border-bottom: 1px solid white;
         }
        .last_row {
                //border-right: 1px solid white;
                border-bottom: 1px solid white;
                //border-left: 1px solid white;
        }
        .first_col {
            background-color: #045;
            color: white;
        }
        .last_col {
            border-right: 1px solid white;
            }
        .table_hover tr:hover {background-color: #448}
    </style>
    """
    box_style = "background-color: rgb(0,0,0);"
    if not isempty(width):
        # dbug(box_style)
        box_style += f" width: {width};"
    col_colors = [xlate_clr(clr, 'rgb') for clr in col_colors]
    # dbug(col_colors)
    html = ""
    if page_cntr:
        html += "\n<center id='page_cntr'>\n"
    # html += "<div class='mycanvass'>\n"
    """--== Functions (Internal) ==--"""
    def do_table(data, *args, **kwargs):
        """--== Inner Table ==--"""
        # dbug(funcname())
        # dbug(type(data))
        """--== Config ==--"""
        my_title = kvarg_val(["title", "caption"], kwargs, dflt="")
        my_footer = kvarg_val(["footer"], kwargs, dflt="")
        """--== Init ==--"""
        table_html = ""
        """--== Convert ==--"""
        if isinstance(data, dict):
            # dbug("separate data from options (title\, footer\, etc...)")
            #  eg: data = {'table': data, 'options': {'title': "my title", 'footer': 'my footer'}}
            my_data = data['table']
            my_options = data['options']
            if 'title' in my_options:
                my_title = my_options['title']
            else:
                my_title = ""
            if 'footer' in my_options:
                my_footer = my_options['footer']
            else:
                my_footer = ""
            # dbug(my_footer)
            rtrn_code = do_table(my_data, title=my_title, footer=my_footer)
            # dbug("Returning my_data")
            return rtrn_code
        """--== SEP_LINE ==--"""
        table_html += f"\n<table id={my_title} class='mytable table_hover'>"
        # do a title
        table_html += f"\n<caption>{my_title}</p></caption>\n"
        for row_num, my_row in enumerate(data):
            this_row = ""
            this_row += f"  <tr id={row_num}>"
            row_class = ""
            if row_num == 0:  # hdr row
                row_class += " hdr_row"
            if row_num == 1:  # first_data_row
                row_class += " first_row"
            if (row_num + 1) == len(data):  # last row
                # dbug(row_num)
                # dbug(len(data))
                row_class += " last_row "
            for col_num, elem in enumerate(my_row):
                # style = "background-color: black;"
                style = ""
                # col_color = col_color.replace("!", "")
                # dbug(col_color)
                if row_num == 0:
                    style += " text-align: center; "
                    col_color = "white!"
                else:
                    color_num = col_num % len(col_colors)
                    col_color = col_colors[color_num]
                col_color = xlate_clr(col_color, 'rgb')
                style += f"color: {col_color};" 
                col_class = ""
                if col_num == 0:  # first cell
                    col_class += " first col"
                if col_num == len(my_row) - 1:  # last cell
                    col_class += " last_col"
                this_row += f"    <td style='{style}' class='{row_class}{col_class}'>{elem}</td>"
            this_row += f"\n  </tr id={row_num}>\n"
            if 'hdr_row' in row_class:
                # set this in case it is needed later
                my_hdr_row = this_row
            table_html += this_row
        if end_hdr:
            table_html += my_hdr_row
        table_html += f"</table id={my_title}>\n"
        # do a footer
        # dbug(footer)
        table_html += f"<center id='footer'>\n    <p>{my_footer}</p>\n  </center id='footer'>\n"
        # browseit(table_html, title)
        return table_html
        """--== EOB Inner Table ==--"""
    """--== Process ==--"""
    """--== Outer Table(s) ==--"""
    if multirow_flag:
        for row in data:
            html += f"<table style='{box_style} border: none;'>\n"
            html += "  <tr id=multi_row>\n"
            for table in row:
                html += "    <td id='outer' style='border: none;'>"
                html += "\n<center>\n"
                # dbug(table)
                html += do_table(table)
                html += "\n</center>\n"
                html += "    </td id='outer'>"
            html += "  </tr id=multi_row>\n"
        html += "</table>\n"
    else:
        # dbug("not multirow")
        html += "  <tr id=outer_not_multi_row>\n"
        # start a single row
        html += f"<table style='{box_style} border: none;'>\n"
        if multitable_flag:
            for table in data:
                html += "\n    <td id='outer' style='border: none;'>"
                html += "\n<center>\n"
                html += do_table(table)
                html += "\n</center>\n"
                html += "\n    </td id='outer'>"
        else:
            # not multitable
            html += "    <td>\n"
            html += "<center>\n"
            html += do_table(data, title=title, footer=footer)
            html += "\n</center>\n"
            html += "    </td>"
        # stop a single row
        html += "\n  </tr id=outer_non-multitable>\n"
    html += f"<center><p>{footer}</p></center>\n"
    html += "</center>\n</table id='outer'>\n"
    if page_cntr:
        html += "</center id='page_cntr'>\n"
    if styles_b:
        # dbug("adding in styles first")
        html = styles + html
    """--== SEP_LINE ==--"""
    if show:
        browseit(html)
    # dbug("Returning: html")
    return html
    # ### EOB def htmltable(data, *args, **kwargs): ### #


def htmltable_tst(*args, **kwargs):
    """
    purpose: runs a test on htmltable
    returns: None
    """
    url = "https://finance.yahoo.com/world-indices?guccounter=1"
    tables = get_html_tables(url)
    data = tables[0][:5]
    html = htmltable(data, 'end_hdr', 'show', 'pg_cntr', width="80%", title="htmltable(data, 'end_hdr', 'show', 'pg_cntr', width='80%', ...)", footer=dbug('here'))
    """--== SEP_LINE ==--"""
    url = "https://finance.yahoo.com/commodities"
    tables = get_html_tables(url, 'show')
    selected = ["Symbol", "Name", "Last Price", "Change", "% Change"]
    filterby = {"Name": r'S&P|Dow|Russel|Nasdaq|Crude'}
    lol = cnvrt2lol(tables[0], selected=selected, filterby=filterby)
    html = htmltable(lol)
    browseit(html)
    """--== SEP_LINE ==--"""
    return 



def chunkit(my_l, size, *args, **kwargs):
    """
    purpose: break a list into a list of chunks - each chunk having size=size
    requires: my_l: list (eg boxes), size: int
    options:
        - full: bool   # puts empty "cells" to make all "list chunks" the same number of elems
        - cols: bool   # turn size into number of chunks or cols
            note: you can do this yourself eg size = len(my_l) // cols  # where cols = number of columns <-- this method would probably less confusing
    returns: a list of lists(chunks)
    note: this is used: in a dashboard columns of boxes - see gcolumnize and in gtables
    """
    # """--== Config ==--"""
    full_b = bool_val(["full", "even", "equal"], args, kwargs, dflt=False)
    cols = bool_val(["cols", "chunks", "columns"], args, kwargs, dflt=False)
    # """--== Init ==--"""
    if cols:
        size = len(my_l) // size
    # """--== Process ==--"""
    def divide_chunks(my_l, n):
        # looping till length my_l
        for i in range(0, len(my_l), n):
            yield my_l[i:i + n]
    rtrn = list(divide_chunks(my_l, size))
    # """--== SEP_LINE ==--"""
    if full_b:
        new_rtrn = []
        for elem in rtrn:
            if len(elem) < size:
                diff = size - len(elem)
                for x in range(diff):
                    if isinstance(elem, list):
                        elem.append([""])
                    if isinstance(elem, str):
                        elem.append("")
            new_rtrn.append(elem)
        rtrn = new_rtrn
    return rtrn


def splitit(s, delimiter=" "):
    """
    purpose: given a string (s), split it using delimiter which can be a string or regex
    requires: import re
    input:
        - s: str  # string to split
        - delimiiter=" ": str
    options: none
    returns: phrases: list  # string split into elements
    notes:
        eg:
            delimiter = r"[\"|\'] +[-–—―] +"  # amazingly all those dashes are different symbols...
            phrase = splitit('"A great city is not to be confounded with a populous one" - Aristotle', )
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(s)
    # dbug(delimiter)
    # """--== Validate ==--"""
    if type(s) != str or len(s) == 0:
        dbug(f"Nothing to work with s: {s} delimiter: [{delimiter}]")
        return None
    # """--== Process ==--"""
    phrases = re.split(delimiter, s)
    # dbug(f"Returning phrases: {phrases}")
    return phrases


def split_codes(val, *args, **kwargs):
    """
    purpose: to split out ansi codes and return them
    input: elem: str (that contains ansi codes for color)
    options: TODO include elem dflt=False
    returns: codes: list (unless elem=True [or 'with_elem' or 'asdict'], then it is a dictionary with preffix, elem, and suffix as key/value pairs)
    notes: - used in cond_num() aka: color_neg()
        - NOTE: this function expects both a prefix code and a suffix code!
        - this function is not perfect and can lead to problems so use judiciously
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(repr(val))
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    asdict_b = bool_val(['elem', 'with_elem', 'asdict'], args, kwargs, dflt=False)
    # dbug(asdict_b)
    # """--== Init ==--"""
    # """--== Process ==--"""
    val = str(val) + gclr('reset')  # make sure it has an ending code
    pat = r"(?P<prefix>\x1b[\[\d\;]+m)(?P<elem>.*)(?P<suffix>\x1b.*m)"
    r = re.match(pat, str(val))
    if r:
        my_d = r.groupdict()
    else:
        my_d = {'prefix': "", 'elem': val, 'suffix': ""}
    if asdict_b:
        # dbug(f"Returning: my_d: {my_d}")
        return my_d  # also includes ['elem': elem] ... see above
    else:
        return [my_d['prefix'], my_d['suffix']]  # returning a list with prefix and postfix code
    # ### EOB def split_codes(val, *args, **kwargs): ### #


def split_codes_demo(my_s=gclr('red')+"test string"+gclr('reset'), *args, **kwargs):
    """
    purpose: test/demo of splitting ansii code away from a string
    returns: None
    """
    pre_post_codes_l = split_codes(my_s)
    pre_post_codes_l = split_codes(my_s, 'asdict')
    my_s = my_s.replace(gclr('reset'), "")
    pre_post_codes_l = split_codes(my_s, 'asdict')
    gtable(pre_post_codes_l, 'hdr', 'prnt', footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    print("-"*40)
    dbug(pre_post_codes_l)
    words_l = ["one", gclr('red on white')+'two', gclr('reset')+'word with reset before and after'+gclr('reset')]
    for wrd in words_l:
        dbug(split_codes(wrd), 'asdict')
    print("-"*40)
    dbug('ask')
    # """--== SEP_LINE ==--"""
    my_words = gclr('white! on black') + "one and " + gclr("blue on white") + 'two' + gclr('reset')
    dbug(my_words)
    words_l = my_words.split()
    for word in words_l:
        dbug(gclr('reset'))
        dbug(word)
        dbug(split_codes(word, 'asdict'))
    # ### EOB split_code_demo() ### #


# #################
def cond_num(elem, *args, **kwargs):
    # #############
    """
    purpose: this conditions (colorizes, rounds, and adds commas and unit indicators) elems if they are numbers
    input: elem
    options: "neg_color=red on black!": str, pos_color="green! on black!": str, rnd=0: int
    -   color: bool         # will color the number ... default red for negative and green for positive
    -   neg_color: str      # you can change the color for negative numbers
    -   pos_color: str      # you can change the color for positive numbers
    -   rnd: int            # if rnd == "" nothing will be done,
            if rnd is 0 it will make elem an integer,
            if rnd > 0 then that will be used for the number of places to round
    -   human: bool         # adds reduces large numbers to 10000000 to 1M etc
    -   nan: str            # allows you to change "nan" or "NaN" to any string you want. default=""
    returns: elem (conditioned; colored)
    use:
    -   for n, row in enumerate(lol):
    -       ...
    -       if neg:
    -           row = [color_neg(elem) for elem in row]
    -       # table.add_row(*row)
    -       table_lol.append(*row)
    NOTE: this may return an elem with a different length
    aka: color_neg(elem)
    """
    # dbug(funcname())
    # dbug(repr(elem))
    # """--== Config ==--"""
    clr_b = bool_val(["neg", "color", "clr", "colorize", "pos"], args, kwargs, dflt=False)  # "neg" and 'pos'are remanants of past code
    rnd = kvarg_val(['round', 'rnd'], kwargs, dflt="")
    neg_color = kvarg_val(['neg_color'], kwargs, dflt='red! on rgb(0,0,0)')
    pos_color = kvarg_val(['pos_color'], kwargs, dflt='green! on rgb(0,0,0)')
    human = bool_val(["human", "h"], args, kwargs, dflt=False)
    nan = kvarg_val(["nan", "NaN"], kwargs, dflt="")
    rset = bool_val(['rset', 'reset'], args, kwargs, dflt=False)
    # """--== Convert ==--"""
    if 'numpy' in str(type(elem)):
        import numpy
        elem = elem.item()
    # """--== Init ==--"""
    elem_CODES = split_codes(elem)
    # dbug(elem_CODES)
    # last_msg = ""
    RESET = sub_color('reset')
    if clr_b:
        elem = escape_ansi(elem)
        # dbug(f"pos_color: {pos_color} neg_color: {neg_color}")
        NEG_COLOR = sub_color(neg_color)
        POS_COLOR = sub_color(pos_color)
    else:
        elem = str(elem)
        NEG_COLOR = ""
        POS_COLOR = ""
    # NOTE! IMPORTANT! If you want a number to be treated like a string, ie ignored here, precede it with an underscore (_) or surround it with [] or someother means
    #   or set neg to False in table or rnd="", human=""
    if nan != "":
        if str(elem).lower() == "nan":
            elem = str(nan)
    # strip off any human symbols except "-"
    had_commas = False
    if "," in elem:
        had_commas = True
        elem = elem.replace(",", "")
    suffix = ""
    tst_elem = elem.strip("%BGMK+")
    if isnumber(tst_elem) and not str(elem).startswith("_"):
        suffix = prefix = ""
        if str(elem).endswith("G"):
            elem = elem.replace("G", "")
            suffix = "G"
        if str(elem).endswith("B"):
            elem = elem.replace("B", "")
            suffix = "B"
        if str(elem).endswith("M"):
            elem = elem.replace("M", "")
            suffix = "M"
        if str(elem).endswith("K"):
            elem = elem.replace("K", "")
            suffix = "K"
        if str(elem).endswith("%"):
            elem = elem.replace("%", "")
            suffix = "%"
        if str(elem).startswith("+"):
            prefix = "+"
            elem = elem.lstrip("+")
        elem_val = escape_ansi(elem)
        # dbug(elem_val)
        if rnd == 0:
            elem_val = str(int(float(elem_val)))  # needs to be str for next test
        if isnumber(rnd) and rnd > 0:
            # rnd scale is declared
            elem_val = str(round(float(elem_val), rnd))
        if clr_b:  # and not re.search(r"[BGMK]", elem_val):
            if "." in str(elem_val):  
                # this must be a float number
                clean_val = elem_val.replace(",", "")
                elem_val = float(clean_val)
            else:
                # not a float number
                if isnumber(elem):
                    elem_val = int(elem_val)
            # dbug(f"chkg elem_val: {elem_val} for pos/neg")
            if elem_val < 0:
                prefix = NEG_COLOR
                # dbug(f"setting {NEG_COLOR}color{RESET} for elem_val: {elem_val} elem: {elem")
            else:
                prefix = POS_COLOR
                # dbug(f"POS_COLOR: {POS_COLOR} {repr(POS_COLOR)}")
        if human:
            # dbug(f"working on humanizing elem_val: {elem_val}")
            if not str(elem_val).endswith(("B", "M", "K", "G", "T", "Kb", "Mb", "%")):
                if float(elem_val) >= 1000000000:
                    elem_val = float(elem_val) / 1000000000
                    elem_val = str(round(elem_val, 2)) + "B"
            if not str(elem_val).endswith(("B", "M", "K", "G", "T", "Kb", "Mb", "%")):
                try:
                    if float(elem) >= 1000000:
                        elem_val = float(elem_val) / 1000000
                        elem_val = str(round(elem_val, 2)) + "M"
                except Exception as Error:
                    dbug(f"Error: {Error} elem_val: {elem_val}")
            if not str(elem_val).endswith(("B", "M", "K", "G", "T", "Kb", "Mb", "%")):
                if float(elem_val) >= 1000:
                    # dbug(elem_val)
                    elem_val = float(elem_val) / 1000
                    if isnumber(rnd) and int(rnd) > 0:
                        elem_val = str(round(elem_val, rnd))
                        elem_val = str(elem_val) + "K"
                    # dbug(elem_val)
            if "," in str(elem_val):
                elem_val = str(elem_val).replace(",", "")
                elem_val = "'" + elem_val + "'"
            if str(elem_val).replace(".", "").isnumeric():
                elem_val = f"{float(elem_val):,}"
            # dbug(elem_val)
            # if clr_b and str(elem_val).endswith(("B", "M", "K", "G", "T", "Kb", "Mb", "%")):
            #     dbug(elem_val)
            #     raw_val = elem_val[:-1]
            #     dbug(raw_val)
            #     prefix = POS_COLOR
            #     # dbug(pos_color)
            #     # dbug(neg_color)
            #     if float(raw_val) < 0:
            #         dbug(f"raw_val: {raw_val} is neg")
            #         prefix = NEG_COLOR
            #     my_elem = prefix + str(elem_val) + suffix
            #     dbug(my_elem)
        elem = prefix + str(elem_val) + suffix
    # dbug(elem_CODES)
    elem = elem_CODES[0] + elem + elem_CODES[1]
    if rset:
        elem += RESET
    # dbug(f"Returning elem: {elem}")
    return elem
    # ###  EOB def cond_num(elem, *args, **kwargs): ### #


# alias for above
# cond_num = color_neg
color_neg = cond_num

def cond_num_tst(*args, **kwargs):
    """
    WIP
    """
    n_l = [1, 1.1, "1B", -1, "-1B", "1K", "-1K", "1,000"]
    for number in n_l:
        returned_cond_num = cond_num(number, 'neg', 'human')
        dbug(f"number: {number} returned_cond_num: {returned_cond_num}")


# ####################################
def get_random_line(file, prnt=False, *args, **kwargs):
    # ################################
    """
    purpose: grabs one random line from a file
    requires:
        from this_file purify_file, centered, boxed, printit, cat_file
        import random
        file: str | list  # can be a filename or it can be a list of lines
    returns: line
    Note: file has all comments removed first (purified)
    """
    # """--== Imports ==--"""
    import random
    # """--== Validation  ==--"""
    if isinstance(file, str):
        file = os.path.expanduser(file)
    if isinstance(file, list):
        contents_l = purify_file(file)
    else:
        contents_l = purify_file(file)
    # """--== Process ==--"""
    line = random.choice(contents_l)
    if prnt:
        lines = boxed(line, title=" Quote ")
        printit(centered(lines))
    return line
    # ### EOB def get_random_line(file, prnt=False): ### #


# #########################################
def run_cmd_threaded(cmd, *args, **kwargs):
    # #####################################
    """
    purpose: runs a cmd as a thread
    options:
        - lst: bool  # returned output lines will be put into a list rather than a str
    return: output from cmd
    Note: Please, be aware that a result will be returned only after this finishes
    so put it "later" rather than "sooner" in your app
      - does not currently return error msgs
    """
    # """--== debugging ==--"""
    dbug("who uses this?")
    # """--== Config ==--"""
    lst = bool_val(['lst', 'list'], args, kwargs, dflt=False)
    """--== Process ==--"""
    t = ThreadWithReturn(target=run_cmd, args=(cmd,))
    t.start()
    result = t.join()
    if lst:
        result = result.split("\n")
    return result


# ###############
def run_cmd(cmd, *args, prnt=False, runas="", **kwargs):
    # ###########
    """
    purpose: runs cmd and returns output
      eg: out = run_cmd("uname -o",False)
      # now you can print the output from the cmd:
      print(f"out:{out}")
    options:
        - lst: bool   # ouput will return as a list of line rather than a str
        - rc: bool    # returns the cmd return code instead of output
        - error: bool # also returns error
        - both: bool  # returns (output, rc)
        - runas: str  # you can declare who to run the cmd as
        - prnt: bool  # print output - returns None
    returns: output from command
    Note: if runas == sudo then the command will be sun with sudo...
      -  this function strips out all ansi code and filters all errors
      - does not currently return error msgs
      - as it is today 20221201 you lose color output - use os.system(cmd) instead for simple output or use 'prnt' option
    Test:
    >>> r = run_cmd("uname -o")
    >>> print(r)
    GNU/Linux
    <BLANKLINE>
    """
    # dbug(funcname)
    # dbug(cmd)
    # """--== Config ==--"""
    return_l = bool_val(['list', 'lines', 'lst'], args, kwargs)
    return_rc = bool_val(['rc', 'return_rc', 'rtrn_rc'], args, kwargs, dflt=False)
    both = bool_val(['both'], args, kwargs, dflt=False)
    runas = kvarg_val(["runas", "sudo"], kwargs, dflt=runas)
    errors_b = bool_val(["errors", "err", "errs", "error"], args, kwargs, dflt=False)
    prnt = bool_val(['prnt', 'print', 'show'], args, kwargs)
    """--== SEP_LINE ==--"""
    out = ""
    # """--== Notes ==--"""
    # so many ways to do this...
    # resource: https://janakiev.com/blog/python-shell-commands/
    # simplest is os.system(cmd) but lacks flexibility like capturing the output
    # stream = os.popen(cmd)
    # print(stream.read())
    #   or
    # print(os.popen(cmd.read())) # returns one str
    #   but subprocess is the recommended method
    # import subprocess
    # import shlex
    # dbug(prnt)
    # NOTE: declaring runas will require that user to have sudo for the cmd
    # eg in /etc/sudoers of /etc/sudoers.d/www-data
    #   # user HOSTS=USER(S) OPTION: cmds
    #   www-data ALL=(user) NOPASSWD: /path/to/cmd
    # note: the env vars will be limited to the named user
    if runas != "":
        if runas == 'sudo':
            cmd = f"sudo {cmd}"
        else:
            cmd = f"sudo -u {runas} {cmd}"
    # dbug(cmd)
    if prnt:
        os.system(cmd)
        return None
    try:
        # dbug(f"Tying cmd: {cmd}")
        # process gets used below
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8')
        (out, err) = process.communicate()
        rc = process.returncode
        # dbug(out)
        # dbug(err)
        # dbug(rc)
        if errors_b:
            out += err
    except Exception as Error:
        # dbug(Error, 'ask')
        # if process fails then run one of these
        # out = os.system(cmd)
        # out = os.popen(cmd)
        out = subprocess.check_output(cmd.split(), universal_newlines=True)
        return out
    # dbug(f"cmd.split():{cmd.split()} process:{process}")
    # dbug(f"Done: Running os.system({cmd})  r: {r}")
    # dbug(f"note: out: {out} rc: {rc}")
    if return_l:
        # dbug(return_l)
        out = out.split("\n")
    if return_rc:
        # dbug(out)
        # dbug(rc)
        if rc == '':
            rc = 0
        return (out, rc)
    if both:
        # dbug("returns a tuple")
        # use: r = run_cmd(cmd, 'both')
        # output = r[0]
        # rc = r[1]
        return (out, rc)
    # dbug(out)
    return out
    # ### EOB def run_cmd(cmd, *args, prnt=False, runas="", **kwargs): ### #


def run_cmd_demo(*args, **kwargs):
    """
    purpose: demo of run_cmd(cmd)
    returns: None
    """
    cmd = "ls -l --color | head"
    out, rc = run_cmd(cmd, 'rc', 'error')
    if rc == 0:
        printit(out, 'boxed', title=f"cmd: {cmd}", footer=dbug('here'))
    else:
        dbug("Error")
        printit(out, 'boxed', title=f"cmd: {cmd}", footer=dbug('here'))
    """--== SEP_LINE ==--"""
    import json
    url = "ipinfo.io"
    cmd = f'curl {url}'
    out = run_cmd(cmd)
    if len(out) < 1:
      dbug(f"Are you connected to the internet? url: {url} failed...")
      do_close()
    jout = json.loads(out)
    gtable(jout, 'prnt', 'hdr', title=f"cmd: {cmd}", footer=dbug('here'))
    return None


def grep_lines(lines, pattern, *args, **kwargs):
    """
    purpose: searches lines (or file if lines is a filename) for pattern
    options:
    -    ic: bool (insensitive case)
    -        rtrn_bool=False: bool    #  (whether to rtrn lines [default] or bool result)
    -        csv: bool                # will convert a list of lists to a list of csv style lines before searching
    -                                 #   and but returns the line as a list, just the way we got it
    returns: matched line(s) (or True False if rtrn_bool is True)
    Note: if only one line is matched then it will return that one line otherwise it will return a list of matched_lines
    """
    # used in do_watch and maybe others
    # dbug(funcname())
    # dbug(pattern)
    # """--== Config ==--"""
    ic = bool_val(['ic', 'ci', 'case_insensitive', 'ignore_case'], args, kwargs)
    rtrn_b = bool_val(['rtrn_bool', 'rtrn_d', 'bool', 'rtrn'], args, kwargs, dflt=False)
    csv_b = bool_val(['csv'], args, kwargs, dflt="")
    # """--== Xlate filename to lines ==--"""
    if isinstance(lines, str):
        lines = cat_file(lines, 'lst')
    # """--== Process ==--"""
    matched_lines = []
    for line in lines:
        line = str(line)
        # dbug(line)
        # this might have been taken from a list of list (lol) so convert the list to a csv style line
        if csv_b or isinstance(line, list):
            # dbug(line)
            csv_b = True
            orig_line = line
            # dbug(orig_line)
            line = [str(elem) for elem in line]
            line = ", ".join(line)
        # dbug(line)
        if ic:
            # ignore case
            rex_b = re.search(pattern, line, re.I)
        else:
            # case sensitive
            # dbug(pattern)
            # dbug(line)
            rex_b = re.search(pattern, line)
            # dbug(rex_b)
        if rex_b:
            # use the regex set above
            if csv_b:
                matched_lines.append(orig_line)
            else:
                matched_lines.append(line)
    if rtrn_b:
        if len(matched_lines) > 0:
            return True
        else:
            return False
    if len(matched_lines) == 1:
        matched_lines = matched_lines[0]
    if len(matched_lines) == 0:
        matched_lines = None
    return matched_lines


# # ###########################################################
# def sshp(cmd='uptime', rhost="192.168.86.61", user="geoffm"):
#     # #######################################################
#     """
#     purpose:
#     - ssh parallel
#     - uses paramiko module
#     input: cmd, remote_host, user
#     returns: output of the command
#     WIP
#     """
#     dbug("who uses this")
#     import paramiko
#     ssh = paramiko.SSHClient()
#     timeout = 2
#     # printit(f"Running cmd: {cmd} on server: {rhost} with ssh and user: {user}...")
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
#     ssh.connect(rhost, port=22, timeout=timeout, username=user)  # , password="password")
#     stdin, stdout, stderr = ssh.exec_command(cmd)
#     out = stdout.readlines()
#     out = "".join(out).strip()
#     # dbug(f"[{out}]")
#     return out


# ###############################
def list_files(dirs, file_pat="*", *args, **kwargs):
    # ###########################
    """
    purpose: prints a list of enumerated basename filenames (sorted by name)
    input:
        dirs=list|str
    options:
        pattern: str|list = "*"  # glob pattern
        return_msgs<bolean> = False
        prnt<bolean> = False
        dirs: bool               # include dirs
        dir_only: bool           # only dirs
        links: bool              # include links
        mtime: bool              # with mtime
    returns:
        a sorted list of those names
        or
        return_msgs and sorted names
    use: list_files("/tmp")
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(dirs)
    # dbug(file_pat)
    # dbug(args)
    # dbug(kwargs)
    # dbug(file_pat)
    # """--== Config ==--"""
    ptrns = kvarg_val(['file_pat', 'patterns', 'pattern', 'ptrn', 'ptrns', 'pat'], kwargs, dflt=[file_pat])
    links = bool_val('links', args, kwargs, dflt=False)  # should links be followed
    dirs_b = bool_val(["dirs_b", "dirs"], args, kwargs, dflt=False)
    dirs_only = bool_val(["dirsonly", "dirs_only", "dironly", "dir_only"], args, kwargs, dflt=False)
    sortby = kvarg_val(['sortby'], kwargs, dflt='name')
    mtime = bool_val(["with_mtime", "with_mdate", "mtime", "long", "ll"], args, kwargs, dflt=False)
    # dbug(with_mtime)
    # """--== Inits ==--"""
    msgs = []
    files_l = []
    # """--== Converts ==--"""
    if isinstance(ptrns, str):
        ptrns = [ptrns]
    if isinstance(dirs, str):
        dirs = dirs.split()
    # """--== Process ==--"""
    for ptrn in ptrns:
        for dir in dirs:
            # dbug(f"chkg ptrn: {ptrn} in dir: {dir}")
            # file_pat = f"{file_pat}*"
            # dbug(f"Searching dir: {dir} for file pattern: {file_pat}...")
            pathname = f"{dir}/{ptrn}"
            # dbug(pathname)
            for n, file in enumerate(glob.glob(pathname)):
                if dirs_b:
                    if os.path.isdir(file):
                        files_l.append(file)
                        # d_l = os.listdir(file)
                        # dbug(d_l)
                        continue
                # dbug(f"Checking file: {file} in pathname: {pathname}")
                if os.path.islink(file):
                    # dbug(f"File: {file} found in dir: {dir} is a link.... skipping...")
                    if links:
                        files_l.append(file)
                    else:
                        continue
                # abs_file = f"{dir}/{file}"
                # dbug(f"Found file {file} appending to files_l: {files_l}")
                if not dirs_only:
                    if os.path.isfile(file):
                        files_l.append(file)
                        msgs.append("{:>2})  {}".format(n, file))
            if sortby.lower() == 'name':
                files_l = sorted(files_l)
            if sortby.lower() in ("date", "mtime", "mdate"):
                files_with_mtime = [(f, os.path.getmtime(f)) for f in files_l]
                files_mtime_l = sorted(files_with_mtime, key=lambda x: x[1])
                if mtime:
                    len_mdate = 19
                    max_len = maxof(files_mtime_l) - (len_mdate + 4)
                    new_files_l = []
                    for file in files_mtime_l:
                        mdate = datetime.fromtimestamp(file[1])
                        mdate = str(mdate)[:len_mdate]
                        new_files_l.append(f"{file[0]:{max_len}} {mdate}")
                    files_l = new_files_l
                    # dbug(files_l, 'ask')
            if len(files_l) > 0:
                msg = "Found these files:"
                for f in files_l:
                    msg += f"\n   {f}"
    # if return_msgs:
    #     return msgs, names
    # else:
    return files_l
    # ### EOB def list_files(dirs, file_pat="*", *args, **kwargs): ### #


def list_files_demo(*args, **kwargs):
    """
    purpose: a demo of using list_files
    returns: None
    """
    DIR = "/etc/profile.d"
    # """--== SEP_LINE ==--"""
    lines = list_files(DIR)
    lines = gcolumnize(lines, width="60%")
    printit(lines, 'boxed', 'centered', title=f"DIR: {DIR}, gcolumnize(width='60%')", footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    print()
    lines = list_files(DIR, sortby='mtime', with_mdate=True)
    lines = gcolumnize(lines, width="60%", sep=" | ")
    printit(lines, 'boxed', 'centered', title=f"DIR: {DIR}, sortby='mtime' with_mdate=True", footer=dbug('here'))


# #########################
def select_file(path="./", *args, pattern="*", **kwargs):
    # ######################
    """
    purpose: select a file (or dir) from using pattern(s)
    required:
    options:
        - path: str|list  (defaults to "./")
        - pattern: str|list
        - prompt: str
        - mtime: bool      # include mtime in listing
        - centered
        - dirs: bool       # include dirs
        - dirs_only: bool  # only directories
        - shadow: bool
        - title: str
        - footer: str
        - sortby: str      # default='name - or choose "mtime" | "mdate" |"date" then this will sortby mtime
        - width=0
    use: f = select_file("/home/user","*.txt")
    prints a file list and then asks for a choice
    returns basename of the filename selected
    Note: this uses list_files
    """
    # prnt=True, color="", boxed=False, box_color="", title="", footer="", shadow=False, center=False, displaywidth=0, rtrn="value", **kwargs):
    # """--== Config ==--"""
    # prnt = bool_val(["prnt", "print"], args, kwargs, dflt=True)
    color = kvarg_val(["color", 'clr'], kwargs, dflt="")
    # boxed = kvarg_val(["boxed", "box"], kwargs, dflt=False)
    box_color = kvarg_val(['box_color', 'box_clr', 'bx_clr'], kwargs, dflt="")
    title = kvarg_val("title", kwargs, dflt="")
    footer = kvarg_val("footer", kwargs, dflt="")
    shadow = bool_val(["shadow", "shadowed"], args, kwargs, dflt=False)
    centered = bool_val(["center", 'centered'], args, kwargs, dflt=False)
    width = kvarg_val(["width", 'display_width', 'displaywidth', 'length'], kwargs, dflt=0)
    rtrn = kvarg_val("rtrn", kwargs, dflt='value')
    ptrns = kvarg_val(['pattern', 'patterns', 'pat', 'ptrn', 'ptrns'], kwargs, dflt=pattern)
    prompt = kvarg_val('prompt', kwargs, dflt="Please select: ")
    mtime = bool_val(['ll', 'long', 'long_list', 'mtime', 'with_mtime'], args, kwargs, dftt=False)
    # dbug(mtime)
    # choose = bool_val(['choose', 'select', 'pick'], args, kwargs, dflt=True)
    dirs_b = bool_val(['dirs_b', 'dirs', 'dir'], args, kwargs, dflt=False)
    dirs_only = bool_val(['dirs_only', 'dirsonly', 'dironly', 'dir_only', 'only_dirs'], args, kwargs, dflt=False)
    sortby = kvarg_val(['sortby'], kwargs, dflt='name')
    # """--== Process ==--"""
    file_l = list_files(path, ptrns=ptrns, dirs_b=dirs_b, dirs_only=dirs_only, sortby=sortby, with_mtime=mtime)
    # dbug(file_l)
    # dbug(file_l)
    # if not choose:
    #     # just use list_files() instead
    #     return file_l
    file_d = {}
    for file in file_l:
        base_filename = os.path.basename(file)
        file_d[base_filename] = file
    if width == 0:
        width = int(get_columns() * .8)
    if title == "":
        title = " File Selection "
    # dbug(file_d)
    if len(file_d) == 1:
        return file_d
    ans = gselect(file_d, rtrn=rtrn, width=width, box_color=box_color, color=color, centered=centered, shadow=shadow, title=title, footer=footer, prompt=prompt)
    if mtime:
        ans = ans.split()[0]
    # dbug(ans,'ask')
    return ans
    # ### EOB def select_file(path="./", *args, pattern="*", **kwargs): # ###


# ##################################
def reduce_line(line, max_len, pad):
    # ##############################
    """
    purpose: reduce a line to no more than max_len with and no broken words
        then return the reduced_line, and remaining_line
    returns: tuple - this_line(reduced) and the remaining part of the line
    Note - this is used in wrapit() 
    """
    this_line = ""
    remaining_line = ""
    msg_len = len(line)
    msg = line
    if msg_len + pad > max_len:
        # dbug("msg: " + msg)
        # dbug(f"msg_len [{msg_len}] > max_len [{max_len}] and pad: {pad}")
        words = msg.split(" ")
        word_cnt = len(words)
        cnt = 0
        for word in words:
            # dbug("word: " + word)
            # dbug("len(this_line): " + str(len(this_line)))
            if len(this_line) + pad + len(word) + 4 > max_len:
                remaining_line = " ".join(words[cnt:])
                break
            else:
                cnt += 1
                # dbug("adding word: " + word)
                if len(this_line) == 0:
                    this_line += word
                else:
                    this_line += " " + word
                if cnt > word_cnt:
                    break
        # dbug("this_line: " + this_line)
        # dbug("remaining_line: " + remaining_line)
    return this_line, remaining_line


# ####################
def escape_ansi(line, *args, **kvargs):
    # ################
    """
    purpose: Removes ansii codes from a string (line)
    returns: "cleaned no_code" line
    TODO: allow option to return clr_codes[1], nocode(elem), clr_codes[2]
    see: split_codes()
    aka: name should be escape_ansii
    """
    # """--== debugging`` ==--"""
    # dbug(line)
    # dbug(type(line))
    # """--== Converts ==--"""
    line = str(line)  # this is needed
    line = gclr("", line)  # this converts color coded strings to ansii coded first before stripping those codes below
    # dbug('ask')
    # if isinstance(line, list):
    #     dbug(f"line: {type(line)} should be a string, not a list....")
    #     return None
    # else:
    #     line = str(line)
    # """--== Process ==--"""
    # ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    ansi_escape = re.compile(r'\x1b[^m]*m')  # suggested by chatGPT
    # ansi_escape2 = re.compile(r"\[\d+.*?m")  # not needed???????
    # ansi_escape2 = re.compile(r"(?:\x1b[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    # ansi_escape3 = re.compile(r"(?:\033[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    ncline = ""
    if isinstance(line, list):
        new_lines = []
        for new_line in line:
            if not isinstance(new_line, str):
                # dbug(new_line)
                new_lines.append(new_line)
            else:
                if isinstance(new_line, list):
                    if len(new_line) == 0:
                        new_line.append(" ")
                        dbug(f"length of newline was 0 so now new_line: [{repr(new_line)}]... continuing...")
                        continue
                # new_lines.append(ansi_escape.sub("", new_line))
                new_line = ansi_escape.sub("", new_line)
                new_line = re.compile(r"\[\d+.*m")
                # new_line = ansi_escape.sub("", ncline)
                # dbug(new_line)
                # new_line = ansi_escape2.sub("", ncline)
                # dbug(new_line)
                new_lines.append(new_line)
                # new_lines.append(escape_ansi(new_line))
        return new_lines
    if isinstance(line, str):
        # rgx = re.findall(ansi_escape, line)
        # dbug(rgx)
        ncline = ansi_escape.sub("", line)
        # ncline = ansi_escape2.sub("", ncline)
    # dbug(repr(ncline))
    return ncline



# ##############
def nclen(line, *args, **kwargs):
    # ##########
    """
    purpose: finds the length of a string minus any ansi-codes and returns that lenght
    returns: length
    aka: no_color len of line (length w/o ansii codes)
    """
    # """--== Debugging ==--"""
    # dbug(line)
    # dbug(type(line))
    # dbug(len(line))
    # my_dbug = False
    # if "Alabama" in line:
        # my_dbug = True
        # dbug(line)
    # """--== Config ==--"""
    # """--== Inits ==--"""
    nclen = 0
    # """--== Converts ==--"""
    line = str(line)
    # dbug(repr(line))
    # if isinstance(line, str):
    # """--== Process ==--"""
    nc_line = escape_ansi(line)
    # trying to account for weird chars above ascii value 60000
    my_len = 0
    for char in nc_line:
        my_len += 1
        # dbug(repr(char))
        # dbug(ord(char))
        if ord(char) > 60000:
            # dbug(char, 'ask')
            my_len += -1
    # if my_dbug:
        # dbug(my_len)
        # dbug(len(nc_line))
    # nclen = len(nc_line)
    nclen = my_len
    # dbug(repr(nc_line))
    # dbug(f"returning nclen: {nclen}")
    return nclen


# ########################
def do_edit(file, lnum=0):
    # ####################
    """
    purpose: launches vim editor with file
        a quick-n-dirty utility to edit a file
    options:
        - lnum: line number
    Initiate edit on a file - with lineno if provided
    """
    if lnum:
        # cmd = f"vim {file} +{str(lnum)}"
        cmd = "vim " + file + " " + str(lnum)
    else:
        # cmd = f"vim {file}"
        cmd = "vim " + file
    try:
        r = subprocess.call(cmd, shell=True)
    except:
        # this is unlikely and really not a solution because fails on syntax occur on compilation
        cmd = f"vimit {file}"
        r = subprocess.call(cmd, shell=True)
    # print(f"{cmd}")
    return r
    # ### EOB def do_edit(file, lnum=0): ### #``


# ##################################
def cinput(prompt, *args, **kwargs):
    # ##############################
    """
    aka: centered input
    purpose: gets input from user using provided promt - centers the prompt on the screen
    options:
        - shift: int   # allows you to shift the position of the prompt (from the center) eg shift=-5
        - quit|exit|close: bool   # will quit with do_close() if availaable or just sys.exit()
    returns: user response
    """
    # """--== Config ==--"""
    quit = bool_val(['quit', 'exit', 'close'], args, kwargs, dflt=False)
    shift = kvarg_val('shift', kwargs, dflt=0)
    dflt_s = kvarg_val(["default", "dflt"], kwargs, dflt="")
    # dbug(shift)
    # """--== Process ==--"""
    if prompt == "":
        prompt = "Hit Enter to continue..." + dflt_s
    # dbug(prompt)
    prompt = printit(prompt, prnt=False, centered=True, rtrn='str', shift=shift)
    # dbug(prompt)
    # dbug(repr(prompt))
    # dbug(dflt_s)
    ans = input(prompt) or dflt_s
    # dbug(ans)
    if quit and ans.lower() == "q":
        try:
            do_close("Exiting as requested...", 'centered')
        except:
            sys.exit()
    return ans
    # ### EOB def cinput(prompt, *args, **kwargs): ### #


# ##############################################
def pbar(amnt, full_range=100, *args, bar_width=40, show_prcnt=True, **kwargs):
    # ##########################################
    # aliased below to prcnt_bar(...)
    """
    purpose: displays a percentge bar
    args: amnt (prcnt)
    options: full_range=100 if you submit this prcnt will be based on it
        - bar_width=40: int   # declares width of bar
        - color: str          # text color
        - done_color:         # color of done portion
        - undone_color:       # color of undone portion
        - done_chr: str       # done character
        - undone_chr: str     # undone character
        - prompt: str         # prompt (before the bar)
        - suffix: str         # suffix (afterr the bar)
        - brackets=["[", "]"]: list
        - show_prcnt=True: bool  # include the percentage at the end
        - prnt=False: bool  # False to allow use in dashboards  # you can tell this to not print so you can include in in a box etc
    returns: percent bar line as a str
    #>>> rh = 56
    #>>> rl = 50
    #>>> cp = 51
    #>>> amnt = cp - rl
    #>>> full_range = rh - rl
    #>>> print(f"rl {do_prcnt_bar(amnt,full_range)} rh")
    # rl [██████----------------------------------]16% rh
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # """--== Config ==--"""
    full_range = kvarg_val(["full_range", "total", "tot"], kwargs, dflt=full_range)
    bar_width = kvarg_val(["bar_width", 'length', 'width'], kwargs, dflt=bar_width)
    color = kvarg_val(['color'], kwargs, dflt="")
    done_color = kvarg_val(['done_color', 'done_clr'], kwargs, dflt=color)
    # done_chr = u'\u2588'   # █ <-- full, solid shadow
    # done_chr = "\u2593"    # ▓ <-- full, light shadow
    done_chr = "\u2592"      # ▒ <-- full, medium shadow
    # done_chr = "\u2591"    # ░ <-- full, dark shadow
    # done_chr = "\u2584"    # ▄ <-- Lower five eighths bloc
    # rdone_chr = "\u2585"   # ▆ <-- Lower five eighths bloc
    # done_chr = "\u2586"    # ▆ <-- 3/4 high solid block
    # done_chr = "\u2582"    # ▂ <-- lower 1/4 block
    done_chr = kvarg_val(['done_chr', 'chr'], kwargs, dflt=done_chr)
    undone_color = kvarg_val(['undone_color', 'undone_clr', 'fill_color', 'fill_clr'], kwargs, dflt="")
    undone_chr = "\u2015"    # ― <-- horizontal line
    undone_chr = kvarg_val(['fill', 'fc', 'undone_chr'], kwargs, dflt=undone_chr)
    # done_color = sub_color(done_color + " on rgb(255,255,255)")
    # done_chr = done_color + done_chr
    prompt = kvarg_val(["prefix", 'prompt', 'title'], kwargs, dflt="")
    suffix = kvarg_val(["suffix", 'ending', 'end_with'], kwargs, dflt="")
    # brackets = kvarg_val(["brackets"], kwargs, dflt=["", ""])
    brackets = kvarg_val(["brackets"], kwargs, dflt=["[", "]"])
    show_prcnt = bool_val("show_prcnt", args, kwargs, dflt=show_prcnt)
    prnt = bool_val(["prnt", 'print', 'show'], args, kwargs, dflt=False)
    centered = bool_val(["centered", 'center'], args, kwargs, dflt=False)
    # """--== Init ==--"""
    # dbug(done_color)
    COLOR = sub_color(color)
    DONE_COLOR = sub_color(done_color)
    UNDONE_COLOR = sub_color(undone_color)
    RESET = sub_color('reset')
    if color == "" and done_color == "" and undone_color == "":
        # dbug()
        RESET = ""
    # """--== Converts ==--"""
    if isinstance(amnt, str):
        amnt = amnt.replace("*", "")
    # """--== Process ==--"""
    amnt = float(escape_ansi(amnt))
    full_range = float(full_range)
    try:
        prcnt = float(amnt / full_range)
    except Exception as Error:
        dbug(f"prcnt calc failed... amnt: {amnt} / full_range: {full_range}... returning None")
        return None
    # dbug(f"amnt: {amnt} full_range: {full_range} prcnt: {prcnt} bar_width: {bar_width}")
    # done_len = int(prcnt / 100 * bar_width)
    done_len = int(prcnt * bar_width)
    done_len = ceil(prcnt * bar_width)
    undone_len = int(bar_width - done_len)
    # dbug(f"done_len: {done_len} undone_len: {undone_len}")
    done_fill = DONE_COLOR + done_chr * done_len
    undone_fill = UNDONE_COLOR + (undone_chr * undone_len)
    # dbug(undone_fill)
    bar = done_fill + undone_fill   # <--bar
    # dbug(bar)
    # dbug(f"bar_width: {bar_width} len(bar): {len(bar)}")
    # if len(bar) > bar_width:
        # # happens with neg percent
        # bar = bar[:bar_width]
    # bar = COLOR + brackets[0] + RESET + bar + COLOR + brackets[1]
    # dbug(bar)
    rtrn = bar
    if show_prcnt:
        prcnt = str(ceil(prcnt * 100)) + "%"
        rtrn = COLOR + prompt + RESET + bar + UNDONE_COLOR + COLOR + f"{prcnt:>4}" + suffix
    if prnt:
        printit(RESET + rtrn + RESET, prnt=prnt, centered=centered, rtrn_type='str')
    return RESET + rtrn + RESET
    # ### EOB def pbar(amnt, full_range=100, *args, bar_width=40, show_prcnt=True, **kwargs): ### #


# alias
do_prcnt_bar = pbar  # for back compatibility
# prcnt_bar = pbar
# percent_bar = pbar


def pbar_demo(*args, **kwargs):
    """
    purpose: demo of do_prcnt_bar()
    """
    cmd = "upower -i `upower -e | grep BAT`"
    out = run_cmd(cmd, 'list')
    content_line = "state:  unknown"
    fill_sep = " " * 39
    found_l = grep_lines(out, r"percent|state")
    for line in found_l:
        if 'percent' in line:
            words = line.split(":")
            for word in words:
                word = word.strip()
                word = word.replace("%", "")
                if isnumber(word):
                    prcnt = int(word)
        if 'state' in line:
            words = line.split()
            if 'discharging' == words[1]:
                content_line = f"{words[0]}{fill_sep[:-3]}{gclr('red!')}{ words[1].upper()}{RESET}"
            if 'charging' == words[1]:
                content_line = f"{words[0]}{fill_sep}{gclr('green!')}{ words[1].upper()}{RESET}"
            if 'charged' in words[1]:
                content_line = f"{words[0]}{fill_sep[:-5]}{gclr('green!')}{ words[1].upper()}{RESET}"
    content = content_line
    undone_color = "red!"
    done_color = "green!"
    text_color = 'white'
    box_color = 'white!'
    if prcnt < 35:
        box_color = 'yellow'
    if prcnt < 15:
        box_color = 'red'
    if prcnt > 85:
        box_color = 'green'
    prompt = "Battery: "
    p_bar = do_prcnt_bar(prcnt, prompt=prompt, color=text_color, done_color=done_color, undone_color=undone_color)
    msg = [content, p_bar]
    printit(msg, 'shadowed', 'boxed', 'centered', box_color=box_color, color=text_color)
    return




# #############################################
def progress(progress, *args, **kwargs):
    # #########################################
    """
    purpose: displays a progress bar typically used within a loop
    options:
       - width 
       - prompt
       - color
       - done_color
       - undone_color
       - prnt
       - COLOR
       - DONE_COLOR
       - UNDONE_COLOR
       - RESET
       - done_chr 
       - undone_chr 
       - status 
       - center_b 
       - shift:
    returns: none
    # prcnt = 0.20
    # progress(prcnt, width=60)
    Percent: [############------------------------------------------------] 20%
    # or
    >>> for i in range(100):
    ...     time.sleep(0.1)
    ...     progress(i/100.0, width=60)
    Percent: [############################################################] 99%
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # """--== Config ==--"""
    width = kvarg_val(['bar_width', 'length', 'width'], kwargs, dflt=40)  # Modify this to change the length of the progress bar  # noqa:
    prompt = kvarg_val(['prompt', 'prefix'], kwargs, dflt="")
    color = kvarg_val(['color', 'text_color', 'txt_color', 'txt_clr'], kwargs, dflt="")
    done_color = kvarg_val(['done_color'], kwargs, dflt="")
    undone_color = kvarg_val(['fill_color', 'fcolor', 'fclr', 'undone_color'], kwargs, dflt="")
    prnt = bool_val(['print', 'prnt'], args, kwargs, dflt=True)
    COLOR = sub_color(color)
    DONE_COLOR = sub_color(done_color)
    UNDONE_COLOR = sub_color(undone_color)
    RESET = sub_color('reset')
    # FILL_COLOR = sub_color(fill_color)
    done_chr = kvarg_val(['done_chr', 'chr'], kwargs, dflt="\u2588")
    undone_chr = kvarg_val(['fill_chr', 'fc', 'undone_chr'], kwargs, dflt=" ")
    status = kvarg_val(['status', 'done_msg', 'done_txt', 'done_text', 'post_prompt', 'suffix'], kwargs, dflt="")
    center_b = bool_val(["centered", "center"], args, kwargs, dflt=False)
    shift = kvarg_val("shift", kwargs, dflt=0)
    # """--== SEP_LINE ==--"""
    if isinstance(progress, int):
        progress = float(progress)
        # if not isinstance(progress, float):
        # progress = 0
        # status = "error: progress var must be float\r\n"
    # """--== SEP_LINE ==--"""
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
        if prnt:
            sys.stdout.write('\x1b[?25h')  # retore cursor
            sys.stdout.flush()
    if progress >= 1:
        progress = 1
        if prnt:
            status = f"{status}\r\n"
            status += "\x1b[?25h"          # Restore cursor
            sys.stdout.write('\x1b[?25h')  # retore cursor
            sys.stdout.flush()
        # dbug(status)
    done_len = int(round(width * progress))
    done_fill = done_chr * done_len + RESET
    undone_fill = undone_chr * (width - done_len) + RESET
    shift = abs(shift)
    prcnt = progress * 100
    # """--== SEP_LINE ==--"""
    if center_b:
        # ruleit()
        shift -= (int(get_columns()) - (width + nclen(prompt))) // 2
        # dbug(shift)
        lfill = " " * shift
        prompt = lfill + prompt
    txt = COLOR + f"\r{prompt}[{RESET}" + DONE_COLOR + f"{done_fill}" + RESET + UNDONE_COLOR + f"{undone_fill}" + COLOR + f"] {prcnt}%"
    txt = txt + f" {status}" + RESET
    # """--== SEP_LINE ==--"""
    if prnt:
        sys.stdout.write('\x1b[?25l')  # Hide cursor
        sys.stdout.write(txt)
        sys.stdout.flush()
    # dbug(txt)
    return txt
    # ### EOB def progress(progress, *args, **kwargs): ### #


# ################################
def from_to(filename, *args, include="none", **kwargs):
    # ############################
    """
    purpose: returns lines from a *file* from BEGIN pattern to END pattern" (between BEGIN and END)
    required:
        - filename: str|list  # filename to parse or content (ie lines of text)
        - begin: str          # pattern in line to begin with
        - end: str            # pattern in line to end with
    options:
    -  include: can be equal to "none", top|begin|start, bottom|end, or 'both'
    --    include='top' will include the begin pattern line, (also: 'top' '| 'before' | 'begin')
    --    include='bottom' will include the end pattern line  )also: 'after' | 'end')
    --    include='both' will include top and end pattern matching lines
    returns: lines between (or including) begin pattern and end pattern from filename (or a list of lines)
    note: begin is used here because 'from' is a python keyword
    """
    # dbug(funcname())
    # dbug(filename)
    # dbug(begin)
    # dbug(end)
    # """--== Config ==--"""
    begin = kvarg_val(['begin', 'after'], kwargs, dflt="")  # you can not use 'from' a variable name becuase it is apython keyword
    # dbug(begin)
    end = kvarg_val(['end', 'to', 'before'], kwargs, dflt="")
    # dbug(end)
    # """--== Init ==--"""
    include = include.lower()  # can be 'top', 'bottom', or both to include the {begin} and or {after}
    lines = []
    return_lines = []
    start_flag = False
    # dbug(f"begin: [{begin}] end: [{end}]")
    # askYN()
    # """--== Convert ==--"""
    if "\n" in filename:
        filename = filename.split("\n")
    if isinstance(filename, list):
        lines = filename
    else:
        lines = cat_file(filename, 'lst')
        # with open(filename) as fp:
        #     lines = fp.readlines()
    # dbug(lines)
    """--== Process ==--"""
    for line in lines:
        # dbug(line)
        line = line.rstrip("\n")
        beg_regex = re.search(begin, line)
        end_regex = re.search(end, line)
        # dbug(f"chkg line: {line} begin: {begin} end: {end}")
        # if end in line and start_flag:
        if end_regex and start_flag:
            # dbug(f"Found {end} in [line]")
            # askYN()
            if include in ("bottom", "end", "both", "after", 'all'):
                return_lines.append(line)
                # dbug(f"Added [{line}]")
            # return_lines = [line.strip() for line in return_lines]
            return return_lines
        if start_flag:
            return_lines.append(line)
            # dbug(f"Added [{l}]")
        # if begin in line:
        if beg_regex:
            # dbug(f"Found {begin} in {line}")
            start_flag = True
            if include in ("top", "start", "begin", "both", "before", 'all'):
                return_lines.append(line)
                # dbug(f"Added [{line}]")
            else:
                continue
    return return_lines  # return lines if end not found
    # ### END def from_to(filename, begin, end): ### #


def from_to_demo(*args, **kwargs):
    """
    purpose: quick demo of from_to()
    required:
    """
    content = """
    one
    two
    three
    four
    five
    six """
    begin_pat = "tw"
    end_pat = "ou"
    printit(content, 'boxed', title="Content to be parsed", footer=dbug('here'))
    lines = from_to(content, begin=begin_pat, to=end_pat)
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}') [nclude default is 'none']")
    lines = from_to(content, begin=begin_pat, to=end_pat, include="before")
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}', include='before')")
    lines = from_to(content, begin=begin_pat, to=end_pat, include="after")
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}', include='after')")
    lines = from_to(content, begin=begin_pat, to=end_pat, include="both")
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}', include='both')")
    """--== SEP_LINE ==--"""
    content = """
    one
    == 0.1.4a0 ==
    two
    three
    == 0.1.3 ==
    four
    five
    """
    begin_pat = "= \d\.\d\.\da0 ="
    end_pat = "= \d\.\d\.\d ="
    printit(content, 'boxed', title="Content to be parsed", footer=dbug('here'))
    lines = from_to(content, begin=begin_pat, to=end_pat)
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}') [nclude default is 'none']")
    lines = from_to(content, begin=begin_pat, to=end_pat, include="before")
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}', include='before')")
    lines = from_to(content, begin=begin_pat, to=end_pat, include="after")
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}', include='after')")
    lines = from_to(content, begin=begin_pat, to=end_pat, include="both")
    printit(lines, 'boxed', title=f"from_to(content, begin=''{begin_pat}', end='{end_pat}', include='both')")



# ############################################################
def add_content(file, content="", header="", **kvargs):
    # ########################################################
    """
    purpose: will add content to a file at a specified point in the file (after=pattern or before=pattern) or position=n)
    Required:
        file: str
        content: str | list | dict
    Options:
        after: str     =pattern
        before: str    =pattern
        replace: str   =pattern
        position: int  =##
        if none of those,  content is appended to the end of the file
        if content is a dictionary the will be considered the keys() and  if the header is also included 
            it will be added to the begining of the file (if it does not already exist)
    notes: I wrote this because I am constantly building csv files with a header line
        (also consider add_or_replace() function)
        used_to_be: add_line()
    """
    # dbug(funcname(), 'centered')
    # """--== Config ==--"""
    position = kvarg_val('position', kvargs, dflt=None)
    after = kvarg_val("after", kvargs, dflt="")
    before = kvarg_val("before", kvargs, dflt="")
    replace = kvarg_val("replace", kvargs, dflt="")
    backup = kvarg_val("backup", kvargs, dflt=False)
    pattern = ""
    if after != "":
        pattern = after
    if before != "":
        pattern = before
    if replace != "":
        pattern = replace
    # dbug(f"file: {file} header: {header} after: {after} before: {before} pattern: {pattern} position: {position}")
    show = kvarg_val('show', kvargs, dflt=False)
    DBUG = show
    # dbug(position)
    # """--== Functions ==--"""
    def insert_line(file, line, position=None):
        # dbug(position)
        lines = []
        lines = cat_file(file, 'list')
        # lines.insert(position, line)
        if position is None:
            if isinstance(line, list):
                line = "\n".join(line)
            f = open(file, "a")
            f.write(line)
            if not line.endswith("\n"):
                f.write("\n")
            # f.write(line)
            f.close()
            return
        new_lines = []
        if len(lines) > 0:
            for n, l in enumerate(lines):
                # dbug(f"position: {position} n: {n} l: {l}")
                if n == position and position == 0:
                    new_lines.append(line)
                if (n + 1) != position:
                    new_lines.append(l)
                else:
                    line_l = []
                    line_l = line.split("\n")
                    new_lines.extend(line_l)
                    new_lines.append(l)
        else:
            if isinstance(line, list):
                new_lines.extend(line)
            else:
                new_lines.append(line)
        f = open(file, "w")
        for line in new_lines:
            f.write(line + "\n")
        f.close()
    # """--== Process ==--"""
    if isinstance(content, dict):
        # assumes this is key, value pairs for one intended line str
        # turn the dict into a string of lines using the values, set header= keys
        content_d = {str(key): str(value) for key, value in content.items()}
        # values = content_d.values()
        # dbug(values)
        content_s = ",".join(content_d.values())
        header = list(content_d.keys())
        # dbug(content_s)
        content = content_s
        # dbug(header)
    if isinstance(content, list):
        # turn list into string of lines
        content = "\n".join(content)
    # """--== handle backup ==--"""
    if backup:
        if file_exists(file):
            import shutil
            bak_ext = "-" + datetime.now().strftime("%Y%m%d-%H%M%S")
            trgt_file = file + bak_ext
            # shutil.copy(file, trgt_file)
            shutil.copyfile(file, trgt_file)
            dbug(f"Backed up file: {file} to {trgt_file}", dbug=DBUG)
        else:
            dbug(f"file: {file} does not exist yet ... backup skipped...", dbug=DBUG)
    # """--== write new file ==--"""
    if not file_exists(file):
        f = open(file, "w")
        f.write(content)
        f.close()
    else:
        # dbug(f"position: {position} pattern: {pattern}")
        if pattern != "":
            for line_no, line in enumerate(cat_file(file, 'list'), start=1):
                if pattern in line:
                    if before != "":
                        position = line_no
                        insert_line(file, content, position)
                    if after != "":
                        position = line_no + 1
                        insert_line(file, content, position)
                    if replace != "":
                        import in_place
                        with in_place.InPlace(file) as f:
                            for f_line in f:
                                new_line = line.replace(f_line, content)
                                f.write(new_line)
                    break
        if position is None and pattern == "":
            insert_line(file, content, position)
    # """--== assure header is first ==--"""
    if isinstance(header, list):
        header = ",".join(header)
        # header = "# " + header.replace(",", ":")
    if header != "":
        with open(file, "r") as f:
            first_line = f.readline()
            for line in f:
                # skip the rest
                pass
        if header not in first_line:
            # dbug(f"Header not found ... so inserting header: {header} at position 0")
            insert_line(file, header, position=0)
        # else:
            # dbug(f"Header already exists in the first_line: {first_line}", dbug=DBUG)
    if show:
        printit(cat_file(file), 'boxed', title=f" {funcname()}() ")
    return
    # ### def add_content(file, content="", header="", **kvargs): ### #


# ###############
def sorted_add(filename, line, after="", before=""):
    """
    purpose: to insert a line between two patterns in a sorted way
        insert line into filename between after and before patterns
        the patterns need to be regex ie: r"pattern"
        assumes the block from after to before is sorted
    returns: new_lines
    eg:
     line = 'Insert this line (alphabetically) after "^-alt" but before "^-[a-zA-Z0-9] within block'
     filename = "/home/geoffm/t.f"
     after = r"^-alt"
     before = r"^-[a-zA-Z0-9]"
     lines = sorted_add(filename, line, after, before)
     printit(lines)
    """
    # TODO if after and before are empty just use the whole file
    # tst_lines = from_to(filename, begin=after, end=before)
    # dbug(tst_lines)
    lines = cat_file(filename, lst=True)
    insert_line = line
    # dbug(insert_line)
    # srch_block = False
    inserted = False
    new_lines = []
    # last_line = "0"
    begin = after
    end = before
    beg_regex = False
    end_regex = False
    # end_flag = False
    for ln in lines:
        # dbug(f"working ln: {ln}")
        # if beg_regex and end_regex:
        #     dbug("Done line should have been inserted... but will append ln")
        # else:
        if beg_regex and not end_regex:
            # dbug(f"now chkg ln: {ln} for end_regex")
            end_regex = re.search(end, ln)
            if end_regex and not inserted:
                new_lines.append(insert_line)
                inserted = True
                # dbug(f"Inserted: {insert_line}")
            if not end_regex and not inserted:
                if len(ln) > 0:
                    # case insensitive
                    if insert_line.lower() < ln.lower():
                        # dbug(f"insert_line: \n{insert_line}\n <\nln: {ln}")
                        new_lines.append(insert_line)
                        inserted = True
                        # dbug(f"Inserted: {insert_line}")
        else:
            beg_regex = re.search(begin, ln)
        # dbug(f"beg_regex: {beg_regex} end_regex: {end_regex}")
        # last_line = ln
        new_lines.append(ln)
    # printit(new_lines)
    return new_lines
    # ### EOB def sorted_add() ### #


# ###############
def try_it(func, *args, attempts=1, **kwargs):
    # ###########
    """
    BROKEN BROKEN BROKEN
    This is a wrapper function for running any function that might fail
    - this will report the error and move on
    use:
        @try_it
        def my_func():
            print("if this failed an error would be reported ")
        my_func()
    """
    def inner(*args, **kwargs):
        # for n in range(attempts):
        #     try:
        #         r = func(*args, **kwargs)
        #         dbug(f"Returning r: {r}")
        #     except Exception as e:
        #         dbug(f"Error: {e} in: {func}")
        #         return None
        #     return r
        rsps = func(*args, **kwargs)
        return rsps
    r = inner(*args, **kwargs)
    dbug(f"returning {r}")
    return r


# ##############################
def max_width_lol(input_table):
    # ##########################
    """
    purpose: to determin max_width for each "column" in a list of lists
        this is a way of truncating "columns"
    returns: column sizes
    """
    # dbug(type(input_table))
    # dbug(input_table)
    columns_size = [0] * len(input_table[0])
    last_row_len = len(input_table[0])
    for row in input_table:
        if len(row) < last_row_len:
            dbug("WARNING: Found inconsistent row lengths... returning")
            dbug(f"last_row_len: {last_row_len} this row len: {len(row)}")
            dbug(row)
            dbug(f"First row len: {len(input_table[0])}")
            return
        # dbug(len(row))
        # dbug(type(row))
        for j, column_element in enumerate(row):
            columns_size[j] = max(columns_size[j], len(str(column_element)))
    return columns_size


# ####################
def comma_split(my_s, *args, **kwargs):
    # ################
    """
    purpose: split a line/str (or list of lines) using commas unless the comma is embedded in quotes
    returns: list (or list od lists) of comma separated elements
    notes: this is a kludge but it works for me
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # """--== Recurse if my_s is a list ==--"""
    if isinstance(my_s, list):
        # we will need to recurse...
        # dbug(my_s[:3])
        new_l = []
        for ln in my_s:
            # dbug(ln)
            new_ln = comma_split(ln)
            # dbug(new_ln, 'ask')
            new_l.append(new_ln)
    # """--== Process ==--"""
    # new_l = re.split(r'(?:,\s*)(?=(?:[^"]*"[^"]*")*[^"]*$)', my_s)
    # dbug(new_l)
    if isinstance(my_s, str):
        # this breaks if a single quote mark is embedded in an element - even if it is embedded in a quote bound string TODO - your need to escape it? to avoid this issue?
        comma_pat = re.compile(r",(?=(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)")
        split_result = comma_pat.split(my_s)
        # dbug(split_result)
        new_l = []
        for elem in split_result:
            elem = elem.strip()
            # dbug(elem)
            if elem.startswith('"') and elem.endswith('"'):
                # dbug(elem)
                elem = elem.strip('"')
                # dbug(elem)
            if elem.startswith("'") and elem.endswith("'"):
                # dbug(elem)
                elem = elem.strip("'")
                # dbug(elem)
            if "'" in elem and "," in elem:
                elems = elem.split(",")
                new_l.extend(elems)
            else:
                new_l.append(elem)
    return new_l
    # ### EOB def comma_split(my_s): ### #


def comma_split_demo(*args, **kwargs):
    """
    purpose: demo of using comma_split()
    return: None
    """
    s = "one, two, 'three,with a comma', four"
    dbug(s)
    dbug(comma_split(s))
    print("-"*40)
    s_l = [s, 'six, "seven, with comma", eight']
    dbug(s_l)
    dbug(comma_split(s_l))
    print("-"*40)
    s = "col1_val, col2_val, 'col3w/comma,val', \"col4alsow/comma,val\", col5_val"
    dbug(s)
    dbug(comma_split(s))
    print("-"*40)
    ln = "Root beer chops, 'Original recipe yields 4 srvngs, 4 (1-inch thick) pork chops, 3 turtle doves'"
    dbug(ln)
    dbug(comma_split(ln))
    print("-"*40)
    ln = "Root beer chops, 'Original recipe yields 4 srvngs, Use a #4 pan, 4 (1-inch thick) pork chops, 3 turtle doves'"
    dbug(ln)
    dbug(comma_split(ln))
    print("-"*40)


def comma_join(data, *args, **kwargs):
    """
    purpose: given a list of elems or list or lists (of elems
            this function will turn each row into a proper comma delimited string or line
            The reason for this function is to take a list and make *sure* it is a proper csv list - with quoted elems as needed
    options:
        - newlines = bool - False  # to be used if you want to add a newline to the end of the line(s)
    returns: a list of comma delimited strings (lines) typically used for csv
    notes: this has not been fully tested yet
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(data)
    # dbug(data[:3])
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    newline_b = bool_val(["newlines", "newline"], args, kwargs, dflt=False)
    # """--== Init ==--"""
    line = ""
    elems = []
    # """--== Convert ==--"""
    if isinstance(data, str):
        dbug("Nothing to do ... comma_join needs a list...")
        return
    if islol(data):
        rtrn_l = []
        for row in data:
            new_ln = comma_join(row, newline=newline_b)
            rtrn_l.append(new_ln)
        return rtrn_l
    # dbug(data)
    # """--== SEP_LINE ==--"""
    for elem in data:
        # dbug(elem)
        elem = str(elem)
        if "," in elem or "'" in elem:
            elem.replace('"', '\\"')
            elem.replace("'", "\\'")
            elem = '"' + elem + '"'
        # dbug(f"adding elem: {elem}")
        elems.append(elem)
    line = ", ".join(elems)
    # dbug(line, 'lst')
    # if not lol_flag:
    #     dbug(lines)
    #     # this is such a kludge to deal with a simple list
    #     if len(lines) == 1:
    #         lines = lines[0]
    if newline_b:
        # dbug(newlines)
        line = str(line) + "\n"
    # dbug(f"Returning line: {line}...")
    return line
    # ### EOB def comma_join(data, *args, **kwargs): ### #


def comma_join_demo(*args, **kwargs):
    """
    purpose: demo of using comma_join()
    returns: None
    """
    my_l = ["Date Time", "Values", "value, with a comma"]
    print(f"my_l: {my_l}")
    comma_line = comma_join(my_l)
    printit(comma_line, 'boxed', title="list is now comma delinted string")
    print("-"*40)
    my_lol = [my_l, ["2022-01-22 09:44", 64]]
    print(f"my_lol: {my_lol}")
    comma_lines = comma_join(my_lol)
    printit(comma_lines, 'lst', 'boxed', title="lol is now list of comma delimited string", footer=dbug('here'))
    return None


# ##################################
def get_elems(lines, *args, index=False, col_limit=20, **kwargs):
    # ##############################
    """
    purpose: designed to split a list of lines on delimiter - respects quoted elements that may contain "," even if that is the delimiter
        - wip - this does the same thing as comma_split but adds a few options TODO
    Input:
        lines (as a list)
    options:
        - delimiter: str     # (default is a comma)
        - col_limit: bool    # max column size default=0 - if 0 no truncation occurs otherwise all elems are limited to col_limit
        - index: bool        # will insert an index (line numbers starting with 0)  # not used yet TODO
        - lst: bool          # assumes a single line (ie: lines = str) so it returns a list of elemes from
                                that line instead of a list_of_elems for multiple lines (ie an lol)
    Returns:
        an array: list of list (lol - lines of elements aka rows and columns)
        aka rows_lol
    Notes: be carefull - if a "#" is encountered it will be treated as the begining of a comment
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(lines[:3])
    # dbug(index)
    # dbug(col_limit)
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    delimiter = kvarg_val(["delim", 'delimiter'], kwargs, dflt=",")
    col_limit = kvarg_val(["col_limit", 'collimit' 'colmax', 'col_max'], kwargs, dflt=0)  # not used yet TODO
    index = kvarg_val(["index", 'indx', 'idx'], kwargs, dflt="")  # not used yet TODO
    # dbug(delimiter)
    lst_b = bool_val(["list", "lst"], args, kwargs, dflt=False)
    """--== Imports ==--"""
    # import pyparsing as pp
    # """--== Init ==--"""
    my_array = []
    # """--== Convert ==--"""
    # make it a list of lines
    if isinstance(lines, str):
        lines = [lines]
        # dbug(lines[:3])
    # """--== Validate ==--"""
    if "," not in lines[0] and "," in delimiter:
        # dbug("delimiter: [{delimiter}] not found in lines[0]: {lines[0]} reverting to a whitespace ")
        delimiter = " "
        if delimiter not in lines[0]:
            dbug("delimiter: [{delimiter}] not found in lines[0]: {lines[0]} reverting to a whitespace ")
    # """--== SEP_LINE ==--"""
    if delimiter == " ":
        new_rows = []
        for line in lines:
            elems = line.split()
            # dbug(elems)
            # new_line = ",".join(line.split())
            new_rows.append(elems)
        delimiter = ","
        my_array = new_rows
        # dbug(my_array[:2])
    else:
        # dbug(lines[:3], 'ask')
        my_array = comma_split(lines)
        # dbug(my_array[:3], 'ask')
    # """--== Process ==--"""
    # import csv
    # my_array = csv.reader(lines)
    # dbug(list(my_array)[:3])
    # my_array = list(csv.reader(lines, delimiter=delimiter))
    # dbug(my_array[:3])
    # my_array = list(my_array)
    """--== SEP_LINE ==--"""
    if index:
        for n, row in enumerate(my_array):
            # dbug(f"n: {n}")
            row.insert(0, str(n))
    # dbug(f"len(lines): {len(lines)} len(my_array): {len(my_array)} delimiter: {delimiter}\nmy_array[:2]: {my_array}[:2]")
    # dbug(f"Returning my_array[:2]: {my_array[:2]}")
    if lst_b:
        # this all may change to testing if len(my_array) == 1 then do this
        my_array = my_array[0]
    # """--== SEP_LINE ==--"""
    new_array = []
    for row in my_array:
        my_row = []
        for elem in row:
            if elem.startswith('"') and elem.endswith('"'):
                elem = elem.strip()
                # dbug(elem)
                elem = elem.strip('"')
                # dbug(elem)
            if elem.startswith("'") and elem.endswith("'"):
                # dbug(elem)
                elem = elem.strip("'")
                # dbug(elem)
            my_row.append(elem)
            if col_limit > 0:
                elem = elem[:col_limit]
        new_array.append(my_row)
    # dbug(new_array)
    if index:
        new_array = [row.insert(n) for n, row in enumerate(new_array)]
        # dbug(new_array)
    """--== SEP_LINE ==--"""
    # dbug(f"Returning my_array: {my_array}")
    # return my_array  # aka rows_lol
    # dbug(f"Returning my_array: {new_array}")
    return new_array  # aka rows_lol
    # ### EOB def get_elems(lines, *args, index=False, col_limit=20, **kwargs): ### #


def get_elems_demo(*args, **kwargs):
    """
    purpose: demo of get_elems()
    returns: None
    """
    strng_l = ["one, two, 'three,with a comma', four", "another, 'row', of, cols"]
    dbug(strng_l)
    dbug(get_elems(strng_l))
    dbug(get_elems(strng_l), 'idx')
    print("-"*40)
    strng2_l = strng_l + ['six, "seven, with comma", eight']
    dbug(strng2_l)
    dbug(get_elems(strng2_l))
    print("-"*40)
    strng = "col1_val, col2_val, 'col3w/comma,val', \"col4alsow/comma,val\", col5_val"
    dbug(strng)
    dbug(comma_split(strng))
    print("-"*40)
    line = "Root beer chops, 'recipe yields 4 srvngs, 4 pork chops, 3 turtle doves'"
    dbug(line)
    dbug(comma_split(line))
    print("-"*40)


def pyscraper(url, pat):
    """
    I may deprecate this as I rarely use it
    example: pat
    # pat = '<span class="Trsdu\(0.3s\) Fw\(b\) Fz\(36px\) Mb\(-4px\) D\(ib\)" data-reactid=".*?".*?>.*?</span.*?>'   # noqa:
    Be careful... pay attention to the html page when using a script ... many sites detect the script and block real output
    Required:
        from urllib.request import urlopen
        import re
    """
    # dbug(type(url))
    html = ""
    if file_exists(url):
        # treat this as a file instead of an url
        html = cat_file(url)
    if isinstance(url, list):
        html = "".join(url)
    if isinstance(url, str):
        if html == "" and url.startswith("http"):
            for attempts in range(3):
                try:
                    page = urlopen(url)
                    html = page.read().decode("utf-8")
                    break
                except Exception as e:
                    dbug(f"Attempt: {attempts} ... Retrieving url: {url} failed Error: {e}")
    match_results = re.search(pat, html, re.IGNORECASE)
    if match_results is None:
        print()
        warn = f"\n\nUsing url: {url}\nNo matches found with pat: [{pat}]\n"
        dbug(warn)
        if askYN("Do you want to see the returned html content?", "y"):
            dbug(html)
        return None
    r = match_results.group()
    # now remove html tags
    r = re.sub("<.*?>", "", r)  # Remove HTML tags
    return r
    # ### def pyscraper(url, pat): ### #


# ############################################################
def try_to_get(driver, pat="", by_type="link", action="none"):
    # ########################################################
    """
    may deprecate this as I rarely use it
    This is for use with selenium
    requires:
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
    """
    # """--== debugging ==--"""
    # dbug(funcname())
    # """--== Imports ==--"""
    # from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    # dbug(driver.title)
    # """--== Init ==--"""
    time_to_wait = 10
    # """--== Process ==--"""
    try:
        if by_type == "link":
            element = WebDriverWait(driver, time_to_wait).until(EC.presence_of_element_located((By.LINK_TEXT, pat)))
            element.send_keys(Keys.RETURN)
            # do_nc(element)
        if by_type == "id":
            element = WebDriverWait(driver, time_to_wait).until(EC.presence_of_element_located((By.ID, pat)))
        # if action == "click":
        #    element.send_keys(Keys.RETURN)
        # dbug(f"Looking by: {by_type} for pat: {pat}")
        return element
    except Exception as Error:
        dbug(f"Failed to find pattern: {pat}")
        dbug(driver.title)
        driver.close()
        do_close(f"Failed... Error: {Error}")
        # return False
    # ### EOB def try_to_get(driver, pat, by_type, action) ### #


def has_alnum(string):
    """
    purpose: test whether a string is all alpha numeric
    Is a string blank or all white space...
    isspace() does the samething
    """
    for char in string:
        if char.isalnum():
            return True
    return False


def retry(howmany, *exception_types, **kwargs):
    """
    purpose: a wrapper to retry a function x (howmany) times
    notes: there is a module called retrying that deserves more research and it provides a wrapper function called @retry()
    useage: eg:
        @retry(5, MySQLdb.Error, timeout=0.5)
        def the_db_func():
            # [...]
            pass
    This is untested - completely expimental
    It is essentially the same as:
    for attempts in range(3):
        try:
            do_work()
            break
        except Exception as e:
            print(f"Attempts: {attempts}. We broke with error: {e}")
    """
    try:
        import decorator
    except Exception as e:
        dbug(f"Failed to import decorator Error: {e}")
    timeout = kwargs.get('timeout', 0.0)  # seconds
    @decorator.decorator
    def tryit(func, *fargs, **fkwargs):
        for _ in range(howmany):
            try:
                return func(*fargs, **fkwargs)
            except exception_types or Exception:
                if timeout is not None:
                    time.sleep(timeout)
    return tryit


# ########################################################################
def get_html_tables(url="", *args, **kwargs):
    # ####################################################################
    """
    purpose: to pull/scrape all tables off an url
    required:  url
    requires:
        import pandas as pd
        from selenium import webdriver
    options:
        - show|prnt: bool  # default=False ... whether to print the tables
        - spinner: bool    # default=False ... whether to show a spinner while fetching data
        - selenium: bool   # default-False ... whether to use selenium 
    returns: list of panda dataframes
    """
    """--== Debugging ==--"""
    # dbug(funcname())
    """--== Config ==--"""
    prnt = bool_val(["prnt", "print", "show", "verbose"], args, kwargs, dflt=False)
    spinner_b = bool_val(["spinner"], args, kwargs, dflt=False)
    selenium_b = bool_val(["selenium"], args, kwargs, dflt=False)
    # """--== Validation(s) ==--"""
    # """--== Init ==--"""
    tables = []
    # """--== Process ==--"""
    if selenium_b:
        # dbug("trying selenium to by-pass possible 'Forbidden' consequences")
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options
        # from selenium.webdriver.common.keys import Keys
        # """--== Init ==--"""
        options = Options()
        options.headless = True
        # driver = webdriver.Firefox(executable_path="./bin/geckodriver", options=options)
        # driver = webdriver.Firefox(executable_path="./bin/geckodriver")
        driver = webdriver.Firefox(options=options)
        # """--== SEP_LINE ==--"""
        try:
            if spinner_b:
                with Spinner(f"Retrieving data from url: {url}", 'centered', 'elapsed', elapsed_clr="yellow! on black"):
                    driver.get(url)
            else:
                driver.get(url)
        except Exception as e:
            dbug("See: \nhttps://selenium-python.readthedocs.io/installation.html#drivers ... for drivers")
            dbug(f"Web driver failed on url: {url}... Error: {e}")
            dbug("We look for the geckodriver in your PATH")
            dbug("Note: install the browser (firefox) executable manually... not with snap")
            dbug(f"Get url: {url} failed.... Error: {e}")
            return
        content = driver.page_source
        tables = pd.read_html(content)
    else:
        if spinner_b:
            with Spinner(f"Retrieving data from url: {url}", 'centered', 'elapsed', elapsed_clr="yellow! on black"):
                try:
                    tables = pd.read_html(url)
                except Exception as Error:
                    add_msg = ""
                    if "Forbidden" in str(Error):
                        add_msg = " Consider the selenium=True option"
                    dbug(f"No tables found for url: {url}...Error: {Error}" + add_msg)
                    return
        else:
            try:
                dbug(f"Attempting pd.read_html({url})")
                tables = pd.read_html(url)
            except Exception as Error:
                add_msg = ""
                if "Forbidden" in str(Error):
                    add_msg = " Consider the selenium=True option"
                dbug(f"No tables found for url: {url} ...Error: {Error}" + add_msg)
                return
    if isempty(tables):
        dbug(f"No tables found at url {url}")
        return None
    # """--== show tables ==--"""
    if prnt:  # this is primarily for debugging
        # dbug(f"There are {len(tables)} tables for url: {url}")
        cnt = 1
        for table in tables:
            # dbug(type(table))
            # dbug(f"Printing table: {cnt} of {len(tables)} tables from url: {url}")
            gtable(table, 'hdr', 'prnt', title=f"url: {url} tables[{cnt}] of {len(tables)} tables", footer=dbug('here'))
            cnt += 1
    # """--== Return tables ==--"""
    return tables
    # ### EOB def get_html_tables(url="", access="selenium", show=False): ### #


def get_html_tables_tst(*args, **kwargs):
    # from gtoolz import gtable
    url = "https://finance.yahoo.com/world-indices?guccounter=1"
    tables = get_html_tables(url)
    # dbug(tables)
    gtable(tables[0], 'prnt', 'hdr', title="This is tables[0]", footer=dbug('here'))


def get_html_tst():
    """
    purpose: to test get_html()
    options:
        start-maximized: Opens Chrome in maximize mode
        incognito: Opens Chrome in incognito mode
        headless: Opens Chrome in headless mode
        disable-extensions: Disables existing extensions on Chrome browser
        disable-popup-blocking: Disables pop-ups displayed on Chrome browser
        make-default-browser: Makes Chrome default browser
        version: Prints chrome browser version
        disable-infobars: Prevents Chrome from displaying the notification ‘Chrome is being controlled by automated software
    """
    import requests
    urls = ["http://www.python.org",
            "http://google.com",
            "http://olympus.realpython.org/profiles/poseidon",
            "https://finance.yahoo.com/quote/%5EDJI/",
            "https://ycharts.com/indicators/us_total_market_capitalization",
            ]
    # """--== SEP_LINE ==--"""
    for url in urls:
        # dbug(f"Working on url: {url}")
        r = requests.get(url)
        content = r.text
        status_code = r.status_code
        if status_code == 200:
            dbug(f"url: {url} status_code: {status_code}", 'boxed', 'centered', cntr_txt=99, box_clr="white on black")
            if askYN("Do you want to see the contents? ", 'y', 'centered'):
                printit(content)
            """--== SEP_LINE ==--"""
            # import pandas as pd
            # tables = pd.read_html(content)
            # dbug(tables)
        else:
            dbug(f"url: {url} status_code: {status_code}", 'boxed', 'centered', cntr_txt=99)
            dbug('ask')
        dbug()
        try:
            from selenium import webdriver
            from selenium.webdriver.common.keys import Keys
            browser = webdriver.Firefox(executable_path="./bin/geckodriver")
            browser.get(url)
            print('Title: %s' % browser.title)
            browser.quit()
        except Exception as Error:
            dbug(Error)
        askYN()
    do_close()


# #################################
def display_in_cols(lst, cols=0, reverse="", on="value"):
    # #############################
    """
    deprecated as gtable may take it's place
    input: takes a list or a dict and prints in order across cols
    options:
        order default for list is is as-is
        if it is a dict
            you can sort "on" default "value" or on "key"
            , or reverse=True or reverse=False
    returns: lines (sorted if dict)
    example:
    # >>> lst = [*range(1,20)]
    # >>> display_in_cols(lst)
    then print lines eg printit(lines)
    """
    import math
    # dbug(lst)
    # dbug(type(lst))
    if isinstance(lst, dict):
        from collections import OrderedDict
        my_lst = []
        # so this is a dict, lets change it to a list and continue on, but sort it first
        if on == "value":
            on = 1
        else:
            # sort based on key
            on = 0
        if reverse:
            my_sd = {k: v for k, v in sorted(lst.items(), key=lambda item: item[on], reverse=True)}
            # dbug(my_sd)
        if not reverse:
            # dbug(f"Sorting dict: {lst}")
            # my_sd = {k: v for k, v in sorted(lst.items(), key=lambda item: item[on], reverse=False)}
            my_sd = OrderedDict(sorted(lst.items(), key=lambda t: t[0]))
            # dbug(my_sd)
        if reverse == "":
            my_sd = lst
        # lst = []
        # dbug(my_sd)
        max_k = len(max(lst.keys(), key=len))
        vals = list(lst.values())
        vals = [str(elem) for elem in vals]
        max_v = len(max(vals, key=len))
        # dbug(f"max_k: {max_k} max_v: {max_v}")
        for k, v in my_sd.items():
            # dbug(f"k: {k} v: {v}")
            msg = f"[{k:<{max_k}}]: {v:>{max_v}} "
            my_lst.append(msg)
        lst = my_lst
        # dbug(my_lst)
    tot_num = len(lst)
    screen_cols = get_columns()
    # dbug(lst)
    if cols == 0 or cols == "":
        # dbug(max_len)
        max_elem_len = len(max(lst, key=len))
        # dbug(max_elem_len)
        if screen_cols > max_elem_len:
            # cols = math.floor(screen_cols / max_elem_len)
            cols = math.ceil(screen_cols / max_elem_len)
        else:
            cols = max_elem_len
        # dbug(f"screen_cols: {screen_cols} cols: {cols} max_elem_len: {max_elem_len}")
        # cols -= 1
    # cols = int(cols)
    # dbug(cols,ask=True)
    col = 0
    rows_num = math.ceil(tot_num / cols)
    # dbug(tot_num)
    # dbug(rows_num,ask=True)
    # matrix_tot = cols * rows_num
    max_elem_len = len(max(lst, key=len))
    rows = []
    for num in range(0, tot_num):
        # dbug(f"Processing num: {num}")
        row = []
        this = 0
        col = 0
        # for col in range(cols):
        while col < cols:
            # dbug(f"Processing col: {col} tot cols: {cols} current col:{col}")
            this = num + (rows_num * col)
            col += 1
            if this >= tot_num:
                this_e = " " * max_elem_len
            else:
                elem = lst[this]
                if len(elem) > max_elem_len:
                    elem = elem[max_elem_len:]
                if len(elem) < max_elem_len:
                    elem = elem + " " * (max_elem_len - len(elem))
                this_e = elem
            row.append(this_e)
        # dbug(row,ask=True)
        rows.append(row)
        col += 1
        if len(rows) >= rows_num:
            break
    # dbug(rows)
    # print("-"*screen_cols)
    lines = []
    for r in rows:
        lines.append("".join(r))
    return lines
    # ### EOB def display_in_cols(lst, cols=0, reverse="", on="value"): ### #


# #######################
def shadowed(lines=[], style=4, color="grey"):
    # ###################
    """
    purpose: adds shadowing typically to a box
    requires:
    input: lines as a list
    output: lines as a list
    Use this to see all the styles:
        msg = "this is \nmy message"
        for n in range(0,5):
            printit(centered(shadowed(boxed(msg + f"\nstyle: {n}"),style=n)))
    """
    RESET = sub_color('reset')
    if isinstance(lines, str):
        lines = lines.split('\n')
    styles = []
    # the terminal you use significantly influences this!
    # top_right, vertical, bottom_left, horizontal, bottom_right
    #            .... tr[0] ,      v[1],    bl[2] ,     h[3] ,      br[4]]
    styles.append([chr(9699), chr(9608), chr(9701), chr(9608), chr(9608)])
    styles.append([chr(9617), chr(9617), chr(9617), chr(9617), chr(9617)])
    styles.append([chr(9618), chr(9618), chr(9618), chr(9618), chr(9618)])
    styles.append([chr(9619), chr(9619), chr(9619), chr(9619), chr(9619)])
    styles.append([chr(9612), chr(9612), chr(9600), chr(9600), chr(9624)])
    styles.append([chr(9608), chr(9608), chr(9600), chr(9600), chr(9600)])
    styles.append([chr(9608), chr(9608), chr(9600), chr(9600), chr(9624)])
    #
    shadow_chrs = []
    shadow_chrs = styles[style]
    new_lines = []
    cnt = 0
    color = sub_color(color)
    for line in lines:
        if cnt == 0:
            width = len(escape_ansi(line))
            line = line + " "  # add a space to help when centering
        if cnt == 1:
            # shadow_chrs[0] = chr(9612)
            line = line + color + shadow_chrs[0] + RESET
        if cnt > 1:
            # shadow_chrs[1] = chr(9612)
            line = line + color + shadow_chrs[1] + RESET
        new_lines.append(line)
        cnt += 1
    # now add bottom shadow line
    new_lines.append(" " + color + shadow_chrs[2] + shadow_chrs[3] * (width - 2) + shadow_chrs[4] + RESET)
    return new_lines
    # ### EOB def shadowed(lines=[], style=4, color="grey"): ### #


# ###################################################################
def add_or_replace(filename, action, pattern, new_line, *args, backup=True, **kwargs):
    # ###############################################################
    """
    purpose: Adds or replaces a line in a file where pattern occurs
    required: filename, action: str [before|after|replace|either] ,pattern, new_line
    action: before|after|replace|either (either will replace if it is found or add if it is not)
    options:
    -   backup: bool=True,
    -   ask: bool=False,
    -   prnt: bool=False
    -   centered: bool=False,
    -   shadowed: bool=False
    pattern: needs to be unique regex?
    returns: "done" or None depending on use
    """
    # dbug(funcname())
    # dbug(filename)
    # dbug(pattern)
    # dbug(new_line)
    # """--== Config ==--"""
    ask = bool_val('ask', args, kwargs, dflt=False)
    shadow_b = bool_val('shadowed', args, kwargs, dflt=False)
    center_b = bool_val('centered', args, kwargs, dflt=False)
    prnt = bool_val(['prnt', 'print', 'show', 'verify', 'verbose'], args, kwargs, dflt=False)
    backup = bool_val(["bak", "backup", "bakup"], args, kwargs, dflt=backup)
    prnt = bool_val(["show", "prnt", "print", "verbose"], args, kwargs, )
    # """--== Init ==--"""
    linenum = 0
    cnt = 0
    pattern_found = False
    # """--== Process ==--"""
    import shutil
    if backup:
        try:
            shutil.copy(filename, f"{filename}.bak")
            if prnt:
                dbug(f"Copied [{filename}] to {filename}.bak", 'centered')
        except Exception as e:
            if prnt:
                dbug(f"Something went wrong? Error: {e}")
            return
    # """--== Replace ==--"""
    # dbug(f"action: {action} pattern_found: {pattern_found} pattern: {pattern} ")
    if action == 'replace' or action == 'either':
        reading_file = open(filename, "r")
        # dbug(reading_file)
        new_file_content = ""
        for line in reading_file:
            cnt += 1
            # stripped_line = line.rstrip()
            # dbug(f"Chkg pattern: [{pattern}] if in line: {line}")
            regex = re.search(pattern, line)
            # if pattern in line:
            if regex:
                linenum = cnt
                o_line = line
                if o_line.endswith("\n"):
                    n_line = new_line + "\n"
                else:
                    n_line = new_line
                pattern_found = True
                # dbug(f"Replacing line: {line} with {new_line} in new_file_content...")
                # dbug(f"Found pattern: {pattern} in line: {line}", 'ask')
            else:
                n_line = line
            new_file_content += n_line
        reading_file.close()
        # dbug(new_file_content)
        if not pattern_found and action == 'replace':
            dbug(f"Pattern: {pattern} was not found, action: [{action}]... file not changed")
            return False
        if pattern_found:
            lines = [f"Replace: {o_line}", f"New    : {new_line}"]
            if prnt:
                printit(lines, 'boxed', title=f"Action: {action}. Proposed replace/new content filename: {filename}", centered=center_b, shadowed=shadow_b, footer=dbug('here'))
        if ask:
            if askYN(f"Shall we change [{action}] to the new content? ", "y", centered=center_b):
                writing_file = open(filename, "w")
                writing_file.write(new_file_content)
                writing_file.close()
                # dbug(center_b)
                printit(f"Linenum: {linenum} line: {line} was replaced in {filename}", centered=center_b)
                # WIP TODO need to inform user here
                # dbug()
                return "done"
            else:
                return None
        # """--== SEP_LINE ==--"""
        if linenum == 0:
            linenum = len(new_file_content)
        if pattern_found:
            writing_file = open(filename, "w")
            writing_file.write(new_file_content)
            writing_file.close()
            # dbug(center_b)
            if prnt:
                printit(f"Linenum: {linenum} line: {o_line} was replaced in {filename} in file: {filename}", 'boxed', centered=center_b, footer=dbug('here'), center_txt=99)
            return "done"
    # """--== Add ==--"""
    if not pattern_found and action in ('both', 'either', 'addreplace', 'replaceadd', 'replaceoradd'):
        # dbug(f"action: {action} pattern_found: {pattern_found} pattern: {pattern} ")
        n_line = new_line.rstrip("\n")
        # dbug(f"Pattern: [{pattern}] not found. Adding n_line: {n_line}")
        new_file_content = cat_file(filename, rtrn='str')
        lines = [f"Add: {n_line}"]
        if prnt:
            printit(boxed(lines, title=f"Action: {action}. Proposed add/new content "), centered=center_b, shadowed=shadow_b, footer=dbug('here'))
        # dbug(filename)
        # dbug(new_file_content)
        # dbug(type(new_file_content))
        if isinstance(new_file_content, list):
            dbug(len(new_file_content))
            if len(new_file_content) == 1:
                new_file_content = "\n".join(new_file_content)[0]
        if new_file_content.endswith("\n"):
            new_file_content += n_line + "\n"
        else:
            new_file_content += "\n" + n_line
        linenum = " [linenum: end of file ] "
        if ask:
            if askYN(centered(f"Shall we change [action: {action}] to the new content filename: {filename}? ", "y")):
                writing_file = open(filename, "w")
                writing_file.write(new_file_content)
                writing_file.close()
                printit(f"Line: {linenum} was added in {filename}")
                return "done"
            else:
                dbug("Returning... nothing done...")
                return None
        else:
            # just do it then
            writing_file = open(filename, "w")
            writing_file.write(new_file_content)
            writing_file.close()
            if prnt:
                printit(f"Line: {line} {linenum} was added to {filename}", 'centered')
            return "done"
    # dbug(f"action: {action} pattern_found: {pattern_found} pattern: {pattern} ")
    # assuming this is action == 'add'
    f = open(filename, 'r')
    contents = f.readlines()
    f.close()
    # dbug(filename)
    for line in contents:
        # dbug(line)
        cnt += 1
        # dbug(pattern)
        if pattern.startswith("^"):
            # dbug(pattern)
            pattern = pattern[1:]
            # dbug(pattern)
            if line.startswith(pattern):
                pattern_found = True
                break
        else:
            if pattern in line:
                # old_line = line
                pattern_found = True
                break
    # dbug(type(contents))
    # dbug(f"patter: {pattern} action: {action} cnt: {cnt}")
    # dbug(pattern_found)
    # """--== Before ==--"""
    if action == 'before':
        # dbug(f"Adding new_line before cnt: {cnt}")
        contents.insert(cnt - 1, new_line + "\n")
        # new_content = new_line + '\n' + old_line
    """--== After ==--"""
    if action == 'after':
        # dbug(f"Adding new_line after cnt: {cnt}")
        contents.insert(cnt, new_line + "\n")
        # new_content = old_line + '\n' + new_line
    # """--== Add to end of file ==--"""
    if action == "" or action == "add" or action == "end" or action == "either":
        # dbug(f"Adding new_line at end of file: {cnt}")
        if isinstance(contents, list):
            if contents[-1].endswith("\n"):
                contents.append(new_line)
            else:
                contents.append("\n" + new_line)
    contents = "".join(contents)
    # printit(boxed(new_content, title=" Proposed new/replacement content "), 'center', 'shadow')
    if ask:
        if askYN(printit(f"Pattern: [{pattern}] found: [{pattern_found}] in {filename}. Shall we change [action: {action}] to the new content?: ", "y", 'str', 'centered', prnt=False)):
            f = open(filename, "w")
            f.write(contents)
            f.close()
            # dbug(f"Done ... action: {action}", 'ask')
            # dbug(contents)
            return "done"
    else:
        # just do it then
        f = open(filename, "w")
        f.write(contents)
        f.close()
        # dbug(f"Done ... action: {action}", 'ask')
        # dbug(contents)
        return "done"
    return None
    # ### def add_or_replace(filename, action, pattern, new_line, backup=True): ### #


# ###############################################
def regex_col(file_lines, pat="", col=7, sep=""):
    # ###########################################
    """
    purpose: regex for a pattern in a word|column
        file_lines can be a filename or lines (list)
    returns: lines where pat matches col number word ie words[col]
    notes:    col starts at 0 to be consistent with coding standards
    """
    if isinstance(file_lines, list):
        lines = file_lines
    else:
        # assume it is a filename
        with open(file_lines) as f:
            lines = f.readlines()
    ret_lines = []
    # ### for testing ### #
    # import datetime
    # from dateutil import relativedelta
    # yr = datetime.datetime.now().strftime("%y")
    # nextmonth = datetime.datetime.now() + relativedelta.relativedelta(months=1)
    # mon = nextmonth.strftime("%b").lower()
    # pat = yr + mon
    # dbug(pat)
    # lines = [f"one line here with many words {pat} in it", f"another;line;there;with;many;words;{pat};in;it"]
    # sep = ";"
    # ### #
    for line in lines:
        # dbug(f"chkg line: {line}")
        if sep != "":
            words = line.split(sep)
            dbug(words)
        else:
            words = line.split()
        if len(words) > col:
            if re.search(pat, words[col]):
                ret_lines.append(line)
    # printit(ret_lines)
    return ret_lines
    # ### EOB def regx_col(pat="",col=7,sep=""): ### #


# #####################
def rootname(filename, *args, **kwargs):
    # #################
    """
    purpose: returns the root name of a full filename (not path, no extension)
    input: filename: str
    options:
        - base: bool         # returns simple basename only
        - full_base:_bool    # returns absolute path w/basename only
        - dir: bool          # return just the absolute path w/o the basename.ext
    returns: ROOT_NAME: str
    """
    dir = bool_val(['dir'], args, kwargs, dflt=False)
    base = bool_val(['base', 'basename'], args, kwargs, dflt=False)
    full_base = bool_val(['fbase', 'fbasename', 'full_base', 'full_basename'], args, kwargs, dflt=False)
    REALNAME = os.path.realpath(filename)
    # dbug(REALNAME)
    DIRNAME = os.path.dirname(REALNAME)
    FULL_BASENAME = os.path.splitext(REALNAME)[0]
    BASENAME = os.path.basename(REALNAME)
    ROOTNAME = os.path.splitext(BASENAME)[0]
    if dir:
        return DIRNAME
    if base:
        return BASENAME
    if full_base:
        return FULL_BASENAME
    else:
        return ROOTNAME


# def mod_info():
#    pat = r"def .*[\(?].*[\)?]:"
#    # r = re.search(pat, )
#    dir(__file__)
#    dbug("------------")
#    help(__file__)


# #################
def islol(my_lol, *args, **kwargs):
    # #############
    """
    purpose: determine is my_lol is actually a list of lists
    required: list - my_lol
    options: none
    return: bool True | False
    note:
        - if you want to know if your matrix is a list of list of a list of list (eg: rows, columns, of boxes)
          use: islolol = all([islol(elem) for elem in mtrx])   # True or False... is this a list of lists within an lol
    """
    # """--== Config ==--"""
    # show = bool_val(["show"], args, kwargs, dflt=False)
    # any_b = bool_val(["any"], args, kwargs, dflt=False)
    all_b = bool_val(["all"], args, kwargs, dflt=True)
    # scope = kvarg_val(["scope"], kwargs, dflt="all")
    # dbug(all_b)
    # """--== SEP_LINE ==--"""
    # lvls_b = bool_val(['levels', 'lvls'], args, kwargs)
    # lvls = 0
    #  count = sum( [ len(listElem) for listElem in my_lol)
    if not isinstance(my_lol, list):
        # dbug(f"Woops... this should be a list my_l: [{my_lol}] type(my_lol): {type(my_lol)}")
        return False
    # dbug(my_lol)
    # dbug(type(my_lol))
    if all_b:
        my_islol = all(isinstance(elem, list) for elem in my_lol)  # True or False... is this a list of lists
    else:
        my_islol = any(isinstance(elem, list) for elem in my_lol)  # True or False... is this a list of lists
    return my_islol


def islod(my_lod, *args, **kwargs):
    """
    purpose: is this a list of dictionaries 
    options: None
    returns: bool
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # """--== Process ==--"""
    for elem in my_lod:
        if not isinstance(elem, dict):
            return False
    return True
    # if all(isinstance[elem, dict] for elem in my_lod):
    #    return True
    # else:
    #    return False


def islos(my_los=["a", "list", "of", "strings"], *args, **kwargs):
    """
    purpose: determines if my_los is a list of strings
    returns: bool
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(my_los)
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    show = bool_val(["show"], args, kwargs, dflt=False)
    # any_b = bool_val(["any"], args, kwargs, dflt=False)
    all_b = bool_val(["all"], args, kwargs, dflt=True)
    # scope = kvarg_val(["scope"], kwargs, dflt="all")
    # """--== validate ==--"""
    if my_los is None:
        # dbug("my_los: {my_los} is None ")
        return False
    if not isinstance(my_los, list):
        # dbug("my_los: {my_los} is not a list ")
        return False
    # """--== Init ==--"""
    scope = "all"
    # dbug(type(my_los))
    # """--== validate ==--"""
    if not all_b:
        any_b = True
    if not isinstance(my_los, list) and len(str(my_los)) > 1:
        # yes, it must first be a list - otherwise a simple single string would pass
        # dbug(my_los)
        return False
    rtrn = False
    # """--== SEP_LINE ==--"""
    if show:
        dbug(my_los)
    if all_b or scope in ("all"):
        # dbug(my_los)
        if all([isinstance(x, str) for x in my_los]):
            # dbug("Yes this is a los")
            rtrn = True
    if show:
        dbug(f"Returning rtrn: {rtrn} any_b: {any_b} all_b: {all_b} scope: {scope} ")
    # dbug(f"Returning rtrn: {rtrn}")
    return rtrn


def islols_demo(*args, **kwargs):
    """
    purpose: to demonstatrate islol and islos functions
    required: none
    optons: none
    return: none
    """
    box = boxed("This is a boxed string")
    my_lol = [["one", "two"], "three", box, [box]]
    # my_lol = [["one", "two"]]
    printit(f"Given this list\n my_lol:\n {my_lol}", 'boxed', footer=dbug('here'))
    modes = [True, False]
    for mode in modes:
        lines = []
        lines.append("-"*20 + f" Using all={mode} " + "-"*20)
        if islol(my_lol, all=mode):
            lines.append("The list above IS a list of lists")
        else:
            lines.append("The list above is NOT a list of lists")
        printit(lines, 'boxed', footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    lines = []
    lines.append("Now checking each element to see if it is a list of strings - ie like a block of box...")
    for elem in my_lol:
        if islos(elem):
            lines.extend(boxed(elem, title="This elem is a list of strings", footer=dbug('here'), prnt=False))
    printit(lines, 'boxed', footer=dbug('here'))
    dbug("Done")


# ##############
def maxof(my_l, *args, **kwargs):
    # ##########
    """
    purpose: returns length of longest member of a list (after escape_ansii codes are removed)
    required: list or list_of_lists (lol)
    options:
        - length|len|max_len|elem_len: bool       # default=True longest length is returned
        - height|rows|max_height|row_len: bool    # default=False largest number of elements in list
                                                    (typically the number of lines in a list of strings)
        - elems: bool                             # default=False in a list of lists this will rerturn
                                                    the greatest number of elements in each member of a list (see note below)
        - lst: bool                               # default=False returns a list which will be the max length(s) or height(s) of each elem in a list
    returns: int max length of eleemes
    note: saves me from having to look up how to do this all the time and works with lists or lists of list
        - sometimes I need to know the number of rows in cols (lol of rows in cols
                ie: cols_lol = [row1, row2], [row1, row2, row3], [row1, row2]] ... maxof(cols_lol): 3
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(my_l)
    # dbug(args)
    # dbug(kwargs)
    # """--== Validate ==--"""
    if isempty(my_l):
        # dbug(my_l)
        return 0
    # """--== Config ==--"""
    height_b = bool_val(["height", "max_height", "rows", "row_len"], args, kwargs, dflt=False)
    length_b = bool_val(["length", "max_len", "len", 'elem_len', 'elems', 'cols'], args, kwargs, dflt=False)
    elems_b = bool_val(["number", "num", "items", "elems", "max_num_elems", 'max_elems'], args, kwargs, dflt=False)
    lst_b = bool_val(['lst', 'list'], args, kwargs, dflt=False)
    # """--== Init ==--"""
    max_height = 0
    max_len = 0
    max_elems = 0
    max_lens = []
    max_heights = []
    elems = []
    # """--== Process ==--"""
    # max_len = len(max(escape_ansi(my_l), key=len))
    # or
    # dbug("testing lol")
    if islol(my_l):
        # dbug(f"this is an lol height_b: {height_b} length_b: {length_b} elems_b: {elems_b} lst_b: {lst_b}")
        if elems_b:
            # dbug(elems_b)
            height_b = True
            length_b = False
            elems_b = True
        if not height_b and not length_b:
            if not elems_b:
                length_b = True
        # dbug(f"this is an lol height_b: {height_b} length_b: {length_b} elems_b: {elems_b} lst_b: {lst_b}")
        # """--== is lol ==--"""
        # eg height is number of rows, length is number of cols
        # dbug("This is an lol")
        # max_num_elems = 0
        for elem in my_l:
            if isinstance(elem, list):
                max_len = max(nclen(x) for x in elem)
                # dbug(elem)
            elems.append(len(elem))
            if islos(elem):
                # dbug(elem)
                max_len = max(nclen(x) for x in elem)
                max_lens.append(max_len)
                max_heights.append(len(elem))
            else:
                # dbug(elem)
                max_lens.append(len(elem))
            if height_b:
                if len(elem) > max_height:
                    max_height = len(elem)
        # dbug(f"this is an lol height_b: {height_b} length_b: {length_b} elems_b: {elems_b} lst_b: {lst_b} max_elems: {max_elems} max_len: max_elems")
        # dbug(f"my_l is an lol max_len: {max_len}")
    else:
        # """--== not lol ==--"""
        length_b = True
        if isinstance(my_l, list):
            max_len = max(nclen(elem) for elem in my_l)
            # dbug(max_len)
        if isinstance(my_l, str):
            max_len = nclen(my_l)
        # dbug(max_len)
        # dbug(f"type(my_l): {type(my_l)} must NOT be lol ...max_len: {max_len}")
    if elems_b:
        # dbug(f"max_lens: {max_lens} max_elems: {max_elems}" )
        # dbug(f"for ref max_height: {max_height} max_len: {max_len}i max_heights: {max_heights}")
        rtrn = max_elems
    if height_b:
        # dbug(max_height)
        rtrn = max_height
    if length_b:
        rtrn = max_len
    if lst_b:
        if length_b:
            rtrn = max_lens
        if height_b:
            rtrn = max_heights
        if elems_b:
            rtrn = elems
    # dbug(f"Returning max_len: {max_len}")
    return rtrn


def maxof_demo():
    """
    purpose: Demos of using ruleit() function
    returns: None
    """
    box1 = boxed("one")
    box2 = boxed(["two 2", "2"])
    boxes = [box1, box2]
    for box in boxes:
        printit(box)
    max_len_boxes = maxof(boxes)
    printit(f"maxof(boxes): {max_len_boxes}")
    # """--== SEP_LINE ==--"""
    lines = []
    my_l = ["one", "two", f"this is {gclr('red')}three", "four"]
    lines.append(f"maxof my_l: {my_l} is: {maxof(my_l)}")
    my_lol = [["this is col 1", "this is col two", "this is col3"], [1, 2], [1, 2, 3]]
    lines.append(f"maxof my_lol: {my_lol} is: {maxof(my_lol)}")
    printit(lines, 'boxed', title="Simple example", footer=dbug('here'))
    max_len = maxof(my_lol, 'len')
    max_height = maxof(my_lol, 'height')
    max_lens = maxof(my_lol, 'len', 'lst')
    max_heights = maxof(my_lol, 'height', 'lst')
    lines = []
    lines.append(f"max_len of my_lol:     {max_len:<50}   uses 'len' arg/option")
    lines.append(f"max_height of my_lol:  {max_height:<50}   uses 'height' arg/option")
    lines.append(f"max_heights of my_lol: {str(max_heights):<50}   uses 'height' and 'lst' args/options")
    lines.append(f"max_lens of my_lol:    {str(max_lens):<50}   uses 'len' and 'lst' args/options")
    printit(lines, 'boxed', title="maxof demo", footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    boxes = []
    for i in range(1, 5):
        box = boxed(f"my box {i}\n"*i, title=f"box{i}")
        boxes.append(box)
    box5 = boxed("This is box 5")
    boxes.append(box5)
    for box in boxes:
        printit(box, 'lst')
    max_len = maxof(boxes, 'len')
    printit(ruleit(width=max_len, prnt=False), title='ruler for reference')
    max_height = maxof(boxes, 'height')
    max_lens = maxof(boxes, 'len', 'lst')
    max_heights = maxof(boxes, 'height', 'lst')
    lines = []
    lines.append(f"max_len of boxes:     {max_len:<50}   uses 'len' arg/option")
    lines.append(f"max_height of boxes:  {max_height:<50}   uses 'height' arg/option")
    lines.append(f"max_heights of boxes: {str(max_heights):<50}   uses 'height' and 'lst' args/options")
    lines.append(f"max_lens of boxes:    {str(max_lens):<50}   uses 'len' and 'lst' args/options")
    printit(lines, 'boxed', title="maxof demo", footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    my_lol = [['elem1', 'elem2', 'elem3', 'elem4', 'elem5'],['E-Mini S&P 500 Mar 23', 4084.0, 8.5, '+0.21%'], ['Mini Dow Jones Indus.-$5 Mar 23', 34049.0, 26.0, '+0.08%'], ['Nasdaq 100 Mar 23', 12221.0, 114.25, '+0.94%']]
    printit(f"my_lol: {my_lol}", 'boxed')
    max_my_lol_len = maxof(my_lol)
    max_len = maxof(my_lol, 'len')
    max_height = maxof(my_lol, 'height')
    max_lens = maxof(my_lol, 'len', 'lst')
    max_heights = maxof(my_lol, 'height', 'lst')
    max_num_elems = maxof(my_lol, 'elems')
    lines = []
    lines.append(f"max_my_lol_len of my_lol:     {max_my_lol_len:<45} uses no arg/option")
    lines.append(f"max_len of my_lol:     {max_len:<50}   uses 'len' arg/option")
    lines.append(f"max_height of my_lol:  {max_height:<50}   uses 'height' arg/option")
    lines.append(f"max_heights of my_lol: {str(max_heights):<50}   uses 'height' and 'lst' args/options")
    lines.append(f"max_lens of my_lol:    {str(max_lens):<50}   uses 'len' and 'lst' args/options")
    lines.append(f"max_num_elems of my_lol:    {str(max_num_elems):<45}   uses 'elems' arg/option")
    printit(lines, 'boxed', title="maxof demo", footer=dbug('here'))
    printit(f"Done with {funcname()}")
    do_close()


# #################################
def gblock(msgs_l, *args, **kwargs):
    # #############################
    """
    purpose: justifies using nclen all strngs in msgs_l and maximizes each string length to the longest string - all lines will be the same length (nclen - no-color len)
    required: msgs_l: list   # list of strings
    options:
        - height: int
        - length | width: int
        - pad: str  # char to use for fill
        - position=1: str | list | int  # eg: 'right center' or 'left top' (default) or [top, left] or 'middle bottom' or 1 (default) or 5 or 9 ... etc
                      left              | center             | right
                    +-------------------+--------------------+--------------------+
            top     |  1                |   2                | 3                  |
                    | ['top','left']    |['top','center']    | ['top','right']    |
            ------  +-------------------|--------------------|--------------------+
            middle  |  4                |   5                | 6                  |
                    | ['middle','left'] | [middle','center'] | ['middle','right'] |
            ------  +-------------------|--------------------|--------------------+
            bottom  |  7                |   8                | 9                  |
                    | ['bottom','left'] | [bottom','center'] | ['bottom','right'] |
            ------  +-------------------|--------------------|--------------------+
    returns: all lines the same length (the length of the max) and with strings justified - a new box with the dimensions given
    aka: build_box, maxall
    notes:
        - this function is designed place a block/box in a position in a larger box or to combine rows and columns into a type of dashboard.
        - described above is the original design ie: to handle on box (list of strings) - this enhancement if fragile and not fully tested but is great for building dashvboards
        However: I have modified/enhanced this to allow for building columns and or rows *but* it is difficult to describe how it works
        Best to give examples - assumes box(x) below is a list of strongs of the same length
        gblock([box1, box2])                  # will build two columns into one block
        gblock([box1, [box2, box3]])          # will build one row of two columns with the second column having 2 rows (box2 over box3)
        gblock([[box1], [box2]])              # will build two rows - box1 over box2
        gblock([[box1, box2], [box3, box4]])  # will build two columns with the first column holding box1 over box2 while the second column will hold box 3 over box4
        option include:
            - length: int                     # works just like above - makes the block this length
            - height: int                     # "     "      "        - makes the block this height
            - boxed: bool
            - title: str
            - footer: str
            - txt_center: int                 # this is important as it will center from the top txt_center number of lines within the created block
                                              # typically you would use txt_center=99 to center all the lines within the block
    """
    # TODO: add col_limit to truncate elems if needed
    """--== debugging ==--"""
    # dbug(funcname())
    # dbug(msgs_l[:2])
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    width = kvarg_val(["width", "length", "w"], kwargs, dflt=0)
    height = kvarg_val(["height", "h"], kwargs, dflt=0)
    position = kvarg_val(["just", "justify", "position", "pos"], kwargs, dflt=1)  # can be str | list
    positions = kvarg_val(["positions"], kwargs, dflt=[1, 2, 3])  # list ... applies when msgs_l is actually an list of lists of boxes
    pad = kvarg_val(["pad", "fill"], kwargs, dflt=" ")
    prnt = bool_val(["prnt", "print", "show"], args, kwargs, dflt=False)
    boxed_b = bool_val(['boxed', 'box'], args, kwargs, dflt=False)
    centered_b = bool_val(['centered', 'center'], args, kwargs, dflt=False)
    txt_center = kvarg_val(["text_center", "text_centered", "lines_centered", "txt_center", 'txt_centered'], kwargs, dflt=0)
    title = kvarg_val(['title'], kwargs, dflt="")
    footer = kvarg_val(['footer'], kwargs, dflt="")
    box_color = kvarg_val(["box_color", 'box_clr'], kwargs, dflt="white! on black")
    color = kvarg_val(["color", 'clr'], kwargs, dflt="")
    centered = bool_val(["centered", 'ccentered'], args, kwargs, dflt=False)
    # possiblilities: left, center, right, top, middle, bottom
    # """--== Validations ==--"""
    # dbug(msgs_l)
    if msgs_l is None:
        dbug(f"Returning... nothing to work with.... msgs_l: {msgs_l}")
        return
    for elem in msgs_l:
        if elem is None:
            dbug(f"This list contains some elements that are None... elem: {elem}   Returning...")
            return
    my_group = []
    group = msgs_l
    if any([islos(x) for x in group]) and islol(group):
        # dbug("This must be a group of cols as some elems are a list of strings (los)")
        for x in group:
            if islol(x):
                # found a column with more than one box so lets treat it that way
                x = gblock(sum(x, []))  # , txt_center=txt_center)
                my_group.append(x)
            else:
                my_group.append(x)
        msgs_l = my_group
    # """--== Init ==--"""
    pad = str(pad)
    justify = ""
    vjust = 'top'
    pad = gclr(color) + pad
    if all([islol(elem) for elem in msgs_l]):
        # dbug("This must contain rows")
        new_msgs_l = []
        for elem in msgs_l:
            # dbug(f"This must be a row ... elem: {elem} ")
            if all([islos(item) for item in elem]):
                # dbug("This must be a list containing a list of strings (los)")
                # convert this to rows by adding them on top of each other
                if len(elem) == 1:
                    for item in elem:
                        new_msgs_l += item
                else:
                    new_msgs_l += gcolumnize(elem)
            else:
                # dbug(islos(elem))
                dbug(f"Problem elem: {elem}", 'ask')
        msgs_l = new_msgs_l
    # """--== Convert ==--"""
    if isinstance(msgs_l, str) and "\n" in msgs_l:
        msgs_l = msgs_l.split("\n")
    # """--== SEP_LINE ==--"""
    # if not islol(msgs_l):
    #     # dbug("simple list?")
    #     max_width = maxof(msgs_l)
    #     if width < max_width:
    #         width = max_width
    #     new_list = []
    #     for elem in msgs_l:
    #         elem = str(elem)
    #         # dbug(type(elem), 'ask')
    #         diff = width - nclen(elem)
    #         fill = pad * diff
    #         if str(position) in ("left", "1", "4", "7"):
    #             new_elem = elem + fill
    #         if str(position) in ("center", "2", "5", "8"):
    #             fill = fill * (diff // 2)
    #             new_elem = fill + elem + fill
    #         if str(position) in ("right", "3", "6", "9"):
    #             new_elem = elem + fill
    #         new_list.append(new_elem)
    #     # dbug(f"Returning new_list: {new_list}")
    #     msgs_l = new_list
    if islol(msgs_l):
        # dbug("Treating msgs_l as a lol ... not a simple list?", 'ask' )
        if any([islol(elem) for elem in msgs_l]):
            # dbug(f"Rows of Columns?")
            if any([islol(elem) for elem in msgs_l]):
                my_lines = []
                for msg in msgs_l:
                    if len(msg) > 1:
                        my_lines += gblock(gcolumnize(msg), length=width)  # , height=height)
                my_lines = printit(my_lines, boxed=boxed_b, centered=centered_b, title=title, footer=footer, box_color=box_color, color=color, prnt=prnt, txt_center=txt_center)
            return my_lines
        else:
            # side by side boxes - ie a row
            for box in msgs_l:
                row = gcolumnize(msgs_l, lenght=width)  # , height=height)
                lines = printit(row, boxed=boxed_b, centered=centered_b, title=title, footer=footer, box_color=box_color, color=color, prnt=prnt, txt_center=txt_center)
                return lines
        if len(positions) == 0:
            positions = [1, 2, 3]  # a number for each box, default is left top for all
        # make 3 columns
        col_left_len = 0    # find length of anything in 1,4,7  ie  left column
        col_center_len = 0
        col_right_len = 0
        col1_box = []
        col2_box = []
        col3_box = []
        boxes_lol = msgs_l
        length = width
        for box in boxes_lol:
            if maxof(box) > length:
                length = maxof(box)
            if len(box) > height:
                height = len(box)
        for box_num, box in enumerate(boxes_lol):
            # this middle col will fill any empty space in the (2, 5, 8) block below
            pos = positions[box_num]
            if int(pos) in (1, 4, 7):
                col1_box = gblock(box, length=col_left_len, height=height, position=pos)
            if int(pos) in (3, 6, 9):
                col3_box = gblock(box, length=col_center_len, height=height, position=pos)
            if int(pos) in (2, 5, 8):
                # prepare to fill any empty space
                my_length = length - (col_left_len + col_right_len)
                col2_box = gblock(box, length=my_length, height=height, position=pos)
        # dbug(txt_center)
        row_box = printit(gcolumnize([col1_box, col2_box, col3_box]),
                         width=length,
                         height=height,
                         boxed=boxed_b,
                         centered=centered_b,
                         title=title,
                         footer=footer,
                         box_color=box_color,
                         color=color,
                         prnt=prnt,
                         txt_center=txt_center)
        msgs_l = row_box
        max_len = maxof(msgs_l)
        screen_width = get_columns() - 4
        if max_len >= screen_width:
            dbug(f"It appears that the requested content length {max_len} exceeds theavailable terminal screen width {screen_width}")
            # dbug(msgs_l, 'lst')
            return None
        return row_box
    # """--== SEP_LINE ==--"""
    # dbug(f"Now place the box in the proper position msgs_l: {msgs_l}")
    if isinstance(msgs_l, str):
        msgs_l = [msgs_l]
    msg_len = maxof(msgs_l)
    msg_height = len(msgs_l)
    max_len = msg_len
    max_height = msg_height
    if width > msg_len:
        max_len = width
    if height > msg_height:
        max_height = height
    # deal with position being either str | list
    if str(position) == "1":
        position = ['top', 'left']
    if str(position) == "2":
        position = ['top', 'center']
    if str(position) == "3":
        position = ['top', 'right']
    if str(position) == "4":
        position = ['middle', 'left']
    if str(position) == "5":
        position = ['middle', 'center']
    if str(position) == "6":
        position = ['middle', 'right']
    if str(position) == "7":
        position = ['bottom', 'left']
    if str(position) == "8":
        position = ['bottom', 'center']
    if str(position) == "9":
        position = ['bottom', 'right']
    if 'left' in position:
        justify = 'left'
    if 'center' in position:
        justify = 'center'
    if 'right' in position:
        justify = 'right'
    # """--== build left, center, or right justified "box" ==--"""
    # """--== now build horizontal justification ==--"""
    new_msgs = []
    for msg in msgs_l:
        diff = max_len - nclen(msg)
        fill = pad * diff
        if justify == 'left':
            try:
                msg = str(msg) + fill
            except Exception as Error:
                dbug(Error)
        if justify == 'center':
            fill = pad * (diff // 2)
            msg = fill + msg + fill
            if nclen(msg) != max_len:
                diff = max_len - nclen(msg)
                msg += pad * diff
        if justify == 'right':
            fill = pad * diff
            msg = fill + msg
        new_msgs.append(msg)
        msgs_l = new_msgs
    # """--== deal with position being either str | list """
    if 'top' in position:
        vjust = 'top'
    if 'middle' in position:
        vjust = 'middle'
    if 'bottom' in position:
        vjust = 'bottom'
    # """--== now build vertical justification ==--"""
    diff = max_height - msg_height
    above_lines = 0
    below_lines = 0
    if vjust == 'top':
        below_lines = diff
    if vjust == 'bottom':
        above_lines = diff
    if vjust == 'middle':
        above_lines = diff // 2
        below_lines = diff - above_lines
    blank_line = pad * max_len
    top_lines = [blank_line] * above_lines
    bottom_lines = [blank_line] * below_lines
    new_lines2 = top_lines + msgs_l + bottom_lines
    # dbug(new_lines2)
    # """--== SEP_LINE ==--"""
    max_len = maxof(new_lines2, 'len')
    screen_width = get_columns() - 4
    # dbug(f"max_len: {max_len} screen_width: {screen_width}")
    if max_len >= screen_width:
        # dbug(f"It appears that the requested content length {max_len} exceeds the (approx) terminal screen available width {screen_width}", 'boxed', 'centered')
        new_lines2 = wrapit(new_lines2, length=screen_width)
        # ruleit()
        # dbug(f"real screen width = {get_columns()}")
        for ln in new_lines2:
            if nclen(ln) > screen_width:
                dbug(f"This line is too long: [{ln}]")
        # dbug(new_lines2, 'lst')
        # return None
        # dbug(new_lines2)
    # """--== SEP_LINE ==--"""
    rtrn_lines = printit(new_lines2, boxed=boxed_b, centered=centered, title=title, footer=footer, box_color=box_color, color=color, prnt=prnt, pad=pad, txt_center=txt_center)
    # dbug("Returning rtrn_lines")
    return rtrn_lines
    # ### EOB def gblock(msgs_l, *args, **kwargs): ### #


def gblock_demo():
    """
    purpose: demo of gblock()
    returns: None
    """
    unevn_lines = ["one", "line two", "this is the third line", "forth"]
    boxed_lines = boxed(unevn_lines)
    dbug(unevn_lines, 'lst')
    blcked_lines = gblock(unevn_lines)
    printit(blcked_lines, 'shadowed')
    add_margin = 10
    positions = [1,2,3,4,5,6,7,8,9]
    width = maxof(boxed_lines) + add_margin
    height = len(boxed_lines) + add_margin
    all_bxs = []
    for pos in positions:
        blcked_lines = gblock(boxed_lines, width=width, height=height, pad="x", position=pos, title=f"pos: {pos}")
        printit(blcked_lines, 'boxed', title=f"gblocked lines pos={pos}", footer=f"width: {width} height: {height} ")
        # ruleit()
        all_bxs.append(blcked_lines)
    cnt = 0
    row = []
    rcb_mtrx = []
    for bx in all_bxs:
        cnt  += 1
        row.append(bx)
        if cnt % 3 == 0:
            gcolumnize(row, cols=3, prnt=True)
            dbug('ask')
            rcb_mtrx.append(row)
            row = []
            cnt = 0
    gcolumnize(all_bxs, 'prnt')
    dbug('ask')
    row1 = boxed("row 1")
    dbug(row1, 'lst')
    row2 = boxed("row 2")
    dbug(row2, 'lst')
    dbug("Doing 2 rows in gblock([[row1], [row2]])")
    # rows = row1 + row2
    # dbug(row1 + row2, 'lst', 'boxed', 'titled', 'footerred', title="row1 + row2", footer=dbug('here'))
    # dbug(row1 + row2, 'lst')
    # printit("-"*10)
    footnote_box = boxed("gblock(row1 + row2 + footnote_box, ...")
    gblock(row1 + row2 + footnote_box, 'prnt', 'boxed', title="Rows added together", footer=dbug('here'))
    footnote_box = boxed("gblock([[row1], [row2], [footnote_box]], ...txt_center=99")
    gblock([[row1], [row2], [footnote_box]], 'prnt', 'boxed', title="Using a list of lists for rows", footer=dbug('here'), txt_center=99)
    dbug("Done", 'ask')
    # """--== SEP_LINE ==--"""
    col1 = boxed("col1")
    col2 = boxed("col2")
    footnote_box = boxed("gblock([[row1], [row2],[col1, col2], [footnote_box]], ...")
    gblock([[row1], [row2], [col1, col2], [footnote_box]], 'prnt', 'boxed', title="Using a list of lists for rows", footer=dbug('here'))
    dbug("Done", 'ask')
    # """--== SEP_LINE ==--"""
    weather_boxes = []
    locations = ["Nags_Head,NC", "Orlando,FL", "Herndon,VA", "North_Pole,AK"]
    with Spinner(f"Getting weather for locations: {locations}...", style='vbar', centered=True, progressive=True, elapsed=True, colors=shades('red')):
        for loc in locations:
            cmd = 'curl -s wttr.in/' + loc +"?:0"
            out = boxed(run_cmd(cmd, 'lst'))
            # dbug(out, 'lst')
            weather_boxes.append(out)
    # stacked_boxes = list(itertools.chain.from_iterable(weather_boxes))
    stacked_boxes = gcolumnize(weather_boxes, cols=1)
    col1 = gblock((stacked_boxes), 'boxed', title="Stacked Weather Boxes", footer=dbug('here'))
    printit(col1, 'centered')
    dbug('ask')
    # """--== SEP_LINE ==--"""
    simple_boxes = []
    for i in range(1,5):
        simple_boxes.append(boxed(f"my box {i}", title=f"box{i}"))
    # dbug(boxes)
    # """--== SEP_LINE ==--"""
    stacked_boxes = gcolumnize(simple_boxes, cols=1)
    col2 = gblock((stacked_boxes), 'boxed', title="Stacked Simple Boxes", footer=dbug('here'))
    printit(col2, 'centered')
    dbug("Done with stacked_boxes", 'ask')
    # """--== SEP_LINE ==--"""
    footnote_box = boxed("gblock([[col1, col2],[footnote_box]] 'prnt', 'boxed', footer=dbug('here')")
    gblock([[col1, col2], [footnote_box]], 'prnt', 'boxed', footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    row1 = gblock(simple_boxes)
    # dbug(row1, 'lst')
    row2 = gblock(weather_boxes)
    # dbug(row2, 'lst')
    lines = gblock([[row1], [row2]], 'prnt', 'boxed', title="Boxes", footer=dbug('here'), txt_center=99)
    dbug('ask')
    title_box = boxed("Title: Weather 4 locations")
    col1 = gblock([[simple_boxes[0]], [simple_boxes[1]]])
    dbug(col1, 'lst')
    col2 = gblock([[simple_boxes[2]], [simple_boxes[3]]])
    footnote_box = boxed('gblock([[title_box], [col1, col2], [footnote_box]], "prnt", "boxed", title="Cols", footer=dbug("here"), txt_center=99)')
    lines = gblock([[title_box], [col1, col2], [footnote_box]], 'prnt', 'boxed', title="Cols", footer=dbug('here'), txt_center=99)
    dbug('ask')
    col1 = gblock(col1, "boxed", title="col1")
    col2 = gblock(col2, "boxed", title="col2")
    lines = gblock([[title_box], [col1, col2], [footnote_box]], 'prnt', 'boxed', title="Cols", footer=dbug('here'), txt_center=99)
    dbug('ask')
    # maxof(lines)
    # dbug('ask')
    box = boxed("box")
    group1 = box
    # islos(box, 'show')
    # dbug('ask')
    # islos([box, box], 'show') # cols only                                         all          lvl1 elems are a los
    group2 = [simple_boxes[0], simple_boxes[1]]
    # islos([box, box, [box, box]], 'show') # columns (with some cols with rows)    at least one lvl1 elem   is a los
    group3 = [simple_boxes[0], simple_boxes[1], [simple_boxes[2], simple_boxes[3]]]
    group4 = [[simple_boxes[0]], [simple_boxes[1]], [simple_boxes[2], simple_boxes[3]]]
    groups = [group1, group2, group3, group4]
    dmsg = []
    dmsg.append("grp1 = single box  grp2: [box, box] grp3: [box, box, [box, box]] grp4: [[box], [box], [box, box]]")
    dmsg.append("grp1 = single col  grp2: Two cols   grp3: Three cols one w/rows  grp4: Three rows one w/2 cols")
    dbug(dmsg, 'lst', 'boxed')
    if islol(group4):
        dbug("group4 is a lol")
    for n, group in enumerate(groups, start=1):
        dbug(f"Now working on group {n} len(group): {len(group)}")
        my_group = []
        if any([islos(x) for x in group]) and islol(group):
            dbug("this must be a group of cols as some elems are los")
            for x in group:
                if islol(x):
                    x = gblock(sum(x, []))
                    my_group.append(x)
                else:
                    my_group.append(x)
            # dbug(my_group)
            gblock(my_group, 'prnt', footer=dbug('here'), boxed=True, length=100, height=25, title=f"group{n}")
        if not islol(group):
            dbug("Actually this is probably a single box because it is not a list of lists")
        if all([not islos(x) for x in group]):
            dbug("there are no los elems in the group so must be a group of rows (perhaps w/cols)")
        gblock(group, 'prnt', 'boxed', footer=dbug('here'), length=100, height=30, title=f"group{n} h: 30 l: 100")
        print("-"*60)
    # islos([[box, box], [box, box]], 'show') # rows of cols                        all          lvl1 elems are list[list[los]]
    # islos([[box, box], box, box], 'show') #  columns (with some cols with rows)
    dbug('ask')
    msg = "my simple box right here"
    if islos(msg):
        dbug("YES")
    else:
        if islos(boxed(msg)):
            dbug("Now it is")
    msg2 = f"my len:{len(msg)}"
    pad = "X"  # so you can visually see the padding
    lines = [msg, msg2, "", f"pad: {pad}"]
    positions = [['top', 'right'],
            ['top', 'center'],
            ['top', 'right'],
            ['middle', 'left'],
            ['middle', 'center'],
            ['middel', 'right'],
            ['bottom', 'left'],
            ['bottom', 'center'],
            ['bottom', 'right']]
    # or
    colors = ["green!", "red!", "blue! on black!", "white!"]
    box_color = "white! on black"
    my_box1 = boxed("my_box1")
    my_box2 = boxed("my_box2")
    my_box3 = boxed("my_box3")
    # gblock(my_box1 + my_box2, 'boxed', 'prnt', title="box1 + box2", footer=dbug('here'))
    gblock([my_box1, my_box2], 'boxed', 'prnt', title="[box1, box2]", footer=dbug('here'))
    dbug('ask')
    gblock([[my_box1], [my_box2, my_box3]], 'boxed', 'prnt', title="[[box1], [box2, box3]]", footer=dbug('here'))
    dbug('ask')
    # """--== SEP_LINE ==--"""
    # gblock([my_box1, my_box2, my_box3], 'boxed', 'prnt', positions=[5,2,9], title="[box1, box2, box3] positions: [5,2,9]", footer=dbug('here'), length=100, height=20)
    # dbug('ask')
    # """--== SEP_LINE ==--"""
    positions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # height = 35
    # length = 150
    for n, pos in enumerate(positions):
        cls()
        # print("\n"*10)
        clr_num = n % len(colors)
        color = colors[clr_num]
        # new_box = boxed(run_cmd('date'), box_color=box_color, color=color)
        lines[2] = f"pos: {pos} color: {color} box_color: {box_color}"
        box0 = boxed(lines)
        # dbug(box0, 'lst')
        # """--== SEP_LINE ==--"""
        # color = colors[1]
        # new_box1 = gblock(box0, pad=pad, position=pos, color=color, boxed=True, box_color=box_color, prnt=True, height=height, length=length)
        time.sleep(1)
        # dbug('ask')
    # """--== SEP_LINE ==--"""
    prcnt = 0
    for n in range(20):
        cls()
        prcnt = 100 * n / 20
        box1 = boxed(prcnt_bar(prcnt,length=40), title="box1")
        box2 = boxed(run_cmd('uname -snr'), title="box2")
        box3 = boxed(run_cmd('date'))
        # lines = gblock([box1, box2])
        # printit(lines, title="two boxes", footer=dbug('here'))
        # lines = gblock([[box1, box3]], 'prnt', footer=dbug('here'))
        # lines = gblock([[box1, box3], [box2]], 'prnt' footer=dbug('here'))
        lines = gblock([[box1, box3], [box2]], 'prnt', 'boxed', 'centered', title="rows of boxes", footer=dbug('here'), txt_center=99)
        time.sleep(0.5)
    dbug('ask')
    # """--== SEP_LINE ==--"""
    pcnt = 0
    while True:
        cls()
        print("\n"* 3)
        prcnt += 1
        box0 = boxed(run_cmd('curl -s wttr.in?0'))
        # printit(box0)
        box1 = boxed(prcnt_bar(prcnt,length=40))
        box2 = boxed(run_cmd('uname -a'))
        column = gblock([[box1], [box2]])
        # dbug('ask')
        # dash = gblock([[box0, column]], 'prnt')  # same as next
        print("\n"*3)
        dash = gblock([box0, column], 'prnt', 'boxed', 'centered', title="Dash w/2 Columns", footer=dbug('here'))
        print("\n"*3)
        dash1 = gblock([[box0], [column]], 'prnt', 'boxed', 'centered', title="Dash w/1 column", footer=dbug('here'), txt_center=99)
        # dbug('ask')
        # printit(lines, 'boxed', title="Dash boxes", footer="Ctrl-C " + dbug('here'))
        # printit(dash, 'boxed', title="Dash boxes", footer="Ctrl-C " + dbug('here'))
        # dbug('ask')
        time.sleep(3)
        if prcnt > 99:
            break
    # ### EOB def gblock_demo(): ### #


# #####################################################
def find_file_in_dirs(filename, dirs_l=[], prnt=False):
    # #################################################
    """
    purpose: this is for future use as something like find_file_in_dirs(filename, dirs_l)
    notes: if dirs_l is empty it defaults to ["./"]
    """
    found_file = ""
    # script_basename = Path(__file__).stem
    # cfg_file = os.path.splitext(__file__)[0]
    # cfg_file += ".cfg"
    # from pathlib import Path
    # home = str(Path.home())
    # poss_dirs = [home, home + "/dev/dotfiles"]
    if dirs_l == []:
        dirs_l = ["./", os.path.dirname(__file__)]
    poss_dirs = dirs_l
    # dbug(poss_dirs)
    for dir in poss_dirs:
        # dbug(dir)
        if dir.endswith("/"):
            tst_for_file = dir + filename
        else:
            tst_for_file = dir + "/" + filename
        # dbug(f"Looking for: {tst_for_file}", "ask")
        if os.path.isfile(tst_for_file):
            found_file = tst_for_file
            if prnt:
                printit(f"Found file: {found_file} ...", "center")
            break
    return found_file
    # ### EOB def find_file_in_dirs(filename, dirs_l=[], prnt=False): ### #



def long_proc(msg="testing long process", *args, **kwargs):
    """
    purpose: this is only for test or demos - it nothing but a sleep
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(msg)
    # """--== Config ==--"""
    seconds = kvarg_val(["time", "secs", "seconds"], kwargs, dflt=2)
    # """--== Process ==--"""
    time.sleep(seconds)
    return msg
    # ### EOB def long_proc(msg="testing long process", *args, **kwargs): ### #


def usr_input(prompt="Your input: ", *args, **kwargs):
    """
    purpose: allow user input with editing - see usr_update() as that is likely what you want
    options::
        - prompt: str = "Your input: "
        - edit: bool
        - dft: str
        - centered: bool
        - shift: int
        - update: dict
        - length: int = 0       # all lines will display with the same length
    returns: edit or input data as str or dict if update option
    Notes: 
        - this function is typically called by usr_update()
        - see usr_update()
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    # """--== Import ==--"""
    import readline
    # """--== Config ==--"""
    centered_b = bool_val(["centered", "center", "cntr"], args, kwargs, dflt=False)
    shift = kvarg_val(["shift", "shft"], kwargs, dflt=0)
    # dbug(shift)
    prompt = kvarg_val("prompt", kwargs, dflt=prompt)
    default = kvarg_val(["dflt", 'default'], kwargs, dflt=None)
    edit = bool_val(["edit", "editable", 'edt'], args, kwargs, dflt=False)
    update = kvarg_val(["update"], kwargs, dflt={})
    max_val_len = kvarg_val(["max_v", "max_v_len", "max_val", "max_val_len"], kwargs, dflt=0)
    noedit_b = bool_val(["noedit", "no_edit", "noinput", "no_input"], args, kwargs, dflt=False)
    # """--== Validate ==--"""
    if edit and default is None and len(update) == 0:
        dbug("Edit has been invoked but there is no default|dflt which is needed or make default='' ...")
        return None
    # dbug(f"edit: {edit} update: {update} centered: {centered_b} shift: {shift} default={default}")
    # """--== Init ==--"""
    if prompt is None:
        prompt = "none"
    if default is None or default == "":
        default = " "
    default = str(default)
    edit_text = default
    if edit and len(update) == 0:
        if prompt == "Your input: ":
            prompt = "Edit as needed: "
        # edit_text = default
        if edit_text == "":
            return ""
    # dbug(shift)
    # dbug(prompt)
    # """--== Process ==--"""
    # """--== standard input ==--"""
    if not edit and len(update) == 0:
        # dbug(f"shift: {shift} max_val_len: {max_val_len} nclen(default): {nclen(default)}")
        default_msg = ""
        if len(default) > 0:
            default_msg = f"[{default:>{max_val_len}}]: "
            if prompt.endswith(": "):
                prompt = prompt.rstrip(": ") + default_msg
        if centered_b:
            prompt = centered(prompt, shift=shift)[0]
            # dbug(f"prompt: {prompt} centered_b: {centered_b}")
        if noedit_b:
            # dbug()
            printit(prompt)
            return default
        response = input(prompt) or default
    #
    # """--== update dictionary values ==--"""
    if len(update) > 0:
        response = usr_update(update, centered=centered_b, shift=shift, edit=edit)
        return update
    #
    # """--== edit default input ==--"""
    # dbug(f"edit: {edit} update: {update} centered: {centered_b} shift: {shift} default={default}")
    if edit:
        # dbug(f"edit: {edit} update: {update} centered: {centered_b} shift: {shift} default={default} noedit_b: {noedit_b} prompt: {prompt}")
        readline.set_startup_hook(lambda: readline.insert_text(edit_text))
        shift = shift - (max_val_len // 2)
        response = ""
        try:
            if centered_b:
                # ruleit(center=True)  # debugging
                prompt = centered(prompt, shift=shift)[0]
            if noedit_b:
                # yes, you may want to display the question but not allow an edit...
                # dbug(prompt + default)
                printit(prompt + default)
                return default
            # dbug(prompt)
            response = input(prompt)
        finally:
            if edit:
                readline.set_startup_hook(None)
    #
    # """--== determine default ==--"""
    if not edit and len(default) > 0:
        # dbug(f"edit: {edit}  providing dflt: {default} if empty response: {response} default={default}")
        if response is None:
            response = ""
        if default is None:
            default = ""
        if response == "" and nclen(default) > 1:
            response = default
    return response
    # ### EOB def usr_input(*args, **kwargs): ### #


def usr_input_demo(*args, **kwargs):
    """
    purpose: demo of usr_input()
    returns: None
    """
    cntr_ops = [False, True]
    for cntr in cntr_ops:
        printit("Just a simple input ...")
        ans = usr_input(centered=cntr)
        dbug(ans)
        print("-"*40)
        # """--== SEP_LINE ==--"""
        dflt = "This is the default"
        dbug(dflt)
        prompt = "Just hit enter here to test the dflt: "
        printit(f"supplying prompt: {prompt} and dflt: {dflt}")
        ans = usr_input(prompt=prompt, dflt=dflt, centered=cntr)
        dbug(ans)
        print("-"*40)
        # """--== SEP_LINE ==--"""
        ans = usr_input(dflt="Edit this big ole string until you are happy", edit=True, centered=cntr)
        dbug(ans)
        print("-"*40)
        # """--== SEP_LINE ==--"""
        ans = usr_input(dflt="You can not edit this ", edit=False, centered=cntr)
        dbug(ans)
        print("-"*40)
        # """--== SEP_LINE ==--"""
        my_d = {"elem1": "is one", "elem2": "is two", "elem3": "is three"}
        print(f"Starting usr_input with update={my_d} centered but no edit")
        ans_d = usr_input(update=my_d, centered=cntr)
        dbug(ans_d)
        print("-"*40)
        # """--== SEP_LINE ==--"""
        my_d = {"elem1": "is one", "elem2": "is two", "elem3": "is three"}
        ans_d = usr_input(update=my_d, centered=cntr, edit=True)
        dbug(ans_d)
        dbug("Stop here....", 'ask')
    # ### EOB def usr_input_demo(*args, **kwargs): ### #


# ###########################################
def usr_update(my_d, *args, **kwargs):
    # #######################################
    """
    purpose: given a dict, and a list of keys to change - allow user update(s) to values in  my_d dictionary
        go through the list of keys to fix and prompt user for new value, present the current value as default
    args: my_d: dict        # dict to have updated
    options:
          - fix: list       # default=[]      - list of keys to prompt user for change; if empty, use all the my_d keys
          - centered: bool  # default=False   - whether to center everything on the screen
          - edit: bool      # defualt=False   - whether to allow text edit in place or the default of input replacement input
          - no_edits: list  # default=[]      - list of keys that are presented but not editable
          - quit: bool      # default=False   - whether to immediately quit on an entry of "q" or "Q", or "quit"
    returns: my_d (with user updates)
    Notes:
        - what is in the passed dict values is what will be presented as the default.
        - aka: user_edit()
        - normally usr_update() calls this function
        - this function calls usr_input(), ie: it superceded usr_input
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(args)
    # dbug(kwargs)
    """--== Config ==--"""
    # max_size = kvarg_val(["max", " max_size"], kwargs, dflt=40)
    fix_l = kvarg_val(["fix", "fix_list", "fix_l", "to_fix", "fix_lst", "update", "to_update", "update_lst"], kwargs, dflt=[])
    edit_b = bool_val(["edit", "editable", "edit_txt", "edit_text"], args, kwargs, dflt=False)
    centered_b = bool_val(["center", "centered", "cntr"], args, kwargs, dflt=False)
    noedits_l = kvarg_val(["noedits", "no_edits", "excludes", 'except'], kwargs, dflt=[])  # which keys will not be allowed editing of any form but will be presented/displayed
    quit_b = bool_val(["quit", "q", "exit"], args, kwargs, dflt=False)
    chunks_b = bool_val(["chunks"], args, kwargs, dflt=False)
    # dbug(centered_b)
    # """--== Init ==--"""
    prompt = "Please enter new value for: "
    fix_d = {}
    if len(fix_l) == 0:
        # fix_l was not supplied so make it equal to list(my_d.keys())
        fix_l = list(my_d.keys())
    for k in fix_l:
        # put in values from supplied my_d
        fix_d[k] = my_d[k]  # give fix_d[k] the value from my_d[k]
    scr_cols = int(get_columns())
    max_k = maxof(list(fix_d.keys()))
    # dbug(max_k)
    # dbug(list(my_d.keys()))
    # dbug(fix_d)
    # dbug(list(fix_d.values()))
    max_v = maxof(list(fix_d.values()))
    # dbug(list(fix_d.keys()))
    # dbug(max_v)
    # dbug(prompt)
    if (max_k + max_v) > scr_cols:
        if chunks_b:
            dbug(prompt)
            max_v = scr_cols - (nclen(prompt) + 10)  # arbitrary
            dbug(f'max_v is set to {max_v}')
        else:
            dbug("Houston we have a problem... not enough room on the screen... consider the 'chunks' to break up large values into smaller chunks option")
            # dbug(chunks_b)
            # dbug(max_k)
            # dbug(max_v)
            # dbug(scr_cols)
            return
    new_d = my_d.copy()
    # """--== Process ==--"""
    # dbug(f"fix_l: {fix_l} noedits_l: {noedits_l} edit_b: {edit_b}")
    # dbug(prompt)
    for k, v in fix_d.items():
        # dbug(f"k: {k} v: {v}")
        if v == "":  # this actually will get taken care of in usr_input but doing it anyway
            v = " "
        if k in noedits_l:
            noedit = True
            # dbug(f"making noedit: {noedit} k: {k}")
        else:
            noedit = False
            # dbug(f"k: {k} not found in noedits_l: {noedits_l}")
        # dbug(f"chkg nclen(v): {nclen(v)}")
        if nclen(v) > max_v and chunks_b:
            # dbug(prompt)
            printit(v, 'boxed', title=f"This line will be broken into chunks (len: {max_v}) for editing.", footer=dbug('here'), centered=centered_b)
            my_lines = wrapit(v, length=max_v)
            lines_d = {}
            for num, line in enumerate(my_lines):
                # dbug(f"adding line: {line} to lines_d")
                lines_d[num] = line
            # new_lines = usr_update(lines_d, 'edit', quit=quit, centered=centered_b)
            new_lines = usr_update(lines_d, 'edit')
            # dbug(new_lines)
            ans = " ".join(list(new_lines.values()))
            new_d[k] = ans
            printit(ans, 'boxed', title="New replacement added", footer=dbug('here'), centered=centered_b)
            continue
        if edit_b:
            # allows in-place editing
            # dbug(f"max_k: {max_k} max_v: {max_v}")
            my_prompt = prompt + f"[{k:<{max_k}}]: "
            # dbug(my_prompt)
            ans = usr_input(prompt=my_prompt, default=v, centered=centered_b, max_v=max_v, edit=edit_b, noedit=noedit)
            # dbug(ans)
        else:
            # allow replacement input only
            # dbug(f"max_k: {max_k} max_v: {max_v} k: {k} v: {v}")
            my_prompt = prompt + f"[{k:<{max_k}}]: "
            # dbug(my_prompt)
            ans = usr_input(edit=edit_b, prompt=my_prompt, centered=centered_b, dflt=v, max_v=max_v, noedit=noedit)
            ans = str(ans)
            # dbug(ans)
        if quit_b:
            if ans in ("q", "Q", "quit"):
                # do_close(center=True, box_color="red on black")
                break
        new_d[k] = ans
    # dbug(f"Returning my_d: {new_d}")
    return new_d
    # ### EOB def usr_update(my_d, fix_l=[], *args, **kwargs): ### #


def usr_update_demo(*args, **kwargs):
    """
    purpose: demo for usr_update()
    return: None
    """
    # """--== SEP_LINE ==--"""
    for centered in [False, True]:
        for edit in [False, True]:
            my_d = {"one": 1, "two": 2,  "three": "3", "big value": "this is a long string", 'modified': datetime.now().strftime("%Y-%m%d %H:%M")}
            noedits = ["modified"]
            printit(f"usr_update(my_d, centered={centered}, edit={edit}", 'boxed', centered=centered )
            new_d = usr_update(my_d, centered=centered, edit=edit, noedits=noedits)
            gtable(new_d, 'prnt', 'hdr', centered=centered, title="no edit of default", footer=dbug('here'))


# #############################################
def remap_keys(my_d, remap_d, *args, **kwargs):
    # #########################################
    """
    purpose: remaps keys names AND can select only the k.v pairs you want (in the order specified) (ie option: 'mapped_only')
    requires:
        - my_d: dict       # a dictionary of key-value pairs
        - remap_d: dict    # a dictionary holding orig_key-new_key pairs 
    options:
        - mapped_only: bool  # default=True - returns a dictionary of only the remap_d key-value pairs if True (default)
        - rnd: int           # rounds out numbers to rnd scale
    returns: my_d (remapped and optionally selected pairs)
    notes: remap_d should be dict {orig_key: new_key, ...} but can be a list only (assumes and sets mapped_only=True)
        This is a very useful function that allows you to pick/select columns from a given dictionary in your order and rename any keys as well
        I use this a lot when I download financial data from a web api
    created: 20220423 gwm
    """
    """--== Config ==--"""
    mapped_only_b = bool_val(["mapped_only", "mapped"], args, kwargs, dflt=True)
    rnd = kvarg_val("rnd", kwargs, dflt=0)
    # """--== Convert ==--"""
    new_d = {}
    if isinstance(remap_d, list):
        for elem in remap_d:
            new_d[elem] = elem
        remap_d = new_d
        mapped_only_b = True
    if isinstance(my_d, pd.DataFrame):
        my_d = cnvrt2lol(my_d)
    # """--== Process ==--"""
    # ok this is a special circumstance... if my_d is an lol then select and change the hdr (colnames) and select values appropriately
    if islol(my_d):
        selected_d = remap_d
        data_lol = my_d
        orig_keys_l = list(selected_d.keys())
        new_keys_l = list(selected_d.values())
        data_colnames = data_lol[0]
        rows = data_lol[1:]
        rtrn_lol = [new_keys_l]
        for row in rows:
            new_row = []
            for col, val in enumerate(row):
                if data_colnames[col] in orig_keys_l: 
                    new_row.append(val)
            rtrn_lol.append(new_row)
        return rtrn_lol
    """--== SEP_LINE ==--"""

    if not mapped_only_b:
        # this will change found remap_keys if found and keep all other key_value pairs in my_d
        this_d = {}
        for k, v in my_d.items():
            # dbug(f"testing to see if k: {k} is in remap_d.keys(): {remap_keys}")
            if k in remap_d:
                this_d[remap_d[k]] = v
            else:
                this_d[k] = v
        # dbug(this_d)
        return this_d
    new_d = {}
    for orig_key, new_key in remap_d.items():
        # dbug(f"working on orig_key: {orig_key} and new_key: {new_key}")
        # if new_key not in list(remap_d.keys()):
            # dbug(f"hmmm orig_key: {orig_key} not in remap_d.keys(): {remap_d.keys()}")
        for my_d_key in my_d.keys():
            if orig_key == my_d_key:
                val = my_d[orig_key]
                if val is not None and isnumber(val) and rnd > 0:
                    # dbug(f"rnd: {rnd} val: {val} ")
                    val = round(float(val), rnd)
                new_d[new_key] = val
            else:
                if not mapped_only_b:
                    new_d[orig_key] = my_d[orig_key]
        if new_key not in new_d:
            new_d[new_key] = "None"
    # include ignored keys ????
    if not mapped_only_b:
        for k, v in my_d.items():
            if k not in new_d:
                new_d[k] = v
                # dbug(f"Added new_d[k]: {new_d[k]}")
    return new_d
    # ### EOB def remap_keys(my_d, remap_d, *args, **kwargs): ### #


def remap_keys_tst(*args, **kwargs):
    """
    WIP for testing only
    """
    my_d = {"DEFAULT": {'one': 1, "two": 2, "three": 3}, 's1': {"s1_1": 1, "s1_2": 2, "s1_3": 3}}
    box1 = gtable(my_d, 'noprnt', 'hdr', title="my_d", footer=dbug('here'), colnames=["Key", "Value"])
    # dbug(my_d)
    remap_d = {'DEFAULT': 'default', 'dflt': 'default'}
    box2 = gtable(my_d, 'noprnt', 'hdr', title="remap_d", footer=dbug('here'), colnames=["Key", "Value"])
    new_d = remap_keys(my_d, remap_d, mapped_only=False)
    # dbug(new_d)
    box3 = gtable(new_d, 'noprnt', 'hdr', title='new_d w/mapped_only=False', footer=dbug('here'), colnames=["Key", "Value"])
    boxes = [box1, box2, box3]
    gcolumnize(boxes, 'prnt', 'centered', title="cfg_d test")
    """--== SEP_LINE ==--"""
    raw_d = {"my long name col1": 1, "my long name col2": 2, 'col3': 3, "my long name col4": 4}
    box1 = gtable(raw_d, 'noprnt', 'hdr', title="raw_d", footer=dbug('here'), colnames=["Key", "Value"])
    remap_d = {"my long name col1": "col1", "my long name col2": 'col2', 'col3': 'col3', "my long name col4": 'col4'}
    box2 = gtable(remap_d, 'noprnt', 'hdr', title="rmap_d", footer=dbug('here'), colnames=["Key", "Value"])
    new_d = remap_keys(raw_d, remap_d)
    box3 = gtable(new_d, 'noprnt', 'hdr', title="new_d", footer=dbug('here'), colnames=["Key", "Value"])
    boxes = [box1, box2, box3]
    gtitle(80, "--== SEP_LINE ==--", fc="-", centered=True)
    gcolumnize(boxes, 'prnt', 'centered', title="key name changes - all k,v pairs")
    """--== SEP_LINE ==--"""
    remap_d = {"my long name col1": "col1", "my long name col2": 'col2', 'new_col3': 'col3', 'my long name col4': 'col4'}
    box2 = gtable(remap_d, 'noprnt', 'hdr', title="rmap_d", footer=dbug('here'), colnames=["Key", "Value"])
    selected_d = remap_keys(raw_d, remap_d)
    box3 = gtable(selected_d, 'noprnt', 'hdr', title="selected_d", footer=dbug('here'), colnames=["Key", "Value"])
    boxes = [box1, box2, box3]
    gtitle(80, "--== SEP_LINE ==--", fc="-", centered=True)
    gcolumnize(boxes, 'prnt', 'centered', title="key name changes, includes new replaced col3, selected cols")
    """--== SEP_LINE ==--"""
    csv_file = "~/data/finops/symptomatic.csv"
    gtable(csv_file, 'prnr', footer=dbug('here'), selected=['sym', 'cp', 'lpr'])
    dbug("Done!", 'centered')
    # ### EOB def remap_keys_tst(*args, **kwargs): ### #



# ####################################
def quick_plot(data, *args, **kwargs):
    # ################################
    """
    purpose: quick display of data in  a file or in dataframe
        displays a plot on a web browser if requested
    required: data: df | str | list (filename: csv or dat filename)
    options:
        - centered: bool
        - title: str
        - footer: str
        - choose: bool       # invokes gselect multi mode to allo"w selections of columns to display in the plot (graph)
        - selections: list   # you can declare what columns to plot
        - web: bool          # displays to your browser instead of a plot figure
        - dat: bool | str    # I sometimes use a commented firstline for headers -
                             # using 'dat' declares this to be true, if character is used ie dat=":"
                             # then that will be used as the delimiter
        - type: str          # default=line, bar, barh, hist, box, kde, density, area, pie, scatter, hexbin
        - colnames: list | str     # default = [] if it is a str="firstrow" then the firstrow obviously will be treated as colnames
        - mavgs: bool        # 50 day and 200 day moving averages added to plot
        - box_text: str | list # string or lines to add to a box in fuger default=""
        - subplot: str       # sub plot with area under filled using colname = subplot
        - save_file: str     # name of file to save the plot figure to.  default=""
        - delimiter: str     # assumes a filename for data (above) and use delimiter to seperate elements in each line of the file
        - hlines: dict       # dictionary eg: {"target": 44, "strike": 33, ...} can be one or several
        - pblines: bool      # pullback_lines - only useful for stock history charts
        - rnd: int           # round numbers to int - only useful if show or prnt is invoked for gtable display (see option show | prnt)
        - show | prnt: bool  # shows/prints a limited (see tail option) amount of data in a table centered (for debugging or checking)
        - tail: int          # for the last n rows of the df default=35
    # returns: df
    returns: lol  # list of rows each of which is a list of columns
    NOTE: if a filename is used as data it will get "purified" by removing all comments first (except the first line of a dat file.)
        tail, title and footer only affect the gtable if show is True
    """
    """--== debugging ==--"""
    # dbug(funcname())
    # dbug(data)
    # dbug(f"type(data): {type(data)}")
    # dbug(args)
    # dbug(kwargs)
    # """--== Imports ==--"""
    import matplotlib.pyplot as plt
    import plotly.express as px
    # import pandas as pd
    """--== debug ==--"""
    # dbug(funcname())
    # """--== Config ==--"""
    show = bool_val(["show"], args, kwargs, dflt=False)
    choose = bool_val(["choose", "multi", 'multiple'], args, kwargs, dflt=False)
    selections = kvarg_val(["selections", "select", "choices", "selected"], kwargs, dflt=[])
    # dbug(selections)
    title = kvarg_val("title", kwargs, dflt="")
    footer = kvarg_val("footer", kwargs, dflt="")
    tail = kvarg_val("tail", kwargs, dflt=15)
    centered_b = bool_val(["centered", "center"], args, kwargs, dflt=True)
    web_b = bool_val(['web', 'browser'], args, kwargs, dflt=False)
    colnames = kvarg_val(['colnames', 'col_names', 'columns'], kwargs, dflt=[])
    # dbug(colnames)
    # kind = kvarg_val(['kind', 'type', 'style'], kwargs, dflt='line')  # line, bar, barh, hist, box, kde, density, area, pie, scatter, hexbin
    dat = kvarg_val(["dat"], kwargs, dflt=False)
    dat = bool_val(["dat"], args, kwargs, dflt=dat)  # this needs to be here in combination w/above
    mavgs = bool_val(["mavgs", "mavg", "moving_avgs"], args, kwargs, dflt=False)
    # dbug(mavgs)
    box_text = kvarg_val(["box_text", 'box_txt', "text", "txt"], kwargs, dflt="")
    # dbug(box_text)
    savefile = kvarg_val(["save", "savefile", "save_file"], kwargs, dflt="")
    # dbug(savefile)
    hlines = kvarg_val(["trgt", "target", 'strike', "line", "hline", "hlines"], kwargs, dflt=0)  # must be a dictionary
    # dbug(hlines)
    subplot = kvarg_val(["subplot", "sub_plot", "sub"], kwargs, dflt="")
    pb_lines = bool_val(["pb_lines", "pblines", "pullback_lines", "plines"], args, kwargs, dflt=False)  # only useful for stock history charts
    delimiter = kvarg_val(["delim", "delimiter", "dlmtr"], kwargs, dflt=",")
    # index_b = bool_val(["index", "indexes", "idx"], args, kwargs, dflt=False)
    rnd = kvarg_val(["rnd", "round"], kwargs, dflt=0)
    # """--== Inits ==--"""
    selections_l = []
    hline_name = "HLine"
    simple_list = False
    # """--== Convert to df ==--"""
    # dbug(data)
    # dbug(type(data), 'ask')
    if isinstance(data, pd.DataFrame):
        df = data
        # dbug(df.head(2))
        # dbug(colnames)
        # dbug(df.info())
        src = "df"
    if isinstance(data, str):
        # this is probably a path/filename
        if file_exists(data):
            # assumes it is a csv file
            # df = pd.read_csv(data, thousands=',', comment="#", header=0, on_bad_lines='warn', engine='python', infer_datetime_format=True)
            # dbug(dat)
            # df = cat_file(data, 'df', 'hdr', dat=dat, nums=True, delim=delimiter, index=index)
            df = cat_file(data, 'df')
            # dbug(df[:3])
            dat = False
            df = cat_file(data, 'df', 'hdr', dat=dat, nums=True, delim=delimiter, index=False)
            # dbug(df[:3])
            # dbug(df.info())
            src = f"File: {data}"
    if isinstance(data, dict):
        df = pd.DataFrame.from_dict(data)
        if colnames in ('firstrow', 'first_row', 'firstline', 'first_line'):
            colnames = data[0]
            data = data[1:]
        src = "df"
        # dbug(src)
    # dbug(colnames)
    if isinstance(data, list):
        # dbug(data)
        if not isinstance(data[0], list):
            dbug("This must be a simple list")
            simple_list = True
            # colnames.insert(0, "Index")
            # dbug(colnames)
            # dbug(data[:2])
        if isinstance(data[0], list):
            # dbug("data must be a list of lists")
            # this is an lol so...
            if colnames in ("firstrow", "first", "firstline") or dat:
                colnames = data[0]
            data = data[1:]
            # dbug(colnames)
            # data = [[n, elem] for n, elem in enumerate(data)]  # this would add indexing
            # dbug(data, 'ask')
            # dbug(data)
            # new_data_lol = []
            # data = new_data_lol
            # dbug(colnames)
            # dbug(data)
        df = pd.DataFrame(data)
        # dbug(df.head(2))
        # dbug(df.index.name)
        if colnames != []:
            # dbug(df)
            # dbug(colnames)
            if colnames in ("firstrow", "firstline", "rowone", "first"):
                colnames = df.iloc[0].tolist()  # first row for the header/colnames
                # dbug(colnames)
                # suggested oneliner: df.rename(columns=df.iloc[0]).drop(df.index[0])
            # dbug(colnames)
            # dbug(df.info)
            df.columns = colnames
        src = "list"
        # if colnames[0] != df.index.name:
        if not simple_list:
            # should be a lol
            # dbug(colnames)
            # dbug(f"colnames: {colnames} colnames[0]: {colnames[0]} df.index.name: {df.index.name} index: {index}")
            # dbug(df.info)
            df = df.set_index(colnames[0])  # set the index to the first column
            # dbug(df.info)
            # dbug('ask')
    # dbug(colnames)
    # dbug("All conversions done except colnames... ")
    # """--== Process ==--"""
    # dbug(df.head(3))
    if show:
        footer = f"{footer} Source: {src} "
        # dbug(type(df))
        # dbug(df)
        df = df.round(3)  # TODO make this a config option??
        # dbug(df)
        gtable(df.tail(int(tail)), 'hdr', 'prnt', title=title + f" df.tail({tail})", footer=footer + dbug('here'), centered=centered_b, rnd=rnd)
    # dbug(colnames)
    if colnames != []:
        if colnames in ("firstrow", 'firstline', "first", "rowone"):
            # dbug(df)
            colnames = list(df.iloc[0])
            # dbug(colnames)
            df.columns = colnames
            # dbug(colnames)
            df = df.iloc[1:]
            # dbug(df.head(2))
        # dbug(colnames)
        if not simple_list:
            # dbug(f"Check the number of supplied colnames (len(colnames): {len(colnames)}), should be {len(df.columns)}")
            colnames = df.columns.to_list()
            df
            # colnames.insert(0, df.index.name)
        else:
            df.columns = colnames
    # dbug(f"Now all conversions done including colnames: {colnames}  df:{df}")
    colnames = df.columns.to_list()
    # dbug(colnames)
    if df.index.name is not None:
        colnames.insert(0, df.index.name)  # now insert the index name as the first colname
    # dbug(df.head(3))
    # dbug(colnames)
    choices_l = colnames[1:]
    if selections != []:
        if isinstance(selections, str):
            selections = [selections]
        selections_l = selections
        # dbug(f"selections: {selections} selections_l: {selections_l}")
    else:
        # dbug(colnames)
        selections_l = colnames[1:]
    # dbug(selections_l)
    if choose:
        # dbug(colnames)
        # dbug(selections_l)
        selected_l = []
        # dbug(selected_l)
        # dbug(choices_l)
        selections_l = gselect(choices_l, centered=centered_b, width=140, title=title, rtrn="v", prompt="Add the desired column", footer=f"Selected: {selected_l}", quit=True, multi=True, dflt="q")
        # ruleit()
        # dbug(selected_l)
        # dbug(selections_l)
        if selections_l == []:
            return df
        # dbug(selections_l)
    # dbug(selections_l)
    # dbug(f"colnames: {colnames}")
    # dbug(type(df))
    # dbug(df)
    # dbug(df.dtypes)
    # dbug(df.info)
    if selections_l == []:
        if colnames[0] == df.index.name:
            selections_l = colnames[1:]
        else:
            selections_l = colnames
    # dbug(selections_l)
    # dbug(df.head(3))
    # snp1 = df.iat[0, 0]
    # dbug(snp1)
    # dbug(type(snp1))
    # dbug(df['S&P'])
    # dbug(df.info())
    if mavgs:
        # dbug(f"selections_l: {selections_l} mavgs: {mavgs}")
        df["50ma"] = df[selections_l[0]].rolling(window=50, min_periods=0).mean()
        df["200ma"] = df[selections_l[0]].rolling(window=200, min_periods=0).mean()
        selections_l.append("50ma")
        selections_l.append("200ma")
        df = df.dropna()  # inplace=True)
        # last_50ma = round(df["50ma"].iloc[-1], 2)
        # last_200ma = round(df["200ma"].iloc[-1])
        # """--== SEP_LINE ==--"""
    if isinstance(hlines, dict):
        for k, v in hlines.items():
            if isempty(v):
                continue
            # dict = name/label, value of line
            # typically used for trgt/strike price
            # dbug(hline)
            # hline_name = list(hline.keys())[0]
            # dbug(f"k: {k} v: {v}")
            hline_name = k
            # hline = list(hline.values())[0]
            hline = float(v)
            # dbug(hline_name)
            # dbug(f"hline: {hline} type(hline): {type(hline)}")
            if hline != "":
                if float(hline) > 0:
                    # dbug(len(df))
                    hline_col = []
                    for x in range(len(df)):
                        hline_col.append(hline)
                    df[hline_name] = hline_col
                    selections_l.append(hline_name)
    # """--== Intervals (Experimental) ==--"""
    # interval = kvarg_val(["interval", "int", "xinterval", "xskip"], kwargs, dflt=40)
    # interval = int(len(df) / 20)  #num of ticks = 20 here
    # df = df[::interval]
    # """--== SEP_LINE ==--"""

    df = df.reset_index()  # inplace=True)
    # dbug(type(df))
    # dbug(selections_l, 'ask')
    # gtable(df, 'prnt', 'hdr', footer=dbug('here'))  # debugging only
    # web_b = True
    if web_b:
        # """--== for browser display ==--"""
        # dbug(colnames[0])
        fig = px.line(df, x=colnames[0], y=selections_l, title=title)
        fig.show()
    else:
        if "date" in str(colnames[0]).lower() or "time" in str(colnames[0]).lower():
            # dbug(colnames)
            # dbug("Setting index to colnames[0]: {colnames[0]}")
            if colnames[0] != df.index.name:
                my_df = df.set_index(colnames[0])
            else:
                my_df = df
        else:
            # dbug(df)
            my_df = df
        for col in colnames[1:]:  # cut out the date/time/x scale
            # dbug(colnames)
            # dbug(col)
            # dbug(type(my_df))
            # dbug(my_df.head(3))
            my_df[col] = my_df[col].astype(float)
            # dbug(my_df)
        # """--==  fix dateseries on first column if it has time or date in the name ==--"""
        # dbug(f"colnames: [{colnames[0]}]")
        # dbug(colnames[0])
        if has_substr(colnames[0], ["date", "time"]):
            # dbug(df[:2])
            # dbug(df.iloc[0][0])
            if df.index.name == colnames[0]:
                date_entry = df.first_valid_index()
            else:
                date_entry = str(df.iloc[0][0])
            # dbug(date_entry)
            dtformat = get_dtime_format(date_entry)
            # dbug(dtformat)
            if dtformat != "%Y-%m-%d":
                # df.iloc[:, 0] = pd.to_datetime(pd.Series(df.iloc[:, 0]), format=dtformat, errors='coerce')
                my_df = pd.to_datetime(pd.Series(df.iloc[:, 0]), format=dtformat, errors='coerce')
            # dbug(df[:3])
            # dbug(df.info)
        # """--== SEP_LINE ==--"""
        # dbug('ask')
        # dbug(df)
        # gtable(df.tail(tail), 'prnt', 'idx', 'hdr', title="debugging", footer=dbug('here'))
        # dbug(selections_l[0])  # same as colnames[1]
        # dbug(df.info())
        # dbug(colnames)
        # dbug(list(df))
        # dbug(selections_l[0])
        # dbug(df[selections_l[0]].tolist()[:2])
        pri_max = df[selections_l[0]].max()
        # dbug(pri_max)
        # dbug('ask')
        try:
            pri_max = round(float(pri_max))
            # pri_max = round(df[selections_l[0]].max(), 2)
            pri_min = df[selections_l[0]].min()
            pri_min = round(float(pri_min), 2)
            # dbug(pri_min)
            footer += f"\nMin-Max: {pri_min}-{pri_max}"
        except Exception as Error:
            dbug(Error)
        # grid = (5, 4)
        grid = (6, 1)  # aka shape
        # fig = plt.figure(figsize=(15, 6))
        # fig, ax = plt.subplots()
        top_loc = (0, 0)
        bot_loc = (5, 0)
        # """--== SEP_LINE ==--"""
        top_plt = plt.subplot2grid(grid, top_loc, rowspan=5, colspan=1)
        # dbug(selections_l)
        top_plt.plot(df[selections_l], label=selections_l)
        top_plt.legend(loc="upper right")
        top_plt.set_title(title)
        plt.title(title)
        # plt.xlabel(footer)  This works but it lands between top and sub-plot and crowds subplot
        # """--== SEP_LINE ==--"""
        if box_text != "":
            if isinstance(box_text, list):
                box_text = "\n".join(box_text)
                box_text = escape_ansi(box_text)
                # dbug(repr(box_text))
                # dbug(repr(box_text))
                # dbug(box_text, 'lst')
            # properties
            props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
            top_plt.text(0.01, 0.97, box_text, transform=top_plt.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
            top_plt.legend(loc='upper right')
        # """--== SEP_LINE ==--"""
        if subplot != "":
            bot_plt = plt.subplot2grid(grid, bot_loc, rowspan=1, colspan=1)
            bot_plt.fill_between(df.index, df[subplot], label=subplot, color="blue", facecolor='grey')
            bot_plt.legend(loc="upper right")
            # plt.subplots_adjust(hspace=1)  # make no diff???
        # """--== SEP_LINE ==--"""
        if pb_lines:
            # indx_len = len(df.index)
            # x_val = df.index[int(0.03*indx_len)]
            x_val = df.index[0]
            # dbug(x_val)
            # """--== correction ==--"""
            try:
                correction = round(0.9 * float(pri_max), 2)  # 10% pull back
            except Exception as Error:
                correction = 0
                dbug(Error)
            top_plt.axhline(y=correction, color='cyan', linestyle="--")
            if len(box_text) < 10:
                top_plt.text(x_val, correction, "Correction[10%]", va='center', ha='left', backgroundcolor='w')
            # """--== bear ==--"""
            bear = 0.8 * pri_max  # 20% pull back
            top_plt.axhline(y=bear, color='cyan', linestyle="-.")
            if len(box_text) < 10:
                top_plt.text(x_val, bear, "Bear[20%]", va='center', ha='left', backgroundcolor='w')
            # """--== superbear ==--"""
            superbear = 0.7 * pri_max  # 30% pull back
            top_plt.axhline(y=superbear, color='cyan', linestyle="-.")
            if len(box_text) < 10:
                top_plt.text(x_val, superbear, "SuperBear[30%]", va='center', ha='left', backgroundcolor='w')
            # """--== ultrabear ==--"""
            uberbear = 0.6 * pri_max  # 40% pull back
            top_plt.axhline(y=uberbear, color='cyan', linestyle="-.")
            if len(box_text) < 10:
                top_plt.text(x_val, uberbear, "UberBear[40%]", va='center', ha='left', backgroundcolor='w')
        # """--== SEP_LINE ==--"""
        footer = "\n\n" + footer + f" {dbug('here')} "
        plt.figtext(0.5, 0.01, footer, ha='center', fontsize=11)
        plt.gcf().set_size_inches(15, 5)
        if len(subplot) > 0:
            plt.gcf().set_size_inches(15, 6)
        # """--== SEP_LINE ==--"""
        if savefile != "":
            # NOTE!!!! this has to be called BEFORE plt.show !!!! NOTE #
            # dbug(savefile)
            plt.savefig(f"{savefile}")
        # """--== SEP_LINE ==--"""
        plt.style.use('seaborn')
        # plt.tight_layout()
        # plt.xticks(rotation = 45)
        # plt.autofmt_xdate(rotation = 45)
        # import matplotlib.ticker as ticker
        # tick_spacing = 1
        # top_plt.set_major_locator(ticker.MultipleLocator(tick_spacing))
        plt.show()
    # dbug(f"Returning df: {df}")
    my_lol = cnvrt2lol(df)
    return my_lol
    # return df
    # ### EOB def quick_plot(data, *args, **kwargs): ### #


def quick_plot_demo():
    """
    purpose: to provide examples of displaying data in plots
    returns: None
    """
    # """--== Debugging ==--"""
    # file = "/home/geoffm/data/finops/indexes.dat"
    fname = "tst.dat"
    content = '''# date    elem1 elem2 elem3
2022-09-15  22  66  99
2022-09-16  24  67  100
2022-09-17  25  66  98
2022-09-18  26  66  97'''
    # dbug(fname)
    """--== SEP_LINE ==--"""
    with open(fname, "w") as f:
        f.write(content)
        """--== SEP_LINE ==--"""
    # dbug(fname, 'ask')
    rows_lol = cat_file(fname, 'dat')
    # dbug(rows_lol, 'ask')
    gtable(rows_lol, 'prnt', 'hdr', 'centered', title=f"rows_lol from {fname}", footer=dbug('here'))
    text = ["This text", "should be", "shown to", "the user"]
    hlines = {"line1": 25, "line2": 26}
    # dbug(hlines)
    quick_plot(rows_lol, 'multi', 'hdr', 'dat', text=text, title=f"rows_lol from: {fname}", footer=dbug('here'), hlines=hlines)
    # """--== SEP_LINE ==--"""
    df = cat_file(fname, 'df')
    # dbug(df)
    gtable(df, 'prnt', 'centered', 'hdr', 'index', title="df from cat_file(fname)", footer=dbug('here'))
    quick_plot(df, 'multi', 'hdr', title="df", footer=dbug('here'))
    # dbug('ask')
    # """--== SEP_LINE ==--"""
    try:
        import yfinance as yf
        sym = "BAC"
        trgt = 27
        sym_o = yf.Ticker(sym)
        hx = sym_o.history(start="2020-01-01", end="2022-09-04")
        title = f"History of sym: {sym}"
        quick_plot(hx, 'prnt', 'mavgs', title=title, footer=dbug('here'), selections=["Close"], hline={"Target": trgt}, subplot="Volume", text="Text should\ngo here")
        # dbug('ask')
    except Exception as Error:
        dbug(Error)
        return
    # """--== SEP_LINE ==--"""
    import random
    lst_len = 2000
    sums = []
    for i in range(0, lst_len):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        my_sum = die1 + die2
        sums.append(my_sum)  # adding a sum of 2 dice
    # from collections import Counter
    # dbug(sums)
    # quick_plot(sums, 'show', colnames=["roll", "sum"], title="Demo of Sum (2) dice Plot", footer=dbug('here'))
    quick_plot(sums, 'show', colnames=["sum"], title="Demo of Sum (2) dice Plot", footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    from collections import Counter
    # import pandas as pd
    data = Counter(sums)
    df = pd.pandas.DataFrame.from_dict(data, orient='index')
    df.columns = ["Sums"]
    df = df.sort_index()
    # kinds = ['line', 'bar', 'barh', 'area']
    quick_plot(df, 'show', colnames=["Sum"], title=f"Demo of Frequency of Sum (2) dice", footer=f"{dbug('here')}")
    # """--== SEP_LINE ==--"""
    my_lol = [['date', 'tempC', "tempF"], ['2020-01-01', 40.0, 104.0], ["2020-04-01", 36.0, 96.8], ["2021-01-01", 24.2, 75.56],
            ["2021-09-01", 22, 71.6], ["2021-10-01", 21, 69.8],["2022-01-01", 22.22, 72], ["2022-02-01", 20, 68],
            ["2022-03-01", 23, 73.4], ["2022-04-01", 31, 87.8], ["2022-05-01", 35, 95], ["2022-06-1", 36, 96.8], ["2022-06-10", 34, 93.2]]
    dbug(f"Calling quick_plot with my_lol[:3]: {my_lol[:3]}")
    quick_plot(my_lol, colnames='firstrow', text="You can\nadd text\nif you\nwant", footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    quick_plot(my_lol, 'mavgs', colnames='firstrow', text="You can add\n moving averages\nby default 50 and 200 day", footer=dbug('here'))
    # """--== SEP_LINE ==--"""
    dbug("Done")


def boxed_demo():
    """
    purpose: demo of using boxed()
    """
    do_logo(box_color="yellow! on black", color="black on white")
    print()
    do_logo("Your Organization", 'figlet', box_color="red! on black", color="yellow! on rgb(90,90,90)", fortune=True, quote="~/data/lines.dat")
    print()
    msg = "This is box1"
    color = "blue! on white"
    box_color = "red! on yellow!"
    msg += " " + dbug('here')
    box1 = boxed(msg, 'prnt', color=color, box_color=box_color, title="box1", footer=dbug('here'))
    print()
    box2 = boxed(msg, 'prnt', 'shadowed', color=color, box_color=box_color, title="box1 shadowed", footer=dbug('here'))
    gcolumnize([box1, box2], 'prnt', 'centered', 'shadowed', title="Box unshadowed and Box shadowed", footer=dbug('here'))
    print()
    quote = get_random_line("~/data/lines.dat")
    color = "yellow! on rgb(50,50,90)"
    box_color = "red! on black!"
    title = clr_coded("[white! on black!] Quote  Box[/] ")
    q_box = printit(quote, 'boxed', title=title, prnt=False, shadow=True, box_color=box_color, color=color)
    printit(q_box, 'centered')
    ans = cinput("How many boxes would like printed on a single row: ")
    boxes = []
    for num, in enumerate(range(int(ans)), 1):
        boxes.append(boxed(f"This is\nBox {num}"))
    printit(gcolumnize(boxes), 'centered')
    # ### EOB def boxed_demo(): ### #


# #############
def clr_demo():
    # #########
    """
    purpose:  color Demo - used for testing only
    """
    my_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'violet']
    for color in my_colors:
        colors = shades(color)
        with Spinner(f"Demo of shade({color}) ", 'centered', 'prog', 'elapsed', style='vbar', colors=colors):
            time.sleep(3)
    lines1 = []
    lines2 = []
    lines3 = []
    lines4 = []
    lines5 = []
    lines6 = []
    for shade in range(0, 255, 15):
        red_shade = f'rgb({shade}, 0, 0)'
        green_shade = f'rgb(0, {shade}, 0)'
        blue_shade = f'rgb(0, 0, {shade})'
        red_green_shade = f'rgb({shade}, {shade}, 0)'
        red_blue_shade = f'rgb({shade}, 0, {shade})'
        green_blue_shade = f'rgb(0, {shade}, {shade})'
        lines1.append("color: " + gclr(red_shade) + red_shade + RESET)
        lines2.append("color: " + gclr(green_shade) + green_shade + RESET)
        lines3.append("color: " + gclr(blue_shade) + blue_shade + RESET)
        lines4.append("color: " + gclr(red_green_shade) + red_green_shade + RESET)
        lines5.append("color: " + gclr(green_blue_shade) + green_blue_shade + RESET)
        lines6.append("color: " + gclr(red_blue_shade) + red_blue_shade + RESET)
    printit(gcolumnize([lines1, lines2, lines3, lines4, lines5, lines6]), 'boxed', 'centered', box_color="blue on rgb(150,150,200)")
    lines = []
    lines.append("Way to add color: ")
    lines.append("this is [yellow! on grey99]yellow! on grey99[/] done")
    # dbug(repr(msg))
    lines.append('gclr("yellow! on grey30")' + gclr('yellow! on grey30') + 'This is yellow! on grey30')
    lines.append(gclr("yellow!") + "Just yellow!" + RESET)
    lines.append(gclr("on yellow!") + "Just on yellow!" + RESET)
    lines.append(gclr("yellow! on black") + "yellow! on black" + RESET + f"repr(gclr('yellow! on black'): {repr(gclr('yellow! on black'))}")
    lines.append("[yellow! on grey90]yellow! on grey90[/]" + RESET)
    lines.append("[yellow! on black]yellow! on black[/]" + RESET)
    lines.append("[yellow on black]yellow on black[/]" + RESET)
    lines.append(' = [grey99]This is grey99[/]')
    printit(lines, 'boxed', 'centered', box_color="blue on rgb(150,150,200)")
    printit("This is [white! on grey99]white! on grey90[/] ...done", 'boxed', 'centered', box_color="white! on grey90", title=dbug('here'))
    print()
    printit("This is [grey100]grey100[/] ...done", 'boxed', 'centered', box_color="white! on grey90", title=dbug('here'))
    print()
    # """--== SEP_LINE ==--"""
    colors = [['red', 'dim red', 'bold red', 'red!', 'rgb(255,0,0)'],
            ['green', 'dim green', 'bold green', 'green!', 'rgb(0,255,0)'],
            ['blue', 'dim blue', 'bold blue', 'blue!', 'rgb(0,0,255)'],
            ['yellow', 'dim yellow', 'bold yellow', 'yellow!', 'rgb(255,255,0)'],
            ['magenta', 'dim magenta', 'bold magenta', 'magenta!', 'rgb(255,0,255)'],
            ['cyan', 'dim cyan', 'bold cyan', 'cyan!', 'rgb(0,255,255)'],
            ['white', 'dim white', 'bold white', 'white!', 'rgb(255,255,255)']]
    color_lol = []
    for row in colors:
        new_row = []
        for color in row:
            new_row.append(sub_color(color) + color)
        color_lol.append(new_row)
    color_lol.insert(0, ['color', 'dim color', 'bold color', 'color!', 'rgb representation'])
    gtable(color_lol, 'prnt', 'hdr', 'centered', title=' Fundamental Colors ', footer=" Color Demo ")


# ########
def tst(*args, **kwargs):
    # ####
    """
    purpose: for development one testing only - subject to change at anytime
    returns: None
    notes: This is for testing only
    This is just an example testing function.
    This example shows how you can quickly test whatever you want (any function) while you are still editing a file.
    You can completely remove this function.
        or rename it
        or call another function within it
        or leave it as an example.
        It demonstrates the use of the -T argument.
    This is a test function and can be called while editing in vim with...  :! ./% -T tst all,my,arguments,go=here
        or  :! ./% -T tst This is farg1
        or  :! ./% -T tst This is farg1  farg2
        or  :! ./% -T tst This is farg1  farg2,my_kwarg=this_val
        or  :! ./% -T tst This is farg1  "farg2, my_kwarg=this val"
        or  :! ./% -T tst This is farg1  "farg2,my_kwarg=this val"
    Notes:  The args here are do not need to be separated by a space and there is no need to use any quotes unless your key value needs a space.
            All variables will get quoted for you.
            If you separate your function arguments with a space then you will need to quote all the arguments as one string
            The there is a space(s) anywhere in the arguments just quote the while set of argument words
    """
    # printit(globals()[funcname()].__doc__, 'boxed', 'centered', title=f"Docs for {funcname()}", footer=dbug('here'), box_color="yellow! on grey80")
    dbug(f"This function: {funcname()}({args}), {kwargs})", 'boxed', 'centered', box_clr="yellow! on black")
    printit("Now you can quickly run a tst of any code you want without leaving vim...", 'centered')
    return None
    # ### EOB def tst(*args, **kwargs): ### #


# ##################
def do_func_docs():
    # ##############
    """
    purpose: to get function docs
    returns: prints selected function __doc__ boxed and centered
    """
    # """--== SAMPLE TABLE ==--"""
    # gtable(tst_d, 'prnt', 'wrap', title="Simple tst_d no col_limit so default?", footer=dbug('here'))
    # dbug('ask')
    # """--== SAMPLE TABLE 2 ==--"""
    # gtable(tst_d, 'prnt', 'wrap', title='tst_d with list type items no  col_limit', footer=dbug('here'))
    # dbug('ask')
    # """--== SAMPLE TABLE 3 ==--"""
    # gtable(tst_d, 'prnt', 'wrap', title="tst_d no col_limit", footer=dbug('here'))
    # dbug('ask')
    # """--== SEP_LINE ==--"""
    # """--== Get a list of all func except a few... ==--"""
    my_lines = grep_lines(__file__, r"^def .*\(")
    my_funcs_l = [x.replace("def ", "") for x in my_lines]
    funcs_l = [re.sub(r"\((.*)\):.*", "", x) for x in my_funcs_l]
    funcs_l = [x for x in funcs_l if x.strip() not in ("main", 'tst')]
    funcs_l = [x for x in funcs_l if x.strip() if "demo" not in x]
    funcs_l = sorted(funcs_l)
    # gtable(funcs_d, 'prnt', 'wrap', 'center', col_limit=100, footer=dbug('here'))
    # dbug('ask')
    # """--== user select ==--"""
    # func = gselect(stripped_funcs_l, 'centered', title="Which Function would you like information on:")
    exclude_l = ["main", 'tst', 'do_func_demos']
    funcs_l = chk_substr(funcs_l, exclude_l, action='exclude')
    funcs_l = sorted(funcs_l)
    func = gselect(funcs_l, 'centered', title="Which Function would you like information on:", footer=dbug('here'), width='80%')
    if func not in ("", "q", "Q"):
        # dbug(func)
        doc = globals()[func].__doc__
        # func_args = grep_lines(my_funcs_l, "^" + func + r"\(")[0]
        # dbug(func_args)
        # my_args = "(" + func_args.split("(")[1] + ")"
        # r = re.search(r"\((.*)\):", func)
        # my_args = r.group(1)
        # func = func.replace("():", "")
        # eval_this = func + '.__doc__'
        # doc = eval(eval_this)
        # clean up doc first
        doc = doc.split("\n")
        doc = [line.strip() for line in doc if line.strip() != '']
        printit(doc, 'center', 'boxed', title=func+"(...)", footer=dbug('here'))
        # doc_d = {"Func Name": func + "(" + my_args + ")", "Func Doc": doc}
        # gtable(doc_d, 'prnt', 'wrap', 'hdr', 'center', col_limit=120, colnames="firstrow")
    return func
    # ### EOB def do_func_docs(): ### #


def has_substr(text_s, chk_l, *args, **kwargs):
    """
    purpose: determin if any sub-string in chk_l is in text_s
        column_name = "dtime"
        eg is "time" or "date" in column_name... then use has_substr(column_name, ["time", "date"])
    required:
        - text_s: str
        - chk_l: list
    options:
        - ci: bool  # case_insensitive
    returns True | False
    notes:
        used in quick_plot()
    """
    ci_b = bool_val(["ci", "case_insensitive"], args, kwargs, dflt=False)
    if ci_b:
        text_s = text_s.lower()
    has_substr_b = False
    for sstr in chk_l:
        if ci_b:
            sstr = sstr.lower()
        if sstr in text_s:
            has_substr_b = True
    return has_substr_b


# ###############################################
def chk_substr(chk_l, strgs_l, action='exclude'):
    # ###########################################
    """
    purpose: given a list of strings to check (chk_l) and a list of substrings to compare (strgs_l)
            if any "compare" substring is in any string in check list of strings then
                do action either 'exclude' or 'include'
    required:
        - chk_l: list | str
        - strgs_l: list
    options:
        - action: str  # default is 'exclude'
    return: new_list
    usage:
        # given a list of functions, exclude the ones that may have any of the provided  substrings (list) in the exclude_l list
        funcs_l = chk_substr(funcs_l, exclude_l, action='exclude')
        eg:
            exclude_l = ["main", 'tst', 'do_func_demos']
            funcs_l = chk_substr(funcs_l, exclude_l, action='exclude')
            funcs_l = sorted(funcs_l)
    """
    new_l = []
    for string_s in chk_l:
        if any(sub_s in string_s for sub_s in strgs_l):
            if action == 'include':
                new_l.append(string_s)
        else:
            if action == 'exclude':
                new_l.append(string_s)
    return new_l


# ##################
def do_func_demos(*args, **kwargs):
    # ##############
    """
    purpose: allows selection of demos within this module - runs the demo function selected
    options: None
    return: None
    """
    funcs_l = [func for func in globals() if "_demo" in func]
    exclude_l = ["main", 'tst', 'do_func_demos']
    funcs_l = chk_substr(funcs_l, exclude_l, action='exclude')
    funcs_l = sorted(funcs_l)
    # demo_funcs_l = [x.strip(":") for x in funcs_l if "demo" in x]  # only include _demo funcs
    # ans = gselect(demo_funcs_l, 'centered', footer=dbug('here'))
    ans = gselect(funcs_l, 'centered', footer=dbug('here') + " E)dit this file", width='80%')
    if ans in ("E"):
        do_edit(__file__)
    if ans in ("", "q", "Q"):
        return ans
    func = ans.replace("_demo()", "")
    if func in globals():
        doc = eval(f"{func}.__doc__")
        if isempty(doc):
            doc = "No doc is available ..."
        else:
            doc = [ln for ln in doc.split("\n") if len(ln) > 5]
        printit(doc, 'centered', 'boxed', title=f"Doc for {ans} function")
    # dbug(globals())
    # dbug(ans)
    if ans in globals():
        # dbug("Great ans: {ans}")
        globals()[ans]()
    else:
        dbug(f"Failed to find ans: {ans} in globals()")
    # askYN("", 'centered')
    # if askYN(f"Do you want to see the code for this demo: {ans}? ", 'center'):
    #     # dbug(ans)
    #     func = ans.replace('()', '\\(')
    #     # dbug(func)
    #     start_pat = f"^def {func}"
    #     # dbug(start_pat)
    #     demo_code = from_to(__file__, "^def quick_plot_demo()", "^$", include='top')
    #     demo_code = from_to(__file__, start_pat, "^$", include='top')
    #     printit(demo_code, 'boxed', 'centered', box_color='yellow!', title=f"Code for this demo: {ans}", footer=dbug('here'))
    return ans


def gcontains(string_s, pattern_m):
    """
    purpose: determines if any pattern (str|list) is a substring of string (string_s)
    required:
        - string_s: str
        - pattern_m: str | list  # list = [pattern1, pattern2, ...]
    options: none
    returns: bool
    """
    if not isinstance(pattern_m, list):
        pattern_l = [pattern_m]
    else:
        pattern_l = pattern_m
    for pat in pattern_l:
        if pat in string_s:
            # dbug(f"Found pat: {pat} in string_s: {string_s} returning True")
            return True
    return False


def get_mod_docs(mod=__file__, *args, fn="*", **kwargs):
    """
    purpose: lists all functions and the docs from a module
    Note: except some functions eg _demo _tst (declared within this function, for now)
    returns cnt
    """
    """--== Debugging ==--"""
    # dbug(funcname())
    """--== Imports ==--"""
    # import inspect
    from inspect import getmembers, isfunction
    boxed_b = bool_val(["boxed", "box"], args, kwargs, dflt=True)
    # dbug(kwargs)
    # dbug(boxed_b, 'ask')
    """--== SEP_LINE ==--"""
    # exclude_l = ["main", 'tst', 'do_func_demos']
    # funcs_l = chk_substr(funcs_l, exclude_l, action='exclude')
    # funcs_l = sorted(funcs_l)
    md = __import__(mod)
    funcs = [f for _, f in getmembers(md, isfunction) if f.__module__ == md.__name__]
    excludes = ['_demo', 'tst']
    funcs = [f_o for f_o in funcs if not gcontains(f_o.__name__, excludes)]
    cnt = 0
    for f_o in funcs:
        try:
            name = f_o.__name__
            diff = 20 - len(name)
            name = name + ":" + " "*diff
            box1 = [name]
            doc = f_o.__doc__
            doc_l = doc.split("\n")
            doc_l = [ln.strip() for ln in doc_l if ln.strip() != '']
            if boxed_b:
                box2 = boxed(doc_l, width=80)
            else:
                # dbug(f"Here we go boxed_b {boxed_b}")
                box2 = doc_l
            lines = gcolumnize([box1, box2])
            lines.append(("--------------"))
            lines = [escape_ansi(ln) for ln in lines]
            printit(lines)
            cnt += 1
        except Exception as Error:
            dbug(f"func: {name}  Error: {Error}")
    return cnt
    # ### EOB def get_mod_docs(mod=__file__, fn="*"): ### #


# #########################################
def isempty(my_var):  # , *args, **kwargs):
    # #####################################
    """
    purpose: tests if a variable is empty ie len(my_var) == 0 or my_var is None etc
    requires:
        - my_var: str
    options: None
    returns: bool
    """
    # dbug(my_var)
    # dbug(type(my_var))
    if isinstance(my_var, pd.DataFrame):
        # dbug("this is a pandas")
        my_empty = my_var.empty
        # dbug(my_empty)
        return my_empty
    if my_var is None:
        return True
    if isinstance(my_var, list):
        if len(my_var) == 0:
            return True
    if isinstance(my_var, str):
        if my_var.lower() == "none" or len(my_var) == 0:
            # yes, consider this empty
            return True
    return not bool(my_var)
    # ### EOB def isempty(my_var):  # , *args, **kwargs): ### #


# ###############################
def isempty_tst(*args, **kwargs):
    # ###########################
    """
    purpose: to test isempty()
    """
    my_var_l = ["", 0, "none", None, {}, [], "but not this"]
    for my_var in my_var_l:
        if isempty(my_var):
            dbug(f"my_var: [{my_var}] is empty")
        else:
            dbug(f"isempty({my_var}) is False (ie: not empty)")


# ##################################
def columned(my_l, *args, **kwargs):
    # ##############################
    """
    purpose: set a list in X columns
    required: my_l: list
    options:
        - cols=0: int               # number of columns
        - order='v': str            # 'vertical', 'vert', 'v'| 'horizontal', 'hor', 'h'
                                    # order directs the order of the choices - proceed vertically through columns or horizontally through columns
        - justify='left: str        # 'left', 'right', 'center'
        - prnt=False: bool          # 'print', 'prnt' ... to invoke printing the lines
            - boxed: bool
            - centered: bool
            - title: str
            - footer: str
        - width=0: int              # cols will be calculated from this - approximated
    returns: lines for printing
    notes: this takes the place of standard module columnize so we are not dependant on that code
        - you probably do not want to use this function directly - use gcolumnize instead.
        - used by: gcolumnize()
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(my_l)
    # dbug(args)
    # dbug(kwargs)
    # """--== Imports ==--"""
    # from math import ceil
    # """--== Config ==--"""
    cols = kvarg_val(["cols", 'num_cols'], kwargs, dflt=0)
    # dbug(cols)
    prnt = bool_val(['prnt', 'print'], args, kwargs, dflt=False)
    boxed_b = bool_val(["boxed", "box"], args, kwargs, dflt=False)
    centered_b = bool_val(["centered", "center"], args, kwargs, dflt=False)
    color = kvarg_val(["color", "clr"], kwargs, dflt="")
    box_color = kvarg_val(["box_color", "box_clr"], kwargs, dflt="")
    title = kvarg_val("title", kwargs, dflt="")
    footer = kvarg_val("footer", kwargs, dflt="")
    justify = kvarg_val(["just", "justify"], kwargs, dflt='left')
    order = kvarg_val(["order", 'orient', 'orientation'], kwargs, dflt="v")
    # dbug(order)
    pivot = bool_val("pivot", args, kwargs, dflt=False)
    sep = kvarg_val(["sep"], kwargs, dflt=" | ")
    pad = kvarg_val(["pad"], kwargs, dflt=" ")
    blank = kvarg_val("blank", kwargs, dflt="...")
    width = kvarg_val(["width", "w", "length", "len", "l"], kwargs, dflt=0)
    # dbug(width, 'ask')
    # """--== Verify ==--"""
    # if len(my_l) == 0 or my_l is None:
    if isempty(my_l):
        dbug("Nothing to work on... ")
        return None
    if islol(my_l):
        dbug("You should consider using gcolumnize as this is for simple lists only")
        return None
    # """--== Init ==--"""
    scr_cols = get_columns()
    if "%" in str(width):
        width = width.replace("%", "")
        width = int(scr_cols * (int(width)/100))
    col = 0
    if pivot:
        if order == "v":
            order = "h"
        if order == "h":
            order = "v"
    avg_maxof = maxof(my_l)
    if cols == 0 and width == 0:
        width = get_columns()
        # dbug(width)
    if int(width) > 0 and int(cols) < 2:
        # cols is given preference over width
        # dbug(width)
        # dbug(avg_maxof)
        max_cols = ceil(width / avg_maxof)
        # dbug(f"width: {width}  avg_maxof: {avg_maxof} max_cols: {max_cols}")
        cols = max_cols
        if max_cols < len(my_l):
            # without this section you will end up with too many empty or blank cells and columns
            needed_rows = ceil(len(my_l) / max_cols)
            cols = ceil(len(my_l) / needed_rows)
            # dbug(f"len(my_l): {len(my_l)} and avg_maxof * len(my_l): {avg_maxof * len(my_l)}")
        # dbug(cols)
        if cols > len(my_l):
            cols = len(my_l)
        if cols == 1:
            order = "v"
        # dbug(f"width: {width} avg_maxof: {avg_maxof} cols: {cols} order: {order}")
    if cols == 0:
        cols = 1
    # dbug(f"width: {width} avg_maxof: {avg_maxof} cols: {cols} order: {order}")
    # """--== Process ==--"""
    rows = ceil(len(my_l)/cols)
    rc_arr = matrix(rows, cols, dflt_val=blank)
    for num, i in enumerate(my_l):
        elem = i
        # for row in range(rows):
        if order.lower() in ("v", 'vert', 'vertical'):
            row = num % rows
            col = num // rows
            # dbug(f"order: {order} cols: {cols} i: {i} num: {num} row: {row} col: {col} elem: {elem}")
        else:  # ie ("h", "hor", "horizontal")
            row = num // cols
            col = num % cols
            # dbug(f"order: {order} cols: {cols} i: {i} num: {num} row: {row} col: {col} elem: {elem}")
        rc_arr[row][col] = elem
    # dbug(rc_arr)
    # """--== SEP_LINE ==--"""
    max_col_lens = []
    for col in range(cols):
        max_col_lens.append(0)
        for row in range(rows):
            if nclen(rc_arr[row][col]) > max_col_lens[col]:
                max_col_lens[col] = nclen(rc_arr[row][col])
    lines = []
    # for row_num, elem in enumerate(rc_arr):
    for elem in rc_arr:
        new_elems = []
        for col_num, item in enumerate(elem):
            item = str(item)
            item_len = nclen(item)
            max_col_len = max_col_lens[col_num]
            diff = max_col_len - item_len
            fill = pad * diff
            if justify == 'left':
                new_elems.append(item + fill)
            if justify == 'right':
                new_elems.append(fill + item)
            if justify == 'center':
                center_fill = (diff // 2) * pad
                new_elems.append(center_fill + item + center_fill)
        items = [str(i) for i in new_elems]
        elems = ""
        elems = sep.join(items)
        lines.append(elems)
    lines = gblock(lines)  # not needed if you are using blocked or printit with blocked but this makes it hemogenous
    if prnt:
        printit(lines, boxed=boxed_b, centered=centered_b, title=title, footer=footer, color=color, box_color=box_color)
    return lines
    # ### EOB def columned(my_l=["one", "and two", "three", "and four", "five", 6, "my seven", "eight", "9", 10, 11], *args, **kwargs): ### #


def columned_demo():
    """
    purpose: to run a demo of using columned()
    options: None
    returns: None
    """
    my_l = ["one", "item two", "third element", 'four', "and this is five", "six"]
    # dbug(my_l)
    # """--== SEP_LINE ==--"""
    lines = columned(my_l, width=50)
    printit(lines, 'boxed', title="width=50")
    # ruleit(50)
    dbug('ask')
    # """--== SEP_LINE ==--"""
    lines = columned(my_l, width=150)
    printit(lines, 'boxed', title="width=150")
    # ruleit(150)
    dbug('ask')
    # """--== SEP_LINE ==--"""
    lines = columned(my_l, cols=3, order="h")
    printit(lines, 'boxed', title="cols=3")
    dbug('ask')
    # """--== SEP_LINE ==--"""
    cols = 0
    order = "v"
    lines = columned(my_l, order=order)
    printit(lines, 'boxed', title=f"Cols: {cols} Order: {order}", footer=dbug('here'), box_color="yellow! on black")
    # """--== SEP_LINE ==--"""
    cols = 1
    order = "v"
    lines = columned(my_l, order=order)
    printit(lines, 'boxed', title=f"Cols: {cols} Order: {order}", footer=dbug('here'), box_color="yellow! on black")
    # """--== SEP_LINE ==--"""
    cols = 4
    order = "v"
    lines = columned(my_l, cols=cols, order=order)
    printit(lines, 'boxed', title=f"Cols: {cols} Order: {order}", footer=dbug('here'), box_color="blue! on black!")
    # """--== SEP_LINE ==--"""
    cols = 4
    order = "h"
    lines = columned(my_l, cols=cols, order=order)
    printit(lines, 'boxed', title=f"Cols: {cols} Order: {order}", footer=dbug('here'), box_color="red! on black!")
    # """--== SEP_LINE ==--"""
    # scr_cols = get_columns()
    order = "h"
    lines = columned(my_l, cols=cols, order=order)
    printit(lines, 'boxed', title=f"Cols: {cols} Order: {order}", footer=dbug('here'), box_color="cyan! on black")
    # """--== SEP_LINE ==--"""
    cols = len(my_l)
    lines = columned(my_l, cols=cols, order=order)
    printit(lines, 'boxed', title=f"Cols: {cols} Order: {order}", footer=dbug('here'), box_color="red on black")
    # """--== SEP_LINE ==--"""
    boxes = []
    for num, item in enumerate(my_l, start=1):
        boxes.append(boxed(item, title=f"box{num}"))
    printit("Trying columned on boxes.... but it will fail... because you should use gcolumnize for that...")
    columned(boxes, 'prnt')
    # """--== SEP_LINE ==--"""
    gcolumnize(boxes, 'prnt', 'boxed', title="This is boxed using gcolumize", footer=dbug('here'))


def dtree(dir_name="./", *args, **kwargs):
    """
    purpose: print a simple directory tree
    options:
        - files: bool           # default=False
        - prnt: bool            # default=False  should we print out the lines
        - excludes: list | str  # default=[] this is a pattern or list of patterns to skip
        - boxed: bool           # boxes all the lines
        - title: str            # default=f"Directory: {dir_name} Show files: {files_b}"
        - footer: str           # default=f"Excludes: {excludes} " + dbug('here')"
        - centered: bool        # boxes all the lines
        - length: int           # default=3  # size of the "fill"
        - box_clr: str          # color of box if that option is True
    returns: list (lines for printing)
    """
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(dir_name)
    # dbug(args)
    # dbug(kwargs)
    # dbug(dir_name)
    # """--== Config ==--"""
    prnt = bool_val(["prnt", "print", "show"], args, kwargs, dflt=False)
    # dbug(prnt)
    files_b = bool_val(["files", "f"], args, kwargs, dflt=False)
    boxed_b = bool_val(["boxed", "box"], args, kwargs, dflt=False)
    box_clr = kvarg_val(['box_clr', 'box_color'], kwargs, dflt="white! on black")
    centered_b = bool_val(["centered", "center", "cntr"], args, kwargs, dflt=False)
    excludes = kvarg_val(["exclude", "excludes", "filer", "filters"], kwargs, dflt=[])
    length = kvarg_val(["length"], kwargs, dflt=3)
    title = kvarg_val("title", kwargs, dflt="")
    footer = kvarg_val("title", kwargs, dflt="")
    # """--== Init ==--"""
    if title == "":
        title = f"Directory: {dir_name} Show files: {files_b}"
    if footer == "":
        footer = f"Excludes: {excludes} " + dbug('here')
    start_str = "|"
    start_mark = "+"
    fill_str = " " * (length)
    mark_str = "-" * length
    lines = []
    if isinstance(excludes, str):
        excludes = [excludes]
    """--== Process ==--"""
    # dbug(dir_name)
    for root, dirs, files in os.walk(dir_name, topdown=True):
        skip = False
        level = root.replace(dir_name, '').count(os.sep)
        dname = os.path.basename(root)
        """--== SEP_LINE ==--"""
        for pat in excludes:
            if re.search(pat, root):
                skip = True
        if not skip:
            lines.append((level * (start_str + fill_str)) + start_mark + mark_str + dname + os.sep)
        else:
            continue
        # """--== files ==--"""
        if files_b:
            for num, file in enumerate(files, start=1):
                skip = False
                """--== SEP_LINE ==--"""
                for pat in excludes:
                    if re.search(pat, file):
                        skip = True
                if not skip:
                    lines.append(((level + 1) * (start_str + fill_str)) + start_mark + mark_str + file)
    lines = printit(lines, title=f"Directory: {dir_name} Show files: {files_b}",
                    prnt=prnt,  boxed=boxed_b, centered=centered_b, 
                    box_clr=box_clr,
                    footer=footer)
    return lines


def dtree_demo(*args, **kwargs):
    """
    purpose: demo of using dtree()"
    return: None
    """
    dirs = ["/etc/apt", "/sys/dev", "/sys/block"]
    excludes = ["^[au]"]
    for dir in dirs:
        dtree(dir, 'files', 'prnt', 'boxed', 'centered', excludes=excludes)
    return None


# this is here for reference - dont take it out yet
# def imports_list():
#     import sys
#     modulenames = set(sys.modules) & set(globals())
#     allmodules = [sys.modules[name] for name in modulenames]
#     printit(allmodules)


# ###########################################
def chklst(my_l, chkd_l=[], *args, **kwargs):
    # #######################################
    """
    purpose: display a list of empty checkboxes|ballot boxes with chkd_l boxes checked and xed_l boxes with and X
    required:
        - my_l: list      # list of check box names
        - chkd_l: list    # list of boxes to be checked
    options:
        - dflt: str       # default='empty' - alternatives: default= or dflt= 'chk', 'chkd', 'checked', 'all_chkd', 'chk_all , 'xed' 'x_all', 'all_x' ...
        - xed: list   # list of elems to "X"
        - boxed: bool
        - centered: bool
        - prnt: bool
        - color|clr: str      # default="" - text color
        - masterbox_clr: str  # default='white! on black' - outside master box color
        - chkmark_clr: str    # default='green!' - check mark color
        - xmark_clr: str      # default='red!' - X mark color
        - chkbox_color: str   # default="" - check boxes color
        - title: str
        - footer: str
        - cols: int           # number of columns
        - indx|nums|indexed|numbered: bool  # whether to number the items
    returns: list  # printable lines
    notes:
    use:
        ans = []
        my_l = ["one", "two", "three"]
        chkd_l = []
        while ans not in ("q", "Q", ""):
            cls()
            chklst(my_l, chkd_l, 'prnt', 'centered', 'boxed', title="What has been done", footer=dbug('here'))
            ans =  cinput("Select which it you would like to work on (q)uit: ")
            if ans in ("q", "Q", ""):
                break
            chkd_l.append(ans)
    """
    import unicodedata
    # """--== Debugging ==--"""
    # dbug(funcname())
    # dbug(my_l)
    # dbug(chkd_l)
    # dbug(args)
    # dbug(kwargs)
    # """--== Config ==--"""
    dflt = kvarg_val(["dflt", 'default'], kwargs, dflt='empty')
    xed_l = kvarg_val(["xed_l", "xs", "xes", "x's", "xed"], kwargs, dflt=[])
    centered_b = bool_val(["centered", "center"], args, kwargs, dflt=False)
    boxed_b = bool_val(["boxed", "box"], args, kwargs, dflt=False)
    prnt = bool_val(["prnt", "print", "show"], args, kwargs, dflt=False)
    # dbug(prnt)
    chkbox_clr = kvarg_val(["box_clr", "box_color", 'chkbox_clr', 'checkbox_clr'], kwargs, dflt="")
    master_box_clr = kvarg_val(["master_box_clr", "master_box_color", "mstrbox_clr", "masterbox_clr", 'main_box_clr', 'mainbox_clr'], kwargs, dflt="white! on black")
    clr = kvarg_val(["clr", "color"], kwargs, dflt="")
    chkmark_clr = kvarg_val(["checkmark_clr", 'chkmark_clr', 'checkmark_color', 'chkd_clr'], kwargs, dflt="green!")
    xmark_clr = kvarg_val(["xmark_clr", 'xmark_clr', 'xmark_color', 'xed_clr'], kwargs, dflt="red!")
    style = kvarg_val(["style"], kwargs, dflt="checkbox")
    # ballot_b = bool_val(["ballot"], args, kwargs, dflt=True)
    chkbox_b = bool_val(["check_box", 'chk_box', 'chkbox', 'chkbx', 'simple'], args, kwargs, dflt=False)
    title = kvarg_val("title", kwargs, dflt = "")
    footer = kvarg_val("footer", kwargs, dflt = "")
    cols = kvarg_val("cols", kwargs, dflt=1)
    indx = bool_val(["numbered", "indx", "indexed", "nums"], args, kwargs, dflt=False)
    # dbug(style)
    # dbug("\u2713")  # check mark
    # dbug("\u2714")  # bold check mark
    # dbug("\u2715")  # X
    # dbug("\u2716")  # bold X
    # dbug("\u2717")  # stylized X
    # dbug("\u2718")  # bold stylized X
    # """--== Init ==--"""
    CLR = gclr(clr)
    CHKBOX_CLR = gclr(chkbox_clr)
    CHKMARK_CLR = gclr(chkmark_clr)
    XMARK_CLR = gclr(xmark_clr)
    # dbug(CHKBOX_CLR + "chkbox_clr" + RESET)
    # dbug(CHKMARK_CLR + "chkmark_clr" + RESET)
    # dbug(XMARK_CLR + "xmark_clr" + RESET)
    # style_d syntax     [empty_box, chkd_box,  xed_box]
    # note 2716 is bold X 2718 is italisized X
    style_d = {'ballot': [f"{CHKBOX_CLR}{chr(9744)} {RESET}",
                          f"{CHKMARK_CLR}{chr(9745)} {RESET}",
                          f"{XMARK_CLR}{chr(9746)}{RESET}"],
               'checkbox': [f"{CHKBOX_CLR}[_]{RESET}",
                            f"{CHKBOX_CLR}[{CHKMARK_CLR}" + "\u2714" + f"{RESET}{CHKBOX_CLR}]{RESET}",
                            f"{CHKBOX_CLR}[{XMARK_CLR}" + "\u2716" + f"{RESET}{CHKBOX_CLR}]{RESET}",
                            ]
               }
    # dbug(style)
    if style.lower() in ("ballot"):  # or ballot_b:
        style = 'ballot'
    if style.lower() in ('check_box', 'chkbox', 'chk_box', 'chk_bx', 'checkbox', 'simple') or chkbox_b:
        style = 'checkbox'
    # dbug(style)
    style_l = style_d[style]
    # dbug(f"Style: {style_l}")
    # """--== SEP_LINE ==--"""
    lines = []
    for item in my_l:
        # box = "[" + "_" + "]"
        if dflt.lower() in ("empty", "", 'mpty', 'none'):
            box = style_l[0]
        if dflt.lower() in ("checked", 'chkd', 'all_chkd', 'all_chk', 'chk_all', 'chkf_all'):
            box = style_l[1]
        if dflt.lower() in ("xed", 'xd', 'x', 'all_x', 'all_xd', 'all_xed', 'all_xes' 'all_xs'):
            box = style_l[2]
        if item in xed_l:
            # box = "[" + "\u2718" + "]"
            box = style_l[2]
        if item in chkd_l:
            box = style_l[1]
        lines.append(f"{box}  {RESET}{CLR}{item}{RESET}")
        lines = gblock(lines)
    if indx:
        lines = [f"{num:>2}. {line}" for num, line in enumerate(lines, start=1)]
    if cols > 1:
        lines = gcolumnize(lines, cols=cols)
    lines = printit(lines, boxed=boxed_b, prnt=prnt, centered=centered_b, title=title, footer=footer, box_clr=master_box_clr, clr=clr)
    return lines
    # ### EOB def chklst(my_l, chkd_l=[], xed_l=[], *args, **kwargs): ### #


# ###############################
def chklst_demo(*args, **kwargs):
    # ###########################
    """
    purpose: chkbox() demo
    returns: None
    """
    # """--== Debugging ==--"""
    dbug(funcname())
    # """--== Config ==--"""
    centered_b = True
    # """--== Init ==--"""
    my_l = ["one", "two", "three"]
    chkd_l = []
    ans = "none"
    # """--== SEP_LINE ==--"""
    printit(chklst.__doc__, 'boxed', 'centered')
    askYN('Continue', 'centered' )
    while True:
        # cls()
        printit("Making all boxes 'X'ed. The default is for them to be empty ... these style defaults to 'checkbox' boxes but we are setting it to 'ballot' box style, centered", 'centered')
        chklst(my_l, chkd_l, 'all_xed', 'prnt', 'centered', 'boxed', style='ballot', dflt="x", title="chkbox() demo", footer=dbug('here'), xed_clr='red', chkd_clr='green')
        ans = gselect(my_l, centered=centered_b, title="Checkmark Selection", prompt="Select one for 'checked'")
        # dbug(ans)
        if ans in ("q", "Q", ""):
            # dbug(ans)
            break
        chkd_l.append(ans)
    # dbug("Done")
    # """--== SEP_LINE ==--"""
    gtitle(80, "--== SEP_LINE ==--", fc="-")
    xed_l = ["three"]
    chkd_l = []
    ans = "none"
    while True:
        # cls()
        printit("Making only the 'three' box X'ed", 'centered')
        # dbug(ans)
        chklst(my_l, chkd_l, 'prnt', 'centered', 'boxed', 'chkbox', xed_l=xed_l, chkbox_clr="white on grey40",
               mstrbox_clr='red! on black', footer=dbug('here'),
               title="Boxed checklist: checkbox style box_clr='white on grey40' mstrbox_clr='red! on black' centered")
        ans = gselect(my_l, centered=centered_b)
        # dbug(ans)
        if ans in ("q", "Q", ""):
            # dbug(ans)
            break
        chkd_l.append(ans)
    return


def do_cli(cmd, args_s, *args, **kwargs):
    """
    purpose: runs command-line requests with cmd args...
    returns: none
    """
    # dbug(args_s)
    if 'help' in args_s:
        cli_help()
        do_close()
    # dbug(cmd)
    # dbug(args_s)
    # limit_cmds = ['printit', 'boxed', 'centered', 'chklst', 'gselect', 'gblock', 'gcolumnize', 'gtable']
    # if cmd not in limit_cmds:
        # dbug("cmd: {cmd} not found... ")
    # else:
    args_d = get_args(args_s)
    args = args_d['args']
    kwargs = args_d['kwargs']
    # dbug(f"Running cmd: {cmd} with args: {args} kwargs: {kwargs}")
    out = globals()[cmd](*args, **kwargs)
    # dbug(out)
    # dbug("Returning out...")
    return out


def cli_help(*args, **kwargs):
    """
    purpose: provide basic help with do_cli()
    notes: This is work-in-progress (TODO)
    """
    msg = """
    gtoolz-cli <function> <argument_string>
        - the function call is without quotes
        - the argument string must be in quotes
            - within the argument string you have the option of quoting or not quoting
    Examples:
        - gtoolz-cli printit 'Please open the door', 'boxed', 'centered', 'shadowed', box_clr='red! on black
        - gtoolz-cli printit 'Please open the door!', 'boxed', 'centered', 'shadowed', box_clr='red! on black'
        - gtoolz-cli boxed "This is my message, box_clr=yellow! on black, prnt=True"
        - gtoolz-cli boxed "'This is my message', box_clr='yellow on black', prnt=True"
        - gtoolz-cli gtable "~/data/speedtst.csv, 'hdr', centered"
        - gtoolz-cli gtable "~/data/speedtst.csv, hdr, centered"
        
    gtoolz-cli is under development; a work in progress ... any suggeted improvements are encouraged. Currently this is limited in usefulness.
    """
    printit(msg, 'boxed', 'centered', title="gtoolz-cli", box_clr="yellow! on black", footer=dbug('here'))


# ##### Main Code #######
def main(main_args=""):  # ######
    # ###################
    """
    purpose: allows user to see some of the fuctionality of this tool set
    """
    # dbug(sys.argv)
    # ### Note: {0}-cli <cmd. [<fargs>...] is handles by handeOPTS ### #
    #           ie: {0} <cmd> [<fargs>...]
    if main_args == "":
        main_args = docopt(handleOPTS.__doc__, version=SCRIPT + "\nversion: " + __version__)
        handleOPTS(main_args)
    """--== SEP_LINE ==--"""
    if not main_args['-T'] or '-cli' not in sys.argv[0]:
        do_logo("companionway", box_color="red! on black!")
        credits_caveats = """I offer sincere thanks to any and all who have shared or posted code that has helped me produce this file.
        I am sure there are much better ways to achieve the results provided in every function or class etc.
        Please let me know of any problems, issues, improvements or suggestions.     geoff.mcanamara@gmail.com
        """
        credits_caveats = [ ln.lstrip() for ln in credits_caveats.split("\n") ]
        printit(credits_caveats, 'centered', 'boxed', box_color="blue on black!", txt_center=99)
    ans = ''
    if main_args['--demos']:
        while ans not in ("q", "Q"):
            ans = do_func_demos()
    # """--== SEP_LINE ==--"""
    if main_args['--docs']:
        while ans not in ("q", "Q"):
            ans = do_func_docs()
    # """--== SEP_LINE ==--"""


if __name__ == "__main__":
    # main_args = docopt(handleOPTS.__doc__, version=SCRIPT + "\nversion: " + __version__)
    # handleOPTS(main_args)
    main_args = ""
    main(main_args)
