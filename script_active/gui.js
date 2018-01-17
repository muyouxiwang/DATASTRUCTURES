
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

var AddSelect = {add: function (){
    var selected = [];
    $("input:checkbox").each(function(){

    if ($(this).prop("checked")){
        selected.push($(this).val());
       }});
    selected_info[curr_company] = [];
    for (var i=0; i<selected.length; i++){
            selected_info[curr_company].push(selected[i]);
        }
    var tt = ""
    for (var cid in selected_info){
        tt += companys.get_company_name(cid) + selected_info[cid].length + "/" + servers.get_cm_servers_num(cid) + "\n"
    
    }
    $("#selected_servers").text(tt);
    $("#selected_servers").scrollTop($("#selected_servers")[0].scrollHeight);
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

update_company_menu();

function update_history(){
    var hh = historys.get_historys();
    $("#acthistory").empty();
    var tmp = "";
    for (var i=0; i<hh.length; i++){
        tmp = "<option value='"+hh[i].id+"'>"+hh[i].actname+"</option>"
            $("#acthistory").append($(tmp));
    }
}

function update_history_panel(){
    update_history();
    show_active_name();
}

update_history_panel();






function show_active_name(){
var hid = $("#acthistory").val();
$("#active_name").val($("select option[value='"+ hid +"']").text());
$("#active_type").val(historys.get_active_type(hid));
$("#script_name").val(historys.get_act_script(hid));
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
    var active_name = $("#active_name").val();
    var active_type = $("#active_type").val().toLowerCase();
    var script_name = $("#script_name").val();
    if (!(active_name && active_type && script_name)) {
        alert("请完善活动信息");
        return;
    }
    var p = new RegExp(/\W/g);
    if (p.test(active_type)){
        alert("活动类型只能由字母数字下划线组成");
        return;
    }
    var tt = script_name.split(".");
    if (tt.length!=2 || tt[1].toUpperCase()!="PY"){
        alert("脚本文件必须是py脚本");
        return;
    }

    do_active(active_name, active_type, script_name, sids);
}}



var SyncGm = {sync: function(){update_gm_data();}}


function add_active_fail(server_name){
    var tt = "失败：" + server_name + "\n";
    $("#active_results").text($("#active_results").text() + tt);
    $("#active_results").scrollTop($("#selected_servers")[0].scrollHeight);
}

function add_active_success(server_name){
    var tt = "成功：" + server_name + "\n";
    $("#active_results").text($("#active_results").text() + tt);
    $("#active_results").scrollTop($("#selected_servers")[0].scrollHeight);
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

set_command($("#checkresult"), CheckResultCommand(CheckResult));
set_command($("#checkprocess"), CheckProcessCommand(CheckProcess));
set_command($("#btn_logout"), QuitAppCommand(QuitApp));
set_command($("#do_active"), DoActiveCommand(DoActie));
set_command($("#syncgm"), SyncGmCommand(SyncGm));



