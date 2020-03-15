### My first Flask app ever

*An API for reporting stolen bike and assigning free officer for finding them*

**Libraries used in this repo:**
 * [Flask-restplus](https://flask-restplus.readthedocs.io/en/stable/): An extension for Flask. It provides a coherent collection of decorators and tools to describe your API and expose its documentation properly (using Swagger).
 * [marshmallow](https://marshmallow.readthedocs.io/en/stable/): Simplified object serialization
 * [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/): An extension for Flask that adds support for SQLAlchemy to your application
 
**My slogan in python**:

**"Clean code in minimum lines"**
 
 #### Structure and design implemented in this app: 
 
We have two tables. bike and officer.
There are exactly two scripts in all below folders, and both scripts are very similar.

Code different parts (folder):
* **db_model**: Sqlalchemy model
* **schema**: marshmallow schema for serialize and deserialize
* **core**: all db transaction and db operation reside here (repo) 
* **api_model**: this was needed only for swagger documentation. restplus not integrated yet with marshmallow for documenting
* **resource**: all rest-plus class which works like controller
* **server**: server, api, and db configuration exists here

app would run by:
```python
PYTHON_ENV=development python src/index.py
```


### API endpoints:
***[bike_officer.jpg](https://pasteboard.co/IY2YkAC.png)*** shows all endpoints clearly.

***Post methods***:

        For adding officers and bicycles

***Delete methods***: 

        in bike: It only results in tagging the bike as a 'founded case'.
        However, elimination does not actually occur in the database.

        in officer: It merely results in tagging the officer as a 'off officer'.
        elimination does not actually occur in the database.
      


Assigning the free bikes and officer to each other was handled by:
    
```python
   def assign():
        polices = Police.query.filter(and_(Police.bike_id.is_(None), Police.off.is_(False)))
        bikes = Bike.query.filter(and_(Bike.police_id.is_(None), Bike.resolved.is_(False)))
        for police, bike in zip(polices, bikes):
            police.bike_id = bike.id
            bike.police_id = police.id
```
 
transaction handled like this:
```python
def add_bike(**data):
    try:
        bike = Bike(**data)
        db.session.add(bike)
        assign()  # assigning the free bikes and officer to each other
        db.session.commit()
        return True
    except exc.SQLAlchemyError:
        db.session.rollback()
        return False
```
 

 
