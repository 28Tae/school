# 3.0 - Flask, Jinja & Web Applications
<hr>
<sup>[Return Home](../README.md)</sup>

<div class="alert alert-block alert-warning">
This is the culmination of the past two years of computing, to develop a Flask Web Application.
</div>

On the **frontend**, you have `templates/FILE.html` as a baseline HTML structure, topped with _static_ CSS styling & JavaScript dynamic content generation.

On the **backend**, you have your SQL database and the `app.py` which runs the entire programme.


```python
project/
├── app.py                # Main application to EXECUTE
├── templates/            # Jinja templates
│   ├── layout.html       # Base template for Jinja
│   └── index.html        # Extended template
├── static/               # Static files (CSS, JavaScript, Images)
│   ├── style.css 
│   ├── script.js
│   └── images/
└── database.db           # SQLite database
```

<hr>

## **`3.1` - Dynamic Objects**
Here are baseline files to run a simple web app.


```python
# app.py

from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# INSERT OTHER ROUTES

if __name__ == '__main__':
    app.run(debug=True)
```


```python
<!-- templates/layout.html -->
<!DOCTYPE html>
<html>
<head>
    <!-- Take note of rel="stylesheet" and the url_for to link filename-->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    {% block main %}{% end block %}
</body>
</html>
```


```python
/* style.css */
h1 {
    color: blue;
    font-size: 24px;
}
.class {
    padding: 10px;
}
```


```python
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}Homepage{% endblock %}

{% block content %}
    <h1>Welcome, {{ name }}!</h1>
    
    <!-- If-Else Condition -->
        {% if user_role == 'admin' %}
            <p>Admin Dashboard</p>
        {% else %}
            <p>User Dashboard</p>
        {% endif %}
    
    <!-- For Loop -->
    <ul>
        {% for item in list %}
            <li><a href="{{ item[0] }}">{{ item[1] }}</a></li>
        {% endfor %}
    </ul>
    
    <!-- Filters -->
    <p>Escapable: {{ name|safe }}</p>
    <p>Name length: {{ name|length }}</p>
    <p>Random number: {{ range(1,8)|length}}</p>
{% endblock %}
```

### **3.1.1** - Jinja Syntax
- `{{ ... }}` inserts variables <br>
- `{% ... %}` refer to conditionals and logic
<br>

| Item | Syntax | ? |
| --- | --- | --- |
| Extension | `{% extends 'base.html' %}` |	Base template structure |
| Blocks | `{% block content %}...{% endblock %}` | Replaceable sections |
| Vars | `{{ variable }}` | Output dynamic var |
| If-else |	`{% if %}{% elif %}{% else %}{% endif %}` | ... |
| Loops | `{% for item in list %}...{% endfor %}` | ... |
| Safe filter | `{{ str\|safe }}` | Escapable characters |
| **Length** | `{{ str\|length }}` | Returns length |
| **Random** | `{{ range(9)\|random }}` | Selects random |
| **URL Generate** | __`{{url_for('profile')}}`__ | Dynamic links |

### **3.1.2** - URL Building

You can build dynamic URLs by using **converters**.<br>
This dumps integers/floats/strings in the URL to be processed in the route.<br>
The format of a custom converter is **`<type: var>`** where type is either `int`, `float`, or `str` (default).


```python
@app.route('/conv/')
@app.route('/conv/<float:page>/')
def converter(page=1):
	try:    
		return render_template("converter.html", page=page)
	except Exception as e:
		return str(e)

# /conv/5    works
# /conv/5.00 works
# /conv/     defaults to page 1
# /conv/ee   throws error
```

To build a URL for a specific object, you can dynamically find routes/static files through `url_for(...)`.

**In Python**, you normally want to just `return redirect(url_for('index'))`

**In Jinja**...


```python
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">

<!--- or --->
<form action="{{ url_for('submit', id=some_id) }}" method="post">
    <input type="text" name="Submittable">
    <input type="submit" value="Submit">
</form>
```

<hr>

# **`3.2` - GET, POST and SQL**
<code>GET</code> is the default method, in which data is _downloaded_ from the server to you in a non-private way

<code>POST</code> is where you _submit_ data and make _server-side changes_, which is more private due to the form nature
Remember, `from flask import request`

### **3.2.1** - Form by GET Method
> Data is sent in the URL query string `/search?query=input`<br>
> Do note you use **`request.args.get('...')`** here


```python
<!--- GET Method Form -->
{% extends "layout.html" %}
{% block main %}
<form action = "{{ url_for('get_result') }}">
    <p>Username: <input type = "text" name = "username"></p>
    <p>E-mail: <input type="email" name = "email"></p>
    <p>Message:</p>
    <p><textarea name = "message" rows="3" cols="50">
    </textarea></p>
    <p><input type="submit" value="Post by GET"></p>
</form>
{% endblock %}
```


```python
from flask import request

@app.route('/get_result/')
def get_result():
    username = request.args.get('username')
    message = request.args.get('message')

    # Parse request.args.get() values inside
    return render_template(
        'message_result.html',
        username=username,
        message=message
    ) 

```

### **3.2.2** - Form by POST Method
> Explicitly mention the `method = "POST"` in Jinja<br>
> Include `methods = ['GET', 'POST']` within the _route decorator_<br>
> Use `request.form[arg]` as though it's a _list_


```python
<!-- POST form method -->
<form action="{{ url_for('post_result')}}" method="POST">
    ...
    <input type="submit" value="Post by POST">
</form>
```


```python
from flask import request
import sqlite3

def get_db():
    db = sqlite3.connect("my_data.db")
    return db

@app.route('/post_result', methods=["GET", "POST"])
def post_result():
    if request.method == "GET":
        return render_template("index.html")

    db = get_db()
    query = """
    INSERT INTO posting
    (username, email, message)
    VALUES
    (?,?,?)
    """

    # Use request.form[...]
    username = request.form['username']
    email = request.form['email']
    message = request.form['message']

    # Executes INSERT and commits
    db.execute(query, (username, email, message))
    db.commit()
    db.close()

    return redirect(url_for('success'))
```

### **3.3.3** - CRUD Integration


```python
# Find the continued data structure in templates/index.html

@app.route('/success/')
@app.route('/index/')
def success():
    db = get_db()
    cursor = db.execute("SELECT * FROM posting")
    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        'index.html',
        data=data
    ) 
```
