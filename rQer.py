#!/usr/bin/env python

#Copyright 2013 Mitchell Jon Stanton-Cook Licensed under the
#Educational Community License, Version 2.0 (the "License"); you may
#not use this file except in compliance with the License. You may
#obtain a copy of the License at
#
##http://www.osedu.org/licenses/ECL-2.0
#
##Unless required by applicable law or agreed to in writing,
#software distributed under the License is distributed on an "AS IS"
#BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#or implied. See the License for the specific language governing 
#permissions and limitations under the License. 

"""
Ensure uncalled bases ('N') have a quality score of 2
"""

import gzip
import os
import sys
import traceback
import argparse
import time
import __init__ as meta

epi     = "Licence: %s by %s <%s>" % (meta.__licence__, meta.__author__, 
                                      meta.__author_email__)
prog    = meta.__name__.replace(' ', '_')
__doc__ = " %s v%s - %s" % (prog, meta.__version__, meta.__description__)


def reset_quality(args):
    full_file_path = args.input
    full_out_path  = args.output
    enc = args.qual_enc
    enc = int(enc)
    nQ = ''
    if enc == 33:
        nQ = '#'
        print "Using Q33"
    elif enc == 64:
        nQ = 'B'
        print "Using Q64"
    else:
        print "Only support 33 or 64 PHRED encoded"
        sys.exit(1)
    full_file_path = os.path.expanduser(full_file_path)
    if full_file_path.endswith('.gz'):
        f    = gzip.open(full_file_path, 'r')
        fout = gzip.open(full_out_path, 'w')
        was_gzipped = True
    elif full_file_path.endswith('.fastq'):
        f = open(full_file_path, 'r')
        fout = open(full_out_path, 'w')
    else:
        print "Not supported"
        sys.exit(1)
    num_lines = sum(1 for line in f)
    f.seek(0)
    i = 0
    while i < num_lines:
        header = f.readline()
        seq    = list(f.readline())
        misc   = f.readline()
        qual   = list(f.readline())
        # Find all N chars
        pos =  [n for (n, q) in enumerate(seq) if q == 'N']
        #Update to '2'
        for p in pos:
            qual[p] = nQ
        fout.write(header)
        fout.write(''.join(seq))
        fout.write(misc)
        fout.write(''.join(qual))
        i = i+4
    print "Done - processed a total of %i reads" % (i/4)


if __name__ == '__main__':
    try:
        start_time = time.time()
        desc = __doc__.strip()
        parser = argparse.ArgumentParser(description=desc,epilog=epi)
        parser.add_argument('-v', '--verbose', action='store_true',
                                default=False, help='verbose output')
        parser.add_argument('--version', action='version',
                                version='%(prog)s ' + meta.__version__)
        parser.add_argument('-q', '--qual_enc', action='store',
                                default=33, help='Quality encoding (33 | 64)')
        parser.add_argument('input', action='store',
                                type=str, help='Full path to the input file')
        parser.add_argument('output', action='store', type=str,
                                help='Full path to the output file')
        parser.set_defaults(func=reset_quality)
        args = parser.parse_args()
        args.func(args)
        if args.verbose: print "Executing @ " + time.asctime()
        if args.verbose: print "Ended @ " + time.asctime()
        if args.verbose: print 'total time in minutes:',
        if args.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
