# Dependency: vgio
# Install with: 'pip install vgio'
#
# Consolidate a Quake gamedir with loose files and PAKs into a single PAK file.
#
# Command-line usage: python -m consolidate_quake_gamedir [--quiet | --verbose] gamedir
# Outputs: gamedir_consolidated/pak0.pak
#
# Or from a script:
# from consolidate_quake_gamedir import consolidate, PrintOut
# consolidate('gamedir', PrintOut.INFO)

import os
import sys
import shutil

from vgio.quake import pak

from enum import Enum
class PrintOut(Enum):
    NONE = 1
    INFO = 2
    VERBOSE = 3

def copy2_verbose(src, dst, dst_root, printout):
    if printout:
        fwdslash_src = src.replace('\\', '/')   # only for consistency of the output
        print(f'  Copying {fwdslash_src} to {dst_root}')
    shutil.copy2(src, dst)

def unpak(pak_filename, unpak_dir, printout=False):
    with pak.PakFile(pak_filename, 'r') as pak_file:
        for item in pak_file.infolist():
            if printout: print(f'  Extracting {item.filename} from {pak_filename} to {unpak_dir}')
            pak_file.extract(item.filename, unpak_dir)

def repak(pak_filename, pak_dir, printout=False):
    with pak.PakFile(pak_filename, 'w') as pak_file:
        old_cwd = os.getcwd()
        os.chdir(pak_dir)
        cwd = os.getcwd()
        for root, dirs, files in os.walk(cwd):
            for name in files:
                fullpath = os.path.join(root, name)
                relpath = os.path.relpath(fullpath, cwd).replace('\\', '/')
                if printout: print(f'  Adding {pak_dir}/{relpath} to {pak_filename}')
                pak_file.write(relpath)
        os.chdir(old_cwd)

def consolidate(gamedir, printout=PrintOut.INFO):
    gamedir_temp = gamedir + '_temp'
    gamedir_consolidated = gamedir + '_consolidated'

    # Clean up any old files and folders first
    shutil.rmtree(gamedir_temp, True)
    shutil.rmtree(gamedir_consolidated, True)
    os.makedirs(gamedir_temp)
    os.makedirs(gamedir_consolidated)

    # Determine if we are to print any output and if it is verbose
    printoutVerbose = printout is PrintOut.VERBOSE
    printout = not printout is PrintOut.NONE

    for pak_filename in sorted([f for f in os.listdir(gamedir) if f.endswith('.pak')]):
        pak_relpath = gamedir + '/' + pak_filename
        if printout: print(f'Unpaking {pak_relpath} to {gamedir_temp}')
        unpak(pak_relpath, gamedir_temp, printoutVerbose)

    if printout:print(f'Copying free files from {gamedir} to {gamedir_temp}')
    shutil.copytree(gamedir, gamedir_temp,
        ignore=shutil.ignore_patterns('*.pak'),
        copy_function=lambda src, dst: copy2_verbose(src, dst, gamedir_temp, printoutVerbose),
        dirs_exist_ok=True)

    repak_relpath = gamedir_consolidated + '/pak0.pak'
    if printout: print(f'Repaking {gamedir_temp} to {repak_relpath}')
    repak(repak_relpath, gamedir_temp, printoutVerbose)

    if printout: print(f'Cleaning up temporary files from {gamedir_temp}')
    shutil.rmtree(gamedir_temp, True)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('gamedir', help='the gamedir to consolidate')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet', action='store_true', help='do not print any output')
    group.add_argument('-v', '--verbose', action='store_true', help='print verbose output')
    args = parser.parse_args()

    printout = PrintOut.INFO
    if args.quiet:
        printout = PrintOut.NONE
    if args.verbose:
        printout = PrintOut.VERBOSE

    consolidate(args.gamedir, printout)
