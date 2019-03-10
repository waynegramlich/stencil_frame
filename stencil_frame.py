#!/usr/bin/env python

#<----------------------------------------- 100 characters --------------------------------------->|
#
# Codeing guidelines:
# * Lines are no longer than 100 characters.
# * Classes are listed alphabetically.
# * Methods are listed alphabetically within a class.
# * All comments are written in Markdown syntax.
# * Argument types are usually verified at method/function entry (no duck typing!)
# * An attempt is made to adhere to PEP 8 with the following exceptions:
#   * Documentation strings are allowed to go to 100 characters.
#   * Similar calls with similar arguments are typically vertically aligned.
#   * Assignments with similar expressions are typically vertically aligned.

from EZCAD3 import *

def main():
    # Create *ezcad* object for EZCAD 3.0:
    ezcad = EZCAD3(0)

    # Create the *stencil_frame* assembly and process it:
    stencil_frame = StencilFrame(None, "Stencil_Frame", debug=True)
    stencil_frame.process(ezcad)

class BottomClamp(Part):
    """ *BottomClamp*: Represents the part that the *West_Clamp* screws into.
    """

    def __init__(self, up, name, debug=False):
	""" *BottomClamp*: Initialize the *BottomClamp* object (i.e. *self*.)
	"""

	# Standard initialization sequence for *bottom_clamp*:
	bottom_clamp = self
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(debug, bool)
	Part.__init__(bottom_clamp, up, name)
	bottom_clamp.debug_b = debug

    def construct(self):
	""" *BottomClamp*: Construct the *BottomClamp* object.
	"""

	# Grab some *Part*'s from *bottom_clamp* (i.e. *self*):
	bottom_clamp  = self
	stencil_frame = bottom_clamp.up
	stencil       = stencil_frame.stencil_
	west_clamp    = stencil_frame.west_clamp_
	frame_block   = stencil_frame.frame_block_

	# Grab some values from the *Part*'s:
	debug               = bottom_clamp.debug_b
	frame_block_bsw     = frame_block.bsw
	frame_block_tne     = frame_block.tne
	stencil_bsw         = stencil.bsw
	stencil_fold_amount = stencil.fold_amount_l
	stencil_thickness   = stencil.thickness_l
	stencil_tne         = stencil.tne
	west_clamp_bsw      = west_clamp.bsw
	west_clamp_tne      = west_clamp.tne
	
	# Define some X coordinates:
	west_dx = L(inch="3/4")
	zero = L()
	end_mill_radius = L(inch="1/2")
	x21 = west_clamp_tne.x + end_mill_radius
	x20 = west_clamp_tne.x
	x15 = stencil_bsw.x + stencil_thickness
	x10 = west_clamp.bsw.x
	x0  = west_clamp_bsw.x - west_dx

	# Define some Y coordinates:
	y20 = west_clamp_tne.y + end_mill_radius
	y19 = west_clamp_tne.y
	y15 = stencil_tne.y
	y10 = zero
	y5  = stencil_bsw.y
	y1  = west_clamp_bsw.y
	y0  = west_clamp_bsw.y - end_mill_radius

	# Define some Z coordinates:
	z20 = frame_block_tne.z
	z10  = stencil_tne.z
	z6  = stencil_tne.z - stencil_thickness
	z4  = stencil_tne.z - stencil_fold_amount - L(mm=1.00)
	z0  = frame_block_bsw.z

	# Start with a block of *material*:
	material = Material("Plastic", "HDPE")
	color = Color("lime")
	corner1 = P(x0,  y1,  z0)
	corner2 = P(x20, y19, z20)
	bottom_clamp.block("Bottom_Clamp", material, color, corner1, corner2, "")

	# Mount *bottom_clamp* on the tooling plate:
	extra_dx = L(inch="1/4")
	extra_dy = L(inch="1/4")
	bottom_clamp.vice_mount("Top_Vice", "t", "w", "l", extra_dx, extra_dy)
	bottom_clamp.tooling_plate_drill("Plate_Drill", (0,), (0,), [])
	bottom_clamp.tooling_plate_mount("Top_Plate")
	
	# Perform the exterior contour:
	radius = L(inch="1/16")
	bottom_clamp.rectangular_contour("Exterior_Contour", radius)

	# Mill out a landing for the *west_clamp*:
	corner1 = P(x10, y20, z10)
	corner2 = P(x20, y0,  z20)
	bottom_clamp.simple_pocket("Clamp_Pocket", corner1, corner2, radius, "")
	bottom_clamp.cnc_fence()

	# Mill out the hole for the stencil landing:
	corner1 = P(x10, y5,  z6)
	corner2 = P(x21, y15, z20)  #FIXME: Why doesn't *z10* work here???!!!
	bottom_clamp.simple_pocket("Stencil_Landing", corner1, corner2, radius, "")

	# Mill out the hole for the stencil lock:
	corner1 = P(x10, y1,  z4)
	corner2 = P(x15, y19, z20)  #FIXME: Why doesn't *z5* work here???!!!
	bottom_clamp.simple_pocket("Stencil_Lock", corner1, corner2, radius, "")

	# Perform any requested visualization *debug*:
	if debug:
	    radius = L(inch="1/2")
	    extra = L(inch=1.000)
	    corner1 = P(x0 - extra,  y10,        z0)
	    corner2 = P(x20 + extra, y0 - extra, z20)
	    bottom_clamp.simple_pocket("Debug", corner1, corner2, radius, "t")


class Clamp(Part):
    """ *Clamp*: Represents the 
    """

    def __init__(self, up, name, is_east, debug=False):
        """ *Clamp*: Initialize the *Clamp* object (i.e. *self*).
	"""

	# Standard initialization sequence for *clamp*:
	clamp = self
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(is_east, bool)
	assert isinstance(debug, bool)
	Part.__init__(clamp, up, name)
	clamp.debug_b = debug
	clamp.is_east_b = is_east

    def construct(self):
	""" *Clamp*: Construct the *Clamp* object (i.e. *self*):
	"""

	# Grab some *Part*'s from *clamp* (i.e. *self*):
	clamp = self
	stencil_frame = clamp.up
	frame_block   = stencil_frame.frame_block_
	stencil       = stencil_frame.stencil_

	# Grab some values from the *Part*'s:
	frame_block_tne   = frame_block.tne
	frame_block_bsw   = frame_block.bsw
	frame_block_dz    = frame_block.dz
	stencil_tne       = stencil.tne
	stencil_bsw       = stencil.bsw
	stencil_thickness = stencil.thickness_l
	is_east           = clamp.is_east_b
	debug             = clamp.debug_b
	
	# Compute some X coordinates:
	zero = L()
	dx = L(inch="3/4")
	x20 = stencil_tne.x + dx/2
	x18 = stencil_tne.x
	x16 = stencil_tne.x - dx/2
	x10 = zero
	x4  = stencil_bsw.x + dx/2
	x2  = stencil_bsw.x
	x0  = stencil_bsw.x - dx/2

	# Compute some Y coordinates:
	end_mill_radius = L(inch="1/2")
	extra_dy = L(inch="1/2")
	y20 = stencil_tne.y + extra_dy + end_mill_radius
	y19 = stencil_tne.y + extra_dy
	y10 = zero
	y1  = stencil_bsw.y - extra_dy
	y0  = stencil_bsw.y - extra_dy - end_mill_radius

	# Compute some Z coordinates:
	z20 = frame_block.tne.z
	z10 = stencil_tne.z
	z5  = stencil_bsw.z
	z0  = frame_block.bsw.z

	# Create the *clamp* from a block of *material*:
	material = Material("Plastic", "HDPE")
	color = Color("purple")
	if is_east:
	    corner1 = P(x16, y1,  z0)
	    corner2 = P(x20, y19, z20)	
	    comment = "East_Clamp"
	else:
	    corner1 = P(x0, y1,  z0)
	    corner2 = P(x4, y19, z20)	
	    comment = "West_Clamp"
	clamp.block(comment, material, color, corner1, corner2, "")

	# Mount with the *clamp* bottom facing up:
	extra_dx = L(inch="1/4")
	extra_dy = L(inch="1/4")
	clamp.vice_mount("Vice_Bottom", "b", "w", "l", extra_dx, extra_dy)
	clamp.tooling_plate_drill("Plate_Drill", (0,), (0,), [])
	clamp.tooling_plate_mount("Plate_Mount")
	radius = L(inch="1/4")
	clamp.rectangular_contour("Exterior_Contour", radius)
	
	# Make space for the stencil:
	end_mill_radius = L(inch="3/16")
	if is_east:
	    corner1 = P(x16, y0,  z10)
	    corner2 = P(x18, y20, z0)
	    comment = "East_Stencil_Pocket"
	else:
	    corner1 = P(x2,  y0,  z10)
	    corner2 = P(x4,  y20, z0)
	    comment = "West_Stencil_Pocket"
	clamp.simple_pocket(comment, corner1, corner2, end_mill_radius, "")

	# Remove the "bottom" of the clamp:
	if is_east:
	    corner1 = P(x16, y0,  z0)
	    corner2 = P(x20, y20, z5)
	else:
	    corner1 = P(x0, y0,  z0)
	    corner2 = P(x4, y20, z5)
	clamp.simple_pocket("Bottom_Remove", corner1, corner2, end_mill_radius, "")
	
	# Peform any requested vizualization *debug* operation:
	if debug:
	    extra = L(inch="1/2")
	    corner1 = P(x0 - extra,  zero,       z0)
	    corner2 = P(x20 + extra, y0 - extra, z20)
	    clamp.simple_pocket("Debug", corner1, corner2, end_mill_radius, "")

class FrameBlock(Part):
    """ *FrameBlock*: Represents the main block of the frame:
    """

    def __init__(self, up, name, debug=False):
	""" *FrameBlock*: Initialize the *FrameBlock* object (i.e. *self*.)
	"""

	# Standard initialization sequence for *frame_block*:
	frame_block = self
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(debug, bool)
	Part.__init__(frame_block, up, name)
	frame_block.debug_b = debug

    def construct(self):
	""" *FrameBlock*: Construct the *FrameBlock* object (i.e. *self*):
	"""

	# Grab some *Part*'s from *frame_block* (i.e. *self*):
	frame_block   = self
	stencil_frame = frame_block.up
	bottom_clamp  = stencil_frame.bottom_clamp_
	east_clamp    = stencil_frame.east_clamp_
	stencil       = stencil_frame.stencil_
	west_clamp    = stencil_frame.west_clamp_

	# Grab some values from the *Part*'s:
	bottom_clamp_tne    = bottom_clamp.tne
	bottom_clamp_bsw    = bottom_clamp.bsw
	east_clamp_tne      = east_clamp.tne
	east_clamp_bsw      = east_clamp.bsw
	west_clamp_tne      = west_clamp.tne
	west_clamp_bsw      = west_clamp.bsw
	stencil_tne         = stencil.tne
	stencil_bsw         = stencil.bsw
	stencil_thickness   = stencil.thickness_l
	stencil_fold_amount = stencil.fold_amount_l
	debug               = frame_block.debug_b

	# Compute some X coordinates:
	end_mill_radius = L(inch="1/2")
	gap_dx = L(inch="1/4")
	east_dx = L(inch=1.000)
	west_dx = L(inch=1.000)
	zero = L()
	x21 = east_clamp_tne.x + east_dx + L(inch=1.000) # For visualization only
	x20 = east_clamp_tne.x + east_dx
	x15 = east_clamp_tne.x
	x13 = stencil_tne.x - stencil_thickness
	x12 = east_clamp_bsw.x
	x11 = east_clamp_bsw.x - end_mill_radius
	x10 = zero
	x5  = bottom_clamp_bsw.x - gap_dx
	x0  = bottom_clamp_bsw.x - gap_dx - west_dx

	# Compute some Y coordinates:
	material_dy = L(inch=1.000)
	y20 = east_clamp_tne.y + material_dy
	y15 = east_clamp_tne.y
	y12 = stencil_tne.y
	y10 = zero
	y8  = stencil_bsw.y
	y5  = west_clamp_bsw.y
	y0  = west_clamp_bsw.y - material_dy 

	# Compute some Z coordinates:
	frame_block.dz_l    = dz    = L(inch=0.800)
	z10 =  dz/2
	z5  = stencil_tne.z
	z3  = stencil_tne.z - stencil_thickness
	z1  = stencil_tne.z - stencil_fold_amount - L(mm=1.00)
	z0  = -dz/2
	frame_block.y_gap_l = y_gap = L(inch="1/2")

	# Start with a block of *material*:
	material = Material("Plastic", "HDPE")
	color = Color("tan")
	corner1 = P(x0,  y0,  z0)
	corner2 = P(x20, y20, z10)
	frame_block.block("Frame_Block", material, color, corner1, corner2, "")

	# Drill the mounting holes for the tooling plate and mount on tooling plate:
	extra_dx = L(inch="1/4")
	extra_dy = L(inch="1/4")
	frame_block.vice_mount("Top_Vice", "t", "n", "l", extra_dx, extra_dy)
	frame_block.tooling_plate_drill("Plate_Drill", (0, 2, 5, 9, 13, 17), (0, 4, 8), [])
	frame_block.tooling_plate_mount("Top_Plate")
	radius = L(inch="1/16")
	frame_block.rectangular_contour("Exteriof_Contour", radius)

	# Mill out the hole in the middle of the frame:
	corner1 = P(x5,  y5,  z0)
	corner2 = P(x12, y15, z10)
	radius = L(inch="1/4")
	frame_block.simple_pocket("Main_Pocket", corner1, corner2, radius, "t")
	frame_block.cnc_fence()

	# Mill out a landing for the *east_clamp*:
	corner1 = P(x11, y5,  z5)
	corner2 = P(x15, y15, z10)
	frame_block.simple_pocket("Clamp_Pocket", corner1, corner2, radius, "")
	frame_block.cnc_fence()

	radius = L(inch="3/16")
	# Mill out a landing for the *stencil*:
	corner1 = P(x11, y8,  z3)
	corner2 = P(x15, y12, z10)  #FIXME: Why doesn't *z5* work here???!!!
	frame_block.simple_pocket("Stencil_Landing", corner1, corner2, radius, "")

	# Mill out the hole for the stencil lock:
	corner1 = P(x13, y5,  z1)
	corner2 = P(x15, y15, z10)  #FIXME: Why doesn't *z5* work here???!!!
	frame_block.simple_pocket("Stencil_Lock", corner1, corner2, radius, "")

	# Do any requested *debug* visualation operations:
	if debug:
	    extra = L(inch="1/2")
	    corner1 = P(x0  - extra, y0,  z0)
	    corner2 = P(x20 + extra, y10, z10)
	    frame_block.simple_pocket("Debug", corner1, corner2, radius, "t")


class Stencil(Part):
    """ *Stencil*: Represents the stencil to be mounted.
    """

    def __init__(self, up, name, debug=False):
	""" *Stencil*: Initialize the 
	"""

	# Standard initialization sequence:
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(debug, bool)
	stencil = self
	Part.__init__(stencil, up, name)

	# Same *debug* into *stencil*:
	stencil.debug_b = debug

    def construct(self):
	""" *Stencil*: Construct the *Stencil* object (i.e. *self*).
	"""
	
	# Define some value and stuff them into *stencil* (i.e. *self*):
	stencil = self
	stencil.fold_amount_l = fold_amount = L(inch="1/4")
	stencil.dx_l          = dx          = L(cm=15.00) - 2 * fold_amount
	stencil.dy_l          = dy          = L(cm=10.00)
	stencil.thickness_l   = thickness   = L(mm=1.00) # L(mm=0.12)

	# Grab *debug* from *stencil*:
	debug = stencil.debug_b

	# Construct the main stencil:
	#material = Material("Steel", "Stainless")
	material = Material("Plastic", "HDPE")
	color = Color("cyan")
	zero = L()
	corner1 = P(-dx/2, -dy/2, zero)
	corner2 = P( dx/2,  dy/2, -thickness)
	stencil.block("Stencil_Flat", material, color, corner1, corner2, "")

	# Construct the two folds:
	corner1 = P(-dx/2,             -dy/2, zero)
	corner2 = P(-dx/2 + thickness,  dy/2, -fold_amount)
	stencil.block("West_Fold", material, color, corner1, corner2, "")
	corner1 = P( dx/2 - thickness, -dy/2, zero)
	corner2 = P( dx/2,              dy/2, -fold_amount)
	stencil.block("East_Fold", material, color, corner1, corner2, "")

	# Perform any debug visualization:
	if debug:
	    stencil.vice_mount("Top_Vice", "t", "n", "")
	    extra = L(inch="1/4")
	    corner1 = P(-dx/2 - extra, zero, -fold_amount - extra)
	    corner2 = P( dx/2 + extra, -dy/2 - extra, zero)
	    stencil.simple_pocket("Debug", corner1, corner2, L(inch="1/4"), "t")

class StencilFrame(Part):
    """ *StencilFrame*: Represents the entire Stencil frame assembly.
    """

    def __init__(self, up, name, debug=False):
	""" *StencilFrame*: Initialize the *StencilFrame* object (i.e. *self*.)
	"""

	# Standard initialization sequequence:
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(debug, bool)
	stencil_frame = self
	Part.__init__(stencil_frame, up, name)

	# Save some values into *stencil_frame* (i.e. *self*):
	stencil_frame.debug_b       = debug
	stencil_frame.stencil_      = Stencil(stencil_frame,     "Stencil",            debug=debug)
	stencil_frame.frame_block_  = FrameBlock(stencil_frame,  "Frame_Block",        debug=debug)
	stencil_frame.east_clamp_   = Clamp(stencil_frame,       "East_Clamp",  True,  debug=debug)
	stencil_frame.west_clamp_   = Clamp(stencil_frame,       "West_Clamp",  False, debug=debug)
	stencil_frame.bottom_clamp_ = BottomClamp(stencil_frame, "Bottom_Clamp",       debug=debug) 

    def construct(self):
	""" *StencilFrame*: Construct the *StencilFrame* assembly (i.e. *self*.)
	"""
                          
	# This is a pure assembly, so there is no construction here:
	pass

if __name__ == "__main__":
    main()
