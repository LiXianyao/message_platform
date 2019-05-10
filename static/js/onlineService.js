/**
 * Created by LENOVO on 2018/4/4.
 */
//增加输入条目
function addInputRow(form_id, label_text, input_id_array) {
    if(input_id_array.length == 0) //id 池已空
        return false;
    var input_id = input_id_array.pop();
    var new_form_grop = document.createElement("li");
    new_form_grop.className = "list-group-item container";
    new_form_grop.id = input_id + "_group";

    var new_form_content_row = document.createElement("div");
    new_form_content_row.className = "row form-group ";
    //文字部分
    var new_form_label = document.createElement("label");
    new_form_label.className = "control-label col-sm-2";
    new_form_label.setAttribute("for", input_id + "_content");
    new_form_label.innerText = label_text;
    //输入框
    var new_form_div = document.createElement("div");
    new_form_div.className = "col-sm-9";

    var new_form_input = document.createElement("input");
    new_form_input.className = "form-control";
    new_form_input.id = input_id + "_content";
    new_form_input.setAttribute("type","text");
    new_form_input.setAttribute("placeholder",label_text);
    //删除按键
    var new_form_span = document.createElement("span");
    new_form_span.className = "btn btn-default btn-xs glyphicon glyphicon-trash";
    new_form_span.setAttribute("row_id", input_id);

    new_form_content_row.appendChild(new_form_label);
    new_form_div.appendChild(new_form_input);
    new_form_content_row.appendChild(new_form_div);
    new_form_content_row.appendChild(new_form_span);

    //标签展示行
    var new_form_label_row = document.createElement("div");
    new_form_label_row.className = "row control-label";
    new_form_label_row.id = input_id + "_labels";

    //输入组插入页面
    new_form_grop.appendChild(new_form_content_row);
    new_form_grop.appendChild(new_form_label_row);
    document.getElementById(form_id).appendChild(new_form_grop);

    addLabel(input_id + "_labels", "行业标签1", input_id, "industry1", "success");
    addLabel(input_id + "_labels", "行业标签2", input_id, "industry2", "success");
    addLabel(input_id + "_labels", "行业标签3", input_id, "industry3", "success");
    addLabel(input_id + "_labels", "风险标签", input_id, "offlineRisk", "warning");
    addLabel(input_id + "_labels", "行业标签1概率", input_id, "industry1Prob", "success");
    addLabel(input_id + "_labels", "行业标签2概率", input_id, "industry2Prob", "success");
    addLabel(input_id + "_labels", "行业标签3概率", input_id, "industry3Prob", "success");
    addLabel(input_id + "_labels", "风险标签概率", input_id, "offlineRiskProb", "warning");

    addLabel(input_id + "_labels", "模板编号", input_id, "tcode", "info");
    addLabel(input_id + "_labels", "模板内容", input_id, "template", "info");

    return true;
}

///删除输入条目
function bindGlyohicon_trash_onlineService(id_array, form_id){
    $("span.glyphicon-trash").click(function(){
        var row_id = $(this).attr("row_id");
        //alert(row_id + "_group");
        var to_remove = document.getElementById(row_id + "_group");
        document.getElementById(form_id).removeChild(to_remove);
        id_array.push(row_id);
    });
}

//增加输入条目按键的触发函数，调用addInputRow尝试增加条目，失败则给出一个alert
function plusRow(pageName, id_Array, form_id){
    var addRes = addInputRow("onlineServiceInputForm", "短信文本", id_Array);
    if(addRes == false){
        alertMsg(pageName,"warning","短信文本添加条数已达上限");
    }
    else{
        //添加行成功，给删除键绑定功能
        bindGlyohicon_trash_onlineService(id_Array, form_id);
    }
}

//在指定id的输入条目下增加一个标签结果
function addLabel(label_row_id, label_text, input_id, data, label_type){
    var new_label_div = document.createElement("div");
    new_label_div.className =  "col-sm-3 ";

    var new_label = document.createElement("span");
    new_label.className = "pull-left label label-" + label_type;
    new_label.setAttribute("prefix", label_text);
    new_label.innerText = label_text;
    new_label.style.margin = "10px";
    new_label.style.lineHeight = "2";
    new_label.style.fontSize = "90%";
    new_label.id = input_id + "_" + data;

    new_label_div.appendChild(new_label);
    document.getElementById(label_row_id).appendChild(new_label_div);
}


//获取模态框中的输入，构造为post参数
function getRowsInput(input_array, id_max){
    var request_data = {};
    var msglist = new Array();
    for(var i=0; i<id_max; i++){
        var input_id = pageName + "Input_" + i.toString();
        if($.inArray(input_id, input_array) === -1){
            //alert(input_id);
            var id = input_id;
            var content = $("#" + input_id + "_content").val();
            var new_msg = {};
            new_msg.id = id;
            new_msg.content = content;
            msglist.push(new_msg);
        }
    }
    request_data.text = {"msg_list":msglist}
    return request_data;
}

//将json对象中的内容填入指定位置
function showAnalysisRes(result_obj, display_list){
    var input_id = result_obj.id;
    for(var i=0;i < display_list.length; i++){
        var display_seg = display_list[i];
        var target_id = input_id + "_" + display_seg;
        var target_dom = $("#" + target_id);
        var target_prefix = target_dom.attr("prefix");
        //alert(target_id);
        target_dom.text(target_prefix + ": " + result_obj[display_seg].toString());
    }
}

///绑定页面上的分类按键的功能--发送表单并在收到结果后更新界面内容
function bindOnlineServiceButton(pageName, action, id_max,input_array){
    $("#" + pageName + action).click(function(){
        var request_data = getRowsInput(input_array, id_max);
        request_data.target = action;
        //alert(JSON.stringify(request_data));
        //ajax发送请求
        $.ajax({
            url:"/" + pageName + "/" + action + "/",
            type:'POST',
            processData:false,
            contentType:"application/json;charset=utf-8",
            data: JSON.stringify(request_data),
            datatype :'json', //是预期服务器返回的数据格式=。=
            success: function(data){
                var obj = jQuery.parseJSON(data); //字符串转为json格式
                if(obj.hasOwnProperty('alertType'))
                    alertMsg(pageName,obj.alertType,obj.alertMsg);
                if(obj.succeed == true) {
                    alert("success!");
                    var result_list = obj.msg_list;
                    var display_list = obj.displayList;
                    for(var i=0;i < result_list.length; i++){
                        showAnalysisRes(result_list[i], display_list);
                    }
                }
            }
        })
    });
}