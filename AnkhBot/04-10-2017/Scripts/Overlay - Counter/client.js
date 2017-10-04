if (window.WebSocket) {
    //---------------------------------
    //  Variables
    //---------------------------------
	//  Connection Information
	var serviceUrl = "ws://127.0.0.1:3337/AnkhBot";
	var socket = null;
	var reconnectIntervalMs = 10000;   
    var counterUpdateQueue = [];
    var isAnimating = false;
    
    //---------------------------------
    //  Animations
    //---------------------------------
    var FadeIn = anime.timeline({autoplay: false});
    FadeIn.add({
        targets: '.bar',
        opacity: 0.90,
        easing: 'linear',
        duration: 1000,
        begin: function ()
        {
            isAnimating = true;
            console.log("DDoing Shit");
        }
    }).add({
        targets: '.bar p',
        opacity: 1,
        fontSize: 70,
        easing: 'easeOutQuart',
        offset: 750,
        duration: 1000
    }).add({
        targets: ['.bar'],
        opacity: 0,
        easing: 'linear',
        offset: 2500,
        duration: 1000,
        complete: function()
        {                
            setTimeout(function(){
                Dequeue();
            },500);
        }
    });
    
    
	function Connect() {
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
					"EVENT_COUNTER_INCREASE",
					"EVENT_COUNTER_DECREASE",
					"EVENT_COUNTER_SET"
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
	
            console.log(jsonObject);
			//------------------------------------
			//  Pass Data to correct Functions
			//------------------------------------
			if (jsonObject.event == "EVENT_COUNTER_INCREASE") 
            {
				Increase(JSON.parse(jsonObject.data));
			}
			else if (jsonObject.event == "EVENT_COUNTER_DECREASE") 
            {
				Decrease(JSON.parse(jsonObject.data));
			}
			else if (jsonObject.event == "EVENT_COUNTER_SET") 
            {
				Set(JSON.parse(jsonObject.data));
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
    
    function Increase(data)
    {
        EnQueue(data.template_msg.replace("#",data.deaths));
    }
    
    function Decrease(data)
    {
        EnQueue(data.template_msg.replace("#",data.deaths));
    }
    
    function Set(data)
    {
        EnQueue(data.template_msg.replace("#",data.deaths));
    }
    
    function EnQueue(msg)
    {
        if(counterUpdateQueue.length != 0 || isAnimating)
        {
            counterUpdateQueue.push(msg);
        }
        else
        {
            $(`.bar p`).html(msg);
            FadeIn.restart();
        }
    }
    
    function Dequeue()
    {
        console.log("A");
        var obj = counterUpdateQueue[0];
        
        if(obj == null || obj == undefined)
        {
            isAnimating = false;
            return;
        }
        
        $(`.bar p`).html(obj);
        FadeIn.restart();
        counterUpdateQueue.shift();
    }
}
