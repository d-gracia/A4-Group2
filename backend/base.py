from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb://localhost/app'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users
 
@app.route('/users', methods=['POST'])
def createUser():
    id = db.insert({
        'name': request.json['name'],
        'postalcode': request.json['postalcode'],
    })
    return jsonify({'id': str(ObjectId(id)), 'msg':"User Added Successfully"})

@app.route('/users', method=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'postalcode': doc['postalcode']
        })
    return jsonify(users)

@app.route('/user/<id>',methods=['GET'])
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'postalcode': user['postalcode']
    })
    
@app.route('/users/<id>',methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': "Deleted Successfully"})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'postalcode': request.json['postalcode'],
    }})
    return jsonify({'msg': "Updated Successfully"})



if __name__ == '__main__':
    app.run(debug=True)
