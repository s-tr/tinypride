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

    def background(self, colour):
        self.output.background(colour)

    def stringArt1(self, x, y, r, nNodes, spacing, offset=0, colour="#ffffff", strokeWidth=1):
        """
        Generates a form of string art. On a circle with ``n`` equally
        spaced notches on its rim, every node ``i`` is connected to
        another node ``i+spacing`` modulo ``nNodes``.
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

    def stringArt2(self, x, y, r, nNodes, colourList, offset=0, strokeWidth=1):
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
            beginning = i * (nNodesPerColour)
            for j in range(nNodesPerColour):
                self.output.nodeChord(x, y, r, nNodes, offset, beginning+j, beginning+j*nColours)


    def arcs(self, x, y, r, colourList, spacing=0.035, offset=0, strokeWidth=1):
        """
        Creates a circle out of arcs of the specified colours.
        """

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

    def flag(self, x, y, width, height, colours, proportions=None, angle = math.pi/2, border=None, borderColour=None, borderWidth = 1):
        """
        Angle = how far away from the vertical the stripes are tilted.
        0 = vertical, pi/2 = horizontal
        """
        
        def line_coords(pos):
            """
            For a line a proportion `pos` of the way from top left to bottom
            right, finds the coordinates of the top and bottom.
            """
            if pos <= ratio_top:
                if ratio_top == 0:
                    x_top, y_top = x,y
                else:
                    x_top = x + width*pos/ratio_top
                    y_top = y
            else:
                x_top = x + width
                y_top = y + height*(pos-ratio_top)/(1-ratio_top)
            if pos <= ratio_bottom:
                if ratio_bottom == 0:
                    x_bottom, y_bottom = x,y
                else:
                    x_bottom = x
                    y_bottom = y + height*pos/ratio_bottom
            else:
                x_bottom = x + width*(pos-ratio_bottom)/(1-ratio_bottom)
                y_bottom = y + height
            return x_top, y_top, x_bottom, y_bottom

        def angle_as_number():
            if angle == 'vertical':
                return 0
            elif angle == 'horizontal':
                return math.pi/2
            elif angle == 'diagonal':
                return math.atan2(width, height)
            elif float(angle) == angle:
                if angle < 0 or angle > math.pi/2:
                    raise ValueError("Angle must be in [0, pi/2]")
                else:
                    return angle
            else:
                raise ValueError("Invalid angle "+str(angle))

        # default: all stripes are the same width
        if proportions is None:
            proportions = [1] * len(colours)

        colours = list(colours)
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive")
        if len(colours) == 0:
            raise ValueError("Empty colour list")
        if len(proportions) != len(colours):
            raise ValueError("Proportions list length is different from colours list length")

        angle = angle_as_number()

        # compute the positions of each stripe
        scaled_proportions = [p/sum(proportions) for p in proportions]
        stripes = []
        accum = 0
        for prop in scaled_proportions:
            stripes.append((accum, accum+prop))
            accum += prop

        # useful ratios for detecting when a stripe crosses a corner
        H_ = height*math.sin(angle)
        W_ = width*math.cos(angle)
        L_ = H_ + W_
        ratio_top = W_ / L_
        ratio_bottom = H_ / L_


        self.output.setColour("none")
        self.output.setStrokeWidth(0)

        for i, colour in enumerate(colours):
            points = []
            stripe_start, stripe_end = stripes[i]
            x_start_top, y_start_top, x_start_bottom, y_start_bottom = line_coords(stripe_start)
            x_end_top, y_end_top, x_end_bottom, y_end_bottom = line_coords(stripe_end)

            # compute the boundary of the stripe
            points.append((x_start_top, y_start_top))
            points.append((x_start_bottom, y_start_bottom))

            if stripe_start <= ratio_bottom and stripe_end > ratio_bottom:
                # stripe crosses bottom corner
                points.append((x,y+height))

            points.append((x_end_bottom, y_end_bottom))
            points.append((x_end_top, y_end_top))

            if stripe_start <= ratio_top and stripe_end > ratio_top:
                # stripe crosses bottom corner
                points.append((x+width,y))

            self.output.polygon(points,fill = colour)

        if border is not None:
            self.output.setColour(colour)
            self.output.setStrokeWidth(borderWidth)
            self.output.rectangle(x,y,width,height)

