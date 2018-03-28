function handleTime(e) {
	var time = e.target.time;
	var video = e.target;
	for(var j = 0; j < time.length; j++) {
		time[j][0] = Math.round(time[j][0]);
		time[j][1] = Math.round(time[j][1]);
	}
	for(var i = time.length - 1; i >= 0; i--) {
		if(video.currentTime >= time[i][0] && video.currentTime < time[i][1]) {
			video.pause();
			var decision = confirm("Do you want to skip to the next segment?");
			video.play();

			if(decision == true) { // Skip section
				video.currentTime = time[i][1];
			}
			else { // Wait until past section
				time.splice(i,1);
			}					
		}
	}
}

// This is where the background message is received.
chrome.runtime.onMessage.addListener(
	function(request, sender, sendResponse) {
	
		var video = document.getElementsByTagName("video")[0];
		video.removeEventListener("timeupdate", handleTime, false);
		var data = request.info;

		if(data["isAnalyzed"] && data["isAnalyzed"] == "No") {
			video.pause();
			var decision = confirm("This video has not been analyzed. Would you like to wait while it is analyzed?");
			if(decision) {
				sendResponse({analyze : true});			
			}
			else {
				video.play();
				sendResponse({analyze : true});
			}
		}	
		else {
			if(data["isSafe"] && data["isSafe"] == "Yes") {
				alert("This video has been analyzed and is deemed safe");
			}
			else {
				var time = data["timestamps"];
 				alert("This video has been flagged as potentially seizure inducing.\nYou will be prompted to skip certain sections.")

 				// Every second, check if we are in a flagged section
 				video.time = time;
	 			video.addEventListener("timeupdate", handleTime, false);
	 			
	 		}
		}
	}
);
