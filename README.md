# YCircuit #
-------------------------------------------------------------------------------

In my experience with drawing pretty schematics that could create publication quality exports, I was told about [XCircuit](www.opencircuitdesign.com/xcircuit/). And while it is true that XCircuit produces beautiful schematics, its UI and UX left a lot to be desired (in my opinion). I decided to start working on an alternative whose output could rival that of XCircuit's in my spare time and as a result, YCircuit was born.

Just to be clear, this tool is intended to be used only for drawing circuit schematics. This is not intended to be a circuit simulator or anything more than a drawing program. This might change in the future, but I think it is useful to spell out exactly what YCircuit is designed to do.

YCircuit is written in [Python 3](https://www.python.org) and uses [PyQt5](https://www.riverbankcomputing.com/software/pyqt/download) as the GUI framework. The move from PyQt4 to PyQt5 makes this a little more future-proof but it comes with some tradeoffs, the worst of which is the inability to export to EPS.

Please check out the [YCircuit website](https://siddharthshekar.bitbucket.io/public/ycircuit) for further details and some tutorials! Binary files for Windows and Linux are available for download in the [downloads section](https://bitbucket.org/siddharthshekar/ycircuit/downloads).
