yamltool
========

Tools to assist with operations such as merges on yaml files

yaml-merge.py -: Merge a input yaml file into a directory of yaml files

	usage: yaml-merge.py [-h] [source-dir] [source-yaml]

	Merge yaml files.

	positional arguments:
  	source-dir   directory containing yaml to be modfied
  	source-yaml  input yaml with changes

See the example for the input format, the first layer does a simple
match against the file name to merge into.
