/**
 * Created by LENOVO on 2018/3/31.
 */
function addTableHeader(table_header_list, table_header_id) {
     var head_list = table_header_list;
     var new_table_row = document.createElement("tr");
    for(var i = 0; i< head_list.length ; i++){
        var new_table_header = document.createElement('th');
        new_table_header.innerText = table_header_list[i].name;
        new_table_row.appendChild(new_table_header);
    }
    document.getElementById(table_header_id).appendChild(new_table_row);
}

function addTableBody(table_data_list, table_header_list, table_body_id, row_id_name) {
     var head_list = table_header_list;
     var body_list = table_data_list;
     var undefined_cnt = 0;
    //alert("add table start");
    for (var j = 0; j < body_list.length; j++){
        //alert("row = " + j);
        var new_table_row = document.createElement("tr");
        var row_id;
        if(body_list[j].hasOwnProperty(row_id_name) == true)
            row_id = body_list[j][row_id_name];
        else{///此列未定义行号，追加一个
            row_id = "urow_" + undefined_cnt.toString();
            undefined_cnt ++;
        }

        for(var i = 0; i< head_list.length ; i++){

            var new_table_data = document.createElement('td');
            //alert("i =" + i +", type = " +  table_header_list[i].type);
            //根据字段的类型插入各种东西
            if(table_header_list[i].type == 'text'){
             //数据类型的元素，插入对应的键值
                new_table_data.innerText = body_list[j][table_header_list[i].data];
                new_table_data.id = row_id + "_" + table_header_list[i].data;
            }
            else{//目前这里一定是指放按钮
                var new_table_span = document.createElement("span");
                new_table_span.className = "btn btn-default btn-xs glyphicon glyphicon-" + table_header_list[i].type;
                new_table_span.setAttribute("row_id",row_id);
                new_table_data.appendChild(new_table_span);
            }
            new_table_row.appendChild(new_table_data);
        }
        document.getElementById(table_body_id).appendChild(new_table_row);
    }

    if(body_list.length > 0)
        $("#" + pageName + "-page-nav").removeAttr("hidden");
    else
        $("#" + pageName + "-page-nav").attr("hidden","hidden");
    //alert("add table finish");
}

function deleteTableContent(table_body_id){
    var to_remove_array = $("#" + table_body_id + " tr");
    for( var i=0; i< to_remove_array.length; i++){
        document.getElementById(table_body_id).removeChild(to_remove_array[i]);
    }
}


////**********searchTable related
function addSearchBoard(jsonObj, pageName) {
    var search_form_id = pageName + "SearchBoard";
     var head_list = jsonObj.table_schema_list;
     var searchKeys = new Array();

    for(var i = 0; i< head_list.length ; i++){
        if(head_list[i].hasOwnProperty("searchType") == false)
            continue;
        searchKeys.push(head_list[i].data);
        var new_form_grop = document.createElement("div");
        new_form_grop.className = "form-group";

        var new_form_label = document.createElement("label");
        new_form_label.setAttribute("for","search_form_" + head_list[i].data);
        new_form_label.innerText = head_list[i].name;
        new_form_label.style.marginRight = "10px";
        new_form_label.style.marginTop = "10px";

        var new_form_input = document.createElement(head_list[i]["searchType"]);
        new_form_input.id = "search_form_" + head_list[i].data;
        new_form_input.className = "form-control";
        new_form_input.setAttribute("type","text");
        new_form_input.style.marginRight = "10px";

        new_form_grop.appendChild(new_form_label);
        new_form_grop.appendChild(new_form_input);

        //输入组插入页面
        document.getElementById(search_form_id).appendChild(new_form_grop);
    }

    //确认按键
    var new_form_btn = document.createElement("button");
    new_form_btn.className = "btn btn-primary";
    new_form_btn.innerText = "查询";
    new_form_btn.setAttribute("type","button");

    document.getElementById(search_form_id).appendChild(new_form_btn);
    return searchKeys;
}

function addSelectInput(form_id, option_list){
    var select_list = document.getElementById(form_id);

    //加一个空项
    var empty_select_option = document.createElement("option");
    empty_select_option.innerText = "";
    empty_select_option.setAttribute("value","");
    empty_select_option.setAttribute("opt_id",0);
    select_list.appendChild(empty_select_option);

    for(var i in option_list){
        var new_select_option = document.createElement("option");
        new_select_option.innerText = option_list[i].name;
        new_select_option.setAttribute("value", option_list[i].name);
        new_select_option.setAttribute("opt_id", option_list[i].id);
        //new_select_option.setAttribute("option_id",option_list[i].id);
        select_list.appendChild(new_select_option);
    }
}

function addSelectDict(form_id_prefix, select_dict, jsonObj){
    for(var key in select_dict){
        //alert(select_dict[key]);
        addSelectInput(form_id_prefix + "_" +select_dict[key],jsonObj["opt_list"][select_dict[key]]);
    }
}

////////////&&&&alert inform
function alertMsg(pageName, alertType, alertMsg){
    var new_alert_div = document.createElement("div");
    new_alert_div.className = "alert alert-" + alertType;
    document.getElementById(pageName + "Alert").appendChild(new_alert_div);

    var new_alert_a = document.createElement("a");
    new_alert_a.className = "close";
    new_alert_a.href = "#";
    new_alert_a.innerText = "×";
    new_alert_a.setAttribute("data-dismiss","alert");
    var new_alert_strong = document.createElement("strong");
    new_alert_strong.innerText = alertMsg;

    new_alert_div.appendChild(new_alert_strong);
    new_alert_div.appendChild(new_alert_a);
}
