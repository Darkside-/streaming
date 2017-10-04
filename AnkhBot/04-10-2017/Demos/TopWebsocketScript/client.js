if( window.WebSocket ){
    //---------------------------------
    //  Variables
    //---------------------------------
    var serviceUrl = "ws://127.0.0.1:3337/AnkhBot"
    var socket = new WebSocket(serviceUrl);
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
                "EVENT_TOP_10_POINTS",
                "EVENT_TOP_10_HOURS"
            ]
        }
        
        //  Send your Data to the server
        socket.send(JSON.stringify(auth));
    };

    socket.onerror = function(error)
    {
        //  Something went terribly wrong... Respond?!
        console.log("Error: " + error);
    }

    socket.onmessage = function (message) 
    {
        var jsonObject = JSON.parse(message.data);

		if(jsonObject.event == "EVENT_TOP_10_POINTS" || jsonObject.event == "EVENT_TOP_10_HOURS")
		{
			 var outputDiv = document.getElementById('output');
			 
			 var output  = "";
			 
             console.log(jsonObject);
             var arr = JSON.parse(jsonObject.data);
             console.log(arr);
             outputDiv.innerHTML = ""; 

             for(var key in arr)
             {
                 outputDiv.innerHTML += "<div class=\"anim\"><span>"+arr[key][0] + "</span> <span class=\"floatRight\">" + arr[key][1] + "</span></div>";
             }
			 
			 
		}
        //  You have received new data now process it
        //console.log(message.data);
    }

    socket.onclose = function () 
    {
        //  Connection has been closed by you or the server
        console.log("Connection Closed!");
    }    
}