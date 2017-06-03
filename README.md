# YCircuit #
-------------------------------------------------------------------------------

Because XCircuit produces amazing output but has unintuitive GUI and PyCircuit was already taken ):.

Written in Python. Currently built using PyQt, but this may change in the future.

Current status is pre-alpha at best.

## Installation ##
-------------------------------------------------------------------------------

You can download the zip file from this repo or clone it manually using the command:

`git clone https://bitbucket.org/siddharthshekar/ycircuit.git`

The master branch is the latest stable branch and this is likely the one you will end up using. Develop branch is where new code is tested so expect a few more bugs than on the master branch. Send me an email if you're having issues.

## Dependencies ##
-------------------------------------------------------------------------------

YCircuit currently has the following dependencies:

  * Python - tested on 2.7.11
  * PyQt4 - for rendering the GUI
  * matplotlib - for handling LaTeX inputs
  * NumPy - for handling some of the math (may not even be entirely necessary)

The easiest way to satisfy all dependencies is to use [Anaconda](https://www.continuum.io/downloads). This is what I use also, and so we can be sure that the environments are (more or less) similar.

## Usage ##
-------------------------------------------------------------------------------

The software is fairly easy to use (partially because of the limited feature set). To start the software, run the following command

`python top.py`

As of this point in time, the following options are available:

  * Saving and loading (Alt+F)
    * Save and load symbols (.sym files) (Ctrl+Shift+S, Ctrl+Shift+L)
    * Save and load schematics (.sch files) (Ctrl+S, Ctrl+L)
    * Export symbol or schematic as a PDF, EPS, JPEG, PNG or BMP file (Ctrl+E)
  * Editing (Alt+E)
    * Undo (Ctrl+Z)
    * Redo (Ctrl+Y)
    * Delete (D)
    * Move (M)
    * Copy (C)
    * Rotate (R)
    * Mirror (Shift+R)
    * Change pen colour, style and width (Alt+E->C,P,W)
    * Change fill colour and style
  * Shapes (Alt+A)
    * Line (Alt+A->L)
    * Rectangle (Alt+A->R)
    * Circle (Alt+A->C)
    * Ellipse (Alt+A->E)
    * Arcs (3-point and 4-point Bezier curves) (Alt+A->A)
    * Text box (with support for bold, italics, underline, overline, subscript and superscript) (Alt+A->T)
        * LaTeX support is present, but each new expression is saved as a separate image for now. Font sizes are currently mismatched but will be fixed later on
        * An option for a more coherent look would be to use symbols
  * Symbols (Alt+S)
    * Wire (Right click to change the angle of the wire!) (Alt+S->W)
    * Resistor (Alt+S->R)
    * Capacitor (Alt+S->C)
    * Ground (Alt+S->G)
    * Connectivity dot (Alt+S->D)
    * Transistors (Alt+S->T)
        * NFET (With and without arrow) (Alt+S->T->N)
        * PFET (With and without arrow) (Alt+S->T->P)
        * NPN BJT
        * PNP BJT
    * Sources (Alt+S->S)
        * DC (both voltage and current) (Alt+S->S->D->V,C)
        * AC (Alt+S->S->A)
        * Controlled sources (all 4 types) (Alt+S->S->C)

At this point, item shapes cannot be edited once they are drawn. Further, wires are drawn as one long and continuous wire - the implication being that wire segments are not individually selectable.

An example output image would look something like this ([High res image](https://bitbucket.org/siddharthshekar/ycircuit/raw/master/Resources/Examples/Inverter/inverter.png)):

![Image not found ):](https://bitbucket.org/siddharthshekar/ycircuit/raw/master/Resources/Examples/Inverter/inverter_lowRes.png "Such a pretty inverter!")

## Organization ##
-------------------------------------------------------------------------------

Currently, the files have the following uses:

  * top.py: Contains mappings from UI callbacks to actual functions. Used for launching the GUI.
  * src/
    * gui/
        * ycircuit_mainWindow.*: The UI file contains the output of Qt Designer while the py file is the exported version of the same.
    * drawingitems.py: Contains the Grid class for creating the background grid in the GUI and the TextEditor class for handling editing of TextBox objects.
    * drawingarea.py: Handles implementations of functions for responding to UI callbacks. Captures and processes all keyboard and mouse events.
    * components.py: Defines item classes for creating and manipulating shapes.
    * commands.py: Defines command actions including how to handle undoing and redoing.
  * Resources/Symbols/
    * Standard/*.sym: Contains various commonly used standard symbols.
    * Custom/*.sym: Contains user defined symbols.
  * Schematics are currently saved as a .sch file. Try loading inverter.sch from the Resources/Examples directory for an example inverter schematic.

## TODOs ##
-------------------------------------------------------------------------------

This is an (incomplete) list of features that I would like to add at some point (in no particular order):

  * Edit shapes (click and drag to resize rect, for example)
  * Create projects (so each schematic has its own folder to dump LaTeX images in)
  * Copying items in one schematic should allow pasting on to another open schematic

## Feedback ##
-------------------------------------------------------------------------------

At this point, there probably are a few million bugs in this program. I'd appreciate it if you could file bug reports as and when you encounter them. Thanks!
