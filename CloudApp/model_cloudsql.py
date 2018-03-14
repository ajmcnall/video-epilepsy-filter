from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


class ProcessedVideos(db.Model):
    
    __tablename__ = 'processed_videos'
    videoID = db.Column(db.String(11), primary_key = True)
    isSafe = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return '<ProcessedVideos(videoID= %s, isSafe= %r)>' % (self.videoID, self.isSafe)
    
def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

#Gets a video entry if there is one
def read(id):
    result = ProcessedVideos.query.get(id)
    if not result:
        return None
    return from_sql(result)

#Create a new entry
# [START create]
def create(data):
    video = ProcessedVideos(**data)
    db.session.add(video)
    db.session.commit()
    return from_sql(video)
# [END create]

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")
   

if __name__ == '__main__':
    _create_database()