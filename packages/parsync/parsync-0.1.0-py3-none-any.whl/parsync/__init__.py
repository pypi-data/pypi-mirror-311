"""Recursively copy missing files to a directory.

This is equivalent to: cp -r --ignore-existing SRC DST

Note: matching patterns use python regex syntax.
"""

import argparse
import functools
import itertools
import os
import re
import shutil
import signal
import sys
from concurrent.futures import ThreadPoolExecutor


def enumerate_copies(src, dst, filters=[], excludes=[]):
    if not os.path.isdir(src):
        yield src, os.path.join(dst, os.path.basename(src))
        return

    root = "." if os.path.normpath(src) == "." else os.path.dirname(src)

    dirs_todo = [src]

    while len(dirs_todo) > 0:
        src_d = dirs_todo.pop()
        dst_d = os.path.join(dst, os.path.relpath(src_d, root))

        todo_mkdir = not os.path.exists(dst_d)

        with os.scandir(src_d) as it:
            for dirent in it:
                if len(excludes) > 0 and any(e.search(dirent.path) for e in excludes):
                    continue

                if dirent.is_dir():
                    dirs_todo.append(dirent.path)

                else:
                    if len(filters) > 0 and not any(
                        f.search(dirent.path) for f in filters
                    ):
                        continue

                    if todo_mkdir:
                        os.makedirs(dst_d)
                        todo_mkdir = False

                    new_path = os.path.join(dst_d, dirent.name)
                    if not os.path.exists(new_path):
                        yield dirent.path, new_path


def parse_args():
    argparser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    argparser.add_argument(
        "src", metavar="SRC", nargs="+", help="source files and directories"
    )
    argparser.add_argument("dst", metavar="DST", help="destination directory")
    argparser.add_argument(
        "--procs",
        "-p",
        type=int,
        default=10,
        help="maximum number of concurrent copies (default: 10)",
    )
    argparser.add_argument(
        "--filter", "-f", nargs="*", default=[], help="pattern to filter source files"
    )
    argparser.add_argument(
        "--exclude", "-e", nargs="*", default=[], help="pattern to exclude source files"
    )
    argparser.add_argument(
        "--attributes",
        "-a",
        action="store_true",
        help="copy extra metadata (*time, xattrs, etc.)",
    )
    argparser.add_argument("--version", "-v", action="version", version="parsync v1.0")
    return argparser.parse_args()


def copy(pair, attributes=False):
    src, dst = pair

    if attributes:
        shutil.copy2(src, dst + ".tmp")
    else:
        shutil.copy(src, dst + ".tmp")

    os.rename(dst + ".tmp", dst)


def main():
    args = parse_args()
    try:
        filters = [re.compile(f) for f in args.filter]
        excludes = [re.compile(e) for e in args.exclude]
    except re.error:
        print("invalid regular expression")
        sys.exit(1)

    args.src = [os.path.expanduser(src) for src in args.src]
    args.dst = os.path.expanduser(args.dst)
    
    try:
        if not os.path.exists(args.dst):
            os.mkdir(args.dst)

        with ThreadPoolExecutor(max_workers=args.procs) as p:

            def signal_handler(signum, frame):
                p.shutdown(cancel_futures=True)

            signal.signal(signal.SIGTERM, signal_handler)
            for _ in p.map(
                functools.partial(copy, attributes=args.attributes),
                itertools.chain.from_iterable(
                    enumerate_copies(src, args.dst, filters, excludes)
                    for src in args.src
                ),
            ):
                pass

    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
