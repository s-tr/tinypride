"""
This file contains the main bulk of the code to generate pretty patterns.
"""

from __future__ import division

import lxml.etree as ET
import math

import svg_output

class Artist:
    def __init__(self, output=None):
        self.output = output or svg_output.SVGOutput()

    def writeOut(self, outfile):
        """
        Writes the SVG output to a file. ``outfile`` must be a file
        object that supports writes.
        """
        outfile.write(ET.tostring(self.output.svg, pretty_print=True))

    def stringArt1(x, y, r, nNodes, spacing, offset=0, colour="#ffffff", strokeWidth=1):
        """
        Generates a form of string art. On a circle with ``n`` equally
        spaced notches on its rim, every node ``i`` is connected to
        another node ``i+k`` for some k.
        """

        if nNodes<2:
            raise ValueError("Must have 2 or more nodes")
        if spacing<=0:
            raise ValueError("Spacing must be positive")
        if spacing >= nNodes:
            raise ValueError("Spacing must be less than number of nodes")

        self.output.setColour(colour)
        self.output.setStrokeWidth(strokeWidth)
        for i in range(nNodes):
            self.output.nodeChord(x, y, r, nNodes, offset, i, i+spacing)

    def stringArt2(x, y, r, nNodes, colourList, offset=0, strokeWidth=1):
        """
        """

        if len(colourList) < 2:
            raise ValueError("List of colours must have at least 2 elements")

        if nNodes%len(colourList) != 0:
            raise ValueError(
                "Number of nodes must be divisible by number of colours")

        nColours = len(colourList)
        nNodesPerColour = nNodes // len(colourList)
        
        self.output.setStrokeWidth(strokeWidth)
        for i in range(nColours):
            self.output.setColour(colourList[i])
            beginning = i * nNodesPerColour
            for j in range(nNodesPerColour):
                self.output.nodeChord(x, y, r, nNodes, offset, beginning+j, beginning+j*nColours)


    def arcs(x, y, r, colourList, spacing=0.035, offset=0, clockwise=False, strokeWidth=1):
        """
        Creates a circle out of arcs of the specified colours.
        """

        if clockwise == True:
            arcs(x, y, r, colourList[::-1],
                spacing=spacing, offset=offset, clockwise=False, strokeWidth=strokeWidth)

        if len(colourList) < 2:
            raise ValueError("Must have 2 or more colours")
        if len(colourList) * spacing > 2*math.pi:
            raise ValueError("Too much spacing")

        nColours = len(colourList)
        sectorSize = 2*math.pi/nColours

        self.output.setStrokeWidth(strokeWidth)
        for i in range(nColours):
            self.output.setColour(colourList[i])
            self.output.arc(x, y, r,
                fromAngle = offset + i*sectorSize + spacing/2,
                toAngle = offset + (i+1)*sectorSize - spacing/2)

    def dotmatrix()
