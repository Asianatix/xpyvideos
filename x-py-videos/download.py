# Imports
import os
import sys
import urllib2
from regexes import regex_for_video_link
from filename import file_name


# Author and licensing
__Author__ = "Darth_O-Ring"
__Email__ = "darthoring@gmail.com"
__License__ = """
Copyright (C) 2013-2015  Darth_O-Ring	<darthoring@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

def write_video_to_file(arg_dir, vid_file, f_name):
	"""
	
	Opens and writes video to file and displays 
		progress bar during download.

	vid_file	:	open video file
	f_name		:	filename
	arg_dir		:	-dir/--directory value

	"""

	# Join directory and filename
	pathname		=		os.path.abspath(os.path.join(arg_dir, f_name))

	# Check for conflicting filenames
	if os.path.isfile(pathname):
		print "\n\nError: Conflicting filename: ('{}').\nDownload aborted.\n\n".format(f_name)
		sys.exit(1)

	# Grab byte info
	meta			=		vid_file.info()
	file_size		=		int(meta.getheaders("Content-Length")[0])
	file_size_dl		=		0
	block_size		=		8192

	# Open file for writing flv to
	# Handle file opening/writing errors
	try:
		with open(pathname, 'wb') as output:
			print "\nDownloading: '{0}' (Bytes: {1})\n\n".format(f_name, file_size)
			

	# Start loop to display progress bar
			while True:

	# Read video files's block size into buffer
				buffer		=		vid_file.read(block_size)

	# Break if empty buffer
				if not buffer:
					break

	# Add current length of buffer to file's downloaded amount			
				file_size_dl	+=		len(buffer)

	# Write buffer/video's downloaded amount to file
				output.write(buffer)

	# Set download status for display using raw string
				status		=		r'{:10d} [{:3.2f}%]'.format(file_size_dl, 
												file_size_dl * 100.0 / file_size)

	# Update status 
				status		=		status + chr(8) * (len(status)+1)

	# Print status to screen
				print status,

	# Catch open/write exceptions
	except IOError:
		print """\n\nError: Failed on: ('{0}').\nCheck that: ('{1}'), is a valid pathname.\n
				Or that ('{2}') is a valid filename.\n\n""".format(arg_dir, pathname[:-len(f_name)], f_name)
		sys.exit(2)

	except BufferError:
		print '\n\nError: Failed on writing buffer.\nFailed to write video to file.\n\n'
		sys.exit(1)

	except KeyboardInterrupt:
		print "\n\nInterrupt signal given.\nDeleting incomplete video ('{}').\n\n".format(f_name)
		os.remove(pathname)
		sys.exit(1)


def download_video(args):
	"""

	Grabs necessary html information, searches the html for video's flv url
		and writes it to file.
	
	args	:	dictionary of argument keys/values returned by arg_parser

	"""

	# Assign url of video
	url			=		args['u']

	# Open url and grab html information
	# Handle invalid URL errors
	try:
		html			=		urllib2.urlopen(url).read()

	# Catch URL exceptions
	except (urllib2.URLError, urllib2.HTTPError):
		print """\n\nError: Check that URL is valid: ('http://www.website.com/remaining_link')
				\nFailed on: ('{}')\n\n""".format(url)
		sys.exit(2)
	
	# Use regex to search html for the video link
	video_file		=		regex_for_video_link(html)
	
	# Unquote video file URL
	video_file		=		urllib2.unquote(video_file)

	# Open video file for downloading
	# Handle any potential video link errors
	try:
		video_file		=		urllib2.urlopen(video_file)

	# Catch any potential URL errors while opening the video link for download
	except (urllib2.URLError, urllib2.HTTPError):
		print "\n\nError: Failed to open video link's URL.\n\n"
		sys.exit(1)
	
	# Call file_name
	filename		=		file_name(args['f'], url, html)
	
	# Call write_video_to_file for video downloading
	write_video_to_file(args['dir'], video_file, filename) 

	# Print has finished downloading message
	print "\n\n('{}'): has finished downloading.\n\n".format(filename[:-4])
