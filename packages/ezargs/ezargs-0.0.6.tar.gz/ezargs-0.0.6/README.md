# ezargs
Lightweight, zero-setup dynamic Python command line argument parsing. `ezargs` is extremely simple (< 10 SLoC) and pushes as much of the parsing logic into the user's hands as possible. I wrote `ezargs` because I wanted an easier way to set up ephemeral, flexible, or just plain easy CLI arguments for Python scripts. I just wanted to be able to pass whatever I wanted and grab it in the code without having to declare fields beforehand.

The only strict rule pertains to the format of arguments, which is as follows:
* Arguments must be key-value pairs in the format: `key=value`
    * eg. `python my_scripy.py duration=5 max_shift=12 name=foo secret='ab!@#3=e32'` parses the arguments into: `{'duration': '5', 'max_shift': '12', 'name': 'foo', 'secret': 'ab!@#3=e32'}`
    * Subsequent `=` appearances in the value are allowed.
        * eg. `name=fo=o` -> `{'name': 'fo=o'}`
    * Values with spaces must be wrapped in quotes. In general, strings should be sent with quotes (single or double).
        * eg. `name="John Appleseed"` -> `{'name': 'John Appleseed'}`

Type conversions, presence checks, etc. are up to the user to handle. **All values are parsed as strings**.

## Installation:
* Install [ezargs](https://pypi.org/project/ezargs/) with `pip install ezargs`


## Simple Code Recipe:
```py
from ezargs import parse_args

def main(args: dict) -> None:
   max_attempts = int(args.get("max-attempts", 5))  # default value with type conversion
   if not (filename := args.get("filename")):
      # presence check
      raise Exception("missing file name!")
   print(f"{filename=}, {max_attempts=}")


if __name__ == "__main__":
   args: dict = parse_args()
   main(args)
```
