"""
This module provides a context manager interface for easy scripting.
"""

from contextlib import ExitStack, contextmanager
import lxml.etree as ET
import sys

import patterns
import svg_output

@contextmanager
def artist(outputFile=None, width=1920, height=1080, originalFile=None):
	"""
	Context manager for Artist object.

	The caller should not attempt to manually write the file, as it will
	automatically be written when exiting the context.
	"""
	if originalFile is not None:
		with open(originalFile, "r") as origInput:
			svg = ET.fromstring(origInput.read())
	else:
		svg = None

	with ExitStack() as stack:
		if outputFile is not None:
			output = stack.enter_context(open(outputFile,"w"))
		else:
			output = sys.stdout

		artist = patterns.Artist(svg_output.SVGOutput(width=width, height=height, originalSVG=svg))
		yield artist
		artist.writeOut(output)
