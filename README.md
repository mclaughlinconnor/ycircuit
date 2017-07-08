# YCircuit #
-------------------------------------------------------------------------------

In my experience with drawing pretty schematics that could create publication quality exports, I was told about [XCircuit](www.opencircuitdesign.com/xcircuit/). And while it is true that XCircuit produces beautiful schematics, its UI and UX left a lot to be desired (in my opinion). I decided to start working on an alternative whose output could rival that of XCircuit's in my spare time and as a result, YCircuit was born.

Just to be clear, this tool is intended to be used only for drawing circuit schematics. This is not intended to be a circuit simulator or anything more than a drawing program. This might change in the future, but I think it is useful to spell out exactly what YCircuit is intended to do.

YCircuit is written in [Python 3](https://www.python.org) and uses [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download) as the GUI framework. The move from PyQt4 to PyQt5 makes this a little more future-proof but it comes with some tradeoffs, the worst of which is the inability to export to EPS.

## Installation ##
-------------------------------------------------------------------------------

You can download the zip file from this repo or, if you have Git installed on your machine, clone it manually using the command:

`git clone https://bitbucket.org/siddharthshekar/ycircuit.git`

The master branch is the latest stable branch and this is likely the one you will end up using. Develop branch is where new code is tested so expect a few more bugs than on the master branch. Please report issues using the [issue tracker](https://bitbucket.org/siddharthshekar/ycircuit/issues?status=new&status=open) on Bitbucket.

## Dependencies ##
-------------------------------------------------------------------------------

YCircuit currently has the following dependencies:

  * Python - tested on 3.5.2 (**Note**: This version is incompatible with Python 2.x)
  * PyQt5 - for rendering the GUI
  * SymPy - for handling LaTeX inputs
  * NumPy - for handling some of the math

The easiest way to satisfy all dependencies is to use [Anaconda](https://www.continuum.io/downloads). This is what I use also, and so we can be sure that the environments are (more or less) similar.

## Usage ##
-------------------------------------------------------------------------------

The software is fairly easy to use (partially because of the limited feature set). To start the software, navigate to the directory where you extracted the zip or cloned the repository and run the following command:

`python top.py`

A lot of the keyboard shortcuts and mouse interactions have been based on those found in [Cadence's Virtuoso Schematic editor](https://www.cadence.com/content/cadence-www/global/en_US/home/tools/custom-ic-analog-rf-design/circuit-design/virtuoso-schematic-editor.html). As a result, the interface is best navigated with a keyboard and mouse. Scrolling with the mouse wheel zooms in and out of the schematic, while Ctrl (Shift) scrolling pans vertically (horizontally).

As of this point in time, the following options are available:

  * File operations (Alt+F)
    * Create a new schematic (Ctrl+N)
    * Save and load symbols (.sym files) (Ctrl+Shift+S, Ctrl+Shift+L)
    * Save and load schematics (.sch files) (Ctrl+S, Ctrl+L)
    * Export symbol or schematic as a PDF, SVG, JPEG, PNG or BMP file (Ctrl+E)
        * While exporting to EPS was natively supported by PyQt4, the Qt team decided to drop this during the transition to Qt5. As a result, EPS is no longer supported by YCircuit. If you need a vector-based exporting option, use the PDF or SVG options.
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
        * LaTeX support is present but not all available font options apply. Font sizes are currently mismatched but will be fixed later on. This, of course, assumes that you have a suitable LaTeX distribution already installed. Check [here](https://bitbucket.org/siddharthshekar/ycircuit.git/raw/master/Resources/Examples/TIA noise/tia_noise.png) in order to get an idea of what the LaTeX output looks like.
        * An option for a more coherent look would be to use the symbols button in the text editor.
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

Item shapes can typically be edited by selecting them and pressing the E key. The contents of text box items can be edited by double clicking on the text box. It is recommended to use the Wire symbol for drawing schematic nets. Nets support automatically inserting dots at appropriate intersections and split and merge as required. The Line shape should be thought of as being a polyline that should be used for drawing lines at arbitrary angles.

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

  * ~Edit shapes (click and drag to resize rect, for example)~
  * Create projects (so each schematic has its own folder to dump LaTeX images in)
  * Copying items in one schematic should allow pasting on to another open schematic

## Feedback ##
-------------------------------------------------------------------------------

At this point, there probably are a few million bugs in this program. I'd appreciate it if you could file bug reports as and when you encounter them. Thanks!
