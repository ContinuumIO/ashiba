====================================
Formatting and Displaying in Ashiba
====================================


The Ashiba GUI uses the HTML or Enaml layout located in the ``myapp.<html/enaml>`` file.


**HTML**

An app template is used to wrap the HTML in this file, eliminating the need for boilerplate <html> or <head> tags. Ashiba uses Bootstrap 2.3.2 in the wrapper template so follow the standard bootstrap conventions for the grid system and layout. Since everything in the ``myapp`` file is put in a ``<body><div class="container">`` the html is easy to write.

For example, a slider with values 1-100 and the selector starting at 50 is written like this::

    <div class="span4">
        <label>Slider</label>
        <input id="slider_year" type="range" class="plot_control"
            value="50" min="1" max="100" step="5">
    </div>

To create an image container you need nothing more than::

    <div class="span9">    
        <img id="img_name" data-visible="true"></img>
    </div>

A button is as easy as::
    
    <button class="btn btn-primary" id="mybutton">Press Button</button>


Take note of the ``data_visble`` attribute. Any non-form elements, such as set_image or add_tab, that you want to access in Python should have a ``data-visible="true"`` attribute. Form elements including inputs and selects and are always accessible from Python, even without ``data-visible`` set.

For more information on HTML components visit `Bootstrap.com <http://getbootstrap.com/2.3.2/index.html>`_.

If you need to include additional CSS/JS/etc., you can access the header and footers of the wrapper template. See ``examples/dataframes/myapp.html`` for an example.


**Enaml**

Enaml is Not A Markup Language. `Enaml <https://github.com/enthought/enaml>`_ is a library for creating professional quality user interfaces with minimal effort. Enaml combines a domain specific declarative language with a constraints based layout system to allow users to easily define rich UIs with complex and flexible layouts. 


**DOM**

The Document Object Model (DOM) is a cross-platform and language-independent convention for representing and interacting with objects in HTML. Objects in the DOM tree may be addressed and manipulated by using Python methods on the objects. Any element whose state you want to be able to get or set in Python must have an id attribute.

To extract a value from a slider like the example above you would::

    year = int(dom['slider_year']['value'])

To set the image you would::

    dom['img_name'].set_image(plt.get_svg(), 'svg')

When you want to trigger an event from the web page, like from the button, you need to create a function named after the button with a  ``dom`` parameter::

    def mybutton__click(dom):

        return dom

This means that the button is triggered by a click and calls the function, which can then perform calculations and set the DOM elements in your page.


**Themes** 

You can set a theme for your web app in the ``settings.py`` file. These themes come directly from `bootswatch <http://bootswatch.com/2/>`_ and are located in ``app/static/css`` directory. You can download and modify different themes and use them by placing them in the ``css/`` directory.
