# Secure File Shredder Tool

**Version:** 1.0  
**Author:** Steve Mathot  
**Company:** mCoDev Systems  
**Website:** [https://www.mcodev.net](https://www.mcodev.net)

A Python-based utility for securely deleting files and directories by overwriting their contents before removal. Designed for forensic-grade data destruction with options and progress feedback.

---

## 🛠 Features

- Secure multi-pass overwrite using random data
- Optional file renaming before deletion for added obfuscation
- Recursive directory shredding with extension filtering (1)
- Wildcard support including `**/*.ext` for deep matching (2)
- Simulation mode (`--dry-run`) for safe testing
- Silent mode (`--silent`) to skip confirmation prompts
- Verbose output for detailed file processing
- Color-coded terminal output using `colorama`
- Chunk size and pass count customization

---

## 🚀 Usage

python fileshred.py <file_path or wildcard> [options]

### Options

| Option             | Description                                                                         |
|--------------------|-------------------------------------------------------------------------------------|
| `-s`, `--silent`   | Skip confirmation prompt                                                            |
| `--dry-run`        | Simulate deletion without modifying files                                           |
| `--no-delete`      | Overwrite file contents but do not remove from filesystem                           |
| `--chunk-size N`   | Set chunk size in bytes (default: 4096)                                             |
| `-p`, `--passes N` | Number of overwrite passes (default: 3)                                             |
| `-r`, `--recursive`| Enable recursive shredding and support for `**` wildcards   (1)                     |
| `--ext .EXT`       | Filter files by extension when shredding directories (e.g., `.log`)  (2)            |
| `--verbose`        | Show detailed output during execution                                               |
| `--pattern`        | The overwrite pattern to use. (zeros, ones, alternating, random). (default: random) |
| `-h`, `--help`     | Show help message                                                                   |
| `--version`        | Display version and author info                                                     |
| `--man`            | Show manual page                                                                    |

---

## 📂 Examples

python fileshred.py \*.log  
python fileshred.py secret_\*.txt --dry-run  
python fileshred.py \*.txt -s -p 5  
python fileshred.py logs/ -r --ext .log --verbose  
python fileshred.py "\*\*/\*.log" -r  
python fileshred.py "logs/\*\*/\*.txt" -r --ext .txt  
python fileshred.py "\*.tmp"

---

## ⚠️ Disclaimer

This tool performs irreversible data destruction. Use with caution. The author and company are not responsible for any data loss or misuse.

---

## 📦 Requirements

- Python 3.6+
- Colorama library

Install dependencies: `pip install colorama`

---

## ℹ️ Known Issues

- (1) The recursive directory walker (options -r and --recursive) is not really functioning correctly. It will only process files in the target directory, but won't go further down into other directories. I really can't be bothered at the moment to fix this.  Maybe in a future update.   Recursive directories was not in the scope of the development requirements for this script.
- (2) The --ext option remains untested, use at your own risk.

---

## 🧠 Notes

- Overwriting files on SSDs may not guarantee complete data removal due to wear-leveling.
- For maximum security, consider combining this tool with full-disk encryption and secure erase utilities.

---

## ℹ️ Installation
- Git clone the folder somewhere on your system, or download the zip and unzip somwhere.
  
- For Windows (Using PowerShell):
  - Make sure you have all the requirements installed:
    - Install Python3 from the Microsoft App Store
    - Run the command `pip install colorama` for the Colorama dependency
  - Modify the ps1 file (`C:\Users\\\<Username\>\\[OneDrive\\]Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`)
    - (Create the file if it doesn't exist)
    - Add the following function to the bottom of the file:
```
        function shred {
          python "X:\path\to\fileshred.py" @args
        }
```
- For Linux (Using Bash):  (I'm using Debian based system, other distribution may differ on how to install python3 and colorama)
  - Run the following commands to install the requirements (as root):
    - `apt install python3-full python3-colorama -y`
    - Check the location of python3 with the command 'which python3' and take note of it. For example `/usr/bin/python3`
  - Modify your .bashrc  (command: `nano ~/.bashrc`) and add the following function to the bottom of the file:
```
    shred() {
      /path/to/python3 /path/to/fileshred.py "$@"
    }

```
- Now you can use the command `shred <Filepath> [options]` from anywhere on the system to call for the script. (In PowerShell or Bash terminal)
- One additional note for PowerShell users on Windows:
  - If the ps1 script is blocked and you can't use the shred command, open a PowerShell session with elevated permissions and execute the command below to allow script execution:
```
  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 👁️ License

This project is released under the MIT License.
