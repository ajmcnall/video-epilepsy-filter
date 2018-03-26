import logging
import os
import socket
import json

from urlparse import parse_qs, urlparse

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


app = Flask(__name__)
db = SQLAlchemy()
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
db.init_app(app)
with app.app_context():
    db.create_all()
    
builtin_list = list

def is_ipv6(addr):
    """Checks if a given address is an IPv6 address."""
    try:
        socket.inet_pton(socket.AF_INET6, addr)
        return True
    except socket.error:
        return False
    
def getVideoID(URL):
    u_pars = urlparse(URL)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]




class FlaggedSections(db.Model):
    
    __tablename__ = 'flagged_sections'
    videoID = db.Column(db.String(11), db.ForeignKey('db.processed_videos.videoID'), primary_key=True, nullable=False)
    beginTime = db.Column(db.Integer, primary_key=True, nullable=False)
    endTime = db.Column(db.Integer, nullable=False)
    
    __table_args = (
        db.CheckConstraint(endTime > beginTime),
    )
        
    def __repr__(self):
        return '<FlaggedSections(videoID= %s, beginTime= %d, endTime= %d)>' % (self.videoID, self.beginTime, self.endTime) 
    
    
#ProcessedVideos table in the database
class ProcessedVideos(db.Model):
    
    __tablename__ = 'processed_videos'
    videoID = db.Column(db.String(11), primary_key = True)
    isSafe = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
        return '<ProcessedVideos(videoID= %s, isSafe= %r)>' % (self.videoID, self.isSafe)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['videoID'] = row.videoID
    data.pop('_sa_instance_state')
    return data

#Gets a video entry if there is one
def readProcessedVideo(videoID):
    result = ProcessedVideos.query.get(videoID)
    if not result:
        return None
    return from_sql(result)

#Create a new entry
# [START create]
def addProcessedVideo(**data):
    video = ProcessedVideos(data)
    db.session.add(video)
    db.session.commit()
    return from_sql(video)
# [END create]

def readTimeStamps(videoID):
    query = (FlaggedSections.query
             .filter(FlaggedSections.videoID==videoID)
             .order_by(FlaggedSections.beginTime))
    results = builtin_list(map(from_sql, query.all()))
    return results

def addTimeStamps(**data):
    flaggedSection = FlaggedSections(data)
    db.session.add(flaggedSection)
    db.session.commit()
    return from_sql(flaggedSection)

@app.route('/analyze', methods=['POST'])
def analyze_video():

    videoURL = request.form.getlist('videoURL')[0]
    videoID = getVideoID(videoURL)

    timestamps = [] 
    #timestamps = somefunction

    if not timestamps:
        #Flag video as safe
        addProcessedVideo(videoID=videoID, isSafe=True)
        return json.dumps({
            'isSafe':'Yes'
        })
    else:
        #Flag video as not safe
        addProcessedVideo(videoID=videoID, isSafe=False)
        #TODO: Store timestamps
        for timestamp in timestamps:
            addTimeStamps(videoID=videoID, beginTime=timestamp[0], endTime=timestamp[1])
        return json.dumps({
            'isSafe':'No',
            'timestamps':timestamps
        })

@app.route('/', methods=['POST'])
def query_video():
    
    #For postman use:
    #videoURL = request.form['videoURL']
    videoURL = request.form.getlist('videoURL')[0]
    videoID = getVideoID(videoURL)
    
    result = readProcessedVideo(videoID)
    
    if result is None:
        return json.dumps({
            'isAnalyzed':'No'
        })
    else:
        isSafe = result['isSafe']

    if isSafe:
        return json.dumps(
            {
                'isAnalyzed':'Yes',
                'isSafe':'Yes'
            })
    else:
        flaggedSections = readTimeStamps(videoID)
        timestamps = {}
        for section in flaggedSections:
            timestamps[section['beginTime']] = section['endTime']
        return json.dumps({
            'isAnalyzed':'Yes',
            'isSafe':'No',
            'timestamps':timestamps
        })
    
    
    


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)