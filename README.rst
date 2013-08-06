rQer 
====

Make reads output from CASAVA 1.8.2 with option --adapter-sequence sane.

It appears that for CASAVA 1.8.2 providing the --adapter-sequence
option results in the adapter being converted to 'N' while the existing 
quality is retained. This does not make sense. The existing quality should be 
converted to a 2 (PHRED 33 = '#', PHRED 64 = 'B').

RQer takes input reads, and for all N bases which qualities are not equal 
to '2' converts to '2'.


Usage
-----

Something like::

    python rQer.py -h
    
    usage: rQer.py [-h] [-v] [--version] [-q QUAL_ENC] input output

    rQer v0.1 - Ensure the uncalled bases ('N') have a quality score of 2

    positional arguments:
      input                             Full path to the input file
      output                            Full path to the output file

    optional arguments:
      -h, --help                        show this help message and exit
      -v, --verbose                     verbose output
      --version                         show program's version number and exit
      -q QUAL_ENC, --qual_enc QUAL_ENC  Quality encoding (33 | 64)

    Licence: ECL 2.0 by Mitchell Stanton-Cook <m.stantoncook@gmail.com>


Examples
--------

Input reads::

    @HWUSI-EAS1780:33:662Y6AAXX:8:1:13502:1071 1:N:0:GGACTCCT
    CGCNGGCGAGGCATCAATCTTTACGATCTGTATAAAGACGGATTGTTGANGATGTGTTAAAATTGATGTNNNNAAATTGTGAAGTAAATGTGCTTCCGGGGAAAATAAGTGACTTCATTAAAACTCTCAATCGTCCATCGACTGCCGCN
    +
    ABC#FFEEBHHDHBGHHGHHHGHFGB@GGGGGDFHH<HHGBEFGEAEE8#=9<=8==?=EHHHF?????####330143EFEBFBBDBDB@DCEEGAHEEC:BC-@###########################################
    @HWUSI-EAS1780:33:662Y6AAXX:8:1:11509:1073 1:N:0:GGACTCCT
    ATANCACGTTTGTCATTGTCGGTAATGTCGCAGAAGACAAACTCGTGGCNTTAATTACGCGTTACTTAGNANCAATCAAACACTCTGATTCGCCATTAGCCGCAGGTAAACCATTAACTCGCGCGACGGACAACGCATCGGTTACTGTN
    +
    @BA#FFFFFIIIIIIIIHIIIIHIHHHEIHIIIHHGIIIIIIIIGDGG@#??A?BB@@@FIEHG@BB??#1#35::8:;HEGGGFEEDHGEGFGEGGDEEEGEEDC>CEEE@BDECB@B?@@BBBA?BB3:==4?==3=B@/B>=6966


Standard (uncompressed Q33)::


    $ ./rQer.py test1.fastq test1_fixed.fastq
   
    Using Q33
    Done - processed a total of 2 reads

    $ diff  test1.fastq test1_fixed.fastq
    8c8
    < @BA#FFFFFIIIIIIIIHIIIIHIHHHEIHIIIHHGIIIIIIIIGDGG@#??A?BB@@@FIEHG@BB??#1#35::8:;HEGGGFEEDHGEGFGEGGDEEEGEEDC>CEEE@BDECB@B?@@BBBA?BB3:==4?==3=B@/B>=6966
    ---
    > @BA#FFFFFIIIIIIIIHIIIIHIHHHEIHIIIHHGIIIIIIIIGDGG@#??A?BB@@@FIEHG@BB??#1#35::8:;HEGGGFEEDHGEGFGEGGDEEEGEEDC>CEEE@BDECB@B?@@BBBA?BB3:==4?==3=B@/B>=696#

gzipped::


    $ ./rQer.py test2.fastq.gz test2_fixed.fastq.gz

    Using Q33
    Done - processed a total of 2 reads

    $ diff test2.fastq test2_fixed.fastq
    8c8
    < @BA#FFFFFIIIIIIIIHIIIIHIHHHEIHIIIHHGIIIIIIIIGDGG@#??A?BB@@@FIEHG@BB??#1#35::8:;HEGGGFEEDHGEGFGEGGDEEEGEEDC>CEEE@BDECB@B?@@BBBA?BB3:==4?==3=B@/B>=6966
    ---
    > @BA#FFFFFIIIIIIIIHIIIIHIHHHEIHIIIHHGIIIIIIIIGDGG@#??A?BB@@@FIEHG@BB??#1#35::8:;HEGGGFEEDHGEGFGEGGDEEEGEEDC>CEEE@BDECB@B?@@BBBA?BB3:==4?==3=B@/B>=696#

