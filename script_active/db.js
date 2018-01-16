
module.paths.push('C:/Users/youease_server01/AppData/Roaming/npm/node_modules');

var fs = require("fs");
var sqldb = require("sql.js");



var getSingleObj = function (fn){
    var result;
    return function(){
        return result || (result = fn.apply(this, arguments));
    }
}

var create_db = function(db_name){
    var _fb = fs.readFileSync(db_name);
    var _db = new sqldb.Database(_fb);

    return {
select_db : function(sql){
       var res = _db.exec(sql);
       return res[0]? res[0].values:[];
            },
exec_db : function(sql){
        _db.exec(sql);
        var buffer = new Buffer(_db.export());
        fs.writeFileSync(db_name, buffer);
          }
    }
}

var get_db = getSingleObj(create_db);

var db = get_db("./data.db");


//console.log(db.select_db("select * from company"));
//db.exec_db("delete from company");

//db.exec_db("insert into company(id, name)values (1, 'jack'), (3, 'tom')")
//db.exec_db("insert into company(id, name)values (6, 'jack'), (9, 'tom')")
//console.log(db.select_db("select * from company"));

//db.exec_db("delete from company where id = 1");
//console.log(db.select_db("select * from company"));





