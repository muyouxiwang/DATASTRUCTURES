
module.paths.push('C:/Users/youease_server01/AppData/Roaming/npm/node_modules');

var request = require('request');
var fs = require("fs");
var sqldb = require("sql.js");
var fb = fs.readFileSync("./data.db");
var db = new sqldb.Database(fb);

function get_companys(){

    var companys = [];

    var res = db.exec("select * from company");
    if (res[0]){
        var result = res[0].values;
        for (var i=0; i<result.length; i++){
            companys.push({"id": result[i][0], 
                            "name": result[i][1]});
        }
    }
    return companys;
}

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

var servers = [];
var server_infos = {};
var com_serv = {};
var serv_com = {};
function init_servers(){
    servers = [];
    server_infos = {};
    com_serv = {};
    serv_com = {};
    var res = db.exec("select * from server");
    if (res[0]){
        var result = res[0].values;
        for (var i=0; i<result.length; i++){
        var one = {"id": result[i][0],
                        "name": result[i][1],
                        "ip": result[i][2],
                        "lname": result[i][3],
                        "passwd": result[i][4],
                        "mkey": result[i][5],
                        "comid": result[i][6]};
            servers.push(one);
            server_infos[one.id] = one;
            add_info(com_serv, result[i][6], result[i][0]);
            serv_com[result[i][0]] = result[i][6];
            }
        }
}


function get_historys(){
    var historys = [];
    var res = db.exec("select * from history where stime >= "+ get_today_sec() +" order by stime");
    if (res){
        var result = res[0].values;
        for (var i=0; i<result.length; i++){
            historys.push({"id": result[i][0],
                            "actname": result[i][1],
                            "acttype": result[i][2],
                            "filename": result[i][3],
                            "stime": result[i][4]});
        }
    }
    return historys;
}



function get_active_type(hid){
    for (var i=0; i<historys.length; i++){
        if (historys[i].id==hid)
            return historys[i].acttype;
    }

    return "";
}


function get_act_script(hid){
    for (var i=0; i<historys.length; i++){
        if (historys[i].id==hid)
            return historys[i].filename;
    }

    return "";
}

function get_curr_sec(){
    return Math.round(new Date().getTime()/1000); 
}

function get_today_sec(){
    return Math.round(new Date().setHours(0, 0, 0, 0) / 1000);
}

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
    db.exec("delete from company");
    var sql = "insert into company (id, name) values ";
    var cc = [];
    for (var i=0; i<company_data.length; i++){
cc.push("("+company_data[i].id+", \""+company_data[i].name+"\")");
    }
    sql += cc.join(",");
    //console.log(sql);
    db.exec(sql);

    var buffer = new Buffer(db.export());
    fs.writeFileSync("./data.db", buffer);
    companys = get_companys();
    update_company_menu();
}


function add_history(active_name, active_type, script_name){
    var sql = "insert into history(actname, acttype, filename, stime) values ";

    sql += "('"+active_name+"','"+active_type+"','"+script_name+"',"+get_curr_sec()+")";

    db.exec(sql);
    var buffer = new Buffer(db.export());
    fs.writeFileSync("./data.db", buffer);

    historys = get_historys();

    update_history_panel();

}

function update_servers(server_data){
    db.exec("delete from server");
    var sql = "insert into server (id,name,ip,lname,passwd,mkey,comid) values ";
    var ss = [];
    for (var i=0; i<server_data.length; i++){
ss.push("("+server_data[i].id+
            ", \""+server_data[i].name+
            "\", \""+server_data[i].ip+
            "\", \""+server_data[i].lname+
            "\", \""+server_data[i].passwd+
            "\", \""+server_data[i].mkey+
            "\", \""+server_data[i].comid+
            "\")");
    }
    sql += ss.join(",");
    console.log(sql);
    db.exec(sql);

    var buffer = new Buffer(db.export());
    fs.writeFileSync("./data.db", buffer);
    init_servers();
}



function get_company_name(cid){
    for (var i=0; i<companys.length; i++){
        if (cid == companys[i].id){
            return companys[i].name;
        }
    }    
}

function get_server_name(sid){
    return server_infos[sid].name;
}

function get_server_ip(sid){
    return server_infos[sid].ip;
}

function get_server_passwd(sid){
    return server_infos[sid].passwd;
}

function get_server_lname(sid){
    return server_infos[sid].lname;
}

function get_server_mkey(sid){
    return server_infos[sid].mkey;
}


function do_one_server_active(active_name, active_type, script_name, sid, count_down){
    var server_name = get_server_name(sid);
    var server_ip = get_server_ip(sid);

    var atime = get_curr_sec() - 60;
    var passwd = $.md5(get_server_passwd(sid));
    var akey = $.md5($.md5(get_server_lname(sid) + passwd) + atime + get_server_mkey(sid));


    var act_url = "http://"+server_ip+"/activity/scriptactive";

    var post_data = {'aname':active_name,
        'acttype':active_type,
        'filename':script_name,
        'atime':atime,
        'akey':akey,
        'issync':1};



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


var companys = get_companys();
init_servers();
var historys = get_historys();

var selected_info = {};

var curr_company = -1;



