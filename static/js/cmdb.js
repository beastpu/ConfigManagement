

// 创建CodeMirror实例以及全屏插件 - calabash
function code_editor() {

    var editor1 = CodeMirror.fromTextArea(document.getElementById("editor2_demo"), {
    lineNumbers: true,
    mode: "text/x-python",
    matchBrackets: true,
    viewportMargin: 20,
    
});

editor1.setSize(null, 450);
editor1.setOption("extraKeys", {
    // Tab键换成4个空格
    Tab: function(cm) {
        var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
        cm.replaceSelection(spaces);
    },
    // F11键切换全屏
    "F11": function(cm) {
        cm.setOption("fullScreen", !cm.getOption("fullScreen"));
    },
    // Esc键退出全屏
    "Esc": function(cm) {
        if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
    }
});
  
 return editor1;
}

function code_editor2(){

    var editor2 = CodeMirror.fromTextArea(document.getElementById("conf_content"), {
    lineNumbers: true,
    mode: "text/x-python",
    matchBrackets: true,

 });
    return editor2;

}





function editor_style(editor,language){
  
  var txt1=$("#editor2_demo").val();
  var txt2=$("#code2").val();
  if (language == "shell"){   
     editor.setOption("mode","text/x-sh");
         editor.setValue(txt1);
    }
  if (language == "python"){
        editor.setValue("mode","text/x-python");
        editor.setValue(txt2);
    }
}




function api_dialog(){
    var d = dialog({
            width: 400,
            title: 'API',
            content: '<input type="text" class="form-control" id="api_address" value=""/><a href="javascript:;" class="king-btn king-info" data-clipboard-action="copy" data-clipboard-target="#api_address">复制</a>',
            cancel: true,
    });
    d.show();

    var clipboard = new Clipboard('.king-btn');

    clipboard.on('success', function(e) {
        console.log(e);
        alert('复制成功！');
    });

    clipboard.on('error', function(e) {
        console.log(e);
         alert('复制失败！');

    });
}

function edit_dialog(){

    var d = dialog({
            width: 400,
            title: '属性编辑',
            content: '<form id="edit_form" action="editDir/" method="post"><input type="hidden" id="edit_id" name="edit_id"/><input type="hidden" id="edit_type" name="edit_type"/><input type="text" class="form-control" id="edit_content" name="edit_content"/><button type="submit" class="king-btn king-info" id="save" name="save">保存</button><button type="submit" class="king-btn king-danger" id="delete" name="delete">删除</button></form>',
            cancel: true,
    });
    d.show();

    
}


//event 
$(document).ready(function() {
    var editor1 = code_editor();
    var editor2=code_editor2();
    $('#plugin11_demo1').jstree({
    'core' : {
        'data' : {
            "url" : "getdir/",
            "dataType" : "json" 
         }
      }
    }).on("changed.jstree", function (e, data) {
        var test = $('#plugin11_demo1').jstree('get_selected');
        var isParent = $('#plugin11_demo1').jstree(true).is_parent(test);
        nodeName=data.instance.get_node(data.selected[0]).text
        nodeId=data.instance.get_node(data.selected[0]).id
        nodeType=nodeId.substring(0, nodeId.length - 1) 
        nodeId = nodeId.replace(/[^0-9]/ig,"")     
        console.log(nodeName,nodeId,nodeType)
        if(!isParent) {
           
            node_name=data.instance.get_node(data.selected[0]).text
            node_id=data.instance.get_node(data.selected[0]).id
            node_id = node_id.replace(/[^0-9]/ig,""); 
           
        $.ajax({
            url: "getConf/",
            type: "POST",
            data: {"node_id":node_id},
            dataType: 'json',
            success: function (data) {
                 
                 var codeText = data["content"]
                 config_id = data["config_id"]
                 editor1.setValue(codeText);         
                      
            }
        });         

        }
    }),
    $('#fullscreen').click(function() {
        console.log("fullscreen")
        editor1.setOption("fullScreen", true)
    }),
    $("#rollback").click(function(){

    self.location.href= "../rollback"
    }),
    $("#lang").change(function(){
        selected_lan=$("#lang option:selected").text();
        editor_style(editor1,selected_lan) 
    }),
    $("#theme").change(function(){
        var selected_theme=$("#theme option:selected").text(); 
        editor1.setOption("theme", selected_theme);
   
    }),
    $("#history").click(function(){
        toastr.options = {
             positionClass: "toast-top-center",
        
             };
        if(typeof(node_id)=="undefined"){ 
            toastr.remove();
            toastr.error('Node is Not Be Selected,Please Select Config File')
        return false; 
        }
        self.location.href= node_id+"/history/"
    }),
    $("#api").click(function(){
        toastr.options = {       
            positionClass: "toast-top-center",
        };
        if(typeof(node_id)=="undefined"){ 
         toastr.remove();
            toastr.error('Node is Not Be Selected, Please Select Config File')
            return false; 
         }
        api_dialog();
    }),
    $("#api").click(function(){
        $("#api_address").attr("value","http://paas.bk.91act.com/o/cmdb/configApi/"+config_id+"/")

    }),
    $("#create_conf").click(function(){
        var service = $("#service").val(); 
        var model = $("#module").val();
        var fileName = $("#fileName").val();
        var content = $("#content").val();

        if(service == "" ){ 
        alert("service name is null"); 
        return false; 
        }
        if(model == "" ){ 
        alert("model name is null"); 
        return false; 
        } 
        if(fileName == "" ){ 
        alert("fileName name is null"); 
        return false; 
        } 
        if(content == "" ){ 
        alert("content name is null"); 
        return false; 
        } 
     $.ajax({
            url: "createConf/",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"content":editor2.getValue(),"service":service,"module":model,"fileName":fileName}),
            success: function (data) {
                location.reload();

            }
        });         
    }),
    $("#cbutton").click(function(){
         var d = dialog({
            width: 400,
            title: 'Comment',
            content: '<input type="text" class="form-control" id="comment" value=""/>',
            okValue: '确定',
            okValue: '确定',
            ok: function() {
             var comment=$("#comment").val()
             $.ajax({
                url: "updateConf/",
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({"content":editor1.getValue(),"selected_node_id":node_id,"comment":comment}),
                success: function (data) {
                    alert("success");

                        }
                   });  
            },
        
    });
    d.show();
     
    }),
    $("#edit").click(function(){
        toastr.options = {       
            positionClass: "toast-top-center",
        };
        if(typeof(nodeId)=="undefined"){ 
         toastr.remove();
            toastr.error('Node is Not Be Selected, Please Select Config File')
            return false; 
         }
        edit_dialog();
    }),
    $("#edit").click(function(){
        $("#edit_content").attr("value",nodeName);
        $("#edit_id").attr("value",nodeId);
        $("#edit_type").attr("value",nodeType);
    }),
    $("#download").click(function(){
         toastr.options = {       
            positionClass: "toast-top-center",
        };
        if(typeof(node_id)=="undefined"){ 
         toastr.remove();
            toastr.error('Node is Not Be Selected, Please Select Config File')
            return false; 
         }
        self.location.href= site_url+"download/"+node_id+"/"
    // }),
    // $("#upload").click(function(){
         
    }),
    $("#upload").click(function(){
        var file=$("#files").get(0).files[0];
        var data = new FormData();                                      
        data.append("file",file);
        $.ajax({
            url:site_url+'upload/',
            type:'POST',
            data:data,
            cache: false,                                               //上传文件无需缓存
            processData:false,                                          //不对数据做序列化操作
            contentType:false,                                          //不定义特殊连接类型
            success:function (data) {
                editor1.setValue(data)
                
                }
            })
           
       
    });

    


});
