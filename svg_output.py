"""
This module defines useful routines for 
"""

import sys
import math
import lxml.etree as ET

class SVGOutput:
    """
    This class defines useful methods for drawing using SVGs.
    """

    def __init__(self, width=1920, height=1080, originalSVG=None):
        self.height = height
        self.width = width
        self.strokeWidth = 1
        self.colour = "#ffffff"
        self.svg = 
        if originalSVG is None:
            self.svg = ET.Element("svg",
                width=str(width), height=str(height),
                viewBox=("0 0 %d %d" % (width,height)),
                xmlns="http://www.w3.org/2000/svg")
        else:
            self.svg = originalSVG

    def setColour(self, c=None):
        if c is not None:
            self.colour = c
        return self.colour

    def setStrokeWidth(self, w=None):
        if w is not None:
            self.strokeWidth = w
        return self.strokeWidth

    def _emit(self, element):
        self._apply_style(element)
        self.svg.append(element)

    def _apply_style(self, element):
        element.set("stroke", self.colour)
        element.set("stroke-width", str(self.strokeWidth))

    def background(self, colour=None):
        col = colour or self.colour
        self.svg.append(ET.Element("rect",
            width="100%", height="100%", fill=col, stroke=col))

    def line(self, x1, y1, x2, y2):
        self._emit(ET.Element("line",
            x1=str(x1), x2=str(x2), y1=str(y1), y2=str(y2)))

    def chord(self, x, y, r, fromAngle, toAngle, degrees=False):
        """
        Draws a chord on the circle centred at (x,y) with radius r
        between the point at angle fromAngle to the point at toAngle.

        Angles are measured as in mathematics, with the zero angle
        being directly rightwards and going anticlockwise.
        """
        x1 = x + r*math.cos(fromAngle)
        y1 = y - r*math.sin(fromAngle)
        x2 = x + r*math.cos(toAngle)
        y2 = y - r*math.sin(toAngle)
        self.line(x1, y1, x2, y2)

    def nodeChord(self, x, y, r, nNodes, offset, fromPoint, toPoint):
        """
        For a circle with ``nNodes`` equally spaced points on its side
        numbered ``0..nNodes-1`` anticlockwise, and where point 0 is
        located at angle ``offset``, draw a chord between point
        ``fromPoint`` to point ``toPoint``.

        ``offset`` is measured in radians.
        """
        fromAngle = offset + (2*math.pi/nNodes)*(fromPoint % nNodes)
        toAngle   = offset + (2*math.pi/nNodes)*(toPoint % nNodes)
        self.chord(x, y, r, fromAngle, toAngle)

    def ellipse(self, x, y, rx, ry, fill=None):
        self._emit(ET.Element("ellipse",
            cx=str(x), cy=str(y),
            rx=str(rx), ry=str(ry),
            fill=(fill or "none")))

    def circle(self, x, y, r, fill=None):
        self.ellipse(x, y, r, r, fill)

    def arc(self, x, y, r, fromAngle, toAngle):
        """
        Draws an arc on the circle centred at (x,y) with radius r
        from the point at angle fromAngle to the point at toAngle.

        Angles are measured as in mathematics, with the zero angle
        being directly rightwards and going anticlockwise.
        """

        # make sure fromAngle < toAngle
        if fromAngle > toAngle:
            self.arc(x, y, r, toAngle, fromAngle)

        x1 = x + r*math.cos(fromAngle)
        y1 = y - r*math.sin(fromAngle)
        x2 = x + r*math.cos(toAngle)
        y2 = y - r*math.sin(toAngle)

        # large-arc flag in <path> element
        largeArc = 0 if toAngle-fromAngle < math.pi else 1

        # commands for the <path> element
        command = ' '.join([
            "M", str(x1), str(y1),
            "A", str(r), str(r), "0", str(largeArc), "0", str(x2), str(y2)
        ]);

        self._emit(ET.Element("path",
            d=command,
            fill="none"))
        



