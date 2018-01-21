const path = require('path')
const url = require('url')

module.paths.push('C:/Users/youease_server01/AppData/Roaming/npm/node_modules')
module.paths.push('C:/Users/muyouxiwang/AppData/Roaming/npm/node_modules')




var fs = require("fs");
var sqldb = require("sql.js");

var fb = fs.readFileSync("./data.db");

var db = new sqldb.Database(fb);


function show_company(){
    //var res = db.exec("select * from company");
    //var res = db.exec("select * from server");
    var res = db.exec("select * from history order by id desc limit 10");


    if (res){
        //console.log(res);
        var result = res[0].values;

        for (var i=0; i<result.length; i++){
            console.log(result[i][0]);
            console.log(result[i][1]);
        }
    }
}

//db.exec("insert into company(id, name) values (103, '共和国')");


//db.exec("insert into company(id, name) values (101, '共和国'), (102, '共和国')");

//db.exec("delete from company where id >= 100");

//show_company();


var request = require('request');


var act_url = 'http://www.baidu.com';
//var act_url = 'http://192.168.1.42/activity/send';
//

function count_down(){
    var times = 20;
    function __(){
        times -= 1;
        if (times == 0){
            console.log("=====\nthat's enough\n===============\n");
        }
    }
    return __;
}


function test_http_get(){
    request(act_url, function (error, response, body) {
      if (!error && response.statusCode == 200) {
        console.log(body) // Show the HTML for the baidu homepage.
      }
    });
}

//test_http_get();

//request.post({url:'http://service.com/upload', form:{key:'value'}}, function(error, response, body) {
    //if (!error && response.statusCode == 200) {
    //}
//})

function get_curr_sec(){
    return Math.round(new Date().getTime()/1000); 
}

function test_akey(){

    var atime = get_curr_sec() - 60;
    var passwd = $.md5("test");
    var akey = $.md5($.md5("test" + passwd) + atime, + "test");

    console.log("the key is :" + akey)
}

test_akey();
