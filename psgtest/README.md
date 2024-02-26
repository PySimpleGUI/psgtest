<p align="center">
  <p align="center"><img width="238" height="135" src="https://pysimplegui.net/images/logos/psglogofull.svg"><p>

  <h2 align="center">psgtest</h2>
  <h2 align="center">A PySimpleGUI Application</h2>
</p>

Simple Python Testing

Run your Python programs using the interpreter version of your choice,
and display the output in a GUI window.









<p align="center"><img width="850" height="399" src="screenshot.gif"><p>



## Features

* Project testing application to perform regression, stress, and compatibility testing
* Run your Python test programs at the click of a button
* Test using any Python interpreter version
* Run batches of tests to perform regression testing and stress testing
* Get programs output in individual tabs for easy debugging

## Installation

### Using PIP with PyPI

The latest official release of PySimpleGUI products can be found on PyPI.  To pip install the demo applications from PyPI, use this command

#### If you use the command `python` on your computer to invoke Python (Windows):

`python -m pip install --upgrade psgtest`

#### If you use the command `python3` on your computer to invoke Python (Linux, Mac):

`python3 -m pip install --upgrade psgtest`

### Using PIP with GitHub

You can also pip install the PySimpleGUI Applications that are in the PySimpleGUI GitHub account.  The GitHub versions have bug fixes and new programs/features that have not yet been released to PyPI. To directly pip install from that repo:

#### If you use the command `python` on your computer to invoke Python (Windows):

```bash
python -m pip install --upgrade https://github.com/PySimpleGUI/psgtest/zipball/main
```

#### If you use the command `python3` on your computer to invoke Python (Linux, Mac):

```bash
python3 -m pip install --upgrade https://github.com/PySimpleGUI/psgtest/zipball/main
```



## Usage

Once installed, launch psgtest by typing the following in your command line:

`psgtest`

## About

This is an example of another utility used in the development of
PySimpleGUI that is being released for other PySimpleGUI users to use
either as a standalone tool or as example code / design pattern to
follow.

It can be challenging to manage multiple versions of Python and the
need to test across multiple versions.  Virtual Environments are one
approach that are often used.  psgtest does not use virtual
environments.  Instead, it invokes the Python interpreter of your
choice directly.

The advantage is that changing which version of Python that's used is
changed in a single drop-down menu selection as shown in the example
GIF above.  The session in the GIF shows launching the PySimpleGUI
main test harness using multiple versions of Python by selecting the
version from the drop-down at the top.

## Executing Multiple Programs

To run multiple programs, select the files to run from the list of
files on the left portion of the window.  Then click the "Run" button.


## Editing Programs

You can also edit the programs selected by clicking the "Edit" button.
You will need to set up your editor using the PySimpleGUI global
settings.  If you have pip installed a version of PySimpleGUI that's
4.53.0.14 or greater, then you can type `psgsettings` from the command
line.  You can also change the settings by calling `sg.main()` (or
typing from the command line `psgmain`).

## Specifying/Selecting Python Interpreter Locations

The Setup Window is where you enter the path to each version of Python
that you want to test with.  The settings are stored in a file and
thus will be saved from one run to another.

Selecting the version to use can be done in either the settings window
or using the drop-down menu in the main window.

## Output

The stdout and stderr from each program you execute are displayed in a
tab with a name that matches your filename.  Each program you run will
open a new tab.

In each tab you'll find 2 buttons that operate on the output shown in
that tab.

Use the `Copy To Clipboard` button to copy the contents of the output
to the clipboard.

Use the `Clear` button to delete the output.

The `Close Tab` button closes the tab as does the right click menu
item `Close`.  If you run the program again after closing the tab, the
old contents of the tab are retained and shown when the tab is
"re-opened".  (See the GIF above for an example)

## Make a Windows Shortcut

If you're running Windows, then you can use `psgshortcut` to make a
shortcut to the .pyw file (if you download psgtest from GitHub) or the
.py file (if you pip installed).  The icon for `psgtest` is in this
repo and is also included when you pip install psgtest.  It's in the
same folder as the gui.py file.

You can find the location of psgtest after pip installing it by
running psgtest, right clicking, and choosing "File Location".  You'll
be shown where the `gui.py` file is located (the name of the psgtest
program when pip installed).  It will usually be located in the
`site-packages` folder in a folder named `psgtest`.

## License & Copyright

Copyright 2023-2024 PySimpleSoft, Inc. and/or its licensors.

This is a free-to-use "Utility" and is licensed under the
PySimpleGUI License Agreement, a copy of which is included in the
license.txt file and also available at https://pysimplegui.com/eula.

Please see Section 1.2 of the license regarding the use of this Utility,
and see https://pysimplegui.com/faq for any questions.


## Contributing

We are happy to receive issues describing bug reports and feature
requests! If your bug report relates to a security vulnerability,
please do not file a public issue, and please instead reach out to us
at issues@PySimpleGUI.com.

We do not accept (and do not wish to receive) contributions of
user-created or third-party code, including patches, pull requests, or
code snippets incorporated into submitted issues. Please do not send
us any such code! Bug reports and feature requests should not include
any source code.

If you nonetheless submit any user-created or third-party code to us,
(1) you assign to us all rights and title in or relating to the code;
and (2) to the extent any such assignment is not fully effective, you
hereby grant to us a royalty-free, perpetual, irrevocable, worldwide,
unlimited, sublicensable, transferrable license under all intellectual
property rights embodied therein or relating thereto, to exploit the
code in any manner we choose, including to incorporate the code into
PySimpleGUI and to redistribute it under any terms at our discretion.
