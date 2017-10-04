// Start ws connection after document is loaded
$(document).ready(function() {	
  	
	// Connect if API_Key is inserted
	// Else show an error on the overlay
	if (typeof API_Key === "undefined") {
		$("body").html("No API Key found or load!<br>Rightclick on the Scoreboard script in AnkhBot and select \"Insert API Key\"");
		$("body").css({"font-size": "20px", "color": "#ff8080", "text-align": "center"});
	}
	else {
		connectWebsocket();
	}
	
});

// Connect to AnkhBot websocket
// Automatically tries to reconnect on
// disconnection by recalling this method
function connectWebsocket() {
	
	//-------------------------------------------
	//  Create WebSocket
	//-------------------------------------------
	var socket = new WebSocket("ws://127.0.0.1:3337/AnkhBot");

	//-------------------------------------------
	//  Websocket Event: OnOpen
	//-------------------------------------------
	socket.onopen = function() {
		
		console.log("Connected, authenticating now...")
		
		// AnkhBot Authentication Information
		var auth = {
			author: "Ocgineer",
			website: "http://www.twitch.tv/ocgineer",
			api_key: API_Key,
			events: [
				"EVENT_NOW_PLAYING"
			]
		};
		
		// Send authentication data to AnkhBot ws server
		socket.send(JSON.stringify(auth));
	};

	//-------------------------------------------
	//  Websocket Event: OnMessage
	//-------------------------------------------
	socket.onmessage = function (message) {	

		// Parse message
		var socketMessage = JSON.parse(message.data);
		
		// EVENT_CONNECTED
		if (socketMessage.event == "EVENT_CONNECTED") {
			console.log(socketMessage.data.message);
		}
		
		// EVENT_NOW_PLAYING
		if (socketMessage.event == "EVENT_NOW_PLAYING") {

			// Queue animation
			$("#song")
				.queue(function() {
					var data = JSON.parse(socketMessage.data);
					$("#title").html(data.Title);
					$("#requester").html(data.Requester);
					if (data.IsPlaylist)
						// Hide requester if caster
						$("#requesterbox").hide();
					else
						// Show requester if viewer
						$("#requesterbox").show();
					$(this).removeClass("slideOutUp initialHide");
					$(this).addClass("slideInLeft");
					$(this).dequeue();
				})
				.delay(8000)
				.queue(function() {
					$(this).removeClass("slideInLeft");
					$(this).addClass("slideOutUp");
					$(this).dequeue();
				});
				// No delay added to wait for the slideOutUp
				// animation, this way in case of a song
				// skip it doesnt have to slide out first
		}
	}

	//-------------------------------------------
	//  Websocket Event: OnError
	//-------------------------------------------
	socket.onerror = function(error) {	
		// Log message for debugging
		console.log("Error: " + JSON.stringify(error));
	}	
	
	//-------------------------------------------
	//  Websocket Event: OnClose
	//-------------------------------------------
	socket.onclose = function() {
		// Log message for debugging
		console.log("Connection was closed, trying to reconnect!")	
			
		// Clear socket and try to connect again after 5 seconds
		socket = null;
		setTimeout(function(){connectWebsocket()}, 5000);						
	}    

};