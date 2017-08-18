#!/usr/bin/python3.5

import json
import collections
import argparse as ap
from grako import parse
from grako.util import asjson
from dmtcp_log_parser import DmtcpLogLanguageParser
from dmtcp_log_semantics import DmtcpLogLanguageSemantics

HELP='This program implements a parser for DMTCP Jalib log format\n\n'\

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
  args = parser.parse_args()

  text = open(args.log_filename, 'r').read()
  semantics_obj = semantics=DmtcpLogLanguageSemantics()

  if args.filter_pids:
    semantics_obj.add_pid_filter(args.filter_pids)
  if args.filter_logtypes and not("ALL" in args.filter_logtypes):
    semantics_obj.add_logtype_filter(args.filter_logtypes)
  if args.filter_filenames:
    semantics_obj.add_filename_filter(args.filter_filenames)
  if args.filter_functions:
    semantics_obj.add_function_filter(args.filter_functions)

  parser = DmtcpLogLanguageParser(semantics=semantics_obj)
  ast = parser.parse(text)
  print('Results:')
  print(ast)

if __name__ == '__main__':
  main()
