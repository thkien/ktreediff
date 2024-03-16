import os
import sys
import logging
import argparse
from ktreediff.file import DiffNode
from ktreediff.util import Util


logger = logging.getLogger('treediff')



def setup_log(log_level="info"):

    LOG_FORMAT_SIMPLE = '%(message)s'
    LOG_FORMAT_DEBUG = '%(asctime)s: %(levelname)s: %(funcName)s(): %(lineno)d: %(message)s'

    if log_level == "debug":
        lf = LOG_FORMAT_DEBUG
    else:
        lf = LOG_FORMAT_SIMPLE

    ll_map = {
        "debug": logging.DEBUG
        , "info": logging.INFO
        , "warning": logging.WARNING
        , "error": logging.ERROR
        , "fatal": logging.FATAL
    }

    ll = ll_map.get(log_level, "info")

    logging.basicConfig(level=ll, format=lf)


_HELP="""$ treediff [options...] <left> <right>
  Note: <left> and <right> can be a pair of files or a pair of directories

Examples:
To compare files in 2 directories dir_a and dir_b
  $ treediff dir_a dir_b

To compare files in 2 directories dir_a and dir_b, included subfolders
  $ treediff dir_a dir_b --recursive

To compare specific files (*.txt, *.psd) in 2 directories dir_a and dir_b
  $ treediff --filter .txt .psd dir_a dir_b


Exit code:
 0  : directories or files are the same
 1  : directories or files are different
 255: an error/exception occured

"""


def _main():
    parser = argparse.ArgumentParser(description='An utility for comparing directories/files', usage=_HELP)

    parser.add_argument('left'
                        , type=str
                        , help="specify left dir/file")

    parser.add_argument('right'
                        , type=str
                        , help="specify right dir/file")

    parser.add_argument('-r', '--recursive'
                        , action="store_true"
                        , help="search file recursively")

    parser.add_argument('-q', '--quiet'
                        , action="store_true"
                        , help="be quiet")

    parser.add_argument('-f', '--filter'
                        , type=str
                        , nargs='+'
                        , help="file filters separated by space. Ex: -f .psd .txt ...")


    ## parse argv
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    ## setup log
    log_level = os.getenv("treediff.log.level", "info")
    setup_log(log_level)

    if log_level == "debug":
        logger.info("Log level: debug")
        

    if os.path.isfile(args.left) and os.path.isfile(args.right):
        if Util.compare_files(args.left, args.right):
            if not args.quiet:
                print("")
                logger.info("2 files are identical at binary level")
                print("")
            sys.exit(0)
        else:
            if not args.quiet:
                print("")
                logger.info("2 files are not identical at binary level")
                print("")
            sys.exit(1)

    elif os.path.isdir(args.left) and os.path.isdir(args.right):
        root = DiffNode(None, args.left, args.right)
        root.do_folder_matching(filter=args.filter, recursive=args.recursive)

        if not args.quiet:
            max_len, max_depth = root.get_max_child_name_length_and_max_depth()
            root.pprint(max_len, max_depth)
        else:
            if root.is_different():
                sys.exit(1)
            else:
                sys.exit(0)
    else:
        raise RuntimeWarning("Invalid parameters")

def main():
    try:
        _main()
        sys.exit(0)
    except Exception as e:
        if logging.root.level == logging.DEBUG:
            logger.exception(e)
        else:
            logger.error(e)
        sys.exit(255)


if __name__ == '__main__':
    main()

## EOF
