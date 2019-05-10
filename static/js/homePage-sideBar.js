/**
 * Created by LENOVO on 2018/4/4.
 */
function addSection(section_id, section_name){
    var new_section_group = document.createElement('div');
    new_section_group.className = "panel panel-default";
    document.getElementById("section-list").appendChild(new_section_group);

    var new_section_div = document.createElement('div');
    new_section_div.className = "panel-heading";
    new_section_group.appendChild(new_section_div);

    var new_section_h4 = document.createElement('h4');
    new_section_h4.className = "panel-title";

    var new_section_a = document.createElement("a");
    new_section_a.className = "list-group-item";
    new_section_a.href = "#section" + section_id.toString();
    new_section_a.setAttribute("data-toggle","collapse");
    new_section_a.setAttribute("data-parent","section-list");
    new_section_a.innerText = section_name;

    new_section_h4.appendChild(new_section_a);
    new_section_div.appendChild(new_section_h4);

    var new_section_funclist = document.createElement('div');
    new_section_funclist.className = "panel-collapse collapse";
    new_section_funclist.id = "section" + section_id.toString();

    var new_section_funclist_exp = document.createElement('div');
    new_section_funclist_exp.className = "panel-body";

    var new_funclist = document.createElement('div');
    new_funclist.className = "list-group";
    new_funclist.id = "section" + section_id.toString() + "List";

    new_section_funclist_exp.appendChild(new_funclist);
    new_section_funclist.appendChild(new_section_funclist_exp);
    new_section_group.appendChild(new_section_funclist);

};

function addFuction (section_id, function_name, src){
    var new_function = document.createElement('a');
    new_function.href = "#";
    new_function.className = "list-group-item";
    new_function.setAttribute("src", src);
    new_function.innerText = function_name;
    document.getElementById("section" + section_id.toString() + "List").appendChild(new_function);
};

<!--首部标签页增加项目-->
function addFuctionTab (function_name, function_src){
    var new_tab_li = document.createElement('li');
    new_tab_li.setAttribute("role","presentation");
    new_tab_li.id = function_src + "_tab_li";

    var new_tab_a = document.createElement('a');
    new_tab_a.href = "#" + function_src;
    new_tab_a.setAttribute("role","tab");
    new_tab_a.setAttribute("aria-controls", function_src);
    new_tab_a.setAttribute("data-toggle","tab");
    new_tab_a.innerText = function_name;

    var new_tab_i = document.createElement("i");
    new_tab_i.className = "glyphicon glyphicon-remove-circle";
    new_tab_i.setAttribute("aria-hidden","true");
    new_tab_i.setAttribute("function_src",function_src);

    new_tab_a.appendChild(new_tab_i);
    new_tab_li.appendChild(new_tab_a);
    document.getElementById("function_tab_list").appendChild(new_tab_li);

    ///////////////////////////以上是顶部标签、、、、、、、、、、、、、、、、

    ////////以下是底部标签页

    var new_tab_div = document.createElement("div");
    new_tab_div.setAttribute("role","tabpanel");
    new_tab_div.className = "tab-pane fade";
    new_tab_div.id = function_src;

    var new_tab_iframe = document.createElement("iframe");
    new_tab_iframe.setAttribute("width","100%");
    new_tab_iframe.setAttribute("height","700");
    new_tab_iframe.setAttribute("frameborder","no");
    new_tab_iframe.setAttribute("scrolling","yes");
    new_tab_iframe.src =  function_src;

    new_tab_div.appendChild(new_tab_iframe);
    document.getElementById("tab-content").appendChild(new_tab_div);
};