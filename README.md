# YCircuit #
-------------------------------------------------------------------------------

Because XCircuit produces amazing output but has unintuitive GUI and PyCircuit was already taken ):.

Written in Python. Currently built using PyQt, but this may change in the future.

Current status is pre-alpha at best.

## Installation ##
-------------------------------------------------------------------------------

You can download the zip file from this repo or clone it manually using the command:

`git clone git@bitbucket.org/siddharthshekar/ycircuit.git`

This repo is currently private, so I'm not sure if this command actually works. Send me an email if you're having issues.

## Dependencies ##
-------------------------------------------------------------------------------

YCircuit currently has the following dependencies:

  * Python - tested on 2.7.11
  * PyQt4 - for rendering the GUI
  * NumPy - for handling some of the math (may not even be entirely necessary)

I plan to add some additional functionality later that will allow for LaTeX support, so the dependency list may grow. The easiest way to satisfy all dependencies is to use Anaconda (<https://www.continuum.io/downloads>). This is what I use also, and so we can be sure that the environments are (more or less) similar.

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
    * Wire
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

## Organization ##
-------------------------------------------------------------------------------

Currently, the files have the following uses:

  * test.py: Contains mappings from UI callbacks to actual functions. Used for launching the GUI.
  * schematic_mainWindow.*: The UI file contains the output of Qt Designer while the py file is the exported version of the same.
  * drawingitems.py: Contains the Grid class for creating the background grid in the GUI.
  * drawingarea.py: Handles implementations of functions for responding to UI callbacks. Captures and processes all keyboard and mouse events.
  * components.py: Defines item classes for creating and manipulating shapes.
  * Resources/*.pkl: Contains binary files that have the various symbols. Schematics are also currently saved as a .pkl file. Try loading inverter.pkl for an example inverter schematic.

## Feedback ##
-------------------------------------------------------------------------------

At this point, there probably are a few million bugs in this program. I'd appreciate it if you could file bug reports as and when you encounter them. Thanks! 
