$(function()
{
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
						if (progress_info.status == 'success')
						{
							$( ".ProgressionContent" ).append(classicSuccessAlertMessage(progress_info.message));
							progress(progress_info.progress, $('#progressBar'));
						}
						else if (progress_info.status == 'failed')
						{
							$( ".ProgressionContent" ).append(classicErrorAlertMessage(progress_info.message));
						};

						flag_end = progress_info.status;
						percent_progress = progress_info.progress;
					};
				};

				if (flag_end != 'end')
				{
					setTimeout(function() { getProgressSync(d_data);}, 500);
				};
			}
		});
	}

	function ValidateIPaddress(ipaddress) 
	{
		if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress))
		{
			return (true)
		}
		return (false)
	}

	$("#templatemodel").select2({
		id: function(data){ return data.id; },
		minimumInputLength: 1,
		ajax: {
			url: "http://"+urlMaster+"/getlisthost/all",
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

	$("#supervisor_newhost").select2({
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

	$("#supervisor_newhost").on("select2-selecting", function() {$(".create_new_host").prop('disabled', false);})
	$("#templatemodel").on("select2-selecting", function() {$(".create_from_template").prop('disabled', false);})

	$("#hostname_newhost").change(function(){
		var allHost = "";

		//il faut passer en param le nom du superviseur choisi
		/////Il faut mettre en place un select avec indication du superviseur pour choix modele en cas de doublon sur des superviseurs différents

		$.ajax({
			url: "http://"+urlMaster+"/getallhost/all",
			dataType: 'jsonp',
			data: {'supervisor': $("#supervisor_newhost").val()},
			async: false,
			success: function(data)
			{
				allHost = data;
				if ($.inArray($("#hostname_newhost").val(), allHost) == -1)
				{
					$("#hostname_newhost").parent().parent().removeClass("has-error");
					$("#hostname_newhost").parent().parent().addClass("has-success");
				}
				else
				{
					$("#hostname_newhost").parent().parent().removeClass("has-success");
					$("#hostname_newhost").parent().parent().addClass("has-error");
				};
			}
		});
	});

	$("#ip_newhost").change(function(){
		if (!ValidateIPaddress($("#ip_newhost").val()))
		{
			$("#ip_newhost").parent().parent().removeClass("has-success");
			$("#ip_newhost").parent().parent().addClass("has-error");
		}
		else
		{
			$("#ip_newhost").parent().parent().removeClass("has-error");
			$("#ip_newhost").parent().parent().addClass("has-success");
		}
	});

	$("#hostname_template").change(function(){

			var allHost = "";

		//il faut passer en param le nom du superviseur choisi
		/////Il faut mettre en place un select avec indication du superviseur pour choix modele en cas de doublon sur des superviseurs différents

		$.ajax({
			url: "http://"+urlMaster+"/getallhost/all",
			dataType: 'jsonp',
			data: {'supervisor': $("#templatemodel").val().split(":")[0]},
			async: false,
			success: function(data)
			{
				allHost = data;
				if ($.inArray($("#hostname_template").val(), allHost) == -1)
				{
					$("#hostname_template").parent().parent().removeClass("has-error");
					$("#hostname_template").parent().parent().addClass("has-success");
				}
				else
				{
					$("#hostname_template").parent().parent().removeClass("has-success");
					$("#hostname_template").parent().parent().addClass("has-error");
				};
			}
		});
	});

	$('#filterlevelview').bootstrapSwitch({
		onText: 'Simple',
		offText: 'Complet',
		size: 'normal'
	});

	$('#fileupload').fileupload({
		dataType: 'json',
		dropZone: $('#dropzone'),
		done: function (e, data) {
			$.each(data.result.files, function (index, file) {
				$('<p/>').text(file.name).appendTo(document.body);
			});
		}
	});

	$('#dataTables-hostlist').on('draw.dt', function () {
		$('.btn_edit').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('<form action="im_crudhost/edit" method="POST">\
					<input type="hidden" name="templatemodel" value="'+$( this ).closest('tr').children().eq(0).text()+':'+$( this ).closest('tr').children().eq(1).text()+'">\
					<input type="hidden" name="ip_edit" value="'+$( this ).closest('tr').children().eq(2).text()+'">\
					<input type="hidden" name="alias_edit" value="'+$( this ).closest('tr').children().eq(3).text()+'">\
					</form>').appendTo('body').submit();
		});

		$('.btn_delete').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.hostname_remove').html($( this ).closest('tr').children().eq(1).text());
				$('.supervisor_remove').html($( this ).closest('tr').children().eq(0).text());
				$('.hostname_remove').val($( this ).closest('tr').children().eq(1).text());
				$('.supervisor_remove').val($( this ).closest('tr').children().eq(0).text());
				$('#modal_delete_host').modal('show');
			});
		});

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/getlisthostinfo/all",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "superviseur" },
			{ "data": "hote" },
			{ "data": "ip" },
			{ "data": "nom" },
			{ "data": "action" }
		],
		"language": {
						"sProcessing":     "Traitement en cours...",
						"sSearch":         "Rechercher&nbsp;:",
						"sLengthMenu":     "Afficher _MENU_ &eacute;l&eacute;ments",
						"sInfo":           "Affichage de l'&eacute;lement _START_ &agrave; _END_ sur _TOTAL_ &eacute;l&eacute;ments",
						"sInfoEmpty":      "Affichage de l'&eacute;lement 0 &agrave; 0 sur 0 &eacute;l&eacute;ments",
						"sInfoFiltered":   "(filtr&eacute; de _MAX_ &eacute;l&eacute;ments au total)",
						"sInfoPostFix":    "",
						"sLoadingRecords": "Chargement en cours...",
						"sZeroRecords":    "Aucun &eacute;l&eacute;ment &agrave; afficher",
						"sEmptyTable":     "Aucune donnée disponible dans le tableau",
						"oPaginate": {
										"sFirst":      "Premier",
										"sPrevious":   "Pr&eacute;c&eacute;dent",
										"sNext":       "Suivant",
										"sLast":       "Dernier"
						},
						"oAria": {
						"sSortAscending":  ": activer pour trier la colonne par ordre croissant",
						"sSortDescending": ": activer pour trier la colonne par ordre décroissant"
						}
					}
	});
	
	$( '#proceed_remove' ).click(function() {
		var hostname = $('#hostname_remove').val();
		var supervisor = $('#supervisor_remove').val();
		//Ajax pour faire appel a la fonction de suppr du host dans la base en mode sync

		var d_data = {'supervisor': supervisor, 'collection2Sync': 'HostConfig', 'action_type': 'delete_host', 'hosttodelete': hostname};
		var end_progress = false;

		$.ajax({
			url: "http://"+urlMaster+"/deletehostindb",
			dataType: 'jsonp',
			async: false,
			data: {'hosttodelete': hostname ,'supervisor': supervisor},
			success: function(data)
			{
				console.log('success');
			}
		});

		$("#sync_div").show();

		$.ajax({
			url: "http://"+urlMaster+"/launchsync",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			async: true,
			data: d_data,
			success: function(data)
			{
				progress(100, $('#progressBar'));
				for (var key in data['results'])
				{
					$( ".ProgressionContent" ).append(classicSuccessAlertMessage(data['results'][key]));
				};
				end_progress = true;


				$('#modal_delete_host').modal('hide');
				var hostlist_table = $('#dataTables-hostlist').dataTable().api();
				hostlist_table.ajax.reload();
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

	});

});
