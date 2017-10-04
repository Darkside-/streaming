class UserBet
{
    constructor(name,id,amount,animSpeed) 
    {
        this.animSpeed = animSpeed;
        this.newVoteObject = $($.parseHTML(`<div class="betBase"><span>${name}</span><span class="floatRight">${id} - ${amount}</span></div>`));
    }

    display(isAnim, animDone, timeout)
    {
        this.newVoteObject.animate({opacity: 1},{duration: this.animSpeed,queue: true,
        start: function()
        {
            isAnim(true);
        },
        complete: function()
        {
            if(timeout)
            {
            setTimeout(function() {
                isAnim(false);
                animDone();
            },1000)
            }
            else
            {
                isAnim(false);
                animDone();
            }
        }}); 
    }

    destroy()
    {
        this.newVoteObject.animate({ height: 'toggle', opacity: 'toggle' },{duration: this.animSpeed,queue: true,
                    complete: function()
                    {
                        $(this).remove();
                    }
                }); 
    }
}