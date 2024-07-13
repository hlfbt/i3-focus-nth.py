#!/usr/bin/env python
#
# author: syl20bnr (2013), hlfbt (2024)
# goal: Focus the nth window in the current workspace (limited to 10 firsts)
# dependencies: i3ipc
#
# Example of usage in i3 config:
#
# bindsym $mod+0   exec i3-focus-nth.py -n 0
# bindsym $mod+1   exec i3-focus-nth.py -n 1
# ...              ...
# bindsym $mod+8   exec i3-focus-nth.py -n 8
# bindsym $mod+9   exec i3-focus-nth.py -n 9
#

import sys
import argparse
from typing import List, Optional

import i3ipc


PARSER = argparse.ArgumentParser(prog='i3-focus-nth')
PARSER.add_argument('-n', '--number',
                    required=True,
                    type=int,
                    choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    help='Window number (limited to [0,9]).')

i3 = i3ipc.Connection()


def focus_nth_window(nth):
    """ Roughly focus the nth window in the hierarchy (limited to 10 first) """
    windows = get_windows_on_current_workspace()

    if nth == 0:
        nth = 10

    if nth > len(windows):
        print('Window number out of range', file=sys.stderr)

        exit(1)

    i3.command('[con_id={0}] focus'.format(windows[nth - 1].id))


def get_windows_on_current_workspace() -> List[i3ipc.con.Con]:
    """ Returns all windows in the focused workspace """
    workspace = get_current_workspace()

    if workspace is None:
        return []

    root = i3.get_tree()
    nodes = root.find_by_id(workspace.id)

    return [node for node in nodes if node.window]


def get_current_workspace() -> Optional[i3ipc.con.Con]:
    """ Returns the current workspace """
    focused = i3.get_tree().find_focused()

    if focused is None:
        print('No focused workspace', file=sys.stderr)

        return None

    return focused.workspace()


if __name__ == '__main__':
    args = PARSER.parse_args()
    focus_nth_window(args.number)
