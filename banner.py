import sys
import time
import fontc
from optparse import OptionParser

QUIET=0
NORMAL=1
VERBOSE=2

def banner(s):
    for c in s:
        fc = fontc.font[ord(c)]
        for i in range(0,8):
            sys.stdout.write(chr(fc[i]))

def main():
    parser = OptionParser(usage="banner [options] command",
            description="Commands: ...")

    parser.add_option("-v", "--verbose", dest="verbose",
         help="verbose", action="store_true", default=False)
    parser.add_option("-q", "--quiet", dest="quiet",
         help="quiet", action="store_true", default=False)
    parser.add_option("-C", "--count", dest="count",
         help="repeat the specified number of times", metavar="amount", type="int", default=1)
    parser.add_option("-N", "--nulls", dest="nulls",
         help="output nulls between banner", metavar="amount", type="int", default=10)

    (options, args) = parser.parse_args(sys.argv[1:])

    if len(args)==0:
        print("missing message")
        sys.exit(-1)

    verbosity = NORMAL
    if options.quiet:
        verbosity = QUIET
    elif options.verbose:
        verbosity = VERBOSE

    count = options.count
    while (count > 0):
        s = " ".join(args)
        banner(s)

        if (count > 0):
            nulls = options.nulls
            while (nulls>0):
                sys.stdout.write(chr(0))
                nulls -= 1

        count -= 1

if __name__ == '__main__':
    main()
