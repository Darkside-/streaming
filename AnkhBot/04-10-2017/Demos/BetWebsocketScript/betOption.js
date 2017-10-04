class BetOption
{
    constructor(id, percentage,data, animSpeed) 
    {
        this.animSpeed = animSpeed;
        
        //------------------------------------
        //  Update & Calculate %
        //------------------------------------
        if ($(`#${id}`).length == 0) 
        {
            //---------------------------------------------
            //  Generate new Options
            //---------------------------------------------
            var newOption = `<div id="${id}" class="optionContainer">`;
            newOption += `<div class="option">${data.options[id].Key} (!bet ${id} &#60;amount&#62;)</div>`

            if (percentage != 0)
                newOption += `<div class="bets"><span id="bet_${id}" style="width: ${percentage}%;">${percentage}%</span></div>`;
            else
                newOption += `<div class="bets"><span id="bet_${id}" style="width: 0%;">&nbsp0.00%</span></div>`;

            newOption += `</div>`;

            this.newUserObject = $($.parseHTML(newOption));
            this.percentage = percentage;
        }
        return null;
    }

    update(id,percentage,data)
    {
        this.percentage = percentage;

        $(`#${id}`).show();
        $(`#${id}`).css("opacity", 1);
        
        //---------------------------------------------
        //  Update Values incase of changes
        //---------------------------------------------
        $(`#${id} .option`).html(`${data.options[id].Key} (!bet ${id} &#60;amount&#62;)`);
        $(`#bet_${id}`).width(`${percentage}%`);

        if (percentage != 0)
            $(`#bet_${id}`).html(`${percentage}%`);
        else
            $(`#bet_${id}`).html(`&nbsp0.00%`);        
    }

    animate(id,percentage)
    {
        $(`#bet_${id}`).animate({
                width: `${percentage.toFixed(2)}%`
                },{
                duration: this.animSpeed,
                queue: true,
                step: function(now, tween){
                    $(`#${this.id}`).html(`${now.toFixed(2)}%`);
                }});
    }
    
    /*destroy()
    {
        this.newUserObject.animate({opacity: 0},{duration: 500,queue: true,
                    step: function(now, tween)
                    {
                        $(this).remove();
                    }
                    }); 
    }*/
}