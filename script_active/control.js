module.paths.push('C:/Users/youease_server01/AppData/Roaming/npm/node_modules');

const {ipcRenderer} = require("electron");
var request = require('request');
var fs = require("fs");
var sqldb = require("sql.js");
var fb = fs.readFileSync("./data.db");
var db = new sqldb.Database(fb);


var set_command = function(btn, command){
    btn.bind("click", command.execute);
}


var CheckResultCommand = function(receiver){
    return {execute: function(){receiver.check();}}
}


var CheckProcess = {check: function(){
    console.log("check process");
}}

var CheckProcessCommand = function(receiver){
    return {execute: function(){receiver.check();}}
}

var QuitApp = {quit: function(){
    ipcRenderer.send("quit_app");
}}

var QuitAppCommand = function(receiver){
    return {execute: function(){receiver.quit();}}
}

var SelectCompanyCommand = function(receiver, cid){
    return {execute: function(){receiver.do_select(cid);}}
}

var AddSelectCommand = function(receiver){
    return {execute: function(){receiver.add();}}
}

var GetOpCommand = function(receiver){
    return {execute: receiver.getop()}
}

var DoActiveCommand = function(receiver){
    return {execute: function(){receiver.do_act();}}
}

var SyncGmCommand = function(receiver){
    return {execute: function(){receiver.sync();}}
}

var SelectHistoryCommand = function(receiver){
    return {execute: function(){receiver.select();}}
}

var ChooseHistoryCommand = function(receiver, hid){
    return {execute: function(){receiver.choose(hid);}}
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


function do_update_gm_data(data_type){
    request.post({url: data_urls[data_type], form: post_data}, 
            function(error, response, body) {
                if (!error && response.statusCode == 200) {
                    var data = JSON.parse(body);
                    var tt = {"company": function(){
                    companys.update_companys(data);
                    update_company_menu(); },

                    "server": function(){
                    servers.update_servers(data);} 
                    };
                    tt[data_type]();
            }
        });
}

do_update_gm_data("company");
do_update_gm_data("server");

}




function add_history(active_name, active_type, script_name){
    historys.add_history(active_name, active_type, script_name);
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
                    }
            }
            else {
                add_active_fail(server_name);
                console.log("net error :" + error);
            }
            count_down();
        });
*/

}


function set_counter(count, callback){
    var num = count;
    function count_down(){
        callback();
        num -= 1;
        if (num == 0){
            console.log("just finished ...");
        }
    }
    return count_down;
}

function do_active(active_name, active_type, script_name, sids, callback){
    count_down = set_counter(sids.length, callback);

    for (var i=0; i< sids.length; i++){
        do_one_server_active(active_name, active_type, script_name, sids[i], count_down);
    }
}


var strategies = {
noillegalchar: function(value, errorMsg){
    var illegalchars = ["%", "/", "&", "#"];
    for (var i=0; i<illegalchars.length; i++)
        if (value.indexOf(illegalchars[i]) !=-1)
            return errorMsg;
               },

onlyW: function(value, errorMsg){
    var p = new RegExp(/\W/g);
    if (p.test(value))
        return errorMsg;
                },

pyonly: function(value, errorMsg){
    var tt = value.split(".");
    if (tt.length!=2 || tt[1].toUpperCase()!="PY")
        return errorMsg;
                },

noempty: function(value, errorMsg){
    if (!value)
        return errorMsg;
                }

}


var Validator = function(){
    this.cache = [];
}

Validator.prototype.add = function(value, rule, errorMsg){
    var rules = rule.split(":");
    for (var i=0; i<rules.length; i++){
        that = this;
        (function (x){
        that.cache.push(function(){
            return strategies[rules[x]](value, errorMsg);
                });})(i);
        }
}

Validator.prototype.start = function(){
    for (var i=0; i< this.cache.length; i++){
        var errorMsg = this.cache[i]();
        if (errorMsg)
            return errorMsg;
    }
}



