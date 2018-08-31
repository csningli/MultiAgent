
import sys, os, subprocess

if __name__ == "__main__" :
	dir = os.path.dirname(os.path.realpath(__file__))
	cmd = "rm %s/*.data" % dir 
	subprocess.call(cmd, shell = True)
