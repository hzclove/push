var provinceUrl = "/provinces";
var majorUrl = "/majors";
var versionUrl = "/versions";
var pushUrl = "/push";

var AndroidStr = "";
var IOSStr = "";

var AllAndroid = "";
var AllIOS = "";

var isNow = false; //即时发送
var isTimer = false; //定时发送
var isAllUser = false; //全部用户

var push = {
	province: '',
	major: '',
	is_register: 1,
	iOS_version: '',
	Android_version: '',
	article_type: '',
	class_type: "",
	title: '',
	description: '',
	article_id: '00000',
	begin: '',
	end: '',
	target: '',
}

ProvinceAdd();
getVersion();

//ajax 相关
function ProvinceAdd() {
	$.ajax({
		type: 'get',
		url: provinceUrl,
		dataType: "json",
		success: function(data) {
			//			console.log(data);
			for (var i = 0; i < data.msg.length; i++) {
				var opt = $('<option></option>');
				opt.html(data.msg[i]);
				opt.attr('value', data.msg[i]);
				$('#ProvinceSelect').append(opt);
			}
			//这个加上文章的推送链接过来之后会有的
			//			if (Article.provinceId != undefined) {
			//				$("#ProvinceSelect").val(Article.provinceId);
			//				MajorAdd(Article.provinceId);
			//			}

			if (data.msg.length > 0) {
				push.province = data.msg[0];
			}
			//			var opt = $('<option></option>');
			//			opt.html("全部");
			//			opt.attr('value', "全部");
			//			$('#MajorSelect').append(opt);
			MajorAdd("全部");
			$("#ProvinceSelect").trigger("chosen:updated");

			$("#MajorSelect").trigger("chosen:updated");
		},
		error: function(data) {
			//			console.log("province error");
		}
	});
}

function MajorAdd(provincename) {
	$('#MajorSelect').empty();
	var pstr = provincename;
	//	if (pstr == "全部") {
	//		var opt = $('<option></option>');
	//		opt.html("全部");
	//		opt.attr('Value', "全部");
	//		$('#MajorSelect').append(opt);
	//		$("#MajorSelect").trigger("chosen:updated");
	//		return;
	//	}
	$.ajax({
		type: 'get',
		url: majorUrl,
		data: {
			province_name: pstr
		},
		dataType: "json",
		success: function(data) {
			console.log(data);
			for (var i = 0; i < data.msg.length; i++) {
				var opt = $('<option></option>');
				opt.html(data.msg[i]);
				opt.attr('Value', data.msg[i]);
				$('#MajorSelect').append(opt);
			}
			if (data.msg.length > 0) {
				push.major = data.msg[0];
			}

			$("#MajorSelect").trigger("chosen:updated");
		},
		error: function(data) {
			//			console.log("province error");
		}
	});
}

function getVersion() {
	$.ajax({
		type: 'get',
		url: versionUrl,
		dataType: "json",
		success: function(data) {
			console.log(data);
			for (var a = 0; a < data.msg.android.length; a++) {
				console.log(data.msg.android[a]);
				var opt = $('<option></option>');
				opt.html(data.msg.android[a]);
				opt.attr('Value', data.msg.android[a]);
				$('#andriodVersion').append(opt);

				if (data.msg.android[a] != "全部") {
					if (AllAndroid == "") {
						AllAndroid = " " + "," + data.msg.android[a];
					} else {
						AllAndroid = AllAndroid + "," + data.msg.android[a]
					}
				}
			}

			for (var i = 0; i < data.msg.iOS.length; i++) {
				console.log(data.msg.iOS[i]);
				var opt = $('<option></option>');
				opt.html(data.msg.iOS[i]);
				opt.attr('Value', data.msg.iOS[i]);
				$('#IOSVersion').append(opt);
				if (data.msg.iOS[i] != "全部") {
					if (AllIOS == "") {
						AllIOS = " " + "," + data.msg.iOS[i];
					} else {
						AllIOS = AllIOS + "," + data.msg.iOS[i];
					}
				}
			}


			$("#andriodVersion").trigger("chosen:updated");
			$("#IOSVersion").trigger("chosen:updated");

			if (data.msg.android.length > 0) {
				push.Android_version = data.msg.android[0];

			}

			if (data.msg.iOS.length > 0) {
				push.iOS_version = data.msg.iOS[0];
			}
		},
		error: function(data) {
			console.log('version error');
		}
	});
}
//操作相关
$("body").on("change", "#ProvinceSelect", function() {
	MajorAdd($(this).val());
	push.province = $(this).val();
});

$("body").on("change", "#MajorSelect", function() {
	push.major = $(this).val();
});

$("body").on("change", "#regist", function() {
	if ($(this).val() == "注册") {
		push.is_register = 1;
	} else if ($(this).val() == "未注册") {
		push.is_register = 0;
	} else {
		push.is_register = 2;
	}
});

//$("body").on("change", "#andriodVersion", function() {
//	AndroidStr = AndroidStr + "," + $(this).val();
//});
//
//$("body").on("change", "#IOSVersion", function() {
//	IOSStr = IOSStr + "," + $(this).val();
//});

$("body").on("change", "#articleType", function() {
	$('#classType').parents('.form-group').hide();
	push.class_type = "";
	if ($(this).val() == 2) {
		$('#classType').parents('.form-group').show();
		push.class_type = '直买';
	}
	push.article_type = $(this).val();

});

$("body").on("change", "#classType", function() {
	push.class_type = $(this).val();
	console.log($(this).val());
});

$("body").on("click", "#now", function() {
	isTimer = false;
	$('#timer').removeAttr('checked');

	if (isNow) {
		isNow = false;
		$('#now').removeAttr('checked');
	} else {
		$('#now').attr('checked', 'checked');
		isNow = true;
	}

	$('.showtime').hide();
});

$("body").on("click", "#timer", function() {
	isNow = false;
	$('#now').removeAttr('checked');

	if (isTimer) {
		isTimer = false;
		$('#timer').removeAttr('checked');
		$('.showtime').hide();
	} else {
		$('#timer').attr('checked', 'checked');
		isTimer = true;
		$('.showtime').show();
	}


});

$("body").on("click", "#allUser", function() {
	if (isAllUser) {
		$('#allUser').removeAttr('checked');
		isAllUser = false;
		push.target = "";
	} else {
		$('#allUser').attr('checked', 'checked');
		isAllUser = true;
		push.target = "all";

	}


});

$("body").on("click", ".submitbtn", function() {
	savePush();
	$('.submitbtn').attr('disabled', 'disabled');
	console.log(push);

	$.ajax({
		type: 'post',
		url: pushUrl,
		data: {
			province_name: push.province,
			major_name: push.major,
			is_register: push.is_register,
			iOS_version: push.iOS_version,
			Android_version: push.Android_version,
			article_type: push.article_type,
			course_type: push.class_type,
			title: push.title,
			description: push.description,
			article_id: push.article_id,
			begin: push.begin,
			end: push.end,
			target: push.target
		},
		dataType: "json",
		success: function(data) {
			console.log(data);
			$('.submitbtn').removeAttr('disabled');
			AndroidStr = "";
			IOSStr = "";

		},
		error: function(data) {
			console.log('post error');
		}
	});
});

function savePush() {
	push.article_id=$('#artId').val();
	push.title = $('#title').val();
	push.description = $('#descrip').val();
	//android
	var AndroidStrs = $('#andriodVersion_chosen .search-choice span');
	for (var j = 0; j < AndroidStrs.length; j++) {
		if (AndroidStr == "") {
			AndroidStr = AndroidStr + $(AndroidStrs[j]).html();
		} else {
			AndroidStr = AndroidStr + "," + $(AndroidStrs[j]).html()
		}
	}
	if (AndroidStr.indexOf('全部') >= 0) {

		AndroidStr = AllAndroid;

	}
	if (AndroidStr == "") {
		AndroidStr = "NO";
	}
	push.Android_version = AndroidStr;

	//ios
	var IOSStrs = $('#IOSVersion_chosen .search-choice span');
	for (var i = 0; i < IOSStrs.length; i++) {
		if (IOSStr == "") {
			IOSStr = IOSStr + $(IOSStrs[i]).html();
		} else {
			IOSStr = IOSStr + "," + $(IOSStrs[i]).html()
		}
	}
	if (IOSStr.indexOf('全部') >= 0) {
		IOSStr = AllIOS;
	}
	if (IOSStr == "") {
		IOSStr = "NO";
	}
	push.iOS_version = IOSStr;

	if (push.article_type == "") {
		push.article_type = "资讯";
	}

	if (isTimer) {
		push.begin = $('#datetimepicker1').val();
		push.end = $('#datetimepicker2').val();
	}else{
		push.begin="";
		push.end="";
	}
}