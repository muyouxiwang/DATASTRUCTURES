
var GetOp = {getop: function(){
    var flag = true;
    function select_all(){
        $("input:checkbox").each(function(){
        $(this).prop("checked", flag);}); 
        flag = !flag;
        $("#select_all").text({true: "全选",
                                false: "取消"}[flag]);
    }
    return select_all;
}};


function show_select(){
    var tt = ""
    for (var cid in selected_info){
        tt += companys.get_company_name(cid) + selected_info[cid].length + "/" + servers.get_cm_servers_num(cid) + "\n"
    
    }
    $("#selected_servers").text(tt);
    $("#selected_servers").scrollTop($("#selected_servers")[0].scrollHeight);
}


var AddSelect = {add: function(){
    var selected = [];
    $("input:checkbox").each(function(){

            if ($(this).prop("checked")){
            selected.push($(this).val());
            }});
    selected_info[curr_company] = [];
    for (var i=0; i<selected.length; i++){
        selected_info[curr_company].push(selected[i]);
    }
    show_select();
}}

var SelectCompany = {do_select: function(cid){
    curr_company = cid;
    var ss = "<div id='select_ctl'><span id='selected_cname'>"+ companys.get_company_name(cid) + "：</span><a class='btn_submit' id='select_all' href='#'>全选</a>";
    ss += "<a class='btn_submit' id='add_select' href='#'>添加</a>";
    ss += "</div>";

    ss += "<table></tr>";
    
    var count = 1;
    var ses = servers.get_cm_servers(cid);
    for (var i=0; i<ses.length; i++){
        var one = "<td><input type='checkbox' value='"+ ses[i].id +"'/><span>" + ses[i].name + "</span></td>";
        ss += one;
        if (count % 3 == 0){ ss += "</tr><tr>"; }
        count += 1;
    }
    ss += "</tr></table>";
    $("#servers").html(ss);

    set_command($("#select_all"), GetOpCommand(GetOp));
    set_command($("#add_select"), AddSelectCommand(AddSelect));
}};

function update_company_menu(){
    var cs = companys.get_all_companys();
    $("#companymenu").empty();
    for (var i=0; i<cs.length; i++){
        var tmp = $("<li><a href='#' id='selectcompany_"+cs[i].id+"'>"+cs[i].name+"</a></li>");
    $("#companymenu").append(tmp);
    set_command($("#selectcompany_"+cs[i].id), SelectCompanyCommand(SelectCompany, cs[i].id));
    }
}

var validataFunc = function(){
    var validator = new Validator();
    validator.add($("#active_name").val(), 'noempty:noillegalchar', "活动名称不能有特殊字符");
    validator.add($("#active_type").val(), 'noempty:onlyW', "活动类型只能由字母数字下划线组成");
    validator.add($("#script_name").val(), 'noempty:pyonly', "脚本文件必须是py脚本");

    return validator.start();
}



var DoActie = {do_act: function(){
    var sids = [];
for (var cid in selected_info){
    for (var i =0; i< selected_info[cid].length; i++){
        if (sids.indexOf(selected_info[cid][i]) == -1){
                sids.push(selected_info[cid][i]);
            }
        }
    }
    if (sids.length <= 0){
        alert("请选择运营商");
        return;
    }


    var errorMsg = validataFunc();
    if (errorMsg){
        alert(errorMsg);
        return;
    }


    do_active(active_name, active_type, script_name, sids, process_chart(sids.length));

    add_history(active_name, active_type, script_name);
    selected_info = {};
    curr_company = -1;
    show_select();
}}


function process_chart(total){
    $("#servers").empty();
    var gi = 1;
    function process(){
    $("#servers").circleChart({
            value: Math.round(100/total) * gi, 
            color: "#044AE3",
            animate: false,
            lineCap: "round",
            text: "执行中...",
            redraw: false,
      });
        gi += 1;
    }
    return process;
}


var SyncGm = {sync: function(){update_gm_data();}}


function add_active_fail(server_name){
    var tt = "失败：" + server_name + "\n";
    $("#active_results").text($("#active_results").text() + tt);
    $("#active_results").scrollTop($("#active_results")[0].scrollHeight);
}

function add_active_success(server_name){
    var tt = "成功：" + server_name + "\n";
    $("#active_results").text($("#active_results").text() + tt);
    $("#active_results").scrollTop($("#active_results")[0].scrollHeight);
}


var CheckResult = {check: function(){
    layer.open({
        type: 1,
        title: '欢迎页',
        maxmin: true,
        area: ['800px', '500px'],
        content: '为人民服务',
        end: function(){
        layer.tips('Hi', '#about', {tips: 1})
    } });
}}


var ChooseHistory = {choose: function(hid){
    $("#active_name").val(historys.get_active_name(hid));
    $("#active_type").val(historys.get_active_type(hid));
    $("#script_name").val(historys.get_act_script(hid));
    $("#acthistory").hide();
    $("#show_acthistory").toggleClass("show_h hide_h");
}}

var SelectHistory = {select: function(){
    if ($("#show_acthistory").hasClass("show_h")){
        var hh = historys.get_historys();
        $("#acthistory").empty();
        for (var i=0; i<hh.length; i++){
            var tmp = $("<li><a href='#' id='his_"+hh[i].id+"'>"+hh[i].actname+"</a></li>");
            $("#acthistory").append($(tmp)); 
            set_command($("#his_"+hh[i].id), ChooseHistoryCommand(ChooseHistory, hh[i].id));
        }
        $("#acthistory").show();
    }
    else {
        $("#acthistory").hide();
    }
    $("#show_acthistory").toggleClass("show_h hide_h");
}
}


set_command($("#checkresult"), CheckResultCommand(CheckResult));
set_command($("#checkprocess"), CheckProcessCommand(CheckProcess));
set_command($("#btn_logout"), QuitAppCommand(QuitApp));
set_command($("#do_active"), DoActiveCommand(DoActie));
set_command($("#syncgm"), SyncGmCommand(SyncGm));
set_command($("#show_acthistory"), SelectHistoryCommand(SelectHistory));

update_company_menu();


var selected_info = {};

var curr_company = -1;


