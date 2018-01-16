
module.paths.push('C:/Users/youease_server01/AppData/Roaming/npm/node_modules');

var request = require('request');
var fs = require("fs");
var sqldb = require("sql.js");
var fb = fs.readFileSync("./data.db");
var db = new sqldb.Database(fb);










function update_gm_data(){
//var gm_url = "http://hssg.gm.youease.net"
var gm_url = "http://192.168.1.6:8889"
var data_urls = {
             'company': gm_url + "/get_server_data_for_active/company_datas/", 
             'server': gm_url + "/get_server_data_for_active/server_datas/" 
             }

var interface_key = "oPvmOwPWEIO1dPfvAEWy(dtusL1doFpHenE#yVKUThZTzUS22zVg8txhzV2IyzW4hdTtqjPzTgNsVB*LVeJtCBdo8Lk4SRlGneqD7o"

var ctime = get_curr_sec();
var key = $.md5($.md5(interface_key) + ctime);

var post_data = {"key": key, "ctime": ctime};





request.post({url: data_urls['company'], form: post_data}, 
                function(error, response, body) {
    if (!error && response.statusCode == 200) {
        sync_gm_data('company', body);
    }
});

request.post({url: data_urls['server'], form: post_data}, 
                function(error, response, body) {
    if (!error && response.statusCode == 200) {
        sync_gm_data('server', body);
    }
});

}


function sync_gm_data(data_type, data){
    var data = JSON.parse(data);
    if (data_type == "company"){
        update_companys(data);
    }
    if (data_type == "server"){
        update_servers(data);
    }
}

/*
{"id": 1, "name": "\u6e38\u6613"}

{"name": "mi0102mixi",
"passwd": "XUGSG1K8p2qrP6ac6n0KaLqPechkpVdnjmJumuBgwwIQBSwbfGVU",
"ip": "210.168.45.18",
"comid": 8,
"lname": "rt5odz8Arvcr9pFG02RNkV104",
"id": 100867,
"mkey": "sdlfsdflsdf"}
*/

function update_companys(company_data){
    companys.update_companys(company_data);
    update_company_menu();
}


function add_history(active_name, active_type, script_name){
    historys.add_history(active_name, active_type, script_name);
    update_history_panel();
}

function update_servers(server_data){
    servers.update_servers(server_data);
}






function do_one_server_active(active_name, active_type, script_name, sid, count_down){
    var server_name = servers.get_server_name(sid);
    var server_ip = servers.get_server_ip(sid);

    var atime = get_curr_sec() - 60;
    var passwd = $.md5(servers.get_server_passwd(sid));
    var akey = $.md5($.md5(servers.get_server_lname(sid) + passwd) + atime + servers.get_server_mkey(sid));


    var act_url = "http://"+server_ip+"/activity/scriptactive";

    var post_data = {'aname':active_name,
        'acttype':active_type,
        'filename':script_name,
        'atime':atime,
        'akey':akey,
        'issync':1};



add_active_success(server_name);
console.log("iam done:" + server_name);
count_down();


/*
    request.post({url: act_url, form: post_data}, 
            function(error, response, body) {
            if (!error && response.statusCode == 200) {
                var data = JSON.parse(body);
                if (data.retcode != "SUCCESS"){
                    console.log("error:" + server_name + ":" + data.retmsg)
                    add_active_fail(server_name);
                    }
                else {
                    add_active_success(server_name);
                    count_down();
                    }
            }
            else {
                add_active_fail(server_name);
                console.log("net error :" + error);
            }
            });
*/
}


function set_counter(count, callback){
    var num = count;
    function count_down(){
        num -= 1;
        if (num == 0){
            console.log("just finished ...");
            callback();
        }
    }
    return count_down;
}

function do_active(active_name, active_type, script_name, sids){
    function add(){
        add_history(active_name, active_type, script_name);
    }
    count_down = set_counter(sids.length, add);

    for (var i=0; i< sids.length; i++){
        do_one_server_active(active_name, active_type, script_name, sids[i], count_down)
    }
    selected_info = {};
}



var selected_info = {};

var curr_company = -1;



