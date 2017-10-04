if( window.WebSocket ){
    //---------------------------------
    //  Variables
    //---------------------------------
    var serviceUrl = "ws://127.0.0.1:3337/AnkhBot"
    var socket = new WebSocket(serviceUrl);
    var animQueue = [];
    var outputDiv = document.getElementById('output');
    var isAnimating = false;
    var rainbowClass = ["red","orange","yellow","green","blue","indigo","violet"];
    var rainbowID = 0;
    var animationEvent = whichAnimationEvent();

    $("#currStyle").attr("href",settings.Style);
    //---------------------------------
    //  Events
    //---------------------------------
    socket.onopen = function()
    {
        // Format your Authentication Information
        var auth = {
            author: "AnkhHeart",
            website: "https://AnkhBot.com",
            api_key: API_Key,
            events: [
                "EVENT_CURRENCY_SHOW",
                "EVENT_CURRENCY_RELOAD"
            ]
        }
        
        //  Send your Data to the server
        socket.send(JSON.stringify(auth));
        console.log("Connected");
    };

    socket.onerror = function(error)
    {
        //  Something went terribly wrong... Respond?!
        console.log("Error: " + error);
    }

    socket.onmessage = function (message) 
    {
        var jsonObject = JSON.parse(message.data);

		if(jsonObject.event == "EVENT_CURRENCY_SHOW")
		{
             var arr = JSON.parse(jsonObject.data);

             for(var key in arr)
             {
                // Create Object
                var newDiv = document.createElement('div');
                newDiv.innerHTML += "<span>"+ key + "</span> <span class=\"floatRight\">" + arr[key].toLocaleString() + " Points</span>";
                $(newDiv).addClass("base");
                $(newDiv).addClass("anim");

                // Do Rainbow Shit
                if(settings.RainbowMode)
                {
                    rainbowID = rainbowID % 7;
                    $(newDiv).addClass(rainbowClass[rainbowID]);
                    rainbowID++;
                }
                
                
                // Setup Events
                $(newDiv).one(animationEvent,
                function(event) 
                {
                    $(newDiv).removeClass("anim");

                    getNextItem();
                });

                if(animQueue.length != 0 || isAnimating)
                {
                    animQueue.push(newDiv);
                    
                }
                else
                {
                    animQueue.push(newDiv);
                    getNextItem();
                }
             }
			 
			 
		}
        else if(jsonObject.event == "EVENT_CURRENCY_RELOAD")
        {
            //  Pass Data Along
            var jsonData = JSON.parse(jsonObject.data);
            loadSettings(jsonData);
        }
    }

    socket.onclose = function () 
    {
        //  Connection has been closed by you or the server
        console.log("Connection Closed!");
    }   

    function getNextItem()
    {
        removeFirstDiv();

        //  Add Item
        var next = animQueue.shift();
        if (typeof next !== 'undefined') 
        {
            isAnimating = true;
            outputDiv.appendChild(next);
        }
        else
        {
           isAnimating = false; 
        } 
    }

    function removeFirstDiv()
    {
        if(outputDiv.childElementCount > settings.MaxVisible)
        {
            var previousDiv = $(document.querySelector(".base:first-child"));
            if (previousDiv !== null) 
            {
                previousDiv.addClass("deleteAnim");
                previousDiv.one(animationEvent,
                function(event) 
                {
                    outputDiv.removeChild(this);
                });
            }
        }
    }

    function whichAnimationEvent() {
        var t,
            el = document.createElement("fakeelement");

        var animations = {
            "animation": "animationend",
            "OAnimation": "oAnimationEnd",
            "MozAnimation": "animationend",
            "WebkitAnimation": "webkitAnimationEnd"
        }

        for (t in animations) {
            if (el.style[t] !== undefined) {
                return animations[t];
            }
        }
    }
    
    function loadSettings(jsonData) {
        settings = jsonData;
        $("#currStyle").attr("href",settings.Style);
    }
}