from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# messages: get, post
# messages/id: patch, delete

@app.route('/messages', methods = ('GET', 'POST'))
def messages():
    if request.method == "GET":
        
        msgs = Message.query.order_by(Message.created_at).all()
        
        return [m.to_dict() for m in msgs], 200
    
    if request.method == "POST":
        
        data = request.get_json()
        
        new_message = Message(
            body = data.get('body'),
            username = data.get('username')
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        return new_message.to_dict(), 201

@app.route('/messages/<int:id>', methods = ('PATCH', 'DELETE'))
def messages_by_id(id):
    
    msg = Message.query.filter(Message.id == id).first()
    
    if not msg:
        return {"error": "message not found"}, 404
    
    if request.method == "PATCH":
        
        data = request.get_json()
        
        for field in data:
            setattr(msg, field, data[field])
            
        db.session.add(msg)
        db.session.commit()
        
        return msg.to_dict(), 201
    
    elif request.method == "DELETE":
        
        db.session.delete(msg)
        db.session.commit()
        
        return {}, 204
        

if __name__ == '__main__':
    app.run(port=5555)
