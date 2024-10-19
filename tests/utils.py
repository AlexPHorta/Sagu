import shutil
import tempfile

from contextlib import contextmanager


# Stolen from https://getpelican.com
@contextmanager
def temporary_folder():
	"""creates a temporary folder, return it and delete it afterwards.

	This allows to do something like this in tests:

		>>> with temporary_folder() as d:
			# do whatever you want
	"""
	tempdir = tempfile.mkdtemp()
	try:
		yield tempdir
	finally:
	   shutil.rmtree(tempdir)
