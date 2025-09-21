#!/usr/bin/env python

import json
import subprocess
import re
import html
import argparse
import sys


mod_map = {
    64: "SUPER",
    8: "ALT",
    4: "CTRL",
    1: "SHIFT",
}


def mod_to_string(modmask: int) -> str:
    res = []

    for bf, key in mod_map.items():
        if modmask & bf == bf:
            res.append(key)
            modmask -= bf

    if modmask != 0:
        res.append(f"({modmask})")

    return "_".join(res)


def get_rofi_input(align: bool = False) -> str:
    binds = []
    bindstrs = []

    for bind in json.loads(subprocess.check_output(["hyprctl", "binds", "-j"])):
        mod = mod_to_string(bind["modmask"])
        key = bind["key"]
        dispatcher = bind["dispatcher"]
        args = bind["arg"]
        args_escaped = html.escape(args)

        if mod == "":
            modkey = key
        else:
            modkey = mod + "," + key

        binds.append((modkey, dispatcher, args_escaped))

    modkey_mxlen = -1
    if align:
        for bind in binds:
            modkey_mxlen = max(modkey_mxlen, len(bind[0]))

    for bind in binds:
        modkey = (
            bind[0] + " " * (modkey_mxlen - len(bind[0]))
            if modkey_mxlen != -1
            else bind[0] + ":"
        )
        bindstr = (
            f'<span color="lightgray">{modkey}</span> '
            f'<span color="white">{bind[1]}</span> '
            f'<span color="white">{bind[2]}</span>'
        )
        bindstrs.append(bindstr)

    return "\n".join(bindstrs)


def dispatch(choice: str):
    pattern = r'<span color="white">(.*?)</span> <span color="white">(.*?)</span>'
    match = re.search(pattern, choice)

    if match:
        dispatcher = match.group(1)
        args_escaped = match.group(2)
        args = html.unescape(args_escaped)

        if dispatcher == "exec":
            cmd = args
        else:
            cmd = f"hyprctl dispatch {dispatcher} {args}"

        subprocess.run(cmd, shell=True)


def parse_args():
    parser = argparse.ArgumentParser(
        description="rofi hyprland binds viewer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage="%(prog)s [options] [-- rofi_cmd...]",
    )
    parser.add_argument(
        "-A",
        "--no-align",
        default=False,
        help="disable column alignment",
        action="store_true",
    )

    if "--" in sys.argv:
        idx = sys.argv.index("--")
        argv, rofi_cmd = sys.argv[1:idx], sys.argv[idx + 1 :]
    else:
        argv, rofi_cmd = sys.argv[1:], []

    args = parser.parse_args(argv)

    align = not args.no_align

    return (align, rofi_cmd)


def main():
    (align, rofi_cmd) = parse_args()

    if len(rofi_cmd) == 0:
        rofi_cmd = ["rofi", "-dmenu", "-i", "-markup-rows", "-p", "bindings"]

    rofi_input = get_rofi_input(align=align)

    choice = subprocess.check_output(
        rofi_cmd,
        input=rofi_input,
        text=True,
    )

    dispatch(choice)


if __name__ == "__main__":
    main()
