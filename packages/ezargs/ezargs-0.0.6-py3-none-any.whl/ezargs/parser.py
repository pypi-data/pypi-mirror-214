import sys


def parse_args() -> dict:
	args = {}
	for arg in sys.argv[1:]:
		k, v = arg.split("=", 1)
		args[k] = v
	return args
