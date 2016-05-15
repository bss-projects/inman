$(function()
{

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
			});
			var table = $('#dataTables-client_list_freeradius').dataTable().api();
			table.ajax.reload();
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
			});
		},
		submit: function (e, data){
			$('#fileupload_list').append('<tr><td>'+data.files[0]['name']+'</td><td class="fa fa-spin fa-spinner fa-fw"></td></tr>');
		}
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
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	function launchSync(radiusname, collection_info, plugin){

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
				console.log('Error sync');
			}
		});
	};

	$( '#add_client_freeradius' ).click(function() {
		var radiusname = $('#radiusname_client_freeradius').val();
		var vendorname = $('#vendor_client_freeradius').val();
		var name = $('#name_client_freeradius').val();
		var shortname = $('#shortname_client_freeradius').val();
		var ip = $('#ip_client_freeradius').val();
		var sharedsecret = $('#secret_client_freeradius').val();

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_client_freeradius/new",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'radiusname': radiusname, 'client': name, 'vendorname': vendorname, 'shortname': shortname, 'ip': ip, 'sharedsecret': sharedsecret},
			async: false,
			success: function(data)
			{
				location.reload(true);
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
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
								page_limit: 10
								};
						},
						results: function (data, page) {
							return {results: data.results};
						}
					}
				});
				$('#edit_vendor_client_freeradius').select2('data', {'id': vendorname, 'text': vendorname});

				var d_data = {'collection': 'client_freeradius', 'vendorname': vendorname, 'radiusname': radiusname, 'client': client, 'uid': uid, 'fields' : 'client_info'};

				$.ajax({
					url: "http://"+urlMaster+"/im_get_doc_freeradius",
					dataType: 'jsonp',
					async: false,
					data: d_data,
					success: function(data)
					{
						$('#edit_shortname_client_freeradius').val(data['doc']['shortname']);
						$('#edit_secret_client_freeradius').val(data['doc']['sharedsecret']);
					}
				});

				$('#edit_name_client_freeradius').val(client);
				$('#edit_ip_client_freeradius').val(ip);

				$('#uid_edit_freeradius').val(uid);

				$('#modal_edit_client_freeradius').modal('show');
			});

		$('.btn_delete_client').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.client_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
				$('.client_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());

				$('.vendor_remove_freeradius').val($( this ).closest('tr').children().eq(3).text());
				$('.vendor_remove_freeradius').html($( this ).closest('tr').children().eq(3).text());

				$('#uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());

				$('#modal_delete_client_freeradius').modal('show');
			});
		});

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/client_freeradius/client/all",
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
				$('#modal_delete_client_freeradius').modal('hide');
				var table = $('#dataTables-client_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit' ).click(function() {
		var client = $('#edit_name_client_freeradius').val();
		var vendorname = $('#edit_vendor_client_freeradius').val();
		var radiusname = $('#edit_radiusname_client_freeradius').val();
		var shortname = $('#edit_shortname_client_freeradius').val();
		var ip = $('#edit_ip_client_freeradius').val();
		var sharedsecret = $('#edit_secret_client_freeradius').val();
		var uid = $('#uid_edit_freeradius').val();


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
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});



///
/// Manage Range
///

	$("#range_radiusname_client_freeradius").select2({
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

	$( '#add_range_client_freeradius' ).click(function() {
		var radiusname = $('#range_radiusname_client_freeradius').val();
		var rangename = $('#range_name_client_freeradius').val();
		var subnet = $('#range_subnet_client_freeradius').val();
		var sharedsecret = $('#range_sharedsecret_client_freeradius').val();

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_range_freeradius/new",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'radiusname': radiusname, 'rangename': rangename, 'subnet': subnet, 'sharedsecret': sharedsecret},
			async: false,
			success: function(data)
			{
				location.reload(true);
				var collection_info = [{'collection': 'range_freeradius', 'json_field': 'range', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});


	$('#dataTables-range_client_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_range').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {

				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var rangename = $( this ).closest('tr').children().eq(1).text();
				var subnet = $( this ).closest('tr').children().eq(2).text();
//				var sharedsecret = $( this ).closest('tr').children().eq(1).text()
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_range_radiusname_client_freeradius").select2({
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
				$('#edit_range_radiusname_client_freeradius').select2('data', {'id': radiusname, 'text': radiusname});

				var d_data = {'collection': 'range_freeradius', 'rangename': rangename, 'radiusname': radiusname, 'subnet': subnet, 'uid': uid, 'fields' : 'range_info'};

				$.ajax({
					url: "http://"+urlMaster+"/im_get_doc_freeradius",
					dataType: 'jsonp',
					async: false,
					data: d_data,
					success: function(data)
					{
						$('#edit_range_sharedsecret_client_freeradius').val(data['doc']['sharedsecret']);
					}
				});

				$('#edit_range_name_client_freeradius').val(rangename);
				$('#edit_range_subnet_client_freeradius').val(subnet);

				$('#uid_edit_freeradius').val(uid);

				$('#modal_edit_range_client_freeradius').modal('show');
			});

		$('.btn_delete_range').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.rangename_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
				$('.rangename_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());

				$('.subnet_remove_freeradius').val($( this ).closest('tr').children().eq(2).text());
				$('.subnet_remove_freeradius').html($( this ).closest('tr').children().eq(2).text());

				$('#uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());

				$('#modal_delete_range_client_freeradius').modal('show');
			});
		});

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/range_freeradius/range/all",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
			{ "data": "nom" },
			{ "data": "sous-reseau" },
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

	$( '#proceed_remove_range' ).click(function() {
		var rangename = $('#rangename_remove_freeradius').val();
		var radiusname = $('#radiusname_remove_freeradius').val();
		var uid = $('#uid_remove_freeradius').val();

		var d_data = {'radius': radiusname, 'collection': 'range_freeradius', 'action_type': 'delete_range', 'rangename': rangename, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_range_freeradius/delete",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_delete_range_client_freeradius').modal('hide');
				var table = $('#dataTables-range_client_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'range_freeradius', 'json_field': 'range', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit_range' ).click(function() {
		var rangename = $('#edit_range_name_client_freeradius').val();
		var radiusname = $('#edit_range_radiusname_client_freeradius').val();
		var subnet = $('#edit_range_subnet_client_freeradius').val();
		var sharedsecret = $('#edit_range_sharedsecret_client_freeradius').val();
		var uid = $('#uid_edit_freeradius').val();


		var d_data = {'collection': 'range_freeradius', 'action_type': 'edit_range', 'radiusname': radiusname, 'rangename': rangename, 'subnet': subnet, 'sharedsecret': sharedsecret, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_range_freeradius/edit",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_edit_range_client_freeradius').modal('hide');
				var table = $('#dataTables-range_client_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'range_freeradius', 'json_field': 'range', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

});
