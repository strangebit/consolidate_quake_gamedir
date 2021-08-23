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

def copy2_verbose(src, dst, dst_root, printout=False):
    if printout: print(f'  Copying {src} to {dst_root}')
    shutil.copy2(src, dst)

def unpak(pak_filename, unpak_dir, printout=False):
    with pak.PakFile(pak_filename, 'r') as pak_file:
        for item in pak_file.infolist():
            if printout: print(f'  Extracting {item.filename} from {pak_filename} to {unpak_dir}')
            pak_file.extract(item.filename, unpak_dir)

def repak(pak_filename, pak_dir, printout=False):
    with pak.PakFile(pak_filename, 'w') as pak_file:
        previous_cwd = os.getcwd()

        os.chdir(pak_dir)
        current_dir = os.getcwd()
        if os.path.isdir(current_dir):
            for root, dirs, files in os.walk(current_dir):
                for name in files:
                    fullpath = os.path.join(root, name)
                    relpath = os.path.relpath(fullpath, current_dir)
                    relpath = relpath.replace('\\', '/')
                    if printout: print(f'  Adding {relpath} to {pak_filename}')
                    pak_file.write(relpath)
        os.chdir(previous_cwd)

def consolidate(game_dir, printout=PrintOut.INFO):
    temp_game_dir = game_dir + '_temp'
    consolidated_game_dir = game_dir + '_consolidated'

    # Do we print any output or not
    printoutVerbose = printout is PrintOut.VERBOSE
    printout = not printout is PrintOut.NONE

    # Clean any old files first
    shutil.rmtree(temp_game_dir, True)
    shutil.rmtree(consolidated_game_dir, True)
    os.makedirs(temp_game_dir)
    os.makedirs(consolidated_game_dir)

    for pak_filename in sorted([f for f in os.listdir(game_dir) if f.endswith('.pak')]):
        pak_relpath = game_dir + '/' + pak_filename
        if printout: print(f'Unpaking {pak_relpath} to {temp_game_dir}')
        unpak(pak_relpath, temp_game_dir, printoutVerbose)

    if printout:print(f'Copying free files from {game_dir} to {temp_game_dir}')
    shutil.copytree(game_dir, temp_game_dir,
        ignore=shutil.ignore_patterns('*.pak'),
        copy_function=lambda src, dst: copy2_verbose(src, dst, temp_game_dir, printoutVerbose),
        dirs_exist_ok=True)

    repak_relpath = consolidated_game_dir + '/pak0.pak'
    if printout: print(f'Repaking {temp_game_dir} to {repak_relpath}')
    repak(repak_relpath, temp_game_dir, printoutVerbose)

    if printout: print(f'Cleaning up temporary files from {temp_game_dir}')
    shutil.rmtree(temp_game_dir, True)

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
