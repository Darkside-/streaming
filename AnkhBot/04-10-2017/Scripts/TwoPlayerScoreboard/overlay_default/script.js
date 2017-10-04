$(document).ready(function() {	
	
	// Load user settings if present
	if (typeof settings !== "undefined") {
		SetData(settings)
	}
  
	// Connect if API_Key is inserted
	// Else show an error on the overlay
	if (typeof API_Key === "undefined") {
		$("body").html("ERROR: No API Key found!<br/>Rightclick on the Scoreboard script in AnkhBot and select \"Insert API Key\"");
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
				"EVENT_SCOREBOARD_UPDATE",
				"EVENT_SCOREBOARD_SHOW",
				"EVENT_SCOREBOARD_HIDE",
				"EVENT_SCOREBOARD_RELOAD"
			]
		};
		
		// Send authentication data to AnkhBot ws server
		socket.send(JSON.stringify(auth));
	};

	//-------------------------------------------
	//  Websocket Event: OnMessage
	//-------------------------------------------
	socket.onmessage = function (message) {	
		
		// Parse MESSAGE data
		var blobMessage = JSON.parse(message.data);
			
		// EVENT_SCOREBOARD_SHOW
		if (blobMessage.event == "EVENT_SCOREBOARD_SHOW") {			
			
			// Parse EVENT data
			var blobEvent = JSON.parse(blobMessage.data);	
			
			// Set Data
			SetData(blobEvent)
			
			// Show scoreboard
			ShowScoreboard();
		}
		
		// EVENT_SCOREBOARD_HIDE
		if (blobMessage.event == "EVENT_SCOREBOARD_HIDE") {
			HideScoreboard();
		}
				
		// EVENT_SCOREBOARD_UPDATE
		if (blobMessage.event == "EVENT_SCOREBOARD_UPDATE") {	
		
			// Parse EVENT data
			var blobEvent = JSON.parse(blobMessage.data);				
			
			// Set Data
			SetData(blobEvent)
		}
		
	};
	
	//-------------------------------------------
	//  Websocket Event: OnError
	//-------------------------------------------
	socket.onerror = function(error) {
		
		console.log("Error: " + error);
	}	
	
	//-------------------------------------------
	//  Websocket Event: OnClose
	//-------------------------------------------
	socket.onclose = function() {
		
		// Hide the scoreboard on connection loss with the ws
		HideScoreboard();
		
		// Clear socket to avoid multiple ws objects and EventHandlings
		socket = null;
		
		// Try to reconnect every 5s 
		setTimeout(function(){connectWebsocket()}, 5000);						
	}    
};

function SetData(data) {
	// Seperator Style
	$("#seperator").css("color", data["color_seperator"]);
	$("#seperator").css("background-color", data["color_seperator_bg"]);
	
	// Player 1 Style
	$("#p1name").css("color", data["color_p1_name"]);
	$("#p1name").css("background-color", data["color_p1_name_bg"]);
	$("#p1score").css("color", data["color_p1_score"]);
	$("#p1score").css("background-color", data["color_p1_score_bg"]);
	
	// Player 2 Style
	$("#p2name").css("color", data["color_p2_name"]);
	$("#p2name").css("background-color", data["color_p2_name_bg"]);
	$("#p2score").css("color", data["color_p2_score"]);
	$("#p2score").css("background-color", data["color_p2_score_bg"]);
	
	// Scoreboard Border
	if (data["color_scoreboard_showborder"]) {
		$("#left-info-container").css({"border-left-style": "solid", "border-bottom-style": "solid", "border-color": data["color_scoreboard_border"]});
		$("#right-info-container").css({"border-right-style": "solid", "border-bottom-style": "solid", "border-color": data["color_scoreboard_border"]});
	}
	else {
		$("#left-info-container").css("border-style", "none");
		$("#right-info-container").css("border-style", "none");
	}
	
	// If width is given use that
	if (data.override_width > 0) {
		$("#scoreboard").animate({width: data.override_width + "px"}, 800);
	}
	// Else calculate width based on longest name
	else {
		// Starting width
		// 2x 55 (score box) + 50 (seperator box) + 100 (allows padding)
		var width = 260;
		
		// Measure name length using canvas and use the longest
		// width twice added to the total width of the scoreboard
		var c = document.getElementById("measurecanvas");
		var ctx = c.getContext('2d');
		ctx.font = "32px Arial";		
		var name_p1_width = ctx.measureText(data.PlayerOneName).width;
		var name_p2_width = ctx.measureText(data.PlayerTwoName).width;		
		width += (name_p1_width > name_p2_width) ?
			name_p1_width * 2 : name_p2_width * 2;
			
		// Set the width with animation
		$("#scoreboard").animate({width: width + "px"}, 800);
	}
	
	// Set Scoring Data
	$("#p1name").html(data.PlayerOneName);
	$("#p1score").html(data.PlayerOneScore);
	$("#p2name").html(data.PlayerTwoName);
	$("#p2score").html(data.PlayerTwoScore);
};

function ShowScoreboard() {
	$("#seperator").removeClass("animSlideOutUp").addClass("animSlideInDown");
	$("#left-info-container").removeClass("animRetract").addClass("animExpand");
	$("#right-info-container").removeClass("animRetract").addClass("animExpand");
	
	// remove hidden class used at document load
	// to not show the scoreboard untill triggered once
	$("#scoreboard").removeClass("hidden");
};

function HideScoreboard() {
	$("#left-info-container").removeClass("animExpand").addClass("animRetract");
	$("#right-info-container").removeClass("animExpand").addClass("animRetract");
	$("#seperator").removeClass("animSlideInDown").addClass("animSlideOutUp");
};