import logging
import os
import socket

from urlparse import parse_qs, urlparse

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


app = Flask(__name__)

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

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


    
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

@app.route('/', methods=['POST'])
def query_video():
    
    videoURL = request.form['videoURL']
    videoID = getVideoID(videoURL)
    
    print videoURL
    print videoID
    
    result = read(id)
    '''
    if result is None:
        #isSafe = processVideo blah blah blah
    else:
        #Pare the value out of the result
    '''
    #placeholder for now
    isSafe = False

    output = '%r' % isSafe

    return output


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