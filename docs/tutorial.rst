===============
Ashiba Tutorial
===============

Ashiba is an micro app building framework for pythonistas, allowing you to define layout with HTML or Enaml and get a web app running with minimal work and no javascript. 


In this tutorial I will be building a github statistics web app to plot contributions to open source projects.


The first thing we do is create a new anaconda environment on our system, activate it, and install Ashiba::

    conda create -n ashiba anaconda

    source activate ashiba

    git clone git@github.com:ContinuumIO/ashiba.git

    cd ashiba

    python setup.py install


To see what ashiba apps look like run::

    ashiba start examples/dataframes/ --open-browser


Nice right? We will build our own Ashiba app to show just how easy it is to create similar data representations.


The first thing we do is initialize the project with::

    ashiba init ashiba-example

Cd into the new directory and you will see a ``handlers.py``, ``settings.py``, and ``myapp.html`` file. 


Create a `github.py <https://github.com/ContinuumIO/ashiba/blob/master/examples/github-stats/github.py>`_ file which uses the requests library to get the github starts from the rest api then converts the result into a dataframe objects for easy manipulation.

* daily\_commit\_timeline()  = The number of commits per hour in each day
* weekly\_commit\_timeline() = The number of additions and deletions per week


Now that we have our data source we can move on to creating the web app. 

First let us edit the ``settings.py`` to change the name of the app, the css theme, and replace the icon with one I downloaded from `Github <https://github.com/logos>`_ by placing the new ``Ocotocat.png`` image file in the ``static/img`` directory:

.. code-block:: python

    APP_NAME = "Github Stats"
    APP_ICON = "static/img/Octocat.png"

    APP_THEME = "cyborg"


The next step is wrting out the HTML. Like many of you HTML is not a strength of mine but the amount we have to write is minimal.

Here is the `file <https://github.com/ContinuumIO/ashiba/blob/master/examples/github-stats/myapp.html>`_ for this tutorial app.
Easy enough right? 

Lines 5-11 are for the search bar and the Show Stats button. Lines
14-17 display the images.

Now we can write the logic of our app.

Open the `handlers.py <https://github.com/ContinuumIO/ashiba/blob/master/examples/github-stats/handlers.py>`_ file and import the ashiba modules and functions from our github file.

.. code-block:: python

    import ashiba   
    from ashiba.plot import plt
    from github import daily_commit_timeline, weekly_commit_timeline, 


Ashiba has to be triggered with some type of event. This can be anything from selecting a stock to pushing a button. I use a click triggered by clicking the `Get Stats` button. As you see in myapp.html the id is `mybutton` and the function is called `mybutton__click( )` denoting it will have to clicked in the webapp to run.

.. code-block:: python

    def mybutton__click(dom):

From there I get the usesr and repositiory I want to search, defined in the html as:

.. code-block:: html

    <li>Git User or Organization: <input id="usersearch" value=ContinuumIO></li>
    <li>Git Repository: <input id="reposearch" value=conda></li>


So we grab our values from the dom by using the id and value.

.. code-block:: python

    user = dom['usersearch']['value']
    repo = dom['reposearch']['value']

We call our functions, plot them, and return the dom.

.. code-block:: python


    ts = weekly_commit_timeline(user, repo)
    ts2 = daily_commit_timeline(user, repo)

    ts.plot()
    plt.title("Weekly commits for %s".format('Github') %repo)
    dom['img_plot'].set_image(plt.get_svg(), 'svg')

    ts2.plot()
    plt.title("Daily commits for %s".format('Github') % repo)
    dom['img_plot2'].set_image(plt.get_svg(), 'svg')

    plt.close()
 
    return dom


Now that we have our 4 files written we can return to our command line and run::

    ashiba start --open-browser .

Try searching some of Continuum's projects such as 'blaze', 'conda', or 'Bokeh'. 


To distribute the app we can use another cool Continuum project called `conda. <http://docs.continuum.io/conda/>`_


We build a package with the ashiba build command::

    cd ..

    ashiba build ashiba-example


The output should resemble::

    CLEAN: /home/xavier/ashiba/ashiba/examples/ashiba-example/build
    CLEAN: /tmp/tmpnVZLj1/github-stats/app

This print out shows that the command created a build directory and loaded a number of files into it, namely a ``meta.yaml``, ``build.bat``, and ``build.sh`` file. These are the build files for conda recipes, you don't really need to worry about them for now but feel free to view the `conda docs. <http://docs.continuum.io/conda/>`_ ::

    conda build ashiba-example/build/conda-recipe

This command will ask you whether you want to upload the file to `Binstar.org <http://binstar.org>`_. Binstar is a package managment solution also made by Continuum but an account is needed to use it.

