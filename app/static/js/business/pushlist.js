var listUrl = "/statistic";

var Totallist = {
	begin: "",
	end: "",
	type: "total"
}
var IOSlist = {
	begin: "",
	end: "",
	type: "iOS"
}
var umenglist = {
	begin: "",
	end: "",
	type: "umeng"
}
var XMlist = {
	begin: "",
	end: "",
	type: "xiaomi"
}

var getuilist = {
	begin: "",
	end: "",
	type: "getui"
}

IOS();
XM();
getui();
Total();
umeng();


function Total() {
	$('#totalbody').empty();
	var tr = $('<tr></tr>');
	$('#totalbody').append(tr);
	td = $('<td colspan="4" class="text-center"></td>');
	td.html("please wait!");
	td.appendTo(tr);

	$('#totalSearch').attr('disabled', 'disabled');
	$.ajax({
		type: 'get',
		url: listUrl,
		data: {
			source: Totallist.type,
			begin: Totallist.begin,
			end: Totallist.end
		},
		dataType: "json",
		success: function(data) {
			console.log(data);

$('#totalbody').empty();
			for (var t = 0; t < data.msg.length; t++) {
				var otr = $('<tr></tr>');
				$('#totalbody').append(otr);

				ot1 = $('<td></td>');
				ot1.html(data.msg[t].date);
				ot1.appendTo(otr);

				ot2 = $('<td></td>');
				ot2.html(data.msg[t].total_count);
				ot2.appendTo(otr);

				ot3 = $('<td></td>');
				ot3.html(data.msg[t].receive_count);
				ot3.appendTo(otr);

				ot4 = $('<td></td>');
				ot4.html(data.msg[t].click_count);
				ot4.appendTo(otr);
			}


			$("#totaltable").bootgrid({
				css: {
					icon: 'zmdi icon',
					iconColumns: 'zmdi-view-module',
					iconDown: 'zmdi-expand-more',
					iconRefresh: 'zmdi-refresh',
					iconUp: 'zmdi-expand-less'
				},
				templates: {
					header: "",
					footer: ""
				}
			});

			$('#totalSearch').removeAttr('disabled');
		},
		error: function(data) {
			console.log('get error');
			$('#totalSearch').removeAttr('disabled');
		}
	});

}

function IOS() {
	$('#IOSbody').empty();
	var tr = $('<tr></tr>');
	$('#IOSbody').append(tr);
	ot = $('<td colspan="4" class="text-center"></td>');
	ot.html("please wait!");
	ot.appendTo(tr);
	$('#IOSSearch').attr('disabled', 'disabled');

	$.ajax({
		type: 'get',
		url: listUrl,
		data: {
			source: IOSlist.type,
			begin: IOSlist.begin,
			end: IOSlist.end
		},
		dataType: "json",
		success: function(data) {
			console.log(data);

$('#IOSbody').empty();
			for (var t = 0; t < data.msg.length; t++) {
				var otr = $('<tr></tr>');
				$('#IOSbody').append(otr);

				ot1 = $('<td></td>');
				ot1.html(data.msg[t].date);
				ot1.appendTo(otr);

				ot2 = $('<td></td>');
				ot2.html(data.msg[t].total_count);
				ot2.appendTo(otr);

				ot3 = $('<td></td>');
				ot3.html(data.msg[t].receive_count);
				ot3.appendTo(otr);

				ot4 = $('<td></td>');
				ot4.html(data.msg[t].click_count);
				ot4.appendTo(otr);
			}


			$("#IOStable").bootgrid({
				css: {
					icon: 'zmdi icon',
					iconColumns: 'zmdi-view-module',
					iconDown: 'zmdi-expand-more',
					iconRefresh: 'zmdi-refresh',
					iconUp: 'zmdi-expand-less'
				},
				templates: {
					header: "",
					footer: ""
				}
			});

			$('#IOSSearch').removeAttr('disabled');
		},
		error: function(data) {
			console.log('get error');
			$('#IOSSearch').removeAttr('disabled');
		}
	});

}

function umeng() {
	$('#umengbody').empty();
	var tr = $('<tr></tr>');
	$('#umengbody').append(tr);
	ot = $('<td colspan="4" class="text-center"></td>');
	ot.html("please wait!");
	ot.appendTo(tr);
	$('#umengSearch').attr('disabled', 'disabled');

	$.ajax({
		type: 'get',
		url: listUrl,
		data: {
			source: umenglist.type,
			begin: umenglist.begin,
			end: umenglist.end
		},
		dataType: "json",
		success: function(data) {
			console.log(data);
$('#umengbody').empty();

			for (var t = 0; t < data.msg.length; t++) {
				var otr = $('<tr></tr>');
				$('#umengbody').append(otr);

				ot1 = $('<td></td>');
				ot1.html(data.msg[t].date);
				ot1.appendTo(otr);

				ot2 = $('<td></td>');
				ot2.html(data.msg[t].total_count);
				ot2.appendTo(otr);

				ot3 = $('<td></td>');
				ot3.html(data.msg[t].receive_count);
				ot3.appendTo(otr);

				ot4 = $('<td></td>');
				ot4.html(data.msg[t].click_count);
				ot4.appendTo(otr);
			}


			$("#umengtable").bootgrid({
				css: {
					icon: 'zmdi icon',
					iconColumns: 'zmdi-view-module',
					iconDown: 'zmdi-expand-more',
					iconRefresh: 'zmdi-refresh',
					iconUp: 'zmdi-expand-less'
				},
				templates: {
					header: "",
					footer: ""
				}
			});
			$('#umengSearch').removeAttr('disabled');
		},
		error: function(data) {
			console.log('get error');
			$('#umengSearch').removeAttr('disabled');
		}
	});


}

function XM() {
	$('#XMbody').empty();
	var tr = $('<tr></tr>');
	$('#XMbody').append(tr);
	ot = $('<td colspan="4" class="text-center"></td>');
	ot.html("please wait!");
	ot.appendTo(tr);
	$('#XMSearch').attr('disabled', 'disabled');

	$.ajax({
		type: 'get',
		url: listUrl,
		data: {
			source: XMlist.type,
			begin: XMlist.begin,
			end: XMlist.end
		},
		dataType: "json",
		success: function(data) {
			console.log(data);
$('#XMbody').empty();

			for (var t = 0; t < data.msg.length; t++) {
				var otr = $('<tr></tr>');
				$('#XMbody').append(otr);

				ot1 = $('<td></td>');
				ot1.html(data.msg[t].date);
				ot1.appendTo(otr);

				ot2 = $('<td></td>');
				ot2.html(data.msg[t].total_count);
				ot2.appendTo(otr);

				ot3 = $('<td></td>');
				ot3.html(data.msg[t].receive_count);
				ot3.appendTo(otr);

				ot4 = $('<td></td>');
				ot4.html(data.msg[t].click_count);
				ot4.appendTo(otr);
			}


			$("#XMtable").bootgrid({
				css: {
					icon: 'zmdi icon',
					iconColumns: 'zmdi-view-module',
					iconDown: 'zmdi-expand-more',
					iconRefresh: 'zmdi-refresh',
					iconUp: 'zmdi-expand-less'
				},
				templates: {
					header: "",
					footer: ""
				}
			});
			$('#XMSearch').removeAttr('disabled');

		},
		error: function(data) {
			console.log('get error');
			$('#XMSearch').removeAttr('disabled');
		}
	});

}

function getui() {
	$('#getuibody').empty();
	var tr = $('<tr></tr>');
	$('#getuibody').append(tr);
	ot = $('<td colspan="4" class="text-center"></td>');
	ot.html("please wait!");
	ot.appendTo(tr);
	$('#getuiSearch').attr('disabled', 'disabled');

	$.ajax({
		type: 'get',
		url: listUrl,
		data: {
			source: getuilist.type,
			begin: getuilist.begin,
			end: getuilist.end
		},
		dataType: "json",
		success: function(data) {
			console.log(data);

	$('#getuibody').empty();
			for (var t = 0; t < data.msg.length; t++) {
				var otr = $('<tr></tr>');
				$('#getuibody').append(otr);

				ot1 = $('<td></td>');
				ot1.html(data.msg[t].date);
				ot1.appendTo(otr);

				ot2 = $('<td></td>');
				ot2.html(data.msg[t].total_count);
				ot2.appendTo(otr);

				ot3 = $('<td></td>');
				ot3.html(data.msg[t].receive_count);
				ot3.appendTo(otr);

				ot4 = $('<td></td>');
				ot4.html(data.msg[t].click_count);
				ot4.appendTo(otr);
			}


			$("#getuitable").bootgrid({
				css: {
					icon: 'zmdi icon',
					iconColumns: 'zmdi-view-module',
					iconDown: 'zmdi-expand-more',
					iconRefresh: 'zmdi-refresh',
					iconUp: 'zmdi-expand-less'
				},
				templates: {
					header: "",
					footer: ""
				}
			});
			$('#getuiSearch').removeAttr('disabled');
		},
		error: function(data) {
			console.log('get error');
			$('#getuiSearch').removeAttr('disabled');
		}
	});

}
$("body").on("click", "#totalSearch", function() {
	Totallist.begin = $('#totalbegin').val();
	Totallist.end = $('#totalend').val();
	Total();
});
$("body").on("click", "#IOSSearch", function() {
	IOSlist.begin = $('#IOSbegin').val();
	IOSlist.end = $('#IOSend').val();
	IOS();
});
$("body").on("click", "#umengSearch", function() {
	umenglist.begin = $('#umengbegin').val();
	umenglist.end = $('#umengend').val();
	umeng();
});
$("body").on("click", "#XMSearch", function() {
	XMlist.begin = $('#XMbegin').val();
	XMlist.end = $('#XMend').val();
	XM();
});
$("body").on("click", "#getuiSearch", function() {
	getuilist.begin = $('#getuibegin').val();
	getuilist.end = $('#getuiend').val();
	getui();
});