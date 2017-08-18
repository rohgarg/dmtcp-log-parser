#!/usr/bin/python3.5

from __future__ import print_function
import sys
from dmtcp_log_parser import DmtcpLogLanguageParser

class DmtcpLogLanguageSemantics(object):
    def __init__(self):
      self.filters = []

    def apply_filter(self, f, ast):
      if ast.dmtcp_msg:
        return f(ast.dpid, ast.dmtype, ast.dfname, ast.dfnc)
      elif ast.mtcp_msg:
        return f(ast.mpid, ast.mmtype, ast.mfname, ast.mfnc)
      else:
        return False

    def add_pid_filter(self, pid_list):
      self.filters.append(lambda pid, mtype, fname, fnc: str(pid) in pid_list)

    def add_logtype_filter(self, log_list):
      self.filters.append(lambda pid, mtype, fname, fnc: mtype in log_list)

    def add_filename_filter(self, fname_list):
      self.filters.append(lambda pid, mtype, fname, fnc: fname in fname_list)

    def add_function_filter(self, fnc_list):
      self.filters.append(lambda pid, mtype, fname, fnc: fnc in fnc_list)

    def start(self, ast):
      outstr = ""
      for x in ast:
        outstr += x
      return outstr

    def msg(self, ast):
      outstr = ""

      for f in self.filters:
        if not self.apply_filter(f, ast):
          return outstr

      if ast.dmtcp_msg:
        outstr += "[%d]: %s at %s%s:%d in %s; REASON=%s\n" % (ast.dpid, ast.dmtype, ast.dfname, ast.dfext, ast.dlnum, ast.dfnc, ast.drea)
        for x in ast.dargs:
          outstr += x
      elif ast.mtcp_msg:
        outstr += "[%d]: MTCP %s%s:%d in %s; REASON=%s\n" % (ast.mpid, ast.mfname, ast.mfext, ast.mlnum, ast.mfnc, ast.mrea)
        for x in ast.margs:
          outstr += x
      else:
        raise Exception("Unknown log message")
      return outstr

    def pid(self, ast):
        return int(ast)

    def msg_type(self, ast):
        return ast

    def fname(self, ast):
        return ast

    def fext(self, ast):
        return ast

    def lnum(self, ast):
        return int(ast)

    def fnc(self, ast):
        return ast

    def reason(self, ast):
        return ast

    def args(self, ast):
        if ast.avp:
          return "    %s\n" % (ast.avp)
        elif ast.cd:
          return "    %s\n" % (ast.cd)
        elif ast.dl:
          return "    %s\n" % (ast.dl)
        else:
          print(ast)
          raise Exception("Unknown args expression")
        return ""

    def dashed_line(self, ast):
        return str(ast).strip()

    def connection_description(self, ast):
        return str(ast).strip()

    def arg_val_pair(self, ast):
        outstr = ""
        if ast.avpa:
          outstr += ast.avpa
          outstr += " = "
          if ast.avpv:
            outstr += ast.avpv
        else:
          print(ast)
          raise Exception("Unknown arg-val pair expression")
        return outstr

    def arg(self, ast):
        return str(ast).strip()

    def value(self, ast):
        return str(ast).strip()


def calc(text):
    parser = DmtcpLogLanguageParser(semantics=DmtcpLogLanguageSemantics())
    return parser.parse(text)

if __name__ == '__main__':
    text = open(sys.argv[1]).read()
    result = calc(text)
    print(result)
