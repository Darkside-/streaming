class UserVote
{
    constructor(name,id,animSpeed) 
    {
        this.animSpeed = animSpeed;
        this.newVoteObject = $($.parseHTML(`<div class="voteBase"><span>${name}</span><span class="floatRight">${id}</span></div>`));
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