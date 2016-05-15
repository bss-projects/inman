$(function()
{

	var l_right = new Bloodhound({
									datumTokenizer: Bloodhound.tokenizers.whitespace,
									queryTokenizer: Bloodhound.tokenizers.whitespace,
									prefetch: '/im_list_right_autocomplete_freeradius'
								});

	$('#autocomplete_label_right_freeradius .typeahead').typeahead(null,
								{
									name: 'label_right_freeradius',
									source: l_right
								}
	);

	$("#radiusname_right_freeradius").select2({
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

	$("#vendor_right_freeradius").select2({
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

	$("#vendor_right_freeradius").on('select2-selecting', function(e) {

		var d_data = {'vendorname': e.val};

		$.ajax({
			url: "http://"+urlMaster+"/im_list_flag_vendor_freeradius",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				$('.panel-body .list_vendor_flag_freeradius').empty()
				$('.panel-body .list_vendor_flag_freeradius').append(data['data']);
			}
		});
	});

	function getTabVendorFlag(tab) {
		var tab_flag = new Array();

		tab.children().each(function(){
			var list_flag = new Object();

			var flag_name = $( this ).children('.input-group').children('span').eq(0).text();
			var flag_val = $( this ).children('.input-group').children('input').eq(0).val();

			list_flag[flag_name] = flag_val;
			tab_flag.push(list_flag);
		});

		return tab_flag;
	}

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

	$( '#add_vendor_right_freeradius' ).click(function() {
		var radiusname = $('#radiusname_right_freeradius').val();
		var vendorname = $('#vendor_right_freeradius').val();
		var label = $('#label_right_freeradius').val();
		var tab_flag = getTabVendorFlag($('.panel-body .list_vendor_flag_freeradius'));

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_right_freeradius/new",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'radiusname': radiusname, 'label': label, 'vendorname': vendorname, 'l_flag': JSON.stringify(tab_flag)},
			async: false,
			success: function(data)
			{
				location.reload(true);
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$('#dataTables-right_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_right').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var label = $( this ).closest('tr').children().eq(1).text();
				var vendorname = $( this ).closest('tr').children().eq(2).text();
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_radiusname_right_freeradius").select2({
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
				$('#edit_radiusname_right_freeradius').select2('data', {'id': radiusname, 'text': radiusname});

				$('#edit_label_right_freeradius').val(label);

				$("#edit_vendor_right_freeradius").select2({
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
				$('#edit_vendor_right_freeradius').select2('data', {'id': vendorname, 'text': vendorname});


				$("#edit_vendor_right_freeradius").on('select2-selecting', function(e) {

					var d_data = {'vendorname': e.val};

					$.ajax({
						url: "http://"+urlMaster+"/im_list_flag_vendor_freeradius",
						dataType: 'jsonp',
						async: false,
						data: d_data,
						success: function(data)
						{
							$('#modal_edit_right_freeradius .modal-dialog .modal-content .modal-body .row .list_vendor_flag_freeradius').empty()
							$('#modal_edit_right_freeradius .modal-dialog .modal-content .modal-body .row .list_vendor_flag_freeradius').append(data['data']);
						}
					});
				});

				$('#uid_edit_freeradius').val(uid);

				var d_data = {'vendorname': vendorname, 'radiusname': radiusname, 'label': label, 'uid': uid};

				$.ajax({
					url: "http://"+urlMaster+"/im_list_flag_value_vendor_freeradius",
					dataType: 'jsonp',
					async: false,
					data: d_data,
					success: function(data)
					{
						$('#modal_edit_right_freeradius .modal-dialog .modal-content .modal-body .row .list_vendor_flag_freeradius').empty()
						$('#modal_edit_right_freeradius .modal-dialog .modal-content .modal-body .row .list_vendor_flag_freeradius').append(data['data']);
					}
				});

				$('#modal_edit_right_freeradius').modal('show');
			});

		$('.btn_delete_right').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.right_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
				$('.right_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());
				$('.vendor_remove_freeradius').val($( this ).closest('tr').children().eq(2).text());
				$('.vendor_remove_freeradius').html($( this ).closest('tr').children().eq(2).text());
				$('.uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());
				$('#modal_delete_right_freeradius').modal('show');
			});
		});

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/vendor_freeradius/right/all",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
			{ "data": "label" },
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
		var label = $('#right_remove_freeradius').val();
		var vendorname = $('#vendor_remove_freeradius').val();
		var radiusname = $('#radiusname_remove_freeradius').val();
		var uid = $('#uid_remove_freeradius').val();

		var d_data = {'radius': radiusname, 'collection': 'vendor_freeradius', 'action_type': 'delete_right', 'vendorname': vendorname, 'uid': uid, 'label': label};

		$.ajax({
			url: "http://"+urlMaster+"/im_delete_right_freeradius",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_delete_right_freeradius').modal('hide');
				var table = $('#dataTables-right_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit' ).click(function() {
		var label = $('#edit_label_right_freeradius').val();
		var vendorname = $('#edit_vendor_right_freeradius').val();
		var radiusname = $('#edit_radiusname_right_freeradius').val();
		var uid = $('#uid_edit_freeradius').val();
		var tab_flag = getTabVendorFlag($('#modal_edit_right_freeradius .modal-dialog .modal-content .modal-body .row .list_vendor_flag_freeradius'));

		var d_data = {'radiusname': radiusname, 'collection': 'vendor_freeradius', 'action_type': 'edit_vendor_right', 'vendorname': vendorname, 'uid': uid, 'l_flag': JSON.stringify(tab_flag), 'label': label};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_right_freeradius/edit",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_edit_right_freeradius').modal('hide');
				var table = $('#dataTables-right_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

});
