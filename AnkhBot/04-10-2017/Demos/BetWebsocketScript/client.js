if (window.WebSocket) {
    //---------------------------------
    //  Variables
    //---------------------------------
	//  Connection Information
	var serviceUrl = "ws://127.0.0.1:3337/AnkhBot"
	var socket = null;
	var reconnectIntervalMs = 10000;
	
    //  Timer Variables
    var timeLeft = 0;
    var isTiming = false;   
    var timer = null;

    //  Vote Storage Variables
    var showVotes = true; // Set to false if you don't want the right Entries Menu //

    var amountOfBetsToShow = 0; // Gets calculated based on amount of options //
    var totalBets = 0; // Current total votes that is being tracked // 
    var activeOptions = {}; // Active vote options tracked //

    var createdPollOptions = []; // Tracks all created Options //
    var betQueue = []; // Vote Entry Animation Queue //
    var isAnimating = false; // Determines whether the Vote Queue is being animated //

    var userBetAnimSpeed = 500; // UserBet Animation Speed //
    var betOptionAnimSpeed = 1000; // Vote Percentage Animation Speed //

    var betStarted = false; 

    //  Hide Options
    var hideOverlayOnceDone = true;
    var hideAfterMilisecs = 2500;
    var hideTimeout = null;

	function Connect()
	{
		socket = new WebSocket(serviceUrl);
		
		//---------------------------------
		//  Events
		//---------------------------------
		socket.onopen = function () {
			// Format your Authentication Information
			var auth = {
				author: "AnkhHeart",
				website: "https://AnkhBot.com",
				api_key: API_Key,
				events: [
					"EVENT_BET_START",
					"EVENT_BET_ENTER",
					"EVENT_BET_END",
                    "EVENT_BET_ABORT",
					"EVENT_BET_WINNER"
				]
			}
	
			//  Send your Data to the server
			socket.send(JSON.stringify(auth));
			console.log("Connected");
		};
	
		socket.onerror = function (error) {
			//  Something went terribly wrong... Respond?!
			console.log("Error: " + error);
		}
	
		socket.onmessage = function (message) {
			var jsonObject = JSON.parse(message.data);
	
			//------------------------------------
			//  Pass Data to correct Functions
			//------------------------------------
			if (jsonObject.event == "EVENT_BET_START") {
				Start(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_BET_ENTER") {
				Bet(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_BET_END") {
				Stop(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_BET_ABORT") {
				Abort();
			}
			else if (jsonObject.event == "EVENT_BET_WINNER") {
                Win(jsonObject.data);
			}
		}
		
		socket.onclose = function () {
			//------------------------------------
			//  Connection has been closed by you or the server
			//------------------------------------
			console.log("Connection Closed!");
			
			//	Attempt to reconnect
			setTimeout(Connect,reconnectIntervalMs);
		}
	}
    
	//------------------------------------
	//	Start Initial Connection
	//------------------------------------
	Connect();

    function Start(data) {

        if(betStarted) return;

        betStarted = true;

        var jsonObject = JSON.parse(data);

        //-----------------------------------
        //  Abort Fade Out  
        //-----------------------------------
        clearTimeout(hideTimeout);

        //------------------------------------
        //  Fade In
        //------------------------------------
        $("#body").animate({ opacity: 1},{duration: 500,queue: true});

        //------------------------------------
        //  Remove Elements when Options have been removed
        //------------------------------------
        if (activeOptions.length > jsonObject.options.length) {
            var difference = activeOptions.length - jsonObject.options.length;
            $('#optionsOutput .optionContainer').slice(-difference).remove();
        }

        //  Clear Active Options
        activeOptions = [];

        //  Update Title & Cost
        $("#bettingOn").html(`<p>${jsonObject.betting_on}</p>`);
        $("#min").html(`<span>${jsonObject.min_bet}</span>MIN`);
        $("#max").html(`<span>${jsonObject.max_bet}</span>MAX`);
        $("#multibet").html(`<span>${jsonObject.is_multi_bet ? "Yes" : "No"}</span>MULTI`);
        $("#payout").html(`<span>${jsonObject.payout_percent}%</span>PAYOUT`);
        
        $("#optionsTitle").html(`Options`);

        //  Determine if Multi Bet should be shown
        !jsonObject.is_multi_bet ? $("#multibet").hide() : $("#multibet").show();

        //------------------------------------
        //  Create all Bars
        //------------------------------------
        for (var i in jsonObject.options) {
            //------------------------------------
            //  Update Active Options & Create
            //------------------------------------
            activeOptions[i] = jsonObject.options[i].Value;
            var percentage = (activeOptions[i] * 100 / (jsonObject.total_bets == 0 ? 1 : jsonObject.total_bets)).toFixed(2);

            if (i > createdPollOptions.length - 1)
                createdPollOptions[i] = new BetOption(i, percentage, jsonObject, betOptionAnimSpeed);
            else
                createdPollOptions[i].update(i, percentage, jsonObject);

            $("#optionsOutput").append(createdPollOptions[i].newUserObject);

        }

        $("#optionsOutput").css("max-height", "");
        $("#optionsOutput").css("min-height", "");

        if (showVotes) 
        {
            $("#betsOutput").css("max-height", $("#optionsOutput").height());
            $("#betsOutput").css("min-height", $("#optionsOutput").height());
            $("#betsOutput").show();

            amountOfBetsToShow = Math.floor(($("#optionsOutput").height()-28*4)/28);
            console.log(amountOfBetsToShow);
        }
        else 
        {
            $("#betsOutput").hide();
            $("#optionsOutput").css("width", "100%");
        }

        $("#optionsOutput").css("max-height", $("#optionsOutput").height());
        $("#optionsOutput").css("min-height", $("#optionsOutput").height());

        //------------------------------------
        //  Update Total Votes
        //------------------------------------
        totalBets = jsonObject.total_bets;
        $("#totalBets").html(`<span>${jsonObject.total_bets}</span>BETS`);

        //------------------------------------
        //  Start Background Timer if used
        //------------------------------------
        if (jsonObject.is_timed) {
            timeLeft = jsonObject.timer;
            timer = setInterval(runTimer, 1000);
            $("#timeLeft").show();
        }
        else {
            $("#timeLeft").hide();
        }
    }
    function Bet(data) {

        if(!betStarted) return;

        //------------------------------------
        //  Parse
        //------------------------------------
        var jsonObject = JSON.parse(data);

        //------------------------------------
        //  Increase Votes
        //------------------------------------
        totalBets++;
        activeOptions[jsonObject.option]++;


        if (showVotes) 
        {
            var obj = new UserBet(jsonObject.name, jsonObject.option,jsonObject.amount, userBetAnimSpeed);


            if (betQueue.length != 0 || isAnimating) 
            {
                betQueue.push(obj);
            }
            else 
            {
                betQueue.push(obj);
                obj.display(setIsAnimating, animDone, false);
                $("#betsOutput").append(obj.newVoteObject);
            }
        }


        //------------------------------------
        //  Animate Bars
        //------------------------------------
        for (var i in activeOptions) {
            var animPercent = (activeOptions[i] * 100 / totalBets).valueOf();

            if (animPercent > 0) {
                createdPollOptions[i].animate(i, animPercent);
            }
        }

        //------------------------------------
        //  Update Total Votes
        //------------------------------------
        $("#totalBets").html(`<span>${totalBets}</span>BETS`);
    }
    function Stop(data) {
        //------------------------------------
        //  Shutdown the Timer
        //------------------------------------
        var jsonObject = JSON.parse(data);
        timeLeft = 0;
        clearInterval(timer);
        runTimer();
        betStarted = false;

    }
    function Win(data) {

        //  Convert to Object
        var jsonObject = JSON.parse(data);

        //---------------------------
        //   Hide all Options
        //---------------------------
        for (var i in activeOptions) {
            $(`#${i}`).animate({opacity: `0`}, {duration: 500,queue: true,complete: function () {
                        
                        $(`#${this.id}`).hide();
                        
                        //---------------------------
                        //   Unhide Winning Option after last Active Option has finished hiding
                        //---------------------------
                        if (this.id == activeOptions.length - 1) {
                            $("#optionsTitle").html(`Winning Option`);
                            $(`#${jsonObject.option_id}`).show();

                            $(`#${jsonObject.option_id}`).animate({opacity: `1`}, {duration: 2000,queue: true,complete: function()
                                    {
                                        if(hideAfterMilisecs)
                                        {
                                            hideTimeout = setTimeout(function(){
                                                $("#body").animate({ opacity: 0},{duration: 500,queue: true});
                                            },hideAfterMilisecs);
                                        }
                                    }
                                }
                                );
                        }
                    }
                });
        }

    }
    function Abort() {
       
        $("#body").animate({ opacity: 0},{duration: 500,queue: true});
    }

    function runTimer() {

        //------------------------------------
        //  Calculate Timer
        //------------------------------------
        timeLeft = Math.max(0, timeLeft - 1);

        var days = Math.floor(timeLeft / (60 * 60 * 24));
        var hours = Math.floor((timeLeft % (60 * 60 * 24)) / (60 * 60));
        var minutes = Math.floor((timeLeft % (60 * 60)) / (60));
        var seconds = Math.floor((timeLeft % (60)));

        //------------------------------------
        //  Add Zeros
        //------------------------------------
        if (days < 10) { days = "0" + days; }
        if (hours < 10) { hours = "0" + hours; }
        if (minutes < 10) { minutes = "0" + minutes; }
        if (seconds < 10) { seconds = "0" + seconds; }

        //------------------------------------
        //  Create Display String
        //------------------------------------
        var output = "";

        if (days != 0) output += days + ":";
        if (hours != 0) output += hours + ":";
        output += minutes + ":";
        output += seconds;

        $("#timeLeft").html("<span>" + output + "</span>TIME LEFT");
    }

    function setIsAnimating(isAnim) {
        isAnimating = isAnim;
    }

    function animDone() {
        if (betQueue.length > amountOfBetsToShow) {
            betQueue[0].destroy();
            $("#betsOutput").append(betQueue[amountOfBetsToShow].newVoteObject);
            betQueue[amountOfBetsToShow].display(setIsAnimating, animDone, true);
            betQueue.shift();
        }
        else {
            $("#betsOutput").append(betQueue[betQueue.length - 1].newVoteObject);
            betQueue[betQueue.length - 1].display(setIsAnimating, animDone, false);
        }
    }
}
