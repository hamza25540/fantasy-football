# This is where your CREATE, READ, UPDATE AND DELETE functionality is going to go. 
from asyncio import Task
from flask import render_template, url_for, redirect, request 
from application import app, db 
from application.models import Todos, Lists
from application.forms import TodoForm, ListForm

#READ 
#Location of this functionality: ip_address:5000/
@app.route('/', methods=['POST', 'GET'])
def index():
    todos = Todos.query.all()
    return render_template('index.html', title="To do List", todos=todos)

#CREATE 
#Location of this functionality: ip_address:5000/add
@app.route('/add', methods=['POST','GET'])
def add():
    # This points to TodoForm
    form = TodoForm()
    # Checks that we have clicked the submit button
    if form.validate_on_submit():
        # the variable tasks becomes what is put on the form 
        # todos becomes what we are going to be adding to the database
        todos = Todos(
            tasks = form.tasks.data
        )
        # This performs the add to database
        db.session.add(todos)
        # This commits those changes
        db.session.commit()
        # This one redirects to the index functions url
        return redirect(url_for('index'))
    # Otherwise return the template of add.html
    return render_template('add.html', title="Add a new Task", form=form)

#UPDATE 
@app.route('/update/<int:tid>', methods=['GET', 'POST'])
def update(tid):
    form = TodoForm()
    # Get one tasks from the specified ID
    tasks = Todos.query.get(tid)
    # POST method
    # If the user clicks submit
    if form.validate_on_submit():
        # What is put in the form gets ammended to the database
        tasks.tasks = form.tasks.data
        # Commit the changes
        db.session.commit()
        # Redirect to the url for index function 
        return redirect(url_for('index'))
    # Else if the request method is a GET
    elif request.method == 'GET':
        # Update the form with whats in the database
        form.tasks.data = tasks.tasks 
    # If we go to the url return the template update.html
    return render_template('update.html', title='Update you task', form=form)


#DELETE
#Location of this functionality: ip_address:5000/delete/1
@app.route('/delete/<int:tid>')
def delete(tid):
    # Collecting the task we want to delete based on its id
    tasks = Todos.query.get(tid)
    # deleting this item from the database
    db.session.delete(tasks)
    # committing this change
    db.session.commit()
    # returning the url in the index function. 
    return redirect(url_for('index'))
