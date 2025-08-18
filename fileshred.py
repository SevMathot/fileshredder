######
## Secure File Shredder Tool:    Tool to securely delete files from a file system by overwriting with noise before deletion.
##     Author: Steve Mathot      (linktr.ee/sevmato)
##     Company: mCoDev Systems   (www.mcodev.net)
##     License: MIT
##     Last Edit: 18AUG2025
##
##     Dependencies:    Colorama
#######


import os
import sys
import glob
import random
import string
import sys
import sys
from pathlib import Path

from colorama import init, Fore, Style # type: ignore # pip install colorama
init(autoreset=True)



NAME = "Secure File Shredder Tool"
AUTHOR = "Steve Mathot"
COMPANY = "mCoDev Systems"
WEBSITE = "https://www.mcodev.net"
VERSION = "1.0"

CHUNK_SIZE = 4096           # The block size of data in bytes to scramble while shredding.
SCRIPTFILE = os.path.basename(__file__)

HELP_TEXT = f"""Secure File Shredder Tool, Version {VERSION}
Usage: python {SCRIPTFILE} <target> [options]
Use --man for full documentation.
"""

MANUAL_TEXT = f"""SECURE FILE SHREDDER          {COMPANY} Manual           SECURE FILE SHREDDER

NAME
    {NAME} - forensic-grade file and directory shredder for secure deletion

VERSION
    {VERSION}

SYNOPSIS
    python {SCRIPTFILE} <target> [options]

DESCRIPTION
    Secure Shred is a Python utility designed to permanently destroy files and
    directories by overwriting their contents with random data before deletion.
    It supports recursive shredding, extension filtering, wildcard matching,
    and simulation mode for safe testing.

OPTIONS
    -s, --silent
        Skip confirmation prompt before shredding begins.

    --dry-run
        Simulate shredding without modifying or deleting any files.

    --no-delete
        Overwrite file contents but retain the file on disk.

    --chunk-size N
        Set the chunk size in bytes for overwrite operations (default: 4096).

    -p, --passes N
        Number of overwrite passes per file (default: 3).
    
    --pattern
        The overwrite pattern to use. (zeros, ones, alternating, random). (default: random)

    -r, --recursive
        Enable recursive shredding of directories. Supports '**' wildcards.

    --ext .EXT
        Filter files by extension when shredding directories (e.g., .log, .tmp).

    --verbose
        Display detailed output for each file processed.

    -h, --help
        Show brief help message.

    --version
        Display version, author, and company information.

    --man
        Display this manual page.

EXAMPLES
    python {SCRIPTFILE} *.log
        Shred all .log files in the current directory.

    python {SCRIPTFILE} secret_*.txt --dry-run
        Simulate shredding of matching .txt files.

    python {SCRIPTFILE} logs/ -r --ext .log --verbose
        Recursively shred all .log files in the logs directory.

    python {SCRIPTFILE} "**/*.tmp" -r -s -p 5
        Deep shred all .tmp files with 5 overwrite passes, silently.

NOTES
    - SSDs may not guarantee complete data removal due to wear-leveling.
    - Use --dry-run to preview actions before committing to deletion.
    - Combine with full-disk encryption for maximum data security.

AUTHOR
    {AUTHOR} ({COMPANY})  
    {WEBSITE}

COPYRIGHT
    Copyright ©2025, {COMPANY}. All rights reserved.
    MIT License. Use at your own risk. The author is not liable for data loss.
"""



##########################################################################################################

def secure_delete(file_path, passes=3, dry_run=False, no_delete=False, chunk_size=4096, pattern="random", verbose=False):
    from pathlib import Path

    file = Path(file_path)
    if not file.is_file():
        print(f"File not found: {file}")
        return

    file_size = file.stat().st_size
    filename = os.path.basename(file_path)

    try:
        # get current position:
        print("", end="")
        for pass_num in range(passes):
            if not dry_run:
                with open(file_path, "r+b") as f:
                    for offset in range(0, file_size, chunk_size):
                        f.seek(offset)
                        chunk = get_pattern_bytes(pattern, min(chunk_size, file_size - offset), pass_num)
                        f.write(chunk)

                        # Calculate and print remaining percentage
                        percent_complete = (offset / file_size) * 100
                        print(f"\rOverwriting...  Pass {pass_num + 1}/{passes} {percent_complete:.2f}%  ", end="")
            else:
                for offset in range(0, file_size, chunk_size):
                    # Simulate progress
                    percent_complete = (offset / file_size) * 100
                    print(f"\r(Dry-Run) Overwriting...  Pass {pass_num + 1}/{passes} {percent_complete:.2f}%  ", end="")
             
        print("\r                                                                                ") # end line

        # clear operations:
        sys.stdout.write("\033[A")
        sys.stdout.write("\033[A")
        if verbose:
            sys.stdout.write("\033[A")
        print(Fore.LIGHTGREEN_EX + f"✅ Securely destroyed: {file_path}                ")
        print("")
        print("")
        sys.stdout.write("\033[A")
        sys.stdout.write("\033[A")

        if not dry_run and not no_delete:
            random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            temp_path = file.with_name(random_name)
            file.rename(temp_path)
            os.remove(temp_path)
            if verbose:
                print(Fore.LIGHTBLACK_EX + f"📝 Securely deleted: {file_path}")
        else:
            if verbose:
                if dry_run:
                    print(Fore.LIGHTBLACK_EX + f"📝 Securely deleted:'{file_path}' (Dry-run: the file was not modified or actually deleted!).")
                else:
                    #no_delete
                    print(Fore.LIGHTBLACK_EX + f"📝 NO_DELETE:'{file_path}' The file is destroyed, but was not deleted.")

    except Exception as e:
        print(f"Error: {e}")

##########################################################################################################



def get_pattern_bytes(pattern: str, size: int, pass_num: int = 0) -> bytes:
    if pattern == "zeros":
        return b"\x00" * size
    elif pattern == "ones":
        return b"\xFF" * size
    elif pattern == "alternating":
        return bytes([0xAA if (pass_num % 2 == 0) else 0x55] * size)
    else:  # default to random
        return os.urandom(size)


##########################################################################################################

def print_help():
    print(HELP_TEXT)

def print_manual():
    print(MANUAL_TEXT)

##########################################################################################################

def confirm_deletion(matched_files, dry_run):
    print(Fore.YELLOW + f"The following files will be securely deleted{Fore.WHITE+' (Simulated)'+Fore.YELLOW if dry_run else ''}:")
    for f in matched_files:
        print(f"  - {f}")

    response = input(Fore.LIGHTRED_EX + "\n⚠️ DANGER ZONE ⚠️    " + Fore.LIGHTYELLOW_EX + "Type 'yes' to confirm deletion: > " + Fore.LIGHTRED_EX)
    return response.strip().lower() == "yes"



##########################################################################################################






##########################################################################################################

def main():
    args = sys.argv[1:]

    print(Fore.GREEN + r"""
  _________                                    ___________.__.__             _________.__                      .___
 /   _____/ ____   ____  __ _________   ____   \_   _____/|__|  |   ____    /   _____/|  |_________   ____   __| _/
 \_____  \_/ __ \_/ ___\|  |  \_  __ \_/ __ \   |    __)  |  |  | _/ __ \   \_____  \ |  |  \_  __ \_/ __ \ / __ | 
 /        \  ___/\  \___|  |  /|  | \/\  ___/   |     \   |  |  |_\  ___/   /        \|   Y  \  | \/\  ___// /_/ | 
/_______  /\___  >\___  >____/ |__|    \___  >  \___  /   |__|____/\___  > /_______  /|___|  /__|    \___  >____ | 
        \/     \/     \/                   \/       \/                 \/          \/      \/            \/     \/     """)

    print(Fore.CYAN + f"🔧 {NAME} — Version {VERSION}")
    print(Fore.CYAN + f"👤 Author: {AUTHOR}, {COMPANY}")
    print(Fore.CYAN + "🌐 Website: " + "\033[4mhttps://www.mcodev.net\033[0m")
    print(Fore.CYAN + "🌐 GitHub:  " + "\033[4mhttps://github.com/SevMathot/fileshredder\033[0m\n")


    if not args:
        print_help()
        sys.exit(0)

    silent = False
    recursive = False
    dry_run = False
    no_delete = False
    passes = 3
    overwrite_pattern = "random"
    patterns = []
    global CHUNK_SIZE
    verbose = False
    ext_filter = None


    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ("-h", "--help", "--version"):
            print_help()
            sys.exit(0)
        elif arg == "--man":
            print_manual()
            sys.exit(0)
        elif arg in ("-s", "--silent"):
            silent = True
        elif arg == "--dry-run":
            dry_run = True
        elif arg == "--no-delete":
            no_delete = True
        elif arg in ("-r", "--recursive"):
            recursive = True
        elif arg == "--verbose":
            verbose = True
        elif arg == "--pattern":
            try:
                overwrite_pattern = args[i + 1].lower()
                if overwrite_pattern not in ("random", "zeros", "ones", "alternating"):
                    raise ValueError
                i += 1

                if overwrite_pattern != "random":
                    print(Fore.YELLOW + f"⚠️  Warning: Using predictable pattern '{overwrite_pattern}' may reduce shred security.")
            except (IndexError, ValueError):
                print(Fore.RED + "❌ Error: Invalid pattern. Choose from: random, zeros, ones, alternating.")
                sys.exit(1)
        elif arg == "--ext":
            try:
                ext_filter = args[i + 1].lower()
                i += 1
            except IndexError:
                print(Fore.RED + "❌ Error: You must specify an extension after --ext.")
                sys.exit(1)

        elif arg in ("-p", "--passes"):
            try:
                passes = int(args[i + 1])
                i += 1
            except (IndexError, ValueError):
                print(Fore.RED + "❌ Error: You must specify a valid number after --passes.")
                sys.exit(1)
        elif arg in ("--chunk-size"):
            try:
                CHUNK_SIZE = int(args[i + 1])
                i += 1
            except (IndexError, ValueError):
                print(Fore.RED + "❌ Error: You must specify a valid number after --chunk-size.")
                sys.exit(1)
        elif arg == "--version":
            print(f"{NAME} v{VERSION} by {AUTHOR}")
            sys.exit(0)
        else:
            patterns.append(arg)
        i += 1

    if not patterns:
        print(Fore.RED + "❌ Error: No file path or pattern provided.")
        sys.exit(1)

    matched_files = []
    for pattern in patterns:
        # If recursive flag is set, allow '**' patterns to match deeply
        if recursive:
            expanded = glob.glob(pattern, recursive=True)
        else:
            expanded = glob.glob(pattern)

        for path in expanded:
            if os.path.isdir(path):
                if not recursive:
                    print(Fore.RED + f"❌ Error: '{path}' is a directory. Use -r or --recursive to shred directories.")
                    sys.exit(1)
                else:
                    for root, _, files in os.walk(path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            if ext_filter and not file.lower().endswith(ext_filter):
                                if verbose:
                                    print(Fore.LIGHTBLACK_EX + f"📝 Skipping (extension mismatch): {full_path}")
                                continue
                            matched_files.append(full_path)
                            if verbose:
                                print(Fore.LIGHTBLACK_EX + f"📝 Matched: {full_path}")
            else:
                if ext_filter and not path.lower().endswith(ext_filter):
                    if verbose:
                        print(Fore.LIGHTBLACK_EX + f"📝 Skipping (extension mismatch): {path}")
                    continue
                matched_files.append(path)
                if verbose:
                    print(Fore.LIGHTBLACK_EX + f"📝 Matched: {path}")
            #end if
        #end for path
    #end for pattern

    if not matched_files:
        print(Fore.YELLOW + "⚠️ No matching files found.")
        sys.exit(1)


    
    # Confirmation prompt for recursive deletion
    if not silent:
        if not confirm_deletion(matched_files, dry_run):
            print(Fore.RED + "⚠️ Operation cancelled by user.")
            sys.exit(2)


    print("\n")

    total_size = sum(Path(f).stat().st_size for f in matched_files)
    print(f"Total data to shred: {total_size / (1024**2):.2f} MB")

    total_files = len(matched_files)

    for index, file_path in enumerate(matched_files, start=1):
        print(Fore.CYAN + f"📁 Now deleting file {index} of {total_files}: {file_path}")
        
        if verbose:
            print(Fore.LIGHTBLACK_EX + f"🔍 Processing file: {file_path}")
        
        secure_delete(
            file_path,
            passes=passes,
            dry_run=dry_run,
            no_delete=no_delete,
            chunk_size=CHUNK_SIZE,
            pattern=overwrite_pattern,
            verbose=verbose
        )

    print(f"\nSummary:")
    print(f"  Files processed: {len(matched_files)}")
    print(f"  Total data shredded: {total_size / (1024**2):.2f} MB")
    print(f"  Mode: {'Dry-run' if dry_run else 'Live'}")
    print(f"  Overwrite pattern: {overwrite_pattern}")




##########################################################################################################





















# Launch the program
if __name__ == "__main__":
    main()
    sys.exit(0)
