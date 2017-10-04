$(document).ready(function() {	  
	
	// Connect if API_Key is inserted
	if (typeof API_Key === "undefined") {
		$("body").html("ERROR: No API Key found!<br>Rightclick on the TestAlerts script in AnkhBot and select \"Insert API Key\"");
		$("body").css({"font-size": "20px", "color": "#ff8080", "text-align": "center"});
	}
	else {
		// Connect to AnkhBot ws
		connectWebsocket();
	}
	
});

// Connect to AnkhBot websocket
// Automatically tries to reconnect on disconnection
function connectWebsocket() {
	
	//-------------------------------------------
	//  Create WebSocket
	//-------------------------------------------
	var socket = new WebSocket("ws://127.0.0.1:3337/AnkhBot");

	//-------------------------------------------
	//  Websocket Event: OnOpen
	//-------------------------------------------
	socket.onopen = function() {
		
		// AnkhBot ws Authentication Information
		var auth = {
			author: "Ocgineer",
			website: "http://www.twitch.tv/ocgineer",
			api_key: API_Key,
			events: [
				"EVENT_FOLLOW",
				"EVENT_HOST",
				"EVENT_CHEER",
				"EVENT_SUB",
				"EVENT_GW_SUB",
				"EVENT_DONATION"
			]
		}
		
		// Send authentication data to AnkhBot ws server
		socket.send(JSON.stringify(auth));
	};

	//-------------------------------------------
	//  Websocket Event: OnMessage
	//-------------------------------------------
	socket.onmessage = function(message) {
		
		// Parse OnMessage Message
		var blobMessage = JSON.parse(message.data);
				
		// Switch on event type
		switch(blobMessage.event) {
			
			case "EVENT_FOLLOW":
				var blobData = JSON.parse(blobMessage.data);
				TriggerFollowAlert(blobData);
				break;
				
			case "EVENT_HOST":
				var blobData = JSON.parse(blobMessage.data);
				TriggerHostAlert(blobData);
				break;
				
			case "EVENT_CHEER":
				var blobData = JSON.parse(blobMessage.data);
				TriggerCheerAlert(blobData);
				break;
			
			case "EVENT_SUB":
				var blobData = JSON.parse(blobMessage.data);
				TriggerTwitchSubAlert(blobData);
				break;
				
			case "EVENT_GW_SUB":
				var blobData = JSON.parse(blobMessage.data);
				TriggerGameWispSubAlert(blobData);
				break;
				
			case "EVENT_DONATION":
				var blobData = JSON.parse(blobMessage.data);
				TriggerDonationAlert(blobData);
				break;
		}
	};
	
	//-------------------------------------------
	//  Websocket Event: OnError
	//-------------------------------------------
	socket.onerror = function(data) {
		console.log("Error: " + error);
	};
	
	//-------------------------------------------
	//  Websocket Event: OnClose
	//-------------------------------------------
	socket.onclose = function() {		
		// Clear socket to avoid multiple
		// websocket objects and EventHandlings
		socket = null;
		
		// Set timeout to recall this function to reconnect
		// after 5000ms after receving the onclose ws event
		setTimeout(function(){connectWebsocket()}, 5000);						
	};
};

// Follow Alert
function TriggerFollowAlert(data) {
	console.log("Alert: Follow");
	console.log(data);
	console.log("Display Name: " + data.display_name);
};

// Host Alert
function TriggerHostAlert(data) {
	console.log("Alert: Host");
	console.log(data);
};

// Cheer Alert
function TriggerCheerAlert(data) {
	console.log("Alert: Cheer");
	console.log(data);
};

// Twitch Subscription Alert
function TriggerTwitchSubAlert(data) {
	console.log("Alert: Twitch Subscription");
	console.log(data);
};

// GameWisp Subscription Alert
function TriggerGameWispSubAlert(data) {
	console.log("Alert: GameWisp Subscription");
	console.log(data);
};

// Donation Alert
function TriggerDonationAlert(data) {
	console.log("Alert: Donation");
	console.log(data);
	console.log("Donation amount: " + data.amount);
};
