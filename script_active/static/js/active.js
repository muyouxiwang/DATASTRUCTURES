



function init_menu(){
    $("ul>li").removeClass("menu_down");
    $("ul>li").addClass("menu_up");
}

function get_post_data(post_keys){
	var data = {};
	for (var k in post_keys){
		data[post_keys[k]] = $("#"+post_keys[k]).val();
	}
	return data;
}

function check_input(fileid, alertmsg){
	if (!$("#"+fileid).val()){
		alert(alertmsg);
		return false;
	}
	return true;
}


function change_menu_status(menuid){
    init_menu();
    $("#"+menuid).addClass("menu_down");
}





