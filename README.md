# YCircuit #

-------------------------------------------------------------------------------
Because XCircuit produces amazing output but has unintuitive GUI and PyCircuit was already taken ):.

Written in Python. Currently built using PyQt, but this may change in the future.

## Installation ##

-------------------------------------------------------------------------------
You can download the zip file from this repo or clone it manually using the command:
`git clone git@bitbucket.org/siddharthshekar/ycircuit.git`

This repo is currently private, so I'm not sure if this command actually works. Send me an email if you're having issues.

## Dependencies ##

-------------------------------------------------------------------------------
YCircuit currently has the following dependencies:
  * PyQt4 - for rendering the GUI
  * NumPy - for handling some of the math (may not even be entirely necessary)

I plan to add some additional functionality later that will allow for LaTeX support, so the dependency list may grow. The easiest way to satisfy all dependencies is to use Anaconda <https://www.continuum.io/downloads>. This is what I use also, and so we can be sure that the environments are (more or less) similar.

## Usage ##

-------------------------------------------------------------------------------

The software is fairly easy to use (partially because of the limited feature set). To start the software, run the following command
`python test.py`

As of this point in time, the following options are available:
  * Saving and loading
    * Save and load symbols
    * Save and load schematics
    * Export symbol or schematic as a JPEG or PNG
  * Editing
    * Delete
    * Move
    * Copy
    * Rotate
    * Mirror
    * Change pen colour, style and width
    * Change fill colour and style
  * Shapes
    * Line (Same as Symbols -> Wire)
    * Rectangle
    * Circle
    * Ellipse
  * Symbols
    * Resistor
    * Capacitor
    * Ground
    * Connectivity dot
    * Transistors
      * NFET (With and without arrow)
      * PFET (With and without arrow)
      * NPN BJT
      * PNP BJT

At this point, item shapes cannot be edited once they are drawn. Further, wires are drawn as one long and continuous wire - the implication being that wire segments are not individually selectable.

## Feedback ##

-------------------------------------------------------------------------------

At this point, there probably are 104540295845 bugs in this program. I'd appreciate it if you could file bug reports as and when you encounter them. Thanks! 
