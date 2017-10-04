if (window.WebSocket) {
    //---------------------------------
    //  Variables
    //---------------------------------
	//  Connection Information
	var serviceUrl = "ws://127.0.0.1:3337/AnkhBot"
	socket = null;
	var reconnectIntervalMs = 10000;
	
    //  Timer Variables
    var timeLeft = 0;
    var isTiming = false;   
    var timer = null;

    var showEntries = true;
    var maxAmountOfEntries = 10;
    var currentAmountOfEntries = 0;
    var showWinnerForSec = 10000;
    var giveawayStarted = false;

	function Connect() {
		socket = new WebSocket(serviceUrl);
		
		socket.onopen = function () {
			var auth = {
				author: "Brain",
				website: "https://brains-world.eu",
				api_key: API_Key,
				events: [
					"EVENT_GIVEAWAY_START",
					"EVENT_GIVEAWAY_STOP",
					"EVENT_GIVEAWAY_ABORT",
					"EVENT_GIVEAWAY_ENTER",
					"EVENT_GIVEAWAY_WINNER"
				]
			}
			socket.send(JSON.stringify(auth));
			console.log("Connected");
		};
	
		socket.onerror = function (error) {
			console.log("Error: " + error);
		}
	
		socket.onmessage = function (message) {
			var jsonObject = JSON.parse(message.data);

			if (jsonObject.event == "EVENT_GIVEAWAY_START") {
                console.log("Start Event triggered");
				Start(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_GIVEAWAY_STOP") {
                console.log("End Event triggered");
                timeLeft = 0;
                clearInterval(timer);
                runTimer();
				HideGiveAway();
			}
			else if (jsonObject.event == "EVENT_GIVEAWAY_ABORT") {
                console.log("Abort Event triggered");
				HideGiveAway();
			}
			else if (jsonObject.event == "EVENT_GIVEAWAY_ENTER") {
                console.log("Enter Event triggered");
				Enter(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_GIVEAWAY_WINNER") {
                console.log("Winner Event triggered");
				Winner(jsonObject.data);
			}
		}
		
		socket.onclose = function () {
			console.log("Connection Closed!");
			setTimeout(Connect,reconnectIntervalMs);
		}
	}

	Connect();

    function Start(data) {
        if(giveawayStarted) return;
        giveawayStarted = true;

        var jsonObject = JSON.parse(data);
        console.log("Start initialized.");
        console.log(jsonObject);

        $("h1").html(`Giveaway with this prize: ${jsonObject.prize}`);
        $("#gaCmd").html(`Command: <span>${jsonObject.command}</span>`);
        $("#gaPerm").html(`Permission: <span>${jsonObject.permission}</span>`);
        if (jsonObject.info != "") {
            $("#gaInfo").html(`Info: <span>${jsonObject.info}</span>`);   
        }
        $("#gaTicketCost").html(`Ticket cost: <span>${jsonObject.fee}</span> ${jsonObject.currency_name}`);
        $("#gaMaxTickets").html(`Max Tickets: <span>${jsonObject.max_tickets}</span>`);

        if (jsonObject.is_timed) {
            timeLeft = jsonObject.timer;
            timer = setInterval(runTimer, 1000);
            $("#timer").show();
        }
        else {
            $("#timer").hide();
        }

        ShowGiveAway();
    }

    function Enter(data) {
        var jsonObject = JSON.parse(data);
        console.log("Enter GA initialized.");
        newListItem = "";

        $("#entryContainer").css("opacity", "1");

        if (maxAmountOfEntries >= currentAmountOfEntries) {
            console.log("Max: " + maxAmountOfEntries + "Current: " + currentAmountOfEntries);

            newListItem = `<li class='entry'>
                                <div class='entryName'>${jsonObject.user}</div>
                                <div class='entryOption'>Tickets: ${jsonObject.tickets}</div>
                            </li>`;
            console.log("New Item: " + newListItem);
            $("#entryContainer ul").append(newListItem);
            currentAmountOfEntries++;
        }
    }

    function Winner(data) {
        var jsonObject = JSON.parse(data);
        console.log("Winner gets picked.");

        $("#entryContainer ul").html(``);
        newListItem = `<li class='entry'>
                            <div class='entryName'><b>Winner:</b> ${jsonObject.user}</div>
                            <div class='entryOption'><b>Tickets:</b> ${jsonObject.tickets}</div>
                        </li>`;
        $("#entryContainer ul").append(newListItem);

        $("#entryContainer li").css("width", "100%");
        $("#entryContainer li").css("margin", "0");

        $("#entryContainer li").addClass("animated infinite pulse");

        setTimeout(function(){
            HideGiveAway();
        }, showWinnerForSec);
    }

    function ShowGiveAway() {
        console.log("Show GA initialized.");

        $("#container").css("opacity", "1");
    }

    function HideGiveAway() {
        console.log("Hide GA initialized.");

        $("#container").css("opacity", "0");

        
        timeLeft = 0;
        clearInterval(timer);
        runTimer();
        giveawayStarted = false;
    }

    function runTimer() {
        timeLeft = Math.max(0, timeLeft - 1);

        var days = Math.floor(timeLeft / (60 * 60 * 24));
        var hours = Math.floor((timeLeft % (60 * 60 * 24)) / (60 * 60));
        var minutes = Math.floor((timeLeft % (60 * 60)) / (60));
        var seconds = Math.floor((timeLeft % (60)));

        if (days < 10) { days = "0" + days; }
        if (hours < 10) { hours = "0" + hours; }
        if (minutes < 10) { minutes = "0" + minutes; }
        if (seconds < 10) { seconds = "0" + seconds; }

        var output = "";

        if (days != 0) output += days + ":";
        if (hours != 0) output += hours + ":";
        output += minutes + ":";
        output += seconds;

        $("#timer").html("Time remaining: <span>" + output +"</span>");
    }
}
