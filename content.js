// Turns out you can pull an HTML5 audio/video element right off a youtube page,
// this isn't even using the Youtube api, not sure if it will be needed. HTML5 objects have lots of
// useful features.
var video = document.getElementsByTagName("video")[0];

// Obviously this should be pulled from a database/ generated in real time. Not hardcoded.
var timestamps = {"https://www.youtube.com/watch?v=Yw_YDvLWKnY" : [[10,20],[30,40]],
					"https://www.youtube.com/watch?v=YHYz_PLEAbc" : [[10,50],[60,100]]};

// This is where the background message is received.
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {

		var time = timestamps[request.greeting];
		if(time) {
			alert("This video has been flagged as potentially seizure inducing.\nYou will be prompted to skip certain sections.")
		}

		// I tried to make a loop out of these event listeners but it wasn't working. Something about javascript I'm not
		// understanding.
		video.addEventListener("timeupdate", function() {
			if(video.currentTime >= time[0][0] && video.currentTime < time[0][1]) {
				video.pause();
				if(confirm("Do you want to skip to the next segment?") == true) {
					video.currentTime = time[0][1];
					video.play();
					video.removeEventListener("timeupdate",arguments.callee,false);
				}
			}
		});

		video.addEventListener("timeupdate", function() {
			if(video.currentTime >= time[1][0] && video.currentTime < time[1][1]) {
				video.pause();
				if(confirm("Do you want to the skip to next segment?") == true) {
					video.currentTime = time[1][1];
					video.play();
					video.removeEventListener("timeupdate",arguments.callee,false);
				}
			}
		});
	});

