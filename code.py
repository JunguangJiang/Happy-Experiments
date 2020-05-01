import argparse
import time
parser = argparse.ArgumentParser()
parser.add_argument("-s", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.s**2
if args.verbose:
    for i in range(10):
        print("the square of {} equals {}".format(args.s, answer))
        time.sleep(1)
else:
    print(answer)
print('answer = ', answer)