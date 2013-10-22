#!/usr/bin/python
# -*- coding: utf-8 -*-

__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '22.10.2013'


try:
	import sys
	import os
	import subprocess
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Fuzz:

	def __init__(self, spk_directory):
		self.send_tcp_path = "/usr/local/generic_send_tcp"
		self.spk_directory = spk_directory	

		for file in self.send_tcp_path, self.spk_directory:
			if not os.path.exists(file):
				print >> sys.stderr, "%s Doesn't Exists On The System  "% (file)
				sys.exit(1)


	def run_fuzz(self, target, port):
		if not self.spk_directory.endswith("/"):
                	self.spk_directory = self.spk_directory + "/"

		for root, dirs, files in os.walk(self.spk_directory):
    			for file in files:
        			if file.endswith('.spk'):
					file_name = self.spk_directory + file
					fuzz_command = "%s %s %s %s 0 0"% (self.send_tcp_path, target, port, file_name)

					print "%s : Processing"% (file)
					proc = subprocess.Popen(fuzz_command, shell=True,
                        			stdout = subprocess.PIPE,
						stderr = subprocess.PIPE
                        		)
                							
					out, err = proc.communicate()
					errcode = proc.returncode
	
					if errcode == 0:
			 			print "%s : Ok"% file
						os.unlink(file_name)
					

if __name__ == "__main__":
	
	if not len(sys.argv) == 4:
		print >> sys.stderr, "Usage: %s <spk_directory> <target> <port>"% (sys.argv[0])
		sys.exit(2)

	spk_directory = sys.argv[1]
	target = sys.argv[2]
	port = sys.argv[3]
	
	fuzz = Fuzz(spk_directory)
	try:
		file_list = fuzz.run_fuzz(target, port)
	except Exception, err:
		print >> sys.stderr, "Error: %s"% (err.message)
		sys.exit(3)
