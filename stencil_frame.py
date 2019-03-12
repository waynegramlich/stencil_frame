#!/usr/bin/env python

#<----------------------------------------- 100 characters --------------------------------------->|
#
# Codeing guidelines:
# * Lines are no longer than 100 characters.
# * Classes are listed alphabetically.
# * Methods are listed alphabetically within a class.
# * All comments are written in Markdown syntax.
# * Generally, a block of statements is preceed with a comment that explains what the block does.
# * Argument types are usually verified at method/function entry (no duck typing!)
# * An attempt is made to adhere to PEP 8 with the following exceptions:
#   * Documentation strings are allowed to go to 100 characters.
#   * Similar method/function calls with similar arguments are typically vertically aligned.
#   * Assignments with similar expressions are typically vertically aligned.

from EZCAD3 import *

def main():
    # Create *ezcad* object for EZCAD 3.0:
    ezcad = EZCAD3(0)

    # Create the *stencil_frame* assembly and process it:
    stencil_frame = StencilFrame(None, "Stencil_Frame", debug=False)
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
	east_edge     = stencil_frame.east_edge_

	# Grab some values from the *Part*'s:
	debug               = bottom_clamp.debug_b
	east_edge_bsw       = east_edge.bsw
	east_edge_tne       = east_edge.tne
	stencil_bsw         = stencil.bsw
	stencil_fold_amount = stencil.fold_amount_l
	stencil_thickness   = stencil.thickness_l
	stencil_tne         = stencil.tne
	west_clamp_bsw      = west_clamp.bsw
	west_clamp_tne      = west_clamp.tne
	
	# Define some X coordinates:
	west_dx = L(inch=1.000)
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
	z20 = east_edge_tne.z
	z10  = stencil_tne.z
	z6  = stencil_tne.z - stencil_thickness
	z4  = stencil_tne.z - stencil_fold_amount - L(mm=1.00)
	z0  = east_edge_bsw.z

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
	bottom_clamp.tooling_plate_drill("Plate_Drill", (0, 2, 4, 6, 8), (0, 2, 3),
	 [])
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

	# Drill the holes that join *west_clamp* to *bottom_clamp* (i.e. "wcbc"):
	bottom_clamp.fasten("WCBC_NE", stencil_frame.wcbc_ne_fastener_, "thread")
	bottom_clamp.fasten("WCBC_NW", stencil_frame.wcbc_nw_fastener_, "thread")
	bottom_clamp.fasten("WCBC_CW", stencil_frame.wcbc_cw_fastener_, "thread")
	bottom_clamp.fasten("WCBC_SE", stencil_frame.wcbc_se_fastener_, "thread")
	bottom_clamp.fasten("WCBC_SW", stencil_frame.wcbc_sw_fastener_, "thread")

	# Remount *bottom_clamp* so that west edges is facing up:
	bottom_clamp.vice_mount("West_Vice", "w", "b", "l")
	bottom_clamp.fasten("WCBC_BN", stencil_frame.webc_bn_fastener_, "thread")
	bottom_clamp.fasten("WCBC_BS", stencil_frame.webc_bs_fastener_, "thread")
	bottom_clamp.fasten("WCBC_TN", stencil_frame.webc_tn_fastener_, "thread")
	bottom_clamp.fasten("WCBC_TS", stencil_frame.webc_ts_fastener_, "thread")

	# Perform any requested visualization *debug*:
	if debug:
	    radius = L(inch="1/2")
	    extra = L(inch=1.000)
	    corner1 = P(x0 - extra,  y10,        z0)
	    corner2 = P(x20 + extra, y0 - extra, z20)
	    bottom_clamp.simple_pocket("Debug", corner1, corner2, radius, "t")


class Clamp(Part):
    """ *Clamp*: Represents the east and west top stencil clamp:
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
	east_edge   = stencil_frame.east_edge_
	stencil       = stencil_frame.stencil_

	# Grab some values from the *Part*'s:
	stencil_tne         = stencil.tne
	stencil_bsw         = stencil.bsw
	stencil_thickness   = stencil.thickness_l
	stencil_fold_amount = stencil.fold_amount_l
	is_east             = clamp.is_east_b
	debug               = clamp.debug_b
	
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
	z20 = east_edge.tne.z
	z10 = stencil_tne.z
	z5  = stencil_bsw.z
	z0  = east_edge.bsw.z

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
	if is_east:
	    clamp.vice_mount("Vice_Bottom", "b", "e", "l", extra_dx, extra_dy)
	else:
	    clamp.vice_mount("Vice_Bottom", "b", "w", "l", extra_dx, extra_dy)
	clamp.tooling_plate_drill("Plate_Drill", (0, 3, 5, 8), (0, 1), [])
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
	
	# Drill some holes for mounting the *camp* to either *east_edge* or *bottom_clamp*:
	if is_east:
	    # Drill holes for *east_clamp* and *east_edge* (i.e. "ecee") joining:
	    clamp.fasten("ECEE_NE", stencil_frame.ecee_ne_fastener_, "close")
	    clamp.fasten("ECEE_NW", stencil_frame.ecee_nw_fastener_, "close")
	    clamp.fasten("ECEE_CE", stencil_frame.ecee_ce_fastener_, "close")
	    clamp.fasten("ECEE_SW", stencil_frame.ecee_se_fastener_, "close")
	    clamp.fasten("ECEE_SE", stencil_frame.ecee_sw_fastener_, "close")
        else:
	    # Drill holes for *west_clamp* and *bottom_clamp* (i.e. "wcbc") joining:
	    clamp.fasten("WCBC_NE", stencil_frame.wcbc_ne_fastener_, "close")
	    clamp.fasten("WCBC_NW", stencil_frame.wcbc_nw_fastener_, "close")
	    clamp.fasten("WCBC_CW", stencil_frame.wcbc_cw_fastener_, "close")
	    clamp.fasten("WCBC_SE", stencil_frame.wcbc_se_fastener_, "close")
	    clamp.fasten("WCBC_SE", stencil_frame.wcbc_sw_fastener_, "close")

	# Peform any requested vizualization *debug* operation:
	if debug:
	    extra = L(inch="1/2")
	    corner1 = P(x0 - extra,  zero,       z0)
	    corner2 = P(x20 + extra, y0 - extra, z20)
	    clamp.simple_pocket("Debug", corner1, corner2, end_mill_radius, "")

class EastEdge(Part):
    """ *EastEdge*: Represents the main block of the frame:
    """

    def __init__(self, up, name, debug=False):
	""" *EastEdge*: Initialize the *EastEdge* object (i.e. *self*.)
	"""

	# Standard initialization sequence for *east_edge*:
	east_edge = self
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(debug, bool)
	Part.__init__(east_edge, up, name)
	east_edge.debug_b = debug

    def construct(self):
	""" *EastEdge*: Construct the *EastEdge* object (i.e. *self*):
	"""

	# Grab some *Part*'s from *east_edge* (i.e. *self*):
	east_edge   = self
	stencil_frame = east_edge.up
	bottom_clamp  = stencil_frame.bottom_clamp_
	east_clamp    = stencil_frame.east_clamp_
	stencil       = stencil_frame.stencil_
	west_clamp    = stencil_frame.west_clamp_

	# Grab some values from the *Part*'s:
	#bottom_clamp_tne    = bottom_clamp.tne
	#bottom_clamp_bsw    = bottom_clamp.bsw
	east_clamp_tne      = east_clamp.tne
	east_clamp_bsw      = east_clamp.bsw
	stencil_tne         = stencil.tne
	stencil_bsw         = stencil.bsw
	stencil_thickness   = stencil.thickness_l
	stencil_fold_amount = stencil.fold_amount_l
	debug               = east_edge.debug_b

	# Compute some X coordinates:
	end_mill_radius = L(inch="1/2")
	gap_dx = L(inch="1/4")
	east_dx = L(inch=1.250)
	west_dx = L(inch=1.500)
	zero = L()
	x20 = east_clamp_tne.x + east_dx
	x15 = east_clamp_tne.x
	x13 = stencil_tne.x - stencil_thickness
	x10 = east_clamp_bsw.x
	x1  = east_clamp_tne.x - west_dx
	x0  = east_clamp_tne.x - west_dx - end_mill_radius

	# Compute some Y coordinates:
	material_dy = L(inch=1.000)
	y20 = east_clamp_tne.y + material_dy
	y15 = east_clamp_tne.y
	y12 = stencil_tne.y
	y10 = zero
	y8  = stencil_bsw.y
	y5  = east_clamp_bsw.y
	y0  = east_clamp_bsw.y - material_dy 

	# Compute some Z coordinates:
	east_edge.dz_l    = dz    = L(inch=0.800)
	z10 =  dz/2
	z5  = stencil_tne.z
	z3  = stencil_tne.z - stencil_thickness
	z1  = stencil_tne.z - stencil_fold_amount - L(mm=1.00)
	z0  = -dz/2
	east_edge.y_gap_l = y_gap = L(inch="1/2")

	# Start with a block of *material*:
	material = Material("Plastic", "HDPE")
	color = Color("tan")
	corner1 = P(x1,  y0,  z0)
	corner2 = P(x20, y20, z10)
	east_edge.block("East_Edge", material, color, corner1, corner2, "")

	# Drill the mounting holes for the tooling plate and mount on tooling plate:
	extra_dx = L(inch="1/4")
	extra_dy = L(inch="1/4")
	east_edge.vice_mount("Top_Vice", "t", "e", "l", extra_dx, extra_dy)
	east_edge.tooling_plate_drill("Plate_Drill", (0, 3, 6, 9, 12), (0, 1, 2, 3, 4),
	  [(3,0), (6,0), (9,0), (0,1), (12,1), (3,2), (6,2), (9,2), (0,3), (12,3)])
	east_edge.tooling_plate_mount("Top_Plate")
	contour_radius = L(inch="1/16")
	east_edge.rectangular_contour("Exteriof_Contour", contour_radius)

	# Mill out a landing for the *east_clamp*:
	radius = L(inch="3/16")
	corner1 = P(x0,  y5,  z5)
	corner2 = P(x15, y15, z10)
	east_edge.simple_pocket("Clamp_Pocket", corner1, corner2, radius, "")
	east_edge.cnc_fence()

	# Mill out a landing for the *stencil*:
	corner1 = P(x0,  y8,  z3)
	corner2 = P(x15, y12, z10)  #FIXME: Why doesn't *z5* work here???!!!
	east_edge.simple_pocket("Stencil_Landing", corner1, corner2, radius, "")

	# Mill out a through pocket that leads up to the *east_clamp*:
	corner1 = P(x0,  y8,  z0)
	corner2 = P(x10, y12, z10)  #FIXME: Why doesn't *z3* work here???!!!
	east_edge.simple_pocket("Through_Pocket", corner1, corner2, radius, "")

	# Mill out the pocketfor the stencil lock:
	corner1 = P(x13, y5,  z1)
	corner2 = P(x15, y15, z10)  #FIXME: Why doesn't *z5* work here???!!!
	east_edge.simple_pocket("Stencil_Lock", corner1, corner2, radius, "")

	# Drill the holes to join *north_edge*/*south_edge* to *east_edge*:
	east_edge.fasten("NE_NE", stencil_frame.ne_ne_fastener_, "thread")
	east_edge.fasten("NE_NW", stencil_frame.ne_nw_fastener_, "thread")
	east_edge.fasten("NE_SE", stencil_frame.ne_se_fastener_, "thread")
	east_edge.fasten("NE_SW", stencil_frame.ne_sw_fastener_, "thread")
	east_edge.fasten("SE_NE", stencil_frame.se_ne_fastener_, "thread")
	east_edge.fasten("SE_NW", stencil_frame.se_nw_fastener_, "thread")
	east_edge.fasten("SE_SE", stencil_frame.se_se_fastener_, "thread")
	east_edge.fasten("SE_SW", stencil_frame.se_sw_fastener_, "thread")

	# Drill the holes to join *east_clamp* to *east_edge* (i.e. "ecee"):
	east_edge.fasten("ECEE_NE", stencil_frame.ecee_ne_fastener_, "thread")
	east_edge.fasten("ECEE_NW", stencil_frame.ecee_nw_fastener_, "thread")
	east_edge.fasten("ECEE_CE", stencil_frame.ecee_ce_fastener_, "thread")
	east_edge.fasten("ECEE_SW", stencil_frame.ecee_se_fastener_, "thread")
	east_edge.fasten("ECEE_SE", stencil_frame.ecee_sw_fastener_, "thread")

	# Do any requested *debug* visualation operations:
	if debug:
	    extra = L(inch="1/2")
	    corner1 = P(x0  - extra, y0,  z0)
	    corner2 = P(x20 + extra, y10, z10)
	    east_edge.simple_pocket("Debug", corner1, corner2, radius, "t")

class FrameEdge(Part):
    """ *FrameEdge*: Represents the north or south edge of the frame.
    """

    def __init__(self, up, name, is_north, debug=False):
	""" *FrameEdge*: Initialize the *FrameEdge* object (i.e. *self*.)
	"""

	# Standard initialization sequence:
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(is_north, bool)
	assert isinstance(debug, bool)
	frame_edge = self
	Part.__init__(frame_edge, up, name)

	# Stuff argument into *frame_edge*:
	frame_edge.is_north_b = is_north
	frame_edge.debug_b = debug

    def construct(self):
	""" *FrameEdge*: Construct the *FrameEdge* object (i.e. *self*.)
	"""

	# Grab some *Part*'s out of *frame_edge* (i.e. *self*.)
	frame_edge    = self
	stencil_frame = frame_edge.up
	bottom_clamp  = stencil_frame.bottom_clamp_
	east_clamp    = stencil_frame.east_clamp_
	east_edge     = stencil_frame.east_edge_
	west_edge     = stencil_frame.west_edge_

	# Grab some values out of the *Part*'s:
	bottom_clamp_bsw = bottom_clamp.bsw
	bottom_clamp_tne = bottom_clamp.tne
	debug            = frame_edge.debug_b
	east_clamp_bsw   = east_clamp.bsw
	east_clamp_tne   = east_clamp.tne
	east_edge_bsw    = east_edge.bsw
	east_edge_tne    = east_edge.tne
	is_north         = frame_edge.is_north_b
	west_edge_bsw    = west_edge.bsw

	# Define some X coordinates:
	zero = L()
	x40 = east_clamp_tne.x
	x20 = zero
	x0  = west_edge_bsw.x

	# Define some Y coordinates:
	dy  = L(inch=1.000)
	y20 = east_edge_tne.y
	y15 = east_edge_tne.y - dy
	y10 = zero
	y5  = east_edge_bsw.y + dy
	y0  = east_edge_bsw.y

	# Define some Z coordinates:
	dz  = L(inch=0.800)
	z10 = east_edge_tne.z + dz
	z5  = zero
	z0  = east_edge_tne.z

	# Create a block out of *material*:
	material = Material("Plastic", "HDPE")
	if is_north:
	    color = Color("dark_green")
	    corner1 = P(x0,  y15, z0)
	    corner2 = P(x40, y20, z10)
	    comment = "North_Frame_Edge_Block"
	else:
	    color = Color("lime")
	    corner1 = P(x0,  y0, z0)
	    corner2 = P(x40, y5, z10)
	    comment = "South_Frame_Edge_Block"
	frame_edge.block(comment, material, color, corner1, corner2, "")

	# Mount the *frame_edge* onto a tooling block:
	extra_dx = L(inch="1/4")
	extra_dy = L(inch="1/4")
	frame_edge.vice_mount("Top_Vice", "t", "n", "l", extra_dx, extra_dy)
	frame_edge.tooling_plate_drill("Top_Plate_Drill", (0, 3, 6, 9, 12, 15), (0, 1), [])
	frame_edge.tooling_plate_mount("Top_Plate")

	# Drill out the fastener holes:
	if is_north:
	    frame_edge.fasten("NE_NE", stencil_frame.ne_ne_fastener_, "close")
	    frame_edge.fasten("NE_NW", stencil_frame.ne_nw_fastener_, "close")
	    frame_edge.fasten("NE_SE", stencil_frame.ne_se_fastener_, "close")
	    frame_edge.fasten("NE_SW", stencil_frame.ne_sw_fastener_, "close")
	    frame_edge.fasten("NW_NE", stencil_frame.nw_ne_fastener_, "close")
	    frame_edge.fasten("NW_NW", stencil_frame.nw_nw_fastener_, "close")
	    frame_edge.fasten("NW_SE", stencil_frame.nw_se_fastener_, "close")
	    frame_edge.fasten("NW_SW", stencil_frame.nw_sw_fastener_, "close")
	else:
	    frame_edge.fasten("SE_NE", stencil_frame.se_ne_fastener_, "close")
	    frame_edge.fasten("SE_NW", stencil_frame.se_nw_fastener_, "close")
	    frame_edge.fasten("SE_SE", stencil_frame.se_se_fastener_, "close")
	    frame_edge.fasten("SE_SW", stencil_frame.se_sw_fastener_, "close")
	    frame_edge.fasten("SW_NE", stencil_frame.sw_ne_fastener_, "close")
	    frame_edge.fasten("SW_NW", stencil_frame.sw_nw_fastener_, "close")
	    frame_edge.fasten("SW_SE", stencil_frame.sw_se_fastener_, "close")
	    frame_edge.fasten("SW_SW", stencil_frame.sw_sw_fastener_, "close")

	corner_radius = L(inch="1/16")
	frame_edge.rectangular_contour("Exterior_Contour", corner_radius)

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
	stencil.thickness_l   = thickness   = L(mm=0.12)

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
	stencil_frame.stencil_      = Stencil(stencil_frame,     "Stencil",           debug=debug)
	stencil_frame.east_edge_    = EastEdge(stencil_frame,    "East_Edge",         debug=debug)
	stencil_frame.east_clamp_   = Clamp(stencil_frame,       "East_Clamp", True,  debug=debug)
	stencil_frame.west_clamp_   = Clamp(stencil_frame,       "West_Clamp", False, debug=debug)
	stencil_frame.bottom_clamp_ = BottomClamp(stencil_frame, "Bottom_Clamp",      debug=debug) 
	stencil_frame.north_edge_   = FrameEdge(stencil_frame,   "North_Edge", True,  debug=debug)
	stencil_frame.south_edge_   = FrameEdge(stencil_frame,   "South_Edge", False, debug=debug)
	stencil_frame.west_edge_    = WestEdge(stencil_frame,    "West_Edge",         debug=debug)

	# Create a whole bunch of fasteners:
	stencil_frame.ne_ne_fastener_ = Fastener(stencil_frame, "NE_NE")
	stencil_frame.ne_nw_fastener_ = Fastener(stencil_frame, "NE_NW")
	stencil_frame.ne_se_fastener_ = Fastener(stencil_frame, "NE_SE")
	stencil_frame.ne_sw_fastener_ = Fastener(stencil_frame, "NE_SW")
	stencil_frame.nw_ne_fastener_ = Fastener(stencil_frame, "NW_NE")
	stencil_frame.nw_nw_fastener_ = Fastener(stencil_frame, "NW_NW")
	stencil_frame.nw_se_fastener_ = Fastener(stencil_frame, "NW_SE")
	stencil_frame.nw_sw_fastener_ = Fastener(stencil_frame, "NW_SW")
	stencil_frame.se_ne_fastener_ = Fastener(stencil_frame, "SE_NE")
	stencil_frame.se_nw_fastener_ = Fastener(stencil_frame, "SE_NW")
	stencil_frame.se_se_fastener_ = Fastener(stencil_frame, "SE_SE")
	stencil_frame.se_sw_fastener_ = Fastener(stencil_frame, "SE_SW")
	stencil_frame.sw_ne_fastener_ = Fastener(stencil_frame, "SW_NE")
	stencil_frame.sw_nw_fastener_ = Fastener(stencil_frame, "SW_NW")
	stencil_frame.sw_se_fastener_ = Fastener(stencil_frame, "SW_SE")
	stencil_frame.sw_sw_fastener_ = Fastener(stencil_frame, "SW_SW")

	# *west_clamp* and *bottom_clamp* fasteners:
	stencil_frame.wcbc_ne_fastener_ = Fastener(stencil_frame, "WCBC_NE")
	stencil_frame.wcbc_nw_fastener_ = Fastener(stencil_frame, "WCBC_NW")
	stencil_frame.wcbc_cw_fastener_ = Fastener(stencil_frame, "WCBC_CW")
	stencil_frame.wcbc_se_fastener_ = Fastener(stencil_frame, "WCBC_SE")
	stencil_frame.wcbc_sw_fastener_ = Fastener(stencil_frame, "WCBC_SW")

	# *east_clamp* and *east_edge* fasteners:
	stencil_frame.ecee_ne_fastener_ = Fastener(stencil_frame, "ECEE_NE")
	stencil_frame.ecee_nw_fastener_ = Fastener(stencil_frame, "ECEE_NW")
	stencil_frame.ecee_ce_fastener_ = Fastener(stencil_frame, "ECEE_CE")
	stencil_frame.ecee_se_fastener_ = Fastener(stencil_frame, "ECEE_SE")
	stencil_frame.ecee_sw_fastener_ = Fastener(stencil_frame, "ECEE_SW")

	# Tension screws:
	stencil_frame.webc_bn_fastener_ = Fastener(stencil_frame, "WEBC_BN")
	stencil_frame.webc_bs_fastener_ = Fastener(stencil_frame, "WEBC_BS")
	stencil_frame.webc_tn_fastener_ = Fastener(stencil_frame, "WEBC_TN")
	stencil_frame.webc_ts_fastener_ = Fastener(stencil_frame, "WEBC_TS")

    def construct(self):
	""" *StencilFrame*: Construct the *StencilFrame* assembly (i.e. *self*.)
	"""
                          
	# Grab some *Part*'s from *stencil_frame* (i.e. *self*):
	stencil_frame = self
	bottom_clamp  = stencil_frame.bottom_clamp_
	east_clamp     = stencil_frame.east_clamp_
	east_edge     = stencil_frame.east_edge_
	north_edge    = stencil_frame.north_edge_
	stencil       = stencil_frame.stencil_
	south_edge    = stencil_frame.south_edge_
	west_clamp    = stencil_frame.west_clamp_
	west_edge     = stencil_frame.west_edge_

	# Grab some values from *Part*'s:
	bottom_clamp_bsw = bottom_clamp.bsw
	bottom_clamp_dx  = bottom_clamp.dx
	bottom_clamp_tne = bottom_clamp.tne
	east_clamp_bsw   = east_clamp.bsw
	east_clamp_dx    = east_clamp.dx
	east_clamp_tne   = east_clamp.tne
	east_edge_bsw    = east_edge.bsw
	east_edge_dx     = east_edge.dx
	east_edge_tne    = east_edge.tne
	south_edge_bsw   = south_edge.bsw
	south_edge_dy    = south_edge.dy
	south_edge_tne   = south_edge.tne
	stencil_bsw      = stencil.bsw
	stencil_tne      = stencil.tne
	north_edge_bsw   = north_edge.bsw
	north_edge_dy    = north_edge.dy
	north_edge_tne   = north_edge.tne
	west_clamp_bsw   = west_clamp.bsw
	west_clamp_dx    = west_clamp.dx
	west_clamp_tne   = west_clamp.tne
	west_edge_bsw    = west_edge.bsw
	west_edge_dx     = west_edge.dx
	west_edge_dz     = west_edge.dz
	west_edge_tne    = west_edge.tne

	# Define some X coordinates:
	# *ramp_dx* is the overlap between *north_edge*/*south edge* and *east_edge*:
	# *north_edge*/*south_edge* overlap with *east_edge* X coordinates:
	ramp_dx = east_clamp_tne.x - east_edge_bsw.x
	x50 = east_clamp_tne.x
	x48 = east_clamp_tne.x - east_clamp_dx/4
	x46 = east_clamp_bsw.x + east_clamp_dx/4
	x40 = east_edge_bsw.x
	# *bottom clamp + *west_clamp*:
	x19 = west_clamp_tne.x
	x17 = west_clamp_tne.x - west_clamp_dx/4
	x13 = west_clamp_bsw.x + west_clamp_dx/4
	x11 = west_clamp_bsw.x
	# *west_edge*:
	x10 = west_edge_tne.x
	x6  = west_edge_tne.x - west_edge_dx/4
	x2  = west_edge_bsw.x + west_edge_dx/4
	x0  = west_edge_bsw.x

	# Define some Y coordinates:
	# *north_edge*:
	zero = L()
	stencil_gap = north_edge_bsw.y - stencil_tne.y
	y40 = north_edge_tne.y
	y48 = north_edge_tne.y - north_edge.dy/4
	y46 = north_edge_bsw.y + north_edge.dy/4
	y30 = north_edge_bsw.y
	y28 = north_edge_bsw.y - stencil_gap/2
	y25 = stencil_tne.y
	y20 = zero
	y15 = stencil_bsw.y
	y12 = south_edge_tne.y + stencil_gap/2
	y10 = south_edge_tne.y
	y8  = south_edge_tne.y - south_edge.dy/4
	y6  = south_edge_bsw.y + south_edge.dy/4
	y0  = south_edge_bsw.y

	# Define zome Z coordinates:
	z20 = north_edge_tne.z
	z10 = west_edge_tne.z
	z7  = west_edge_tne.z - west_edge_dz/4
	z3  = west_edge_bsw.z + west_edge_dz/4
	z0  = west_edge_bsw.z

	# The 16 screws that bolt together the frame:
	stencil_frame.ne_ne_fastener_.configure(P(x48, y48, z0), P(x48, y48, z20), "#4-40")
	stencil_frame.ne_nw_fastener_.configure(P(x46, y48, z0), P(x46, y48, z20), "#4-40")
	stencil_frame.ne_se_fastener_.configure(P(x48, y46, z0), P(x48, y46, z20), "#4-40")
	stencil_frame.ne_sw_fastener_.configure(P(x46, y46, z0), P(x46, y46, z20), "#4-40")
	stencil_frame.nw_ne_fastener_.configure(P(x6,  y48, z0), P(x6,  y48, z20), "#4-40")
	stencil_frame.nw_nw_fastener_.configure(P(x2,  y48, z0), P(x2,  y48, z20), "#4-40")
	stencil_frame.nw_se_fastener_.configure(P(x6,  y46, z0), P(x6,  y46, z20), "#4-40")
	stencil_frame.nw_sw_fastener_.configure(P(x2,  y46, z0), P(x2,  y46, z20), "#4-40")
	stencil_frame.se_ne_fastener_.configure(P(x48, y8,  z0), P(x48, y8,  z20), "#4-40")
	stencil_frame.se_nw_fastener_.configure(P(x46, y8,  z0), P(x46, y8,  z20), "#4-40")
	stencil_frame.se_se_fastener_.configure(P(x48, y6,  z0), P(x48, y6,  z20), "#4-40")
	stencil_frame.se_sw_fastener_.configure(P(x46, y6,  z0), P(x46, y6,  z20), "#4-40")
	stencil_frame.sw_ne_fastener_.configure(P(x6,  y8,  z0), P(x6,  y8,  z20), "#4-40")
	stencil_frame.sw_nw_fastener_.configure(P(x2,  y8,  z0), P(x2,  y8,  z20), "#4-40")
	stencil_frame.sw_se_fastener_.configure(P(x6,  y6,  z0), P(x6,  y6,  z20), "#4-40")
	stencil_frame.sw_sw_fastener_.configure(P(x2,  y6,  z0), P(x2,  y6,  z20), "#4-40")
        
	# The 5 screws that bolt the *west_clamp* and *bottom_clamp* (i.e. "wcbc") together:
	stencil_frame.wcbc_ne_fastener_.configure(P(x17, y28, z0), P(x17, y28, z10), "#4-40")
	stencil_frame.wcbc_nw_fastener_.configure(P(x13, y28, z0), P(x13, y28, z10), "#4-40")
	stencil_frame.wcbc_cw_fastener_.configure(P(x13, y20, z0), P(x13, y20, z10), "#4-40")
	stencil_frame.wcbc_se_fastener_.configure(P(x17, y12, z0), P(x17, y12, z10), "#4-40")
	stencil_frame.wcbc_sw_fastener_.configure(P(x13, y12, z0), P(x13, y12, z10), "#4-40")

	# The 5 screws that bolt the *east_clamp* and *east_edge* (i.e. "ecee") together:
	stencil_frame.ecee_ne_fastener_.configure(P(x48, y28, z0), P(x48, y28, z10), "#4-40")
	stencil_frame.ecee_nw_fastener_.configure(P(x46, y28, z0), P(x46, y28, z10), "#4-40")
	stencil_frame.ecee_ce_fastener_.configure(P(x48, y20, z0), P(x48, y20, z10), "#4-40")
	stencil_frame.ecee_se_fastener_.configure(P(x46, y12, z0), P(x46, y12, z10), "#4-40")
	stencil_frame.ecee_sw_fastener_.configure(P(x48, y12, z0), P(x48, y12, z10), "#4-40")

	# Fasteners for joining *west_edge* to *bottom_clamp* (i.e. "webc"):
	stencil_frame.webc_bn_fastener_.configure(P(x0, y25, z3), P(x11, y25, z3), "#6-32")
	stencil_frame.webc_bs_fastener_.configure(P(x0, y15, z3), P(x11, y15, z3), "#6-32")
	stencil_frame.webc_tn_fastener_.configure(P(x0, y25, z7), P(x11, y25, z7), "#6-32")
	stencil_frame.webc_ts_fastener_.configure(P(x0, y15, z7), P(x11, y15, z7), "#6-32")

class WestEdge(Part):
    """ *WestEdge*: Represents the west edge of the frame.
    """

    def __init__(self, up, name, debug=False):
	""" *WestEdge*: Initialize the *WestEdge* object (i.e. *self*):
	"""

	# Standard initialization sequence:
	assert isinstance(up, Part) or up == None
	assert isinstance(name, str) and not ' ' in name
	assert isinstance(debug, bool)
	west_edge = self
	Part.__init__(west_edge, up, name)
	west_edge.debug_b = debug

    def construct(self):
	""" *WestEdge*: Construct the *WestEdge* object (i.e. *self*.) """

	# Grab some *Part*'s from *west_edge* (i.e. *self*):
	west_edge     = self
	stencil_frame = west_edge.up
	bottom_clamp  = stencil_frame.bottom_clamp_
	east_edge     = stencil_frame.east_edge_
	north_edge    = stencil_frame.north_edge_
	south_edge    = stencil_frame.south_edge_

	# Grab some values from the *Part*'s:
	bottom_clamp_bsw = bottom_clamp.bsw
	east_edge_bsw    = east_edge.bsw
	east_edge_tne    = east_edge.tne
	north_edge_tne   = north_edge.tne
	south_edge_bsw   = south_edge.bsw

	# Define some X coordinates:
	zero = L()
	gap_dx = L(inch="1/2")
	dx = L(inch=1.25)
	x20 = bottom_clamp_bsw.x - gap_dx
	z10 = bottom_clamp_bsw.x - gap_dx - dx/2
	x0  = bottom_clamp_bsw.x - gap_dx - dx

	# Define some Y coordinates:
	y20 = north_edge_tne.y
	y0  = south_edge_bsw.y

	# Define some Z coordinates:
	z20 = east_edge_tne.z
	z0  = east_edge_bsw.z

	# Start with a block of *material*:
	material = Material("Plastic", "HDPE")
	color = Color("yellow")
	corner1 = P(x0,  y0,  z0)
	corner2 = P(x20, y20, z20)
	west_edge.block("West_Edge_Block", material, color, corner1, corner2, "")

	# Mount the *west_edge* on a tooling plate:
	extra_dx = L(inch="1/4")
	extra_dy = L(inch="1/4")
	west_edge.vice_mount("Top_Vice", "t", "e", "l", extra_dx, extra_dy)
	west_edge.tooling_plate_drill("Vice_Holes", (0, 3, 6, 9, 12), (0, 1), [])
	west_edge.tooling_plate_mount("Top_Plate")

	corner_radius = L(inch="1/16")
	west_edge.rectangular_contour("Exterior_Contour", corner_radius)

	# Drill out the fastener holes:
	west_edge.fasten("NW_NE", stencil_frame.nw_ne_fastener_, "thread")
	west_edge.fasten("NW_NW", stencil_frame.nw_nw_fastener_, "thread")
	west_edge.fasten("NW_SE", stencil_frame.nw_se_fastener_, "thread")
	west_edge.fasten("NW_SW", stencil_frame.nw_sw_fastener_, "thread")
	west_edge.fasten("SW_NE", stencil_frame.sw_ne_fastener_, "thread")
	west_edge.fasten("SW_NW", stencil_frame.sw_nw_fastener_, "thread")
	west_edge.fasten("SW_SE", stencil_frame.sw_se_fastener_, "thread")
	west_edge.fasten("SW_SW", stencil_frame.sw_sw_fastener_, "thread")

	# Remount with west edge facing up:
	west_edge.vice_mount("West_Vice", "w", "b", "l", zero, zero)
	west_edge.fasten("WEBC_BN", stencil_frame.webc_bn_fastener_, "close")
	west_edge.fasten("WEBC_BS", stencil_frame.webc_bs_fastener_, "close") 
	west_edge.fasten("WEBC_TN", stencil_frame.webc_tn_fastener_, "close")
	west_edge.fasten("WEBC_TS", stencil_frame.webc_ts_fastener_, "close")

if __name__ == "__main__":
    main()
