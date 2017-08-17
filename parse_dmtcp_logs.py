#!/usr/bin/python3.5

import json
import collections
import argparse as ap
from grako import parse
from grako.util import asjson

HELP='This program implements a parser for DMTCP Jalib log format\n\n'\

# Example test string:
#teststring = '[8686] TRACE at dmtcp_launch.cpp:473 in main; REASON=\'dmtcp_launch starting new program:\'\n' \
#             '     argv [0] = ./a.out\n' \
#             '[40000] TRACE at dmtcpworker.cpp:424 in waitForCoordinatorMsg; REASON=\'waiting for FD_LEADER_ELECTION message\'\n'

GRAMMAR = '''
    @@grammar :: DmtcpLogLanguage

    start =  { msg }+ $ ;
    
    msg =
         | '[' pid ']' msg_type 'at' fname fext ':' lnum 'in' fnc '; REASON=' reason { args }*
         | '[' pid ']' fname fext ':' lnum 'in' fnc '; REASON=' reason { args }*
         ;

    pid = /\d+/ ;

    msg_type =
        | 'TRACE'
        | 'WARNING'
        | 'NOTE'
        | 'ERROR'
        ;

    fname = /[a-zA-Z_]+/ ;

    fext =
        | '.cpp'
        | '.c'
        | '.h'
        ;

    lnum = /\d+/ ;

    fnc = /[_a-zA-Z][_a-zA-Z0-9]*/ ;

    reason = 
            | /\'.+\'$/ 
            | /.+$/ 
            ;

    args = 
           | arg_val_pair
           | connection_description
           | dashed_line
           ;

    dashed_line = '==================================================' ;

    connection_description = /.*->.*/ ;

    arg_val_pair = arg '=' value ;

    arg = /(?!\[\d+\])[^=]*/ ;

    value = /.*$/ ;

 '''

def flatten(lst):
  for i in lst:
    if isinstance(i, collections.Iterable) and not isinstance(i, (str, bytes)):
      yield from flatten(i)
    else:
      yield i

def main():

  parser = ap.ArgumentParser(prog='./parse_dmtcp_logs.py',
                             description=HELP,
                             formatter_class=ap.RawTextHelpFormatter)
  logtypes = set(("TRACE", "WARNING", "NOTE", "ERROR", "ALL"))

  parser.add_argument('-l', '--log-filename',
                      help='DMTCP log file', required=True)
  parser.add_argument('-p', '--filter-pids', nargs='+',
                      help='List of process ids to filter', required=False)
  parser.add_argument('-n', '--filter-filenames', nargs='+',
                      help='List of filenames (without extension) to filter',
                      required=False)
  parser.add_argument('-f', '--filter-functions', nargs='+',
                      help='List of function names to filter', required=False)
  parser.add_argument('-m', '--filter-logtypes', nargs='+', choices=logtypes,
                      help='List of function names to filter', required=False)
  parser.add_argument('-r', '--print-raw', action='store_true',
                      help='Print raw json (default: False)', required=False)
  args = parser.parse_args()

  lines = []
  with open(args.log_filename, 'r') as logfile:
    lines = logfile.readlines()
  ast = parse(GRAMMAR, "".join(lines), parseinfo=True)

  json_ast = asjson(ast)

  t = json_ast
  if args.filter_pids:
    t = [x for x in t if x[1] in args.filter_pids]
  if args.filter_logtypes and not("ALL" in args.filter_logtypes):
    t = [x for x in t if x[3] in args.filter_logtypes]
  if args.filter_filenames:
    t = [x for x in t if x[5] in args.filter_filenames]
  if args.filter_functions:
    t = [x for x in t if x[10] in args.filter_functions]

  print('Results:')
  if not args.print_raw:
    for i in t:
      print(" ".join(flatten(i)))
  else:
    print(json.dumps(t, indent=2))
  print()

if __name__ == '__main__':
  main()
