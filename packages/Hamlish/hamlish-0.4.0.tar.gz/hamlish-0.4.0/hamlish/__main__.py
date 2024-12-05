import argparse
import sys

from pathlib import Path

from hamlish import Hamlish, OutputMode


def main() -> int:
	argparser = argparse.ArgumentParser()
	argparser.add_argument(
		"--destination", "-d",
		type = Path,
		default = Path("."),
		help = "Destination directory for converted template files"
	)

	argparser.add_argument(
		"--mode", "-m",
		type = OutputMode.parse,
		default = OutputMode.INDENTED,
		help = "Formatting mode for the converted template files"
	)

	argparser.add_argument(
		"--indent-str", "-i",
		help = "String to use for indents when modes is not set to compact"
	)

	argparser.add_argument(
		"files",
		type = Path,
		nargs = "+",
		help = "Template files in HAML-like format to convert"
	)

	args = argparser.parse_args(sys.argv)
	args.destination = args.destination.expanduser().resolve()
	args.destination.mkdir(exist_ok = True, parents = True)

	parser = Hamlish.new(
		mode = args.mode,
		indent_string = args.indent_str
	)

	for path in args.files:
		path = path.expanuser().resolve()

		if not path.exists():
			print(f"ERROR: Path does not exist: {path}")
			return 1

		if not path.is_file():
			print(f"ERROR: Path is not a file: {path}")
			return 1

		with path.open("r", encoding = "utf-8") as fd:
			text = parser.convert_source(fd.read())

		with args.destination.joinpath(f"{path.stem}.html").open("w", encoding = "utf-8") as fd:
			fd.write(text)

	print(f"Saved templates to {args.destination}")
	return 0


sys.exit(main())
