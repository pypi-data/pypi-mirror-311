
import os
import sys
import inspect

def get_abs_path(rel_path=""):
	current_file = os.path.abspath(__file__)
	stack = inspect.stack()
	for frame in stack:
		caller = os.path.abspath(frame.filename)
		if caller != current_file:
			break

	file_path = os.path.dirname(os.path.abspath(caller))
	return os.path.abspath(os.path.join(file_path, rel_path))

def add_abs_path(abs_path):
	if abs_path not in sys.path:
		sys.path += [abs_path]

def add_rel_path(rel_path):
	add_abs_path(get_abs_path(rel_path))
