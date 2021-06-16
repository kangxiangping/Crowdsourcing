//首页删除项目
function deleteProject(id){
    var statu = confirm("确认删除吗?");
    if(!statu)//如果点击的是取消
    {
        return false;//返回页面
    }
    else{//如果点击确定，就继续执行下面的操作
    	$.ajax({
    		type:"POST",
    		url:"/deleteProject",
    		contentType:"application/json",
    		data:JSON.stringify({
    			"id":id,
    		}),
    		success:function(response){
    			if(response.code == 200){
    				console.log("删除成功");
    				location.reload();
    			}else{
    				console.log("删除失败");
    			}
    		},
    		dataType:"json"
    	});
     }
}


//创建project的第一步
function createProjectStep1(){
	var name = $("#name").val();
	var description = $("#description").val();
	var point = $("#point").val();
	var budget =$("#budget").val();
	var time = $("#deadline").val();
	var userPonit = $("#userPoint").val();
	
	if(name==null || name==""){
		alert("项目名称不能为空！");
		return;
	}
	if(description==null || description==""){
		alert("项目描述不能为空！");
		return;
	}
	if(point==null || point==""){
		alert("任务积分不能为空！");
		return;
	}
	if(budget==null || budget==""){
		alert("项目预算不能为空！");
		return;
	}
	if(parseInt(budget) < parseInt(point)){
		alert("任务积分不能小于项目预算！");
		return;
	}
	if(time==null || time==""){
		alert("任务截止日期不能为空！");
		return;
	}
	if(parseInt(userPonit) < parseInt(budget)){
		alert("抱歉，您的积分低于项目预算，不能发布项目！");
		return;
	}
	var deadline = (new Date($("#deadline").val())).valueOf();
	console.log(deadline);
	window.localStorage.setItem('name', name);
	window.localStorage.setItem('description', description);
	window.localStorage.setItem('point', point);
	window.localStorage.setItem('budget', budget);
	window.localStorage.setItem('deadline', deadline);
	location.href = 'step2'
	console.log("创建项目的第一步完成！");
}

function createProjectStep2(){
	var datasetId = $('input:radio:checked').val();
	
	if(datasetId==null || datasetId==""){
		alert("请选择数据集！");
		return;
	}
	window.localStorage.setItem('datasetId', datasetId);
	location.href = 'step3'
	console.log("创建项目的第二步完成！");
	console.log(datasetId);
}

function finishCreateProject(){
	console.log("进入finishCreateProject");
	var question = $("#question").val();
	var tag = $("#tag").val();
	var projectType = $("#projectType").val();
	
	if(question==null || question==""){
		alert("图片属性不能为空！");
		return;
	}
	if(tag==null || tag==""){
		alert("标签不能为空！");
		return;
	}
	console.log(localStorage.getItem("datasetId"));
	
	$.ajax({
		type:"POST",
		url:"/step3",
		contentType:"application/json",
		data:JSON.stringify({
			"name":localStorage.getItem("name"),
			"description":localStorage.getItem("description"),
			"point":localStorage.getItem("point"),
			"datasetId":localStorage.getItem("datasetId"),
			"budget":localStorage.getItem("budget"),
			"deadline":localStorage.getItem("deadline"),
			"question":question,
			"tag":tag,
			"type":projectType,
		}),
		success:function(response){
			if(response.code == 200){
				localStorage.removeItem("name");
				localStorage.removeItem("description");
				localStorage.removeItem("point");
				localStorage.removeItem("datasetId");
				localStorage.removeItem("budget");
				localStorage.removeItem("deadline");
				alert("添加成功！");
				console.log("成功！");
				window.location.href = "/";
			}else{
				console.log("失败！");
				alert(response.message);
			}
		},
		dataType:"json"
	});	
}

//删除成员
function deleteUser(id){
    var statu = confirm("确认删除吗?");
    if(!statu)//如果点击的是取消
    {
        return false;//返回页面
    }
    else{//如果点击确定，就继续执行下面的操作
    	$.ajax({
    		type:"POST",
    		url:"/deleteUser",
    		contentType:"application/json",
    		data:JSON.stringify({
    			"id":id,
    		}),
    		success:function(response){
    			if(response.code == 200){
    				console.log("删除成功");
    				location.reload();
    			}else{
    				console.log("删除失败");
    			}
    		},
    		dataType:"json"
    	});
     }
}


function register(){
	var username = $("#username").val();
	var password = $("#password").val();
	var nickname = $("#nickname").val();
	//var reg = new RegExp("/^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,}$/");
	        
	if(username==null || username==""){
		alert("用户名不能为空！");
		return;
	}
	if(password==null || password==""){
		alert("密码不能为空！");
		return;
	}
	if(nickname==null || nickname==""){
		alert("昵称不能为空！");
		return;
	}
//	if(!reg.test(username)){
//        alert("密码长度要大于6位，由数字和字母组成！");
//　　   	return;
//　	}
	$.ajax({
		type:"POST",
		url:"/register",
		contentType:"application/json",
		data:JSON.stringify({
			"username":username,
			"password":password,
			"nickname":nickname,
		}),
		success:function(response){
			if(response.code == 200){
				alert("注册成功！");
				window.location.href = "/login";
			}else if(response.code == 201){
				alert(response.message);
			}else{
				alert("注册失败！");
			}
		},
		dataType:"json"
	});

	
}

function toWork(projectId, haveTest){
	if(haveTest==0){
		alert("请先完成新手测试！");
		return;
	}
	$.ajax({
		type:"POST",
		url:"/toWork",
		async:false,
		contentType:"application/json",
		data:JSON.stringify({
			"id":projectId
		}),
		success:function(response){
			if(response.code==200){
				//var startTime = (new Date()).valueOf();
				var ans =  new Array(response.data);
				//window.localStorage.setItem('startTime', startTime);
				window.localStorage.setItem('taskCount', response.data);
				window.localStorage.setItem('answers', JSON.stringify(ans));
				window.location.href = "/working/"+projectId+"/0";
			}
		},
		dataType:"json"
	});	
}


function working(projectId, index, taskId){
	var obj=document.getElementsByName('tag'); //选择所有name="'test'"的对象，返回数组 
	var checked =  [];
    for(var i=0; i<obj.length; i++){ 
        if(obj[i].checked) 
        	checked.push(obj[i].value); //如果选中，将value添加到变量s中 
    } 
    if(checked.length==0){
    	alert("请选择标签！");
    	return;
    }else{
    	ans = JSON.parse(localStorage.getItem('answers'));
    	ans[index-1]={
    		"projectId":projectId,
    		"taskid":taskId,
    		"ans":checked,
    	};
    	window.localStorage.setItem('answers', JSON.stringify(ans));
    }
    
    //最后一道题
    var taskCount = localStorage.getItem("taskCount");
	if(index==taskCount){
		console.log(JSON.parse(localStorage.getItem('answers')));
		$.ajax({
			type:"POST",
			url:"/finishedWork",
			async:true,
			contentType: 'application/json;charset=UTF-8',
			data:JSON.stringify(JSON.parse(localStorage.getItem('answers'))),
			success:function(response){
				if(response.code==200){
					alert("提交成功，您获得了"+response.data+"积分！");
					window.location.href = "/";
				}
			},
			dataType:"json"
		});	
	}else{
		window.location.href = "/working/"+projectId+"/"+index;
	}
	
}

function quit(){
	var statu = confirm("返回首页本次标注将作废，您无法获得积分！\n确认要退出吗？")
    if(!statu){  //如果点击的是取消
        return false;  //返回页面
    }
    else{//如果点击确定，就继续执行下面的操作
    	localStorage.removeItem("answers");
    	localStorage.removeItem("taskCount");
    	window.location.href = "/";
     }
}

function dataDetail(datasetId){
	window.location.href = "/dataset/"+datasetId;
}

function newDataset(){
    //第一个参数是提示文字，第二个参数是文本框中默认的内容
    var dataset = prompt("数据集名称：","");
    if(dataset){
    	$.ajax({
    		type:"POST",
    		url:"/createDataset",
    		contentType:"application/json",
    		data:JSON.stringify({
    			"name":dataset
    		}),
    		success:function(response){
    			if(response.code==200){
    				location.reload();
    			}
    		},
    		dataType:"json"
    	});	
     }
}

//删除图片
function deletePicture(id,datasetId){
    var statu = confirm("确认删除吗?");
    if(!statu)//如果点击的是取消
    {
        return false;//返回页面
    }
    else{//如果点击确定，就继续执行下面的操作
     $.ajax({
      type:"POST",
      url:"/deletePicture",
      contentType:"application/json",
      data:JSON.stringify({
       "id":id,
       "datasetId":datasetId,
      }),
      success:function(response){
       if(response.code == 200){
        console.log("删除成功");
        location.reload();
       }else{
        console.log("删除失败");
       }
      },
      dataType:"json"
     });
     }
}





