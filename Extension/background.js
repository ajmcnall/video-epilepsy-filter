console.log("running");
var bkg = chrome.extension.getBackgroundPage();

function processServerResponse(result) {
  bkg.console.log("processed");
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, {info : result}, function(response) {
      var handler = function () {};
      if(response && response.analyze) {
        bkg.console.log(response);
        handler = processServerResponse;
      }
      else {
        bkg.console.log("finished");
        return;
      }
      checkDatabase("https://epilepsy-video-filter.appspot.com/analyze", handler);
    });
  });
}

// Youtube doesn't reload page between videos, using this to detect page changes
chrome.webNavigation.onHistoryStateUpdated.remo
chrome.webNavigation.onHistoryStateUpdated.addListener(function(details) {
    if(details.frameId === 0) {
        // Fires only when details.url === currentTab.url
        chrome.tabs.get(details.tabId, function(tab) {
            if(tab.url === details.url && tab.url.search("watch") != -1) {
                bkg.console.log("onHistoryStateUpdated");

                checkDatabase("https://epilepsy-video-filter.appspot.com", processServerResponse);
            }
        });
    }
});

function checkDatabase(server_url, handleData) {
  bkg.console.log('before query');

  chrome.tabs.query({'active': true, 'lastFocusedWindow': true}, function (tabs) {
    var url = tabs[0].url;
    bkg.console.log('inside query');
    bkg.console.log(url);
    //var postRequest = jQuery.post(server_url);
    jQuery.ajax({
      type: "POST",
      url: server_url,
      data: {'videoURL': url},

      success: function(data) {
        result = JSON.parse(data);
        handleData(result);

        bkg.console.log("success");
        bkg.console.log(data);
        bkg.console.log(JSON.parse(data));
      },

      error: function(status, msg) {
        bkg.console.log(status);
        bkg.console.log(msg);
      }
    });

    bkg.console.log(url);
  });
}

// document.addEventListener('DOMContentLoaded', function () {
//   var divs = document.querySelectorAll('div');
//   for (var i = 0; i < divs.length; i++) {
//     divs[i].addEventListener('click', click);
//   }
// });
