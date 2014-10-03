Ashiba Basics
==============

Ashiba Commands
----------------

init - creates a new empty ashiba project

build - creates a conda-recipe for the ashiba project and places it in build/
 
compile - compiles an app

start - run a compiled app in the browser

qt - run a compiled app in qt

clean - clean up the files created during the build command

--open-browser - automatically open the web browser

--recompile - force a recompile::

    ashiba start --recompile --open-browser .


Ashiba Files
----------------

There are three important files in the folder that are generated with the Ahiba init command:

+ ``myapp.html``
+ ``handlers.py``
+ ``settings.py``

``settings.py``
----------------

This file contains app settings such as:

+ Name of the app
+ Icon to use for the app
+ CSS theme to use
+ Data files, if any

Since settings.py is a Python file, you can use python code (e.g. os.path.whatever) when setting the values.


``myapp.html``
--------------

+ This is where the GUI for the app is laid out.
+ An app template is used to wrap the HTML in this file, so you don't need to write boilerplate ``<html>`` or ``<head>`` tags.
+ Everything in this file will end up inside a ``<body><div class="container">``
+ Bootstrap 2.3.2 is included in the wrapper template. 
  You are encouraged to make use of its grid system to lay out columns, etc.
+ If you need to include additional CSS/JS/etc., you can access the header and footers of the wrapper template. 
  See ``examples/dataframes/myapp.html`` for an example.
+ Any element whose state you want to be able to get or set in Python **must** have an id attribute.

+ In addition, any non-form elements* that you want to access in Python should have a ``data-visible="true"`` attribute.

    + Form elements include `input`s and `select`s. These are always accessible from Python, even without `data-visible`.


+ From Python, you can set DOM properties for any object, even those without `data-visible`. 
  However, in order to get object-specific Python methods such as `set_image` or `add_tab`, you must include the `data-visible` attribute.


``handlers.py``
----------------

+ This is where the application logic is laid out.

+ Function names that match the pattern /\_?.+\_\_.+\\(dom\\)/ define event handlers.
    + For example, if I want to handle the ``click`` event on an HTML object with 'btn\_foo', the function definition would be ``def btn_foo__click(dom):``.

    + Names with a leading underscore refer to classes. Thus, to bind an action to the click event on all controls with class ``control_widget``, the function definition would be ``def _control_widget__click(dom):``.

+ These handlers accept a single argument, the ``dom`` object. This contains the state of all of the ``input's, select's``, and DOM elements with a ``data-visible`` attribute in the DOM.

+ The ``dom`` object is dict-like, so changing the state of a DOM element is done like so: ``dom['object']['property'] = value``
+ Some items in the ``dom`` object will have special methods. 
  For example, if ``select_stock`` is a ``select`` tag in the HTML, one can call ``dom['select_stock'].add_item('aapl', "Apple")`` to add an item to the dropdown.

    + These subclasses of GenericDomElement are defined in ``ashiba/dom.py``