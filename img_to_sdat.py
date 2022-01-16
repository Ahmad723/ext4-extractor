#!/usr/bin/env python
# -*- coding: utf-8 -*-
#====================================================
#          FILE: img_to_sdat.py
#       AUTHORS: Ahmad
#          DATE: 2021-06-23 12:19:12 CEST
#====================================================

from __future__ import print_function

import sys, os, errno, tempfile
import common, blockimgdiff, sparse_img

def main(INPUT_IMAGE, OUTDIR='.', VERSION=None, PREFIX='system'):
    global input

    __version__ = '1.0'

    if sys.hexversion < 0x02070000:
        print >> sys.stderr, "Python 2.7 or newer is required."
        try:
            input = raw_input
        except NameError: pass
        input('Press ENTER to exit...')
        sys.exit(1)
    else:
        print('img_to_sdat.py binary - version: %s\n' % __version__)
        
    if not os.path.isdir(OUTDIR):
        os.makedirs(OUTDIR)

    OUTDIR = OUTDIR + '/'+ PREFIX

    if not VERSION:
        VERSION = 4
        while True:
            print('''            1. Android 5.0 Lollipop
            2. Android 5.1 Lollipop
            3. Android 6.0/6.0.1 Marshmallow
            4. Android 7.0/7.1/8.0/8.1 Nougat/Oreo
            ''')
            try:
                input = raw_input
            except NameError: pass
            item = input('Choose system version: ')
            if item == '1':
                VERSION = 1
                break
            elif item == '2':
                VERSION = 2
                break
            elif item == '3':
                VERSION = 3
                break
            elif item == '4':
                VERSION = 4
                break
            else:
                return

    # Get sparse image
    image = sparse_img.SparseImage(INPUT_IMAGE, tempfile.mkstemp()[1], '0')

    # Generate output files
    b = blockimgdiff.BlockImageDiff(image, None, VERSION)
    b.Compute(OUTDIR)

    print('Done! Output files: %s' % os.path.dirname(OUTDIR))
    return

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Please visit google for more information..')
    parser.add_argument('image', help='input system image')
    parser.add_argument('-o', '--outdir', help='output directory (current directory by default)')
    parser.add_argument('-v', '--version', help='transfer list version number, will be asked by default - more info on xda thread)')
    parser.add_argument('-p', '--prefix', help='name of image (prefix.new.dat)')

    args = parser.parse_args()

    INPUT_IMAGE = args.image
    
    if args.outdir:
        OUTDIR = args.outdir
    else:
        OUTDIR = '.'

    if args.version:
        VERSION = int(args.version)
    else:
        VERSION = None
    
    if args.prefix:
        PREFIX = args.prefix
    else:
        PREFIX = 'system'
    
    main(INPUT_IMAGE, OUTDIR, VERSION, PREFIX)
