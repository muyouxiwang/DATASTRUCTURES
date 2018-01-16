
var create_data_historys = function(db){
    var _historys = [];
    var _infos = {};

    var init_data = function(){
        _historys = [];
        _infos = {};
        var data = db.select_db("select * from history where stime >= "+ get_today_sec() +" order by stime");
        for (var i =0; i<data.length; i++){
            var item = {"id": data[i][0],
                            "actname": data[i][1],
                            "acttype": data[i][2],
                            "filename": data[i][3],
                            "stime": data[i][4]};
            _historys.push(item);
            _infos[item.id] = item;
        }
    }

    init_data();

    return {
get_historys: function(){
    return _historys;
              },
add_history: function(active_name, active_type, script_name){
    var sql = "insert into history(actname, acttype, filename, stime) values ";
    sql += "('"+active_name+"','"+active_type+"','"+script_name+"',"+get_curr_sec()+")";
    db.exec_db(sql);
    init_data();
             },
get_active_type: function (hid){
        if (_infos[hid]){return _infos[hid].acttype;}
        else {return "";}
            },
get_act_script: function (hid){
        if (_infos[hid]) {return _infos[hid].filename;}
        else {return "";}
            }
    };
}



var create_data_companys = function(db){
    var _companys = {};

    var init_data = function(){
        _companys = {};
        var data = db.select_db("select * from company");
        for (var i=0; i<data.length; i++){
            var item = {"id": data[i][0], 
                                "name": data[i][1]};
            _companys[item.id] = item;
    }};

    init_data();


    return {
get_company_name: function(cid){
        if (_companys[cid]){ return _companys[cid].name; }
        else {return null;}
                  },
get_all_companys: function(){
    var res = [];
    for (var cid in _companys){
        res.push({id: cid, name: _companys[cid].name});
    }
    return res;
                  },
update_companys: function(company_data){
    db.exec_db("delete from company");
    var sql = "insert into company (id, name) values ";
    var cc = [];
    for (var i=0; i<company_data.length; i++){
cc.push("("+company_data[i].id+", \""+company_data[i].name+"\")");
    }
    sql += cc.join(",");
    db.exec_db(sql);
    init_data();

                 }
    };
}


var create_data_servers = function(db){
    var _servers = [];
    var _server_infos = {};
    var _com_serv = {};

    var init_data = function(){
        _servers = [];
        _server_infos = {};
        _com_serv = {};
        var data = db.select_db("select * from server");
        for (var i=0; i<data.length; i++){
            var item = {"id": data[i][0],
                        "name": data[i][1],
                        "ip": data[i][2],
                        "lname": data[i][3],
                        "passwd": data[i][4],
                        "mkey": data[i][5],
                        "comid": data[i][6]};
            _servers.push(item);
            _server_infos[item.id] = item;
            add_info(_com_serv, data[i][6], data[i][0]);
        }
    };
    
    init_data();

    return {
get_cm_servers: function (cid){
    var ss = [];
    for (var i=0; i<_com_serv[cid].length; i++){
        ss.push(_server_infos[_com_serv[cid][i]]);
    }
    return ss;
},

get_cm_servers_num: function (cid){
    return _com_serv[cid].length;
},

get_server_name: function (sid){
return _server_infos[sid].name;
},

get_server_ip: function (sid){
    return _server_infos[sid].ip;
},

get_server_passwd: function (sid){
    return _server_infos[sid].passwd;
},

get_server_lname: function (sid){
    return _server_infos[sid].lname;
},

get_server_mkey: function (sid){
    return _server_infos[sid].mkey;
},

update_servers: function (server_data){
    db.exec_db("delete from server");
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
    db.exec_db(sql);

    init_data();

},
    };
}

var companys = getSingleObj(create_data_companys)(db);

var servers = getSingleObj(create_data_servers)(db);

var historys = getSingleObj(create_data_historys)(db);





