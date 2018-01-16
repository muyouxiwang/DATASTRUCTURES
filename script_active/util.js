

function add_info(data, cid, sid){
    if (cid in data){
        if (data[cid].indexOf(sid) == -1){
            data[cid].push(sid);
        }
    }
    else {
        data[cid] = [];
        data[cid].push(sid);
    }
}


function get_curr_sec(){
    return Math.round(new Date().getTime()/1000); 
}

function get_today_sec(){
    return Math.round(new Date().setHours(0, 0, 0, 0) / 1000);
}

