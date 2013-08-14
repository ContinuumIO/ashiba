ashiba
======

Ashiba seeks to be an app building framework, allowing you to define layout with HTML or Enaml and write logic in Python.
No Javascript needed!

## Dependencies
* The only hard dependencies are Python 2.7 and *pyyaml*.
* To run all of the examples, you should also have *numpy* and *pandas* installed.
* In order to make use of the `build` functionality, you need *conda*.
* For the best overall experience, use the [Anaconda](https://store.continuum.io/cshop/anaconda/) Python distribution

## Getting Ashiba

1. Clone this repo.
2. Execute `python setup.py install` or `python setup.py develop`, as desired.

## How to run an Ashiba app
The `examples` folder contains several prewritten apps which showcase the workflow and capabilities of Ashiba.
After you have Ashiba installed, just run
    
    ashiba start path/to/app
    
for example, from the root of this repo:

    ashiba start examples/dataframes

## How to write an Ashiba app
### First steps

1. Navigate to a directory where you want your app to live.
2. Execute `ashiba init app_name`, where app_name can be whatever you want. 
    This will create a skeleton project in a directory with the same name.
3. There are three important files in the folder that you will edit:
    * myapp.html
    * handlers.py
    * settings.py

### settings.py
This file contains app settings such as:
*   Name of the app
*   Icon to use for the app
*   CSS theme to use
*   Data files, if any

Since settings.py is a Python file, you can use python code (e.g. os.path.whatever) when setting the values.

### myapp.html
* This is where the GUI for the app is laid out.
* An app template is used to wrap the HTML in this file, so you don't need to write boilerplate `<html>` or `<head>` tags.
* Everything in this file will end up inside a `<body><div class="container">`
* Bootstrap 2.3.2 is included in the wrapper template. 
  You are encouraged to make use of its grid system to lay out columns, etc.
* If you need to include additional CSS/JS/etc., you can access the header and footers of the wrapper template. 
  See `examples/dataframes/myapp.html` for an example.
* Any element whose state you want to be able to get or set in Python *must* have an id attribute.
* In addition, any non-form elements\* that you want to access in Python should have a `data-visible="true"` attribute.
    * \*Form elements include `input`s and `select`s. These are always accessible from Python, even without `data-visible`.
* From Python, you can set DOM properties for any object, even those without `data-visible`. 
  However, in order to get object-specific Python methods such as `set_image` or `add_tab`, you must include the `data-visible` attribute.

### handlers.py
* This is where the application logic is laid out.
* Function names that match the pattern /\_?.+\_\_.+\\(dom\\)/ define event handlers.
    * For example, if I want to handle the 'click' event on an HTML object with 'btn\_foo', the function definition would be `def btn_foo__click(dom):`.
    * Names with a leading underscore refer to classes. Thus, to bind an action to the click event on all controls with class 'control\_widget', the function definition would be `def _control_widget__click(dom):`.
* These handlers accept a single argument, the `dom` object. This contains the state of all of the `input`s, `select`s, and DOM elements with a `data-visible` attribute in the DOM.
* The `dom` object is dict-like, so changing the state of a DOM element is done like so: `dom['object']['property'] = value`
* Some items in the `dom` object will have special methods. 
  For example, if `select_stock` is a `select` tag in the HTML, one can call `dom['select_stock'].add_item('aapl', "Apple")` to add an item to the dropdown.
    * These subclasses of GenericDomElement are defined in `ashiba/dom.py`
