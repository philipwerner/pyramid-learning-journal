# pyramid-learning-journal
Pyramid Scaffold
================

A simple Pyramid app for listing and displaying learning journal posts.

Authors:

Philip Werner (philip.r.werner@gmail.com)

Website:

https://pure-peak-33912.herokuapp.com/

Routes:

/ - the home page and a listing of all journal posts
/create - to create a new journal entry
/journal/{id:\d+} - the page for an individual post
/journal/{id:\d+}/edit - for editing existing journal entries


Set Up and Installation:

Clone this repository to your local machine.

Once downloaded, cd into the pyramid-leanrning-journal directory.

Begin a new virtual environment with Python 3 and activate it.

cd into the pyramid_scaffold directory. It should be at the same level of setup.py

pip install this package as well as the testing set of extras into your virtual environment.

$ pserve development.ini --reload to serve the application on http://localhost:6543

To Test

If you have the testing extras installed, testing is simple. If you're in the same directory as setup.py type the following:
$ py.test pyramid_scaffold
