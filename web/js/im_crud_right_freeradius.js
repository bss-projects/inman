$(function()
{
	l_right_for_vendor = new Array();

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

	function stringIsOK(string, entry_name, mandatory)
	{
		if (string != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(string))
			{
				return entry_name+' format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}
			return (true);
		}
		else if (mandatory == true)
		{
			return entry_name+' is missing';
		}
		else
		{
			return true;
		}
	}

	function notassocIsOK(radiusname, label, vendorname, previous_radiusname, previous_vendorname, previous_label) {
		if (label != '' && vendorname != '')
		{
			if (radiusname+'-'+label+'-'+vendorname == previous_radiusname+'-'+previous_label+'-'+previous_vendorname) 
			{
				return true;
			}

			if (l_right_for_vendor.includes(radiusname+'-'+label+'-'+vendorname))
			{
				return label+' Already associate to '+vendorname;
			}
		}
		return true;
	}

	function vendor_flag_valueIsOK(tab_flag)
	{
		var errno = new Array();

		for (var i = 0; i < tab_flag.length; i++)
		{
			keys = Object.keys(tab_flag[i]);
			for (var j = 0; j < keys.length; j++)
			{
				if ((ret = stringIsOK(tab_flag[i][keys[j]], 'Flag '+keys[j], false)) != true)
				{
					errno.push(ret+'<br/>')
				}
			}
		}

		if (!errno.length)
		{
			return true;
		}
		else
		{
			return errno;
		}
	}

	function check_input_form(radiusname, vendorname, label, tab_flag, previous_radiusname, previous_vendorname, previous_label)
	{
		var flag_input_error = false;
		var ret = '';
		var errno = new Array();

		if ((ret = radiusnameIsOK(radiusname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = stringIsOK(label, 'Label right', true)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}
		
		if (!vendorname)
		{
			flag_input_error = true;
			errno.push('No vendor selected')
		}

		if ((ret = notassocIsOK(radiusname, label, vendorname, previous_radiusname, previous_vendorname, previous_label)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ( (ret = vendor_flag_valueIsOK(tab_flag)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
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

	function isInArray(value, array)
	{
		return array.indexOf(value) > -1;
	}

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

	$("#radiusname_right_freeradius").on('select2-selecting', function(e) {
		l_right = new Bloodhound({
									datumTokenizer: Bloodhound.tokenizers.whitespace,
									queryTokenizer: Bloodhound.tokenizers.whitespace,
									prefetch: {url: 'im_list_right_autocomplete_freeradius/'+e['val'],
												cache: false
											}
								});

		$('#autocomplete_label_right_freeradius .typeahead').typeahead('destroy');
		$('#autocomplete_label_right_freeradius .typeahead').typeahead(null,
								{
									name: 'label_right_freeradius',
									source: l_right
								}
		);
	});

	$("#vendor_right_freeradius").select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_vendor_freeradius",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					radiusname: $("#radiusname_right_freeradius").val(),
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#vendor_right_freeradius").on('select2-selecting', function(e) {

		var d_data = {'vendorname': e.val, 'radiusname': $("#radiusname_right_freeradius").val()};

		$.ajax({
			url: "http://"+urlMaster+"/im_list_flag_vendor_freeradius",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success list vendor flag');
				//console.log(data);
				$('.panel-body .list_vendor_flag_freeradius').empty()
				$('.panel-body .list_vendor_flag_freeradius').append(data['data']);
				var list_double = new Array();
				var children = $('.panel-body .list_vendor_flag_freeradius').children('.input-group');

				for (var i = 0; i < children.length; i++)
				{
					var node = children.eq(i);
					node_text = node.children('.input-group').children('.input-group-addon').text();
					if (isInArray(node_text, list_double))
					{
						node.remove();
					}
					else
					{
						list_double.push(node_text);
					}
				}
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
		var label = $('#label_right_freeradius').val().trim();
		var tab_flag = getTabVendorFlag($('.panel-body .list_vendor_flag_freeradius'));

		var input_errno = false
		input_errno = check_input_form(radiusname.toLowerCase(), vendorname.toLowerCase(), label.toLowerCase(), tab_flag, null, null, null)

		if (input_errno == false)
		{
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
								radiusname: $("#edit_radiusname_right_freeradius").val(),
								page_limit: 10
								};
						},
						results: function (data, page) {
							return {results: data.results};
						}
					}

				});
				
				$('#edit_vendor_right_freeradius').select2('data', {'id': vendorname, 'text': vendorname});

				$('#edit_label_right_freeradius').prop("disabled", true);
				$("#edit_vendor_right_freeradius").select2("disable");

				/*
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
				*/

				$('#edit_previous_label_right_freeradius').val(label);
				$('#edit_previous_vendor_right_freeradius').val(vendorname);
				$('#edit_previous_radiusname_right_freeradius').val(radiusname);

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

				var radiusname = $('.radiusname_remove_freeradius').val();
				var vendorname = $('.vendor_remove_freeradius').val();

				$('#remove_right_impact_list').empty();
				$('#remove_right_impact_list').append("Nothing </br>");

				$.ajax({
					url: "http://"+urlMaster+"/im_list_client_for_right_freeradius",
					contentType: 'application/json; charset=utf-8',
					dataType: 'jsonp',
					data: {'radiusname': radiusname, 'vendorname': vendorname},
					async: false,
					success: function(data)
					{	
						if (data['results'] != null)
						{
							$('#remove_right_impact_list').empty();
							$('#remove_right_id_impact_list').empty();
							for (var i = data['results'].length - 1; i >= 0; i--) 
							{
								$('#remove_right_impact_list').append(data['results'][i]['client_ip']+" "+data['results'][i]['client_name']+"</br>");
								$('#remove_right_id_impact_list').append('<input type="hidden" value="'+data['results'][i]['id']+'">');
							}
						}
					}
				});
			});
		});

	}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"createdRow": function(row, data, dataIndex){
			l_right_for_vendor.push(data['radius'].toLowerCase()+'-'+data['label'].toLowerCase()+'-'+data['vendeur'].toLowerCase());
		},
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/vendor_freeradius/right/",
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

		var d_data = {'radiusname': radiusname, 'collection': 'vendor_freeradius', 'action_type': 'delete_right', 'vendorname': vendorname, 'uid': uid, 'label': label};

		$.ajax({
			url: "http://"+urlMaster+"/im_delete_right_freeradius",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				var index = l_right_for_vendor.indexOf(radiusname.toLowerCase()+'-'+label.toLowerCase()+'-'+vendorname.toLowerCase());
				if (index >= 0)
				{
					l_right_for_vendor.splice( index, 1 );
				}
				$('#modal_delete_right_freeradius').modal('hide');
				var table = $('#dataTables-right_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'client_freeradius', 'json_field': 'client', 'json_key': 'radiusname'}, {'collection': 'vendor_freeradius', 'json_field': 'vendor', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit' ).click(function() {
		var label = $('#edit_label_right_freeradius').val().trim();
		var vendorname = $('#edit_vendor_right_freeradius').val();
		var radiusname = $('#edit_radiusname_right_freeradius').val();
		var previous_label = $('#edit_previous_label_right_freeradius').val();
		var previous_vendorname = $('#edit_previous_vendor_right_freeradius').val();
		var previous_radiusname = $('#edit_previous_radiusname_right_freeradius').val();

		var uid = $('#uid_edit_freeradius').val();
		var tab_flag = getTabVendorFlag($('#modal_edit_right_freeradius .modal-dialog .modal-content .modal-body .row .list_vendor_flag_freeradius'));

		var input_errno = false
		input_errno = check_input_form(radiusname.toLowerCase(), vendorname.toLowerCase(), label.toLowerCase(), tab_flag, previous_radiusname.toLowerCase(), previous_vendorname.toLowerCase(), previous_label.toLowerCase())

		if (input_errno == false)
		{
			$('#edit_alert_input').hide();

			var d_data = {'radiusname': radiusname, 'collection': 'vendor_freeradius', 'action_type': 'edit_vendor_right', 'vendorname': vendorname, 'uid': uid, 'l_flag': JSON.stringify(tab_flag), 'label': label};

			console.log(d_data);

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