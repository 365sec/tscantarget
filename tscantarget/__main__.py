import netblock
import argparse
from ttarget import TTarget

"""
1.step   get input target
2.step   distinguish between domain names and ip
3.step   domain name resolution
4.step   out put ip and domain file ,and ip count, domain count
"""


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file')
    args = parser.parse_args()
    if args.input_file ==None:
        print "usage: tscantarget -i target.cvs "
        return
    tt = TTarget()
    tt.parser(args.input_file)

if __name__ == "__main__":
    main()