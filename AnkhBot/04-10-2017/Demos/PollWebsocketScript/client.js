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

    //  Vote Storage Variables
    var showVotes = true; // Set to false if you don't want the right Entries Menu //

    var amountOfVotesToShow = 0; // Gets calculated based on amount of options //
    var totalVotes = 0; // Current total votes that is being tracked // 
    var activeOptions = {}; // Active vote options tracked //

    var createdPollOptions = []; // Tracks all created Options //
    var voteQueue = []; // Vote Entry Animation Queue //
    var isAnimating = false; // Determines whether the Vote Queue is being animated //

    var userVoteAnimSpeed = 500; // UserVote Animation Speed //
    var voteOptionAnimSpeed = 1000; // Vote Percentage Animation Speed //

    var pollStarted = false; 

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
					"EVENT_POLL_START",
					"EVENT_POLL_VOTE",
					"EVENT_POLL_END",
					"EVENT_POLL_WIN",
					"EVENT_POLL_TIE"
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
			if (jsonObject.event == "EVENT_POLL_START") {
				Start(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_POLL_VOTE") {
				Vote(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_POLL_END") {
				Stop(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_POLL_WIN") {
				Win(jsonObject.data);
			}
			else if (jsonObject.event == "EVENT_POLL_TIE") {
				Tie(jsonObject.data);
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

        if(pollStarted) return;

        pollStarted = true;

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
        $("#votingOn").html(`<p>${jsonObject.voting_on}</p>`);
        $("#cost").html(`<span>${jsonObject.cost}</span>COST`);
        $("#optionsTitle").html(`Options`);

        //  Determine if Cost should be shown
        jsonObject.cost == 0 ? $("#cost").hide() : $("#cost").show();

        //------------------------------------
        //  Create all Bars
        //------------------------------------
        for (var i in jsonObject.options) {
            //------------------------------------
            //  Update Active Options & Create
            //------------------------------------
            activeOptions[i] = jsonObject.options[i].Value;
            var percentage = (activeOptions[i] * 100 / (jsonObject.total_votes == 0 ? 1 : jsonObject.total_votes)).toFixed(2);

            if (i > createdPollOptions.length - 1)
                createdPollOptions[i] = new VoteOption(i, percentage, jsonObject, voteOptionAnimSpeed);
            else
                createdPollOptions[i].update(i, percentage, jsonObject);

            $("#optionsOutput").append(createdPollOptions[i].newUserObject);

        }

        $("#optionsOutput").css("max-height", "");
        $("#optionsOutput").css("min-height", "");

        if (showVotes) 
        {
            $("#votesOutput").css("max-height", $("#optionsOutput").height());
            $("#votesOutput").css("min-height", $("#optionsOutput").height());
            $("#votesOutput").show();

            amountOfVotesToShow = Math.floor(($("#optionsOutput").height()-28*4)/28);
            console.log(amountOfVotesToShow);
        }
        else 
        {
            $("#votesOutput").hide();
            $("#optionsOutput").css("width", "100%");
        }

        $("#optionsOutput").css("max-height", $("#optionsOutput").height());
        $("#optionsOutput").css("min-height", $("#optionsOutput").height());

        //------------------------------------
        //  Update Total Votes
        //------------------------------------
        totalVotes = jsonObject.total_votes;
        $("#totalVotes").html(`<span>${jsonObject.total_votes}</span>VOTES`);

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
    function Vote(data) {

        if(!pollStarted) return;

        //------------------------------------
        //  Parse
        //------------------------------------
        var jsonObject = JSON.parse(data);

        //------------------------------------
        //  Increase Votes
        //------------------------------------
        totalVotes++;
        activeOptions[jsonObject.option]++;


        if (showVotes) 
        {
            var obj = new UserVote(jsonObject.name, jsonObject.option, userVoteAnimSpeed);


            if (voteQueue.length != 0 || isAnimating) 
            {
                voteQueue.push(obj);
            }
            else 
            {
                voteQueue.push(obj);
                obj.display(setIsAnimating, animDone, false);
                $("#votesOutput").append(obj.newVoteObject);
            }
        }


        //------------------------------------
        //  Animate Bars
        //------------------------------------
        for (var i in activeOptions) {
            var animPercent = (activeOptions[i] * 100 / totalVotes).valueOf();

            if (animPercent > 0) {
                createdPollOptions[i].animate(i, animPercent);
            }
        }

        //------------------------------------
        //  Update Total Votes
        //------------------------------------
        $("#totalVotes").html(`<span>${totalVotes}</span>VOTES`);
    }
    function Stop(data) {
        //------------------------------------
        //  Shutdown the Timer
        //------------------------------------
        var jsonObject = JSON.parse(data);
        timeLeft = 0;
        clearInterval(timer);
        runTimer();
        pollStarted = false;

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
    function Tie(data) {

        //  Convert to Object
        var jsonObject = JSON.parse(data);
       
       //---------------------------
       //   Hide all Options
       //---------------------------
       for (var i in activeOptions) {
           $(`#${i}`).animate({opacity: `0`}, {duration: 500,queue: true,complete: function () 
               {
                       $(`#${this.id}`).hide();

                       //---------------------------
                       //   Unhide Tie Option after last Active Option has finished hiding
                       //---------------------------
                        if (this.id == activeOptions.length - 1) {
                            $("#optionsTitle").html(`Tie`);

                            console.log(jsonObject.options);
                            for(var tie in jsonObject.options)
                            {
                                console.log(tie);
                                $(`#${tie}`).show();

                                $(`#${tie}`).animate({opacity: `1`}, {duration: 2000,queue: true,complete: function()
                                        {
                                            if(hideAfterMilisecs && tie == jsonObject.options[jsonObject.options.length-1])
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
                    }
                });
        }
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
        if (voteQueue.length > amountOfVotesToShow) {
            voteQueue[0].destroy();
            $("#votesOutput").append(voteQueue[amountOfVotesToShow].newVoteObject);
            voteQueue[amountOfVotesToShow].display(setIsAnimating, animDone, true);
            voteQueue.shift();
        }
        else {
            $("#votesOutput").append(voteQueue[voteQueue.length - 1].newVoteObject);
            voteQueue[voteQueue.length - 1].display(setIsAnimating, animDone, false);
        }
    }
}
