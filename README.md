# fileshare_scanner
Scans fileshare for interesting strings in TXT, PDF, and DOCX files.

## Dependencies
* This script requires the python-docx module. If you have installed the python-docx module (using apt or whatever), remove the sys.path.append("/home/sysuser/projects/tools/python-docx-master/") line. If not, grab the source for this module and change this line to point to wherever you have put this code.
* Requires the python-pdfminer package.


## Create a Dictionary File
The dictionary file contains a one-per-line list of regular expressions compliant strings that will be used to scan each line of text pulled from the structure of the files.

Note:
* There is no error checking done on the regular expressions defined in the file, if you define something that isn’t valid the script will probably throw all sorts of errors.
* The script enables the ignorecase setting, so you do not have to take case into account.
* The script will display up 10 characters to each side of the matched string (depending start / end of line barriers).

##	Mount the Target Filesystem
It is unlikely the filesystem to be scanned is local (unless you have python installed on the fileserver and you’re running it there, which I’d advise against), so it will have to be mounted.

Requires the `cifs-util` package

`$ sudo apt-get install cifs-utils`

Make a directory, then, as root, mount the fileshare (in this case /tmp/fileserver01).

This will require a valid account on the system, so replace the <USERNAME> string in the below code block with a valid account username. When the mount command is executed, it will prompt for the password of this account used.

`$ mkdir -p /tmp/fileserver01
$ sudo mount -t cifs //fileserver01.fqdn.co.nz/public /tmp/ fileserver01/ -o username=<USERNAME>`
