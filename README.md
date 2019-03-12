# Stencil Frame Design for Stainless Steel Stencils

This is a design for a 15cm by 10cm stainless steel stencil frame for printed circuit boards.

## Installation

In order to use this code please do the following:

        cd {somewhere}
        git clone https://github.com/waynegramlich/stencil_frame.git
        git clone https://github.com/waynegramlich/ezcad3.git
        sudo -H apt-get install openscad
        sudo -H apt-get install view3dscene

## Execution

To generate the parts, do the following:

        cd {somewhere}/stencil_frame
        ./stencil_frame.py
        view3dscene wrl/StencilFrame.wrl  # Use to view the generated stuff.

