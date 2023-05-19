from app.extensions import db
import uuid

class centuryXVIIIWords(db.Model):
    id = db.Column('id', 
      db.Text(length=36), 
      default=lambda: str(uuid.uuid4()), 
      primary_key=True)
    
    word = db.Column(db.Text)
    counter = db.Column(db.Integer)

    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    updatedAt = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

