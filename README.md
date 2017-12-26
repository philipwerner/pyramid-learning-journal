# pyramid-learning-journal


Pyramid Scaffold
================

A simple Pyramid app for listing and displaying learning journal posts.

##**Authors:**

Philip Werner (philip.r.werner@gmail.com)

##**Website:**

https://ljphilwerner.herokuapp.com/

##**Routes:**

| Route | Route Name | Description |
| --- | --- | --- |
| /  | home | the home page and a listing of all journal posts |
| /create | create | to create a new journal entry |
| /journal/{id:\d+} | detail | the page for an individual post |
|/journal/{id:\d+}/edit| update | for editing existing journal entries |


##**Set Up and Installation:**

Clone this repository to your local machine.
```
$ git clone https://github.com/philipwerner/pyramid-learning-journal.git
```
Once downloaded, cd into the ```pyramid-leanrning-journal``` directory.
```
$ cd pyramid-learning-journal
```

Begin a new virtual environment with Python 3 and activate it.
```
pyramid-learning-journal $ python3 -m venv ENV
pyramid-learning-journal $ source ENV/bin/activate
```
[pip](https://pip.pypa.io/en/stable) install this package as well as the testing set of extras into your virtual enviroment.
```
(ENV) pyramid-learning-journal $ pip install -e .[testing]
```
Create a Postgress datatbase for use with this application. Export an environment variable pointing to the location of your data configuration.
```
(ENV) pyramid-learning-journal $ createdb pyramid_scaffold
(ENV) pyramid-learning-journal $ export DATABASE_URL='postgress://localhost:5432/pyramid_scaffold'
(ENV) pyramid-learning-journal $ initdb development.ini
```
Once the package is installed and the database is created, serve the application using the ```pserve``` command.
```
(ENV) pyramid-learning-journal $ pserve development.ini
```


##**To Test**

If you have the testing extras installed, testing is simple. If you're in the same directory as setup.py type the following:
$ py.test pyramid_scaffold


##**Built With:**

[Pyramid Framework](https://trypyramid.com)

[Cookiecutter-PyPackage](https://github.com/audreyr/cookiecutter)

[Clean-Blog](https://startbootstrap.com/template-overviews/clean-blog/)