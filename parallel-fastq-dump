#!/usr/bin/env python3
import sys
import os
import shutil
import tempfile
import subprocess
import argparse
import logging

__version__ = '0.6.7'

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)
class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.RawDescriptionHelpFormatter):
    pass

desc = 'parallel fastq-dump wrapper, extra args will be passed through'
epi = """DESCRIPTION:
Example: parallel-fastq-dump --sra-id SRR2244401 --threads 4 --outdir out/ --split-files --gzip
"""

parser = argparse.ArgumentParser(description=desc, epilog=epi,
                                 formatter_class=CustomFormatter)
argparse.ArgumentDefaultsHelpFormatter
parser.add_argument('-s','--sra-id', help='SRA id', action='append')
parser.add_argument('-t','--threads', help='number of threads', default=1, type=int)
parser.add_argument('-O','--outdir', help='output directory', default='.')
parser.add_argument('-T', '--tmpdir', help='temporary directory', default=None)
parser.add_argument('-N','--minSpotId', help='Minimum spot id', default=1, type=int)
parser.add_argument('-X','--maxSpotId', help='Maximum spot id', default=None, type=int)
parser.add_argument('-V', '--version', help='shows version', action='store_true', default=False)


def pfd(args, srr_id, extra_args):
    """
    Parallel fastq dump
    Parameters
    ----------
    args : dict
        User-provided args
    srr_id : str
        SRR ID
    extra_args : dict
        Extra args
    """
    tmp_dir = tempfile.TemporaryDirectory(prefix='pfd_',dir=args.tmpdir)
    logging.info('tempdir: {}'.format(tmp_dir.name))

    n_spots = get_spot_count(srr_id)
    logging.info('{} spots: {}'.format(srr_id,n_spots))

    # minSpotId cant be lower than 1
    start = max(args.minSpotId, 1)
    # maxSpotId cant be higher than n_spots
    end = min(args.maxSpotId, n_spots) if args.maxSpotId is not None else n_spots

    blocks = split_blocks(start, end, args.threads)
    logging.info('blocks: {}'.format(blocks))
    
    ps = []
    for i in range(0,args.threads):
        d = os.path.join(tmp_dir.name, str(i))
        os.mkdir(d)
        cmd = ['fastq-dump', '-N', str(blocks[i][0]), '-X', str(blocks[i][1]),
               '-O', d] + extra_args + [srr_id]
        logging.info('CMD: {}'.format(' '.join(cmd)))
        p = subprocess.Popen(cmd)
        ps.append(p)

    wfd = {}
    for i in range(0,args.threads):
        exit_code = ps[i].wait()
        if exit_code != 0:
            logging.warning('fastq-dump error! exit code: {}'.format(exit_code))
            sys.exit(1)

        tmp_path = os.path.join(tmp_dir.name, str(i))
        for fo in os.listdir(tmp_path):
            if fo not in wfd:
                wfd[fo] = open(os.path.join(args.outdir,fo), 'wb')
            with open(os.path.join(tmp_path,fo), 'rb') as fd:
                shutil.copyfileobj(fd, wfd[fo])
            os.remove(os.path.join(tmp_path,fo))
    
    # close the file descriptors for good measure
    for fd in wfd.values():
        fd.close()

def split_blocks(start, end, n_pieces):
    total = (end-start+1)
    avg = int(total / n_pieces)
    out = []
    last = start
    for i in range(0,n_pieces):
        out.append([last,last + avg-1])
        last += avg
        if i == n_pieces-1: out[i][1] += total % n_pieces
    return out

def get_spot_count(sra_id):
    """
    Get spot count via sra-stat
    Parameters
    ----------
    sra_id : str
        SRA ID
    """
    cmd = ['sra-stat', '--meta', '--quick', sra_id]
    logging.info('CMD: {}'.format(' '.join(cmd)))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()    
    txt = stdout.decode().rstrip().split('\n')
    total = 0
    try:
        for l in txt:
            total += int(l.split('|')[2].split(':')[0])
    except IndexError:
        msg = 'sra-stat output parsing error!'
        msg += '\n--sra-stat STDOUT--\n{}'
        msg += '\n--sra-stat STDERR--\n{}'
        etxt = stderr.decode().rstrip().split('\n')
        raise IndexError(msg.format('\n'.join(txt), '\n'.join(etxt)))
    return total

def partition(f, l):
    r = ([],[])
    for i in l:
        if f(i):
            r[0].append(i)
        else:
            r[1].append(i)
    return r

def is_sra_file(path):
    """
    Determine whether path is SRA file
    parameters
    ----------
    path : str
        file path
    """
    f = os.path.basename(path)
    if f.lower().endswith('.sra'): return True
    if 'SRR' in f.upper(): return True
    if 'ERR' in f.upper(): return True
    if 'DRR' in f.upper(): return True
    return False

def main():
    """
    Main interface
    """
    args, extra = parser.parse_known_args()
    if args.version:
        print('parallel-fastq-dump : {}'.format(__version__))
        subprocess.Popen(['fastq-dump', '-V']).wait()
        sys.exit(0)

    elif args.sra_id:
        extra_srrs, extra_args = partition(is_sra_file,extra)        
        args.sra_id.extend(extra_srrs)
        logging.info('SRR ids: {}'.format(args.sra_id))
        logging.info('extra args: {}'.format(extra_args))

        # output directory
        if not os.path.isdir(args.outdir) and args.outdir != '.':
            os.makedirs(args.outdir)
        # temp directory
        if (args.tmpdir is not None and
            not os.path.isdir(args.tmpdir)
            and args.tmpdir != '.'):
            os.makedirs(args.tmpdir)
        # fastq dump
        for si in args.sra_id:
            pfd(args, si, extra_args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()

