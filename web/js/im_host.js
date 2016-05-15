$(function()
{

	function iconHostFormatResult(icon)
	{
		var markup = "<table class='icon-result'><tr>";
		if (icon.text !== undefined && icon.icon !== undefined)
		{
			markup += "<td class='icon-image'><img src='http://"+ urlMaster +'/'+ icon.icon + "'/></td>";
		}
		
		markup += "<td class='icon-info'><div class='icon-title'>" + icon.text + "</div>";

		markup += "</td></tr></table>";
		return markup;
	}

	function iconHostFormatSelection(icon)
	{
		$("#iconplace").contents().remove();
		$("#iconplace").append("<img src='http://"+ urlMaster +'/'+ icon.icon + "'/>");
		return icon.text;
	}

	function progress(percent, $element)
	{
    	var progressBarWidth = percent * $element.width() / 100;
    	$element.find('div').animate({ width: progressBarWidth }, 500).html(percent + "%&nbsp;");
	}

	function classicSuccessAlertMessage(content)
	{
		var message = "\
					<div class=\"alert alert-success col-lg-11\">\
						<i class=\"fa fa-check-circle-o fa-fw\"></i> Success: "+content+"\
					</div>";

		return message
	}

	function classicErrorAlertMessage(content)
	{
		var message = "\
					<div class=\"alert alert-danger col-lg-11\">\
						<i class=\"fa fa-exclamation-triangle fa-fw\"></i> Error: "+content+"\
					</div>";

		return message
	}

	function getProgressSync(d_data)
	{
		var flag_end = '';
		var percent_progress = 0;

		$.ajax({
			url: "http://"+urlMaster+"/getprogresssync",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: d_data,
			async: false,
			complete: function(data)
			{
				for (var i in data.responseJSON)
				{
					progress_info = jQuery.parseJSON(data.responseJSON[i]);
					if (progress_info)
					{
						flag_end = progress_info.status;
						percent_progress = progress_info.progress;

						if (progress_info.status == 'success' || progress_info.status == 'end')
						{
							$( ".ProgressionContent" ).append(classicSuccessAlertMessage(progress_info.message));
							progress(progress_info.progress, $('#progressBar'));
						}
						else if (progress_info.status == 'failed')
						{
							$( ".ProgressionContent" ).append(classicErrorAlertMessage(progress_info.message));
							break;
						};
					};
				};

				if (flag_end != 'end' && flag_end != 'failed')
				{
					setTimeout(function() { getProgressSync(d_data);}, 500);
				};
			}
		});
	}

	$("#hosticon").select2({
		id: function(data){ return data.id; },
		ajax: {
			url: "http://"+urlMaster+"/gettypehosticon",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					page_limit: 10
					};
			},
			results: function (data, page) {
				console.log(data);
				return {results: data};
			}
		},
		formatResult: iconHostFormatResult,
		formatSelection: iconHostFormatSelection,
		dropdownCssClass: "bigdrop",
		escapeMarkup: function(m) { return m; }
	});

	$("#supervisor_name").select2({
		minimumInputLength: 1,
		ajax: {
			url: "http://"+urlMaster+"/getlistsupervisor",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#use_template").select2({
		minimumInputLength: 1,
		multiple: true,
		ajax: {
			url: "http://"+urlMaster+"/getlistusetemplate",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#group").select2({
		minimumInputLength: 1,
		multiple: true,
		ajax: {
			url: "http://"+urlMaster+"/getlistgroup",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

/*
	$("#listservices_select").select2({
		ajax: {
			url: "http://"+urlMaster+"/getlistservices",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});
*/
	$( "#listservices .remove" ).each(function( index ) {
		$( this ).click(function(){
			$( this ).parent().remove();
		});
	});

	$( "#listmacros .remove" ).each(function( index ) {
		$( this ).click(function(){
			$( this ).parent().remove();
		});
	});

	$("#add_service").click(function(){
		$('.no_result_service').each(function( index ) {
			$( this ).parent().remove();
		});

		var service_info = $('#listservices_select').val();
		var t_service_info = service_info.split("#");

		$('#tab_service > tbody:last').append("<tr><td>"+jQuery.trim(t_service_info[0])+"</td><td>"+jQuery.trim(t_service_info[1])+"</td><td class=\"remove\"><button type=\"button\" class=\"btn btn-default\"><i class=\"fa fa-trash-o\"></i> Remove</button></td></tr>");

		$( "#listservices .remove" ).each(function( index ) {
			$( this ).click(function(){
				$( this ).parent().remove();
			});
		});
	});

	$("#add_macro").click(function(){
		$('.no_result_macro').each(function( index ) {
			$( this ).parent().remove();
		});

		$('#tab_macro > tbody:last').append("<tr><td>"+$('#macro_name').val()+"</td><td>"+$('#macro_val').val()+"</td><td class=\"remove\"><button type=\"button\" class=\"btn btn-default\"><i class=\"fa fa-trash-o\"></i> Remove</button></td></tr>");

		$( "#listmacros .remove" ).each(function( index ) {
			$( this ).click(function(){
				$( this ).parent().remove();
			});
		});
	});

	$("#submit_host").click(function (){
		$("#sync_div").show();

		var flag_progress = true;

		var t_services = [];
		$("#tab_service tr > td:first-child").each(function (){
			t_services.push($(this).text());
		});

		var t_macros = [];
		var t_temp = {};
		$("#tab_macro tr").each(function (){
			if ($(this).find("td:first-child").text() != "")
			{
				t_temp["name"] = $(this).find("td:first-child").text();
				t_temp["value"] = $(this).find("td:nth-child(2)").text();
				t_macros.push(t_temp);
				t_temp = {};
			};
		});

		var d_data = {'supervisor': $("#supervisor_name").val(), 'collection2Sync': 'HostConfig'};

		$.ajax({
			url: "http://"+urlMaster+"/publishhostindb",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'addtype': $("#addtype").val(), 'oid': $("#oid").val(), 'conf_filepath': $("#conf_filepath").val(), 'supervisor': $("#supervisor_name").val(), 'use_template': $("#use_template").val(), 'parents': $("#host_parent").val(), 'hostname': $("#hostname").val(), 'ip': $("#ip").val(), 'alias': $("#alias").val(), 'group': $("#group").val(), 'services': JSON.stringify(t_services), 'macros': JSON.stringify(t_macros)},
			async: false,
			success: function(data)
			{
				/*
					Faire le remplacement du message de succes en le recuperant depuis le python comme pour les messages d'erreurs
				*/
				progress(10, $('#progressBar'));
				$( ".ProgressionContent" ).append(classicSuccessAlertMessage("Initialisation complete"));
			},
			error: function(data)
			{				
				for (var key in data.responseJSON['results'])
				{
					$( ".ProgressionContent" ).append(classicErrorAlertMessage(data.responseJSON['results'][key]));
				};
				flag_progress = false
			}
		});

		if (flag_progress)
		{
			$.ajax({
				url: "http://"+urlMaster+"/launchsync",
				contentType: 'application/json; charset=utf-8',
				dataType: 'jsonp',
				async: true,
				data: d_data,
				success: function(data)
				{
					//progress(100, $('#progressBar'));
					for (var key in data['results'])
					{
						$( ".ProgressionContent" ).append(classicSuccessAlertMessage(data['results'][key]));
					};
				},
				error: function(data)
				{	
					for (var key in data.responseJSON['results'])
					{
						$( ".ProgressionContent" ).append(classicErrorAlertMessage(data.responseJSON['results'][key]));
					};
					flag_progress = false;
				}
			});

			getProgressSync(d_data);
		};
	});

	$("#group").select2("data", jQuery.parseJSON($("#group_list").val()));
	$("#supervisor_name").select2("data", jQuery.parseJSON($("#supervisor_name_arg").val()));
	$("#use_template").select2("data", jQuery.parseJSON($("#use_template_list").val()));

	$("#host_parent").select2({
		id: function(data){ return data.id; },
		minimumInputLength: 1,
		multiple: true,
		ajax: {
			url: "http://"+urlMaster+"/getlisthost/"+$("#supervisor_name").val(),
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#listservices_select").select2({
		ajax: {
			url: "http://"+urlMaster+"/getlistservices/"+$("#supervisor_name").val(),
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#host_parent").select2("data", jQuery.parseJSON($("#parents_list").val()));

});
