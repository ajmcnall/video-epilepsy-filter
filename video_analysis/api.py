from flask import Flask, request
from pytube import YouTube

# Instructions for running locally:
# In shell run 'export FLASK_APP=api.py' (if using windows shell w/o linux commands try 'set FLASK_APP=api.py')
# Then run 'flask run' or 'python -m flask run'
# For other options/ more info see http://flask.pocoo.org/docs/0.12/

app = Flask(__name__)

@app.route('/', methods=['POST'])
def download():
	print(request.form['video-url'])

	# YouTube('https://www.youtube.com/watch?v=C0DPdy98e4c').streams.filter(subtype='mp4').first().download()
	if request.form['video-url']:
		if request.form['analyze'] == "true":
			# This downloads the video as an mp4 file, whichever quality is listed first (normally the highest)
			# The quality should be able to be changed using the filter, may want to switch to lowest resolution in future
			YouTube(request.form['video-url']).streams.filter(subtype='mp4').first().download('./video_files')

			# Insert analyze pipeline here
			
			return "Video downloaded and analyzed"

		else: 
			return "no analyze flag or analyze flag set to false"

	return "Malformed request"

