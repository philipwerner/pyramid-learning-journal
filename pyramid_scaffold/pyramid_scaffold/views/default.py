# -*- coding: utf-8 -*-
"""Handles formatting inputs for jinja pages."""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from pyramid_scaffold.models import Posts

POSTS = [
    {'id': 2, 'entry_title': 'Day 2', 'body': "I feel a lot better after today, very relieved that I was able to get everything I missed yesterday. It was also very nice to get my Sublime set up properly and the virtualenv running and know how to use them. Much better day today. The assignment was fun, pretty straight forward, really happy to be focusing on writing tests, all my dev friends tell me that they are a big part of getting a job, so.....YESS!", 'creation_date': 'Tuesday, 17 October, 2017, 10:23 pm'},
    {'id': 3, 'entry_title': 'Day 3', 'body': "So far so good, my head isn't spinning yet. Everything is making so much more sense than JS and that makes me happy. The complexity of using the terminal/command line is a bit intimidating, but I haven't really had any hangups at this point. Really excited about all of this.", 'creation_date': 'Thursday, 19 October, 2017, 4:11 pm'},
    {'id': 4, 'entry_title': 'Day 4', 'body': "So now I feel like the fire hose effect has kicked in. Really wishing I was completely over being sick so it would all sink in a little bit more. I really did like learning about mutability and for the most part how everything is so much better than JS. Still waiting for a solid A HA! moment though. I have faith it will come before too long.", 'creation_date': 'Friday, 20 October, 2017, 9:19 pm'},
    {'id': 5, 'entry_title': 'Day 5', 'body': "Day of Code is completed. I learned a lot about Python today, tried to pick katas that would challenge where I am at. It was fun and a bit tedious. I think it did help with getting used to testing and the testing format. Overall I found it very helpful even though I was too thrilled about having to do it on a Saturday with all this beautiful weather.", 'creation_date': 'Saturday, 21 October, 2017, 5:23 pm'},
    {'id': 6, 'entry_title': 'Day 6', 'body': "So I don't think my head was really recovered for today. We took in a lot of information in class and while it seemed to makes sense at that point and the assignments seemed easy enough....they weren't. I am really hoping a good nights rest and some relaxation will help everything to smooth out and start to jive.", 'creation_date': 'Monday, 23 October, 2017, 11:57 pm'},
    {'id': 7, 'entry_title': 'Day 7', 'body': "Today really help everything click for me. Working on the stack assignment brought some closure and better understanding of the linked list assignment. Best thing that happened today was finally figuring out the issues we were having with the server assignment from yesterday. It felt really good to get it all working together and the encode and decode all jiving together.", 'creation_date': 'Tuesday, 24 October, 2017, 6:12 pm'},
    {'id': 8, 'entry_title': 'Day 8', 'body': "Still struggling with the server assignments. I understand what is going on, just finding it difficult to code it out properly. In the grand scheme though, I feel like everything is coming together and clicking for me, which is good.", 'creation_date': 'Thursday, 26 October, 2017, 8:17 am'},
    {'id': 9, 'entry_title': 'Day 9', 'body': "Everything is starting take make more sense. Making a server is still not enjoyable though. I am able to completely wrap my head around data structures though.", 'creation_date': 'Friday, 27 October, 2017, 8:11 am'},
    {'id': 10, 'entry_title': 'Day 10', 'body': "The code review today was really awesome. It has been great seeing people refactor code during these, it helps me to get a better understanding of the problems. The best part of code review was going over the tests. I am starting to feel a lot more comfortable with writing tests. The whole concept of writing tests before writing the code made my head hurt at first, but it is all making sense now.", 'creation_date': 'Friday, 27 October, 2017, 7:06 pm'},
    {'id': 11, 'entry_title': 'Day 11', 'body': "So in the last couple days, I’ve learned that bootstraps are awesome when you don’t like dealing with CSS. The pyramid scaffold is pretty great, I’m sure it gets better the more you use it and start to know exactly what you have to do without reading through instructions for initial setup. Also the data structures are starting to make way more sense the further we get into them.", 'creation_date': 'Tuesday, 31 October, 2017, 8:10 am'}
]


@view_config(route_name='list', renderer="pyramid_scaffold:templates/home.jinja2")
def list_journal(request):
    """Will handle the request for the home page."""
    posts = request.dbsession.query(Posts).all()
    posts = [posts.to_dict() for post in posts]
    return {
        "title": "Phil's Blog Posts",
        "entries": posts
    }


@view_config(route_name='detail', renderer="pyramid_scaffold:templates/detail.jinja2")
def detailed_journal(request):
    """Will handle the request for detailed entries."""
    post_id = int(request.matchdict['id'])
    post = request.dbsession.query(Posts).get(post_id)
    if post:
        return {
            'title': 'Blog Post',
            'post': post.to_dict()
        }
    raise HTTPNotFound


@view_config(route_name='create', renderer="pyramid_scaffold:templates/post.jinja2")
def new_entry(request):
    """Will handle the request for the new entry."""
    return {
        "title": "New Entry",
    }


@view_config(route_name='update', renderer="pyramid_scaffold:templates/edit.jinja2")
def edit_entry(request):
    """Will handle the request for the edit entry."""
    return {
        "title": "Edit Entry",
    }
