from app.extensions import db
import uuid

class Results(db.Model):
    id = db.Column('id', 
      db.Text(length=36), 
      default=lambda: str(uuid.uuid4()), 
      primary_key=True)
    century = db.Column(db.Integer)
    inputText = db.Column(db.Text)
    outputText = db.Column(db.Text)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    updatedAt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

