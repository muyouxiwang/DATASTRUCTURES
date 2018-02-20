
var black_chess = {r:"车", n:"马", b:"象", a:"士", k:"将", c:"炮", p:"卒"}
var white_chess = {R:"车", N:"马", B:"相", A:"仕", K:"帅", C:"炮", P:"兵"}


function draw_board(pin){
    alert("shit");
    var boardval = [];
    pin = pin.slice(0, -10);
    for (var i=0; i<pin.length; i++){
        var tmp = pin[i];
        if(parseInt(tmp)){
            for (var j=0; j<tmp; j++){
                boardval.push("o");
            }
        }
        else if(tmp=="/"){
            continue;
        }
        else {
            boardval.push(tmp);
        }
    }

    var canvas = document.getElementById("board");
    var ctx = canvas.getContext("2d");

    var o = 15;
    for (var i=0; i<=270; i+=30){
        ctx.moveTo(0+o, i+o);
        ctx.lineTo(240+o, i+o);
        ctx.moveTo(i+o, 0+o);
        ctx.lineTo(i+o, 120+o);
        ctx.moveTo(i+o, 150+o);
        ctx.lineTo(i+o, 270+o);

        ctx.moveTo(90+o, 0+o);
        ctx.lineTo(150+o, 60+o);
        ctx.moveTo(150+o, 0+o);
        ctx.lineTo(90+o, 60+o);

        ctx.moveTo(90+o, 210+o);
        ctx.lineTo(150+o, 270+o);
        ctx.moveTo(150+o, 210+o);
        ctx.lineTo(90+o, 270+o);

        ctx.moveTo(0+o, 120+o);
        ctx.lineTo(0+o, 150+o);
        ctx.moveTo(240+o, 120+o);
        ctx.lineTo(240+o, 150+o);
    }
    ctx.stroke();

    for(var j=0; j<=270; j+=30){
        for (var i=0; i<=240; i+=30){
            var cur = boardval.shift();
            if (cur in black_chess){
                ctx.beginPath();
                ctx.arc(i+o, j+o, 15, 0, 2*Math.PI, true); 
                ctx.fillStyle = "black"
                    ctx.fill();
                ctx.fillStyle = "white"
                    ctx.font = "24px serif";
                ctx.fillText(black_chess[cur], i+3, j+o+9);
            }
            else if (cur in white_chess){
                ctx.beginPath();
                ctx.arc(i+o, j+o, 15, 0, 2*Math.PI, true); 
                ctx.fillStyle = "white"
                    ctx.fill();
                ctx.fillStyle = "red"
                    ctx.font = "24px serif";
                ctx.fillText(white_chess[cur], i+3, j+o+9);
            }
        }
    }
}
