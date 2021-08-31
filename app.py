# importing modules
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow
import random

app = Flask(__name__)

# creating database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
db = SQLAlchemy(app)

# initializing marshmallow(an object serialisation/deserialisation library)
ma = Marshmallow(app)

# ceating columns in database
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Items = db.Column(db.String(50), nullable=False)
    Order_Date = db.Column(db.Date, default=date.today)
    Order_ID = db.Column(db.String(50), nullable=False)
    Status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<{self.Items}-{self.Quantity}-{self.Order_Date}-{self.Order_ID}-{self.Status}>'

# creating a database schema
class OrderSchema(ma.Schema):
    class Meta:
        fields =('id','Items','Order_Date','Order_ID','Status')

order_schema = OrderSchema()
orders_schema = OrderSchema(many='True')            #...for viewing all orders

# adding and retrieving orders from database
# POST -  used to add values to database
# GET - used to retrieve value from database
@app.route('/', methods=['POST','GET'])
def add_items():
    key = random.randint(100,1000)
    if request.method == 'POST':  
        Items = request.json['Items']
        new_task = Order(Items=Items,Order_ID=key, Status="Order Placed Successfuly")
        db.session.add(new_task)
        db.session.commit()
        return order_schema.jsonify(new_task)               #...returning serialised vales
    else:
        task = Order.query.all()
        return orders_schema.jsonify(task)                  #...returning serialised vales

# display orders according to id(Primary Key)
@app.route('/<int:id>',methods=['GET'])
def get_task(id):
    task =Order.query.get_or_404(id)
    return order_schema.jsonify(task)

# updating the values according to id(Primary Key)
@app.route('/<int:id>',methods=['PUT'])                 # PUT - used to update values in database
def  task_update(id):
    task =Order.query.get_or_404(id)
    Items = request.json['Items']
    task.Items = Items
    db.session.commit()
    return order_schema.jsonify(task)

# deleting a value according to id(Primary Key)
@app.route('/<int:id>',methods=['DELETE'])              # DELETE - used to delete a value from database
def delete_task(id):
    delete_msg={"message":"Your order is cancelled"}
    task=Order.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(delete_msg)

if __name__ =='__main__':
    app.run(debug=True)

