/**
 * Get the current URL.
 *
 * @param {function(string)} callback called when the URL of the current tab
 *   is found.
 */
function getCurrentTabUrl(callback) {
  // Query filter to be passed to chrome.tabs.query - see
  // https://developer.chrome.com/extensions/tabs#method-query
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, (tabs) => {
    // chrome.tabs.query invokes the callback with a list of tabs that match the
    // query. When the popup is opened, there is certainly a window and at least
    // one tab, so we can safely assume that |tabs| is a non-empty array.
    // A window can only have one active tab at a time, so the array consists of
    // exactly one tab.
    var tab = tabs[0];

    // A tab is a plain object that provides information about the tab.
    // See https://developer.chrome.com/extensions/tabs#type-Tab
    var url = tab.url;

    // tab.url is only available if the "activeTab" permission is declared.
    // If you want to see the URL of other tabs (e.g. after removing active:true
    // from |queryInfo|), then the "tabs" permission is required to see their
    // "url" properties.
    console.assert(typeof url == 'string', 'tab.url should be a string');

    callback(url);
  });
}

/**
 * Gets the saved background color for url.
 *
 * @param {string} url URL whose background color is to be retrieved.
 * @param {function(string)} callback called with the saved background color for
 *     the given url on success, or a falsy value if no color is retrieved.
 */
function getSavedAnalysis(url, callback) {
  // See https://developer.chrome.com/apps/storage#type-StorageArea. We check
  // for chrome.runtime.lastError to ensure correctness even when the API call
  // fails.
  chrome.storage.sync.get(url, (items) => {
    callback(chrome.runtime.lastError ? null : items[url]);
  });
}

/**
 * Sets the given background color for url.
 *
 * @param {string} url URL for which background color is to be saved.
 * @param {string} color The background color to be saved.
 */
function saveAnalysis(url, data) {
  var items = {};
  items[url] = data;
  // See https://developer.chrome.com/apps/storage#type-StorageArea. We omit the
  // optional callback since we don't need to perform any action once the
  // background color is saved.
  chrome.storage.sync.set(items);
}


// THIS IS THE ONLY THING BEING USED FROM THIS FILE RIGHT NOW
// My though process while making this:
// background.js is always running, content.js is injected into each page.
// We could just use content, but a content script doesn't have access to lots of chrome api, including chrome.storage, which I think
// might be useful. They encourage you to use both background and content and send messages between them, I don't entirely understand it.

// One problem with content script and youtube, youtube doesn't reload pages when you navigate between videos. This onUpdated listener is my current
// work around, basically detecting a tab update. Not perfect, it triggers multiple times between videos.
// Basically background sends a message to content to tell it we went to a new video.

// The rest of the code in this file is a reworking of an example I downloaded. I was trying to set it up where the content then
// sends a message back to the background and does the saving of analysis data, but it was getting hairy and I gave up.
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab){  
    if(changeInfo && changeInfo.status == "complete") {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
          chrome.tabs.sendMessage(tabs[0].id, {greeting: tab.url}, function(response) {
            console.log(response.farewell);
          });
        });
    }
});


// Wait for content to request URL
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {

      // Get URL for this tab
      getCurrentTabUrl((url) => {
        getSavedAnalysis(url, (analysis) => {
          if (analysis) {
            if(analysis["verdict"] == "safe") {
            //  alert("This video has been analyzed and is safe for viewing");
            }
            else {
            //  alert("This video has been flagged as potentially seisure inducing at the following timestamps:" + analysis["timestamps"]);
            }
          }
          else {
            analysis = analyze(url);
            saveAnalysis(url, analysis);
          }
          alert(analysis["timestamps"].length);
          sendResponse({farewell: "hey"});
        });
      });
      return true;
  });

function analyze() {
  return {"verdict": "not safe", "timestamps": [[30,40],[60,70]]};
}