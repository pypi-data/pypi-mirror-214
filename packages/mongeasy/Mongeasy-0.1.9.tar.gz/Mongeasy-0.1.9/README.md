# Mongeasy

Mongeasy is a easy to use library to be used for simple access to a MongoDB database, without any need for schemas or validation. Just store the data as it is used in your application.

### Installation
Mongoeasy is available on PyPI and can be installed using pip:

```bash
pip install mongeasy
```

### Documentation
The documentation can be found at [https://mongeasy.readthedocs.io](https://mongeasy.readthedocs.io)

### What's new in version 0.1.9?
* Improvement and bugfixes for Query

### Connection
Connection to the database is handled automtically for you if you have the conenction information in a configfile or set as environment variables.

#### Connection using configfile
Create a file called `mongeasy_config.yml` and place it in your project root folder.

The contents of the file should be:

```bash
db_config:
  uri: mongodb://localhost:27017
  database: mydatabase
```

#### Connection using environment variables
You can, as an alternative method, define your connection information using environment variables. Just set these two:

```bash
MONGOEASY_CONNECTION_STRING=mongodb://localhost:27017/
MONGOEASY_DATABASE_NAME=mydatabase
```

### Create a document class
To use Mongeasy you will create a document class that can be used with the collection of choice. To do this you will use the `create_document_class` factory function like this:

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

```

The first argument is the name the class will get and the second argument is the name of the collection to use. If the collection does not exist it will be created when you use the class to store documents.

You will not need to assign the returned value to a class variable as in the example above, as the generated class is injected into the current namespace:

```python
from mongeasy import create_document_class


create_document_class('User', 'users')

# The class User exist from this point in the code

```

### Create a store a document
You can create a documnet by using the generated class. You can either use keyword arguments or pass a dict.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Create a document using keyword arguments
user1 = User(name='Alice', age=25)
user1.save()

# Create a document using a dict
user2 = User({'name': 'Bob', 'age': 30})
user2.save()

```

### Find documents
You can find documents using the `find` method on the generated class. This method will return a list of documents.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find all documents
users = User.all()

# Find all documents with age 25
users = User.find({'age': 25})

```
#### Find one document
You can find one document using the `find` method on the generated class.

Find will return a ResultList object that can be used to get the first, or last, document in the list. If no document is found None is returned.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')

```

### Update a document
You can update a document just by changing the attributes and then calling the `save` method.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')
else:
    # Update the age of the user
    user.age = 26
    user.save()
```

### Delete a document
You can delete a document by calling the `delete` method on the document.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')
else:
    # Delete the user
    user.delete()
```

You can also delete all documents in a collection by calling the `delete` method on the generated class.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')


# Delete using a filter
User.delete({'age': 25})

# Delete all documents in the collection
User.delete()
```

### Indexes
You can create indexes on the collection by using the `create_index` method on the generated class.

```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Create a unique index on the name field
User.create_index('name', unique=True)
```

### Other uses
When you create the document class you have an option to pass additional bases classes. You can use this feature to add functionality to the generated class.

This can also be useful if you want to use Mongeasy with for example flask-login.

```python
from flask import Flask
from flask_login import UserMixin, LoginManager
from mongeasy import create_document_class
from bson import ObjectId

login_manager = LoginManager()
# Create User class with mongeasy and UserMixin from flask_login as a base class
User = create_document_class('User', 'users', base_classes=(UserMixin,))
def get_id(self):
    return str(self._id)
# Add get_id method to User class
User.get_id = get_id


def create_app():
    app = Flask(__name__)
   # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        # Load the user object from the database using the user_id
        user_id = ObjectId(user_id)
        user = User.find(_id=user_id).first()
        return user

    return app

```
### Query objects
Mongeasy simplifies the process of creating complex database queries by using the Query object. This object allows you to use Python-like syntax for creating your queries, making it easier and more intuitive than using traditional MongoDB queries.

For instance, consider the following MongoDB query:

```python
query = {'$or': [{'$or': [{'name': {'$eq': 'John'}}, {'age': {'$lt': 40}}]}, {'$and': [{'name': {'$eq': 'Jane'}}, {'age': {'$gt': 20}}]}]}
```

You can achieve the same result using the Query object:

```python
from mongeasy.core import Query

query = Query('(name == "John" or age < 40) or (name == "Jane" and age > 20)')
```

This query can then be used in your database queries like this:

```python
from mongeasy import create_document_class
from mongeasy.core import Query

User = create_document_class('User', 'users')
query = Query('(name == "John" or age < 40) or (name == "Jane" and age > 20)')
result = User.find(query)
```

Mongeasy supports the following operators in the Query object:

* `==`: equality
* `!=`: inequality
* `<`: less than
* `>`: greater than
* `<=`: less than or equal to
* `>=`: greater than or equal to
* `and`: logical AND
* `or`: logical OR
* `not`: logical NOT
* `in`: check if a value is in a list
* `not in`: check if a value is not in a list

You can also access subdocuments or nested fields in your documents using the dot notation:

```python
query = Query('age > 25 and friends.age == 32')
```

In case of invalid queries, an error will be raised with detailed information about the problem:

```python
try:
    query = Query("age <> 25")  # Invalid operator
except ValueError as e:
    print(e)
```

This approach makes it easier to write, read, and manage your database queries in Python, providing a more user-friendly interface for MongoDB.

### ResultList
All queries that can return more than one document will return a `ResultList` object. This object can be used to get the first or last document in the list, or None if no document is found.


```python
from mongeasy import create_document_class


User = create_document_class('User', 'users')

# Find one document with age 25
user = User.find({'age': 25}).first()

if user is None:
    print('No user found')
```

There are also other methods on the `ResultList` object that can be used. These are:

* `first` - Get the first document in the list or None if no document is found
* `last` - Get the last document in the list or None if no document is found
* `first_or_none` - Get the first document in the list or None if no document is found, same as first
* `last_or_none` - Get the last document in the list or None if no document is found, same as last
* `map` - Apply a given function to each element in the list and return a new ResultList containing the results
* `filter` - Filter the list using a given function and return a new ResultList containing the results
* `reduce` - Apply a given function to each element in the list and return a single value
* `group_by` - Group the list by a given key and return a dict with the results grouped by the key
* `random` - Get a random document from the list or None if no document is found

### Planned features
* Enable lazy-loading of query results and support for query chaining
* Implement a schema plugin system to allow for validation and type checking of documents
* Add support for transactions using resource management
* Implement logging and profiling to aid with debugging and performance tuning
* Enable asynchronous I/O support for improved scalability
* Implement caching with customizable caching strategies
* Add support for background tasks using a task queue
* Implement a paginator utility to allow for pagination of query results
* Support for MongoDB Atlas search
* Data migration and seeding utilities
* Real-time sync feature for monitoring and syncing with another database
* Automatic data splitting for large documents approaching the 16 MB limit
* Support for SQL-style auto-increment fields
* Middleware support for request/response processing
* Integration with machine learning libraries for data analysis and prediction
* Built-in analytics to provide insights into database usage and performance
* Visualization tools to aid with data exploration and presentation


### Contributing
Contributions are welcome. Please create a pull request with your changes.

### Issues
If you find any issues please create an issue on the github page.

### License
This project is licensed under the MIT License - see the LICENSE file for details
