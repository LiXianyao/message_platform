/**
 * Created by LENOVO on 2018/4/4.
 */

function newModal(pageName, action){
    //以下是一个模态框的定义，基本都是输入
    var modal_name = pageName + action;
    var new_modal_div = document.createElement("div");
    new_modal_div.className = "modal fade";
    new_modal_div.id = modal_name  + "Modal";
    new_modal_div.setAttribute("tabindex","-1");
    new_modal_div.setAttribute("role","dialog");
    new_modal_div.setAttribute("aria-label", modal_name + "ModalLabel");
    document.getElementById(pageName + "Page").appendChild(new_modal_div);
    var new_modal_dialog = document.createElement("div");
    new_modal_dialog.className = "modal-dialog";
    new_modal_dialog.setAttribute("role","form");
    new_modal_div.appendChild(new_modal_dialog);

    var new_modal_content = document.createElement("div");
    new_modal_content.className = "modal-content";
    new_modal_dialog.appendChild(new_modal_content);

    var new_modal_header = setModalHeader(modal_name);
    new_modal_content.appendChild(new_modal_header);

    var new_modal_body = setModalBody(modal_name);
    new_modal_content.appendChild(new_modal_body);

    var new_modal_footer = setModalFooter(modal_name);
    new_modal_content.appendChild(new_modal_footer);
    //alert("new modal " + action + " finish");
}

function setModalHeader(modal_name){
    var new_modal_header = document.createElement("div");
    new_modal_header.className = "modal-header";

    var new_modal_closeBtn = document.createElement("button");
    new_modal_closeBtn.className = "close";
    new_modal_closeBtn.setAttribute("type","button");
    new_modal_closeBtn.setAttribute("data-dismiss","modal");
    new_modal_closeBtn.setAttribute("aria-label", "Close");

    var new_modal_closeBtn_span = document.createElement("span");
    new_modal_closeBtn_span.setAttribute("aria-hidden", "true");
    new_modal_closeBtn_span.innerText = "×";

    new_modal_closeBtn.appendChild(new_modal_closeBtn_span);
    new_modal_header.appendChild(new_modal_closeBtn);

    var new_modal_title= document.createElement("h4");
    new_modal_title.className = "modal-title";
    new_modal_title.id = modal_name  + "ModalLabel";

    new_modal_header.appendChild(new_modal_title);
    return new_modal_header;
}

function setModalBody(modal_name){
    var new_modal_body = document.createElement("div");
    new_modal_body.className = "modal-body";

    var new_modal_form= document.createElement("form");
    new_modal_form.className = "form-horizontal";
    new_modal_form.id = modal_name  + "ModalForm";

    new_modal_body.appendChild(new_modal_form);
    return new_modal_body;
}

function setModalFooter(modal_name){
    var new_modal_footer = document.createElement("div");
    new_modal_footer.className = "modal-footer";

    var new_modal_cancelBtn = document.createElement("button");
    new_modal_cancelBtn.className = "btn btn-default";
    new_modal_cancelBtn.setAttribute("type","button");
    new_modal_cancelBtn.setAttribute("data-dismiss","modal");
    new_modal_cancelBtn.innerText = "取消";

    var new_modal_confirmBtn = document.createElement("button");
    new_modal_confirmBtn.className = "btn btn-primary";
    new_modal_confirmBtn.setAttribute("type","button");
    new_modal_confirmBtn.id = modal_name + "ModalFormConfirm";
    new_modal_confirmBtn.innerText = "确定";

    new_modal_footer.appendChild(new_modal_cancelBtn);
    new_modal_footer.appendChild(new_modal_confirmBtn);

    return new_modal_footer;
}

function addBoardContent(table_header_list, json_segment_name, pagename, action) {
    var head_list = table_header_list;
    var Keys = new Array();

    for(var i = 0; i< head_list.length ; i++){

        if(head_list[i].hasOwnProperty(json_segment_name) == false)
            continue;

        var form_name = pagename + action;
        var modal_form_id = form_name + "ModalForm";

        Keys.push(head_list[i].data);
        var new_form_grop = document.createElement("div");
        new_form_grop.className = "form-group";

        var new_form_label = document.createElement("label");
        new_form_label.className = "control-label col-sm-4";
        new_form_label.setAttribute("for",form_name + "_" + head_list[i].data);
        new_form_label.innerText = head_list[i].name;

        var new_form_div = document.createElement("div");
        new_form_div.className = "col-sm-8";

        var new_form_input = document.createElement(head_list[i][json_segment_name]);
        new_form_input.id = form_name + "_" + head_list[i].data;
        new_form_input.className = "form-control";
        new_form_input.setAttribute("type","text");

        new_form_grop.appendChild(new_form_label);
        new_form_div.appendChild(new_form_input);
        new_form_grop.appendChild(new_form_div);
        //输入组插入页面
        document.getElementById(modal_form_id).appendChild(new_form_grop);
    }
    return Keys;
}


function showOriginalInform(to_edit_row_id, editKeys, form_name){
    for(var i=0; i< editKeys.length; i++){
        var  key = editKeys[i];
        var value = $("#" + to_edit_row_id + "_" + key).text();
        if($("input[id='" + form_name + "_" + key + "']").length > 0)
            $("input[id='" + form_name + "_" + key + "']").val(value);
        if($("select[id='" + form_name + "_" + key + "']").length > 0){
            $("select[id='" + form_name + "_" + key + "']").find("option[value='" + value +"']").attr("selected", true);
        }
        if($("label[id='" + form_name + "_" + key + "']").length > 0){
            $("label[id='" + form_name + "_" + key + "']").text(value);
            $("label[id='" + form_name + "_" + key + "']").val(value);
        }

    }
}

function clearModalInput(Keys, form_name){
    for(var i=0; i< Keys.length; i++){
        var  key = Keys[i];
        if($("input[id='" + form_name + "_" + key + "']").length > 0)
            $("input[id='" + form_name + "_" + key + "']").attr("value", "");
        if($("select[id='" + form_name + "_" + key + "']").length > 0){
            $("select[id='" + form_name + "_" + key + "']").find("option[opt_id='0']").attr("selected", true);
        }
        if($("label[id='" + form_name + "_" + key + "']").length > 0){
            $("label[id='" + form_name + "_" + key + "']").attr("value", "");
            $("label[id='" + form_name + "_" + key + "']").text("");
        }
    }
}

///修改模态框
function bindGlyphicon_edit(pageName, edit_array, modal_label_text){
    var action = "Edit";
    var form_name = pageName + action;
    var modal_id = form_name + "Modal";
    var modal_label_id = modal_id + "Label";
    $("span.glyphicon-edit").click(function(){
        $("#" + modal_label_id).text(modal_label_text);
        $("#" + modal_id).modal('show');
        var row_id = $(this).attr("row_id");
        showOriginalInform(row_id, edit_array, form_name);
    });
}

///添加模态框
function bindGlyohicon_plus(pageName, add_array, modal_label_text){
    var action = "Plus";
    var form_name = pageName + action;
    var modal_id = form_name + "Modal";
    var modal_label_id = modal_id + "Label";
    $("span.glyphicon-plus").click(function(){
        $("#" + modal_label_id).text(modal_label_text);
        $("#" + modal_id).modal('show');
        clearModalInput(add_array, form_name);
    });
}

///新建模态框
function bindGlyohicon_new(pageName, new_array, modal_label_text, action){
    var form_name = pageName + "New";
    var modal_id = form_name + "Modal";
    var modal_label_id = modal_id + "Label";
    $("span.glyphicon-" + action).click(function(){
        $("#" + modal_label_id).text(modal_label_text);
        $("#" + modal_id).modal('show');
        clearModalInput(new_array, form_name);
    });
}

///删除模态框
function bindGlyohicon_trash(pageName, trash_array, modal_label_text){
    var action = "Trash";
    var form_name = pageName + action;
    var modal_id = form_name + "Modal";
    var modal_label_id = modal_id + "Label";
    $("span.glyphicon-trash").click(function(){
        $("#" + modal_label_id).text(modal_label_text);
        $("#" + modal_id).modal('show');
        var row_id = $(this).attr("row_id");
        showOriginalInform(row_id, trash_array, form_name);
    });
}

//获取模态框中的输入，构造为post参数
function getModalInput(input_array, input_preffix){
    var request_data = "";
    for(var i in input_array){
        if(request_data.length > 0)
            request_data += "&&";
        request_data += input_array[i] + "=";
        var input_val = $("#" + input_preffix + "_" + input_array[i]).val();
        request_data += input_val;
    }
    return request_data;
}

///绑定模态框的确认按键的功能--发送表单并在收到结果后刷新界面
function bindModalConfirmButton(pageName, action, url, input_array){
    $("#" + pageName + action + "ModalFormConfirm").click(function(){
        var request_data = getModalInput(input_array, pageName + action);
        alert(request_data);
        //ajax发送请求
        $.ajax({
            url:"/" + pageName + "/" + url + "/",
            type:'POST',
            data: request_data,
            datatype :'json', //是预期服务器返回的数据格式=。=
            success: function(data){
                obj = jQuery.parseJSON(data); //字符串转为json格式
                $("#" + pageName + action + "Modal").modal('hide');
                window.location.reload();
            }
        })
    });
}