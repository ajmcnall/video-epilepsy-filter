// // Turns out you can pull an HTML5 audio/video element right off a youtube page,
// // this isn't even using the Youtube api, not sure if it will be needed. HTML5 objects have lots of
// // useful features.
var video = document.getElementsByTagName("video")[0];
// // This is where the background message is received.
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
		var data = request.info;

 		var time = data["timestamps"];
 		if(data["isSafe"] == "No") {
 			alert("This video has been flagged as potentially seizure inducing.\nYou will be prompted to skip certain sections.")
 		}

 		video.addEventListener("timeupdate", function() {
 			for(key in time) {
 				if(video.currentTime >= parseInt(key) && video.currentTime < time[key]) {
 					video.pause();
 					if(confirm("Do you want to skip to the next segment?") == true) {
 						video.currentTime = time[key];
 						video.play();
 						
 					}
 				}
 			}
 		});
 	});
