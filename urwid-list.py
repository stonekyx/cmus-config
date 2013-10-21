#!/usr/bin/python2

import urwid
import sys
import os
from bs4 import UnicodeDammit

data = sys.argv[1:-2]
fd_write = int(sys.argv[-2])
proc_write = int(sys.argv[-1])
choices = [UnicodeDammit(''.join(data[x*3:(x+1)*3])).unicode_markup
        for x in range(0,len(data)/3)]

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in enumerate(choices):
        button = urwid.Button(c[1])
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice[1], u'\n'])
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program,
            user_arg=choice[0])
    cancel = urwid.Button(u'Cancel')
    urwid.connect_signal(cancel, 'click', return_to_choice,
            user_arg=main.original_widget)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed'),
        urwid.AttrMap(cancel, None, focus_map='reversed')]))

def exit_program(button, arg):
    fout = open("/proc/%d/fd/%d" % (proc_write, fd_write), 'w')
    fout.write(str(arg))
    raise urwid.ExitMainLoop()

def return_to_choice(button, arg):
    main.original_widget = arg

def fail_exit(key):
    if key in ['q', 'Q']:
        fout = open("/proc/%d/fd/%d" % (proc_write, fd_write), 'w')
        fout.write("-1")
        raise urwid.ExitMainLoop()

main = urwid.Padding(menu(u'Pythons', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 60),
        valign='middle', height=('relative', 60),
        min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')],
        unhandled_input=fail_exit).run()
