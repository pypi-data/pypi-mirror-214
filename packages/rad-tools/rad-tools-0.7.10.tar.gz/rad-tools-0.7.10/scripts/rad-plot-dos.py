#! /usr/local/bin/python3

from radtools.routines import winwait
from radtools.score.plot_dos import create_parser, manager

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    manager(**vars(args))
    winwait()
