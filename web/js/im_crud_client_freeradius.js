$(function()
{
	var l_client_ip = new Array();

	function radiusnameIsOK(radiusname)
	{
		if (radiusname != '')
		{
			return true;
		}
		else
		{
			return 'RADIUS name is missing';
		}
	}

	function ipIsOK(radiusname, ipaddress, previous_radiusname, previous_ip) 
	{
		if (ipaddress != '')
		{
			if (previous_ip && radiusname+'-'+ipaddress == previous_radiusname+'-'+previous_ip)
			{
				return true;
			}

			if (! /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress))
			{
				return 'IP format incorrect';
			}

			if (l_client_ip.includes(radiusname+'-'+ipaddress))
			{
				return 'IP already in use';
			}
	
			return (true);
		}
		else
		{
			return 'IP is missing';
		}

	}

	function stringIsOK(name, shortname, sharedsecret)
	{
		if (name != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(name))
			{
				return 'Client name format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}
		}

		if (shortname != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(shortname))
			{
				return 'Client shortname format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}
		}

		if (sharedsecret != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(sharedsecret))
			{
				return 'Client sharedsecret format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}
		}

		return true;
	}

	function check_input_form(radiusname, name, shortname, ip, vendorname, sharedsecret, previous_radiusname, ip_previousip)
	{
		console.log(name);
		var flag_input_error = false;
		var ret = '';
		var errno = new Array();

		if ((ret = radiusnameIsOK(radiusname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = ipIsOK(radiusname, ip, previous_radiusname, ip_previousip)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = stringIsOK(name, shortname, sharedsecret)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if (!vendorname)
		{
			flag_input_error = true;
			errno.push('No vendor selected')
		}

		if (flag_input_error)
		{
			return errno;	
		}
		else
		{
			return false;
		}
	}

	function format_error_import_client_file(d_error) 
	{
		var ret = '';

		for (var i = 0; i < d_error.length; i++)
		{
			var error_string = '';
			var l_keys = Object.keys(d_error[i]['error']);

			for (var j = 0; j < l_keys.length; j++)
			{
				var eof = '</br>';
				if (j+1 == l_keys.length)
				{
					eof = '';
				}
				error_string += d_error[i]['error'][l_keys[j]] + eof;
			}

			line_number = Number(d_error[i]['line']) + 1;

			ret += '<tr>\
						<td>'+line_number+'</td>\
						<td>'+error_string+'</td>\
					</tr>';
		}

		if (d_error.length == 0)
		{
			ret += '<tr>\
						<td></td>\
						<td>No error detected in file</td>\
					</tr>';
		}

		return ret;
		
	}

	function get_shared_secret_name(uid)
	{
		var d_data = {'collection': 'shared_secret_freeradius', 'uid': uid, 'fields' : 'shared_secret_info->>\'name\''};
		var shared_secret_name = '';

		if (uid)
		{
			$.ajax({
				url: "http://"+urlMaster+"/im_get_doc_freeradius",
				dataType: 'jsonp',
				async: false,
				data: d_data,
				success: function(data)
				{
					shared_secret_name = data['doc'];
				}
			});
		}

		return shared_secret_name
	}

	$('#fileupload').fileupload({
//		dataType: 'json',
		dropZone: $('#dropzone'),
//		uploadedBytes: 250000,
		done: function (e, data) {
			$.each($('#fileupload_list tr'), function () {
				var UFilename = data.files[0]['name'];
				var TFilename = $(this).children().eq(0).html();

				
				if (UFilename == TFilename)
				{
					$(this).children().eq(1).removeClass();
//					$(this).children().eq(1).addClass('fa fa-check-circle-o fa-fw');
					$(this).children().eq(1).append('&nbsp;&nbsp;[OK]');
				};

				$('#table_client_file_import_error tbody').empty();
				$('#import_file_sync_state ul').empty();
				var error_formated = format_error_import_client_file(data['result']['error_data_results']);
				$('#table_client_file_import_error tbody').append(error_formated);
				$('#modal_client_import_file_result_freeradius').modal('show');

				console.log(UFilename);
			});
			$('#import_file_number_of_line').text(data['result']['insert_data_results'].length);
			var table = $('#dataTables-client_list_freeradius').dataTable().api();
			table.ajax.reload();

			var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
			for (var i = 0; i < data['result']['radius_list'].length; i++)
			{
				var radiusname = data['result']['radius_list'][i];

				$('#import_file_sync_state ul').append('<li><i class="fa fa-spinner fa-spin"></i><span> Synchronization in progress for '+radiusname+'</span></li>');

				var state = launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
				if (state == true)
				{
					$('#import_file_sync_state ul li').last().text('Synchronisation complete for '+radiusname);
				}
				else
				{
					$('#import_file_sync_state ul li').last().text(state);
				}
			}
		},
		fail: function (e, data){
			$.each($('#fileupload_list tr'), function () {
				var UFilename = data.files[0]['name'];
				var TFilename = $(this).children().eq(0).html();
				
				if (UFilename == TFilename)
				{
					$(this).children().eq(1).removeClass();
//					$(this).children().eq(1).addClass('fa fa-times-circle-o fa-fw');
					$(this).children().eq(1).append('&nbsp;&nbsp;[Echec]');
				};
				$('#table_client_file_import_error tbody').empty();
				$('#import_file_sync_state ul').empty();
				$('#import_file_number_of_line').text('None');
				$('#table_client_file_import_error tbody').append('<tr>\
																	<td></td>\
																	<td>'+data.errorThrown+'</td>\
																</tr>');
				$('#modal_client_import_file_result_freeradius').modal('show');
			});
		},
		submit: function (e, data){
			$('#fileupload_list').append('<tr><td>'+data.files[0]['name']+'</td><td class="fa fa-spin fa-spinner fa-fw"></td></tr>');
		}
	})
	.bind('fileuploadchange', function (e, data) {
		$('#fileupload_list').empty();
	});

	$("#radiusname_client_freeradius").select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_agent_freeradius",
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

	$("#vendor_client_freeradius").select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_vendor_freeradius",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					radiusname: $("#radiusname_client_freeradius").val(),
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#secret_client_freeradius").select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_shared_secret_freeradius",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					radiusname: $("#radiusname_client_freeradius").val(),
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	function launchSync(radiusname, collection_info, plugin)
	{
		var state = true;

		$.ajax({
			url: "http://"+urlMaster+"/launchsync_freeradius",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'radiusname': radiusname, 'plugin': plugin, 'collection_info': collection_info},
			async: false,
			success: function(data)
			{
				console.log('Success sync');
			},
			error: function(data)
			{
				console.log(data.statusText);
				state = data.statusText;
			}
		});

		return state;
	};

	$( '#add_client_freeradius' ).click(function() {
		var radiusname = $('#radiusname_client_freeradius').val();
		var vendorname = $('#vendor_client_freeradius').val();
		var name = $('#name_client_freeradius').val().trim();
		var shortname = $('#shortname_client_freeradius').val().trim();
		var ip = $('#ip_client_freeradius').val().trim();
		var sharedsecret = $('#secret_client_freeradius').val();

		var input_errno = false
		input_errno = check_input_form(radiusname, name, shortname, ip, vendorname, sharedsecret, null, null)

		if (input_errno == false)
		{
			$('#alert_input').hide();

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_client_freeradius/new",
				contentType: 'application/json; charset=utf-8',
				dataType: 'jsonp',
				data: {'radiusname': radiusname, 'client': name, 'vendorname': vendorname, 'shortname': shortname, 'ip': ip, 'sharedsecret': sharedsecret},
				async: false,
				success: function(data)
				{
					location.reload(true);
					var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}, {'collection': 'shared_secret_freeradius', 'json_field': 'shared_secret', 'json_key': 'radiusname'}]
					launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
				}
			});
		}
		else
		{
			$('#alert_input').empty();
			$('#alert_input').append('<p>Input error on following :</p>');
			for (var i = input_errno.length - 1; i >= 0; i--)
			{
				$('#alert_input').append('- '+input_errno[i]+'</br>');
			}
			$('#alert_input').show();
		}
	});

	$('#dataTables-client_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_client').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {

				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var vendorname = $( this ).closest('tr').children().eq(3).text();
				var ip = $( this ).closest('tr').children().eq(2).text()
				var client = $( this ).closest('tr').children().eq(1).text()
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_radiusname_client_freeradius").select2({
					ajax: {
						url: "http://"+urlMaster+"/im_list_agent_freeradius",
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
				$('#edit_radiusname_client_freeradius').select2('data', {'id': radiusname, 'text': radiusname});

				$("#edit_vendor_client_freeradius").select2({
					ajax: {
						url: "http://"+urlMaster+"/im_list_vendor_freeradius",
						dataType: 'jsonp',
						data: function (term, page) {
							return {
								q: term, // search term
								radiusname: $("#edit_radiusname_client_freeradius").val(),
								page_limit: 10
								};
						},
						results: function (data, page) {
							return {results: data.results};
						}
					}
				});
				$('#edit_vendor_client_freeradius').select2('data', {'id': vendorname, 'text': vendorname});

				$("#edit_secret_client_freeradius").select2({
					ajax: {
						url: "http://"+urlMaster+"/im_list_shared_secret_freeradius",
						dataType: 'jsonp',
						data: function (term, page) {
							return {
								q: term, // search term
								radiusname: $("#edit_radiusname_client_freeradius").val(),
								page_limit: 10
								};
						},
						results: function (data, page) {
							return {results: data.results};
						}
					}
				});

				$('#clear_secret_client_freeradius').click(function(){
					$("#edit_secret_client_freeradius").select2("val", "");
				});

				var d_data = {'collection': 'client_freeradius', 'vendorname': vendorname, 'radiusname': radiusname, 'client': client, 'uid': uid, 'fields' : 'client_info'};
				var shared_secret_name = ''

				$.ajax({
					url: "http://"+urlMaster+"/im_get_doc_freeradius",
					dataType: 'jsonp',
					async: false,
					data: d_data,
					success: function(data)
					{
						$('#edit_shortname_client_freeradius').val(data['doc']['shortname']);
						shared_secret_name = get_shared_secret_name(Number(data['doc']['sharedsecret']));
						$('#edit_secret_client_freeradius').select2('data', {'id': data['doc']['sharedsecret'], 'text': shared_secret_name});
					}
				});

				$('#edit_name_client_freeradius').val(client);
				$('#edit_ip_client_freeradius').val(ip);
				$('#edit_previous_ip_client_freeradius').val(ip);
				$('#edit_previous_radiusname_client_freeradius').val(radiusname);

				$('#uid_edit_freeradius').val(uid);

				$('#modal_edit_client_freeradius').modal('show');
			});
		});

		$('.btn_delete_client').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.client_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
				$('#client_ip_remove_freeradius').html($( this ).closest('tr').children().eq(2).text());
				$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
				$('.client_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
				$('#client_ip_remove_freeradius').val($( this ).closest('tr').children().eq(2).text());
				$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());

				$('.vendor_remove_freeradius').val($( this ).closest('tr').children().eq(3).text());
				$('.vendor_remove_freeradius').html($( this ).closest('tr').children().eq(3).text());

				$('#uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());

				$('#modal_delete_client_freeradius').modal('show');
			});
		});

	}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"createdRow": function(row, data, dataIndex){
			l_client_ip.push(data['radius']+'-'+data['ip']);
		},
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/client_freeradius/client/",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
			{ "data": "client" },
			{ "data": "ip" },
			{ "data": "vendeur" },
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
		var client = $('#client_remove_freeradius').val();
		var ip = $('#client_ip_remove_freeradius').val();
		var vendorname = $('#vendor_remove_freeradius').val();
		var radiusname = $('#radiusname_remove_freeradius').val();
		var uid = $('#uid_remove_freeradius').val();

		var d_data = {'radius': radiusname, 'collection': 'client_freeradius', 'action_type': 'delete_client', 'client': client, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_client_freeradius/delete",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				var index = l_client_ip.indexOf(radiusname+'-'+ip);
				if (index >= 0)
				{
					l_client_ip.splice( index, 1 );
				}
				$('#modal_delete_client_freeradius').modal('hide');
				var table = $('#dataTables-client_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}, {'collection': 'shared_secret_freeradius', 'json_field': 'shared_secret', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit' ).click(function() {
		var client = $('#edit_name_client_freeradius').val().trim();
		var vendorname = $('#edit_vendor_client_freeradius').val();
		var radiusname = $('#edit_radiusname_client_freeradius').val();
		var shortname = $('#edit_shortname_client_freeradius').val().trim();
		var ip = $('#edit_ip_client_freeradius').val().trim();
		var ip_previousip = $('#edit_previous_ip_client_freeradius').val();
		var previous_radiusname = $('#edit_previous_radiusname_client_freeradius').val();
		var sharedsecret = $('#edit_secret_client_freeradius').val().trim();
		var uid = $('#uid_edit_freeradius').val();

		var input_errno = false
		input_errno = check_input_form(radiusname, client, shortname, ip, vendorname, sharedsecret, previous_radiusname, ip_previousip);

		if (input_errno == false)
		{
			$('#edit_alert_input').hide();

			var d_data = {'collection': 'client_freeradius', 'action_type': 'edit_client', 'radiusname': radiusname, 'client': client, 'vendorname': vendorname, 'shortname': shortname, 'ip': ip, 'sharedsecret': sharedsecret, 'uid': uid};

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_client_freeradius/edit",
				dataType: 'jsonp',
				async: false,
				data: d_data,
				success: function(data)
				{
					console.log('success');
					$('#modal_edit_client_freeradius').modal('hide');
					var table = $('#dataTables-client_list_freeradius').dataTable().api();
					table.ajax.reload();
					var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}, {'collection': 'shared_secret_freeradius', 'json_field': 'shared_secret', 'json_key': 'radiusname'}]
					launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
				}
			});
		}
		else
		{
			$('#edit_alert_input').empty();
			$('#edit_alert_input').append('<p>Input error on following :</p>');
			for (var i = input_errno.length - 1; i >= 0; i--)
			{
				$('#edit_alert_input').append('- '+input_errno[i]+'</br>');
			}
			$('#edit_alert_input').show();
		}

	});
});