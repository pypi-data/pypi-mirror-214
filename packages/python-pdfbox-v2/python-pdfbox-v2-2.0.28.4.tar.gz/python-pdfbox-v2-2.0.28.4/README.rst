.. -*- rst -*-

python-pdfbox
=============


Package Description
-------------------
This prject is a fork of python-pdfbox. After the update of pdfbox,
the current version for apache-pdfbox 3.x has breaking changes.

To make sure the the python-wrapper is still useable, this fork is in place.
To use just replace the pip install python-pdfbox with pip install python-pdfbox-v2

Provides a simple Python 3 interface to the 
`Apache PDFBox <https://pdfbox.apache.org/>`_
command-line tools.
          
Requirements
------------
Aside from Python 3 and those packages specified in
`setup.py <https://github.com/lebedov/python-pdfbox/blob/master/setup.py>`_,
python-pdfbox requires ``java`` to be present in the system path.

Some users have reported `issues on
MacOS <https://github.com/lebedov/python-pdfbox/issues/14>`_ with certain
versions of Java. If you encounter such issues, try a recent release of OpenJDK
(14 or later).

Installation
------------
The package may be installed as follows: ::

    pip install python-pdfbox

One may specify the location of the PDFBox jar file via the ``PDFBOX``
environmental variable. If not set, python-pdfbox looks for the jar file
in the platform-specific user cache directory and automatically downloads
the latest available version below 3.0.0 and caches it if not present.

Usage
-----
The interface currently exposes only several features in PDFBox (text extraction, conversion to images, extraction
of images): ::

    import pdfbox
    p = pdfbox.PDFBox()
    p.extract_text('/path/to/my_file.pdf')   # writes text to /path/to/my_file.txt
    p.pdf_to_images('/path/to/my_file.pdf')  # writes images to /path/to/my_file1.jpg, /path/to/my_file2.jpg, etc.
    p.extract_images('/path/to/my_file.pdf') # writes images to /path/to/my_file-1.png, /path/to/my_file-2.png, etc.

Notes
-----
Owing to a change in command line interface, python-pdfbox cannot 
currently use PDFBox 3.0.0.

Development
-----------
The latest release of the package may be obtained from
`GitHub <https://github.com/lebedov/python-pdfbox>`_.

Author
------
See the included `AUTHORS.rst 
<https://github.com/lebedov/python-pdfbox/blob/master/AUTHORS.rst>`_ file for more 
information.

License
-------
This software is licensed under the
`Apache 2.0 License <https://opensource.org/licenses/Apache-2.0>`_.
See the included `LICENSE.rst 
<https://github.com/lebedov/python-pdfbox/blob/master/LICENSE.rst>`_ file for more 
information.
