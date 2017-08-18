# dmtcp-log-parser

This program implements a simple parser for DMTCP Jalib log format.

## Example usage:
    # The following command will filter out warning messages from processinfo.cpp for pids: 40000 and 41000 
    $ ./parse_dmtcp_logs.py -l dmtcp_error.log -p 40000 41000 -n processinfo dmtcpworker -m WARNING
    # Use -h to display help
    $ ./parse_dmtcp_logs.py -h
    usage: ./parse_dmtcp_logs.py [-h] -l LOG_FILENAME
                             [-p FILTER_PIDS [FILTER_PIDS ...]]
                             [-n FILTER_FILENAMES [FILTER_FILENAMES ...]]
                             [-f FILTER_FUNCTIONS [FILTER_FUNCTIONS ...]]
                             [-m {ALL,WARNING,TRACE,NOTE,ERROR} [{ALL,WARNING,TRACE,NOTE,ERROR} ...]]

    This program implements a parser for DMTCP Jalib log format

    optional arguments:
      -h, --help            show this help message and exit
      -l LOG_FILENAME, --log-filename LOG_FILENAME
                            DMTCP log file
      -p FILTER_PIDS [FILTER_PIDS ...], --filter-pids FILTER_PIDS [FILTER_PIDS ...]
                            List of process ids to filter
      -n FILTER_FILENAMES [FILTER_FILENAMES ...], --filter-filenames FILTER_FILENAMES [FILTER_FILENAMES ...]
                            List of filenames (without extension) to filter
      -f FILTER_FUNCTIONS [FILTER_FUNCTIONS ...], --filter-functions FILTER_FUNCTIONS [FILTER_FUNCTIONS ...]
                            List of function names to filter
      -m {ALL,WARNING,TRACE,NOTE,ERROR} [{ALL,WARNING,TRACE,NOTE,ERROR} ...], --filter-logtypes {ALL,WARNING,TRACE,NOTE,ERROR} [{ALL,WARNING,TRACE,NOTE,ERROR} ...]
                            List of log message types to filter
