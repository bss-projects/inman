$(function()
{
	var l_shared_secret_name = new Array();
	var l_shared_secret_subnet = new Array();

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

	function ipIsOK(ipaddress) 
	{
		if (! /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress))
		{
			return 'IP format incorrect';
		}

		return (true);
	}

	function sharedsecretNameIsOK(radiusname, name, previous_radiusname, previous_name) 
	{
		if (name != '')
		{
			console.log(l_shared_secret_name);

			if (previous_name && radiusname+'-'+name == previous_radiusname+'-'+previous_name)
			{
				return true;
			}

			if (l_shared_secret_name.includes(radiusname+'-'+name))
			{
				return 'Shared secret Name already in use';
			}
	
			return (true);
		}
		else
		{
			return 'Shared secret Name is missing';
		}
	}

	function sharedsecretSubnetIsOK(radiusname, subnet, previous_radiusname, previous_subnet) 
	{
		if (subnet != '')
		{
			var l_subnet = subnet.split('/');

			if (l_subnet.length > 2 || l_subnet.length <= 1)
			{
				return 'Shared secret Subnet format incorrect';
			}

			var isIpOK = ipIsOK(l_subnet[0]) 
			if (isIpOK != true)
			{
				return isIpOK;
			}

			if (parseInt(l_subnet[1]) < 0 || parseInt(l_subnet[1]) > 32 || l_subnet[1] == '')
			{
				return 'Shared secret Subnet format incorrect';
			}

			if (previous_subnet && radiusname+'-'+subnet == previous_radiusname+'-'+previous_subnet)
			{
				return true;
			}



			if (l_shared_secret_subnet.includes(radiusname+'-'+subnet))
			{
				return 'Shared secret Subnet already in use';
			}
	
			return (true);
		}
		else
		{
			return 'Shared secret Subnet is missing';
		}
	}

	function sharedsecretKeyIsOK(key) 
	{
		if (key != '')
		{
			return (true);
		}
		else
		{
			return 'Shared secret Key is missing';
		}
	}

	function stringIsOK(list_to_check)
	{
		///**
		// Faire un concat des string en erreur si la string exist alors return sinon return True
		///**
		str_errno = ''
		$.each(list_to_check, function(index, value){
			if (value != '')
			{
				if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(value))
				{
					str_errno += index+' format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~- </br>';
				}
			}
		});
		/*
		if (name != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(name))
			{
				return 'Name format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}
		}

		if (key != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(key))
			{
				return 'Key format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}
		}

		if (comment != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(comment))
			{
				return 'Comment format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}
		}
		*/
		if (str_errno != '')
		{
			return str_errno
		}
		else
		{
			return true;
		}
	}

	function check_input_form(radiusname, name, key, comment, previous_radiusname, name_previous_name)
	{
		var flag_input_error = false;
		var ret = '';
		var errno = new Array();

		if ((ret = radiusnameIsOK(radiusname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = sharedsecretNameIsOK(radiusname, name, previous_radiusname, name_previous_name)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = sharedsecretKeyIsOK(key)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}
		
		if ((ret = stringIsOK({'Name': name, 'Key': key, 'Comment': comment})) != true)
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

	function check_input_range_form(radiusname, name, key, subnet, previous_radiusname, subnet_previous_subnet)
	{
		var flag_input_error = false;
		var ret = '';
		var errno = new Array();
		console.log(l_shared_secret_subnet);

		if ((ret = radiusnameIsOK(radiusname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = sharedsecretSubnetIsOK(radiusname, subnet, previous_radiusname, subnet_previous_subnet)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = sharedsecretKeyIsOK(key)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}
		
		if ((ret = stringIsOK({'Name': name, 'Key': key})) != true)
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

	$("#radiusname_shared_secret_freeradius").select2({
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

	$.toggleShowPassword = function (options) {
		var settings = $.extend({
			field: "#password",
			control: "#toggle_show_password",
			icon: "#i"
		}, options);

		var control = $(settings.control);
		var field = $(settings.field);
		var icon = $(settings.icon);

		control.bind('click', function () {
			if (icon.hasClass('fa-eye')) {
				field.attr('type', 'text');
				icon.removeClass('fa-eye').addClass('fa-eye-slash');
			} else {
				field.attr('type', 'password');
				icon.removeClass('fa-eye-slash').addClass('fa-eye');
			}
		})
	};

	$.toggleShowPassword({
		field: '#key_shared_secret_freeradius',
		control: '#show_hide_shared_secret_freeradius',
		icon: '#icon_show_hide_shared_secret_freeradius'
	});

	$.toggleShowPassword({
		field: '#edit_key_shared_secret_freeradius',
		control: '#edit_show_hide_shared_secret_freeradius',
		icon: '#edit_icon_show_hide_shared_secret_freeradius'
	});

	$.toggleShowPassword({
		field: '#range_sharedsecret_shared_secret_freeradius',
		control: '#show_hide_range_sharedsecret_freeradius',
		icon: '#icon_show_hide_range_sharedsecret_freeradius'
	});

	$.toggleShowPassword({
		field: '#edit_range_sharedsecret_shared_secret_freeradius',
		control: '#edit_show_hide_range_sharedsecret_freeradius',
		icon: '#edit_icon_show_hide_range_sharedsecret_freeradius'
	});

	$( '#add_shared_secret_freeradius' ).click(function() {
		var radiusname = $('#radiusname_shared_secret_freeradius').val();
		var name = $('#name_shared_secret_freeradius').val().trim();
		var key = $('#key_shared_secret_freeradius').val().trim();
		var comment = $('#comment_shared_secret_freeradius').val().trim();

		var input_errno = false
		input_errno = check_input_form(radiusname, name, key, comment, null, null)

		if (input_errno == false)
		{
			$('#alert_input').hide();

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_shared_secret_freeradius/new",
				contentType: 'application/json; charset=utf-8',
				dataType: 'jsonp',
				data: {'radiusname': radiusname, 'name': name, 'key': key, 'comment': comment},
				async: false,
				success: function(data)
				{
					location.reload(true);
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

	$('#dataTables-shared_secret_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_shared_secret').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {

				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var name = $( this ).closest('tr').children().eq(1).text();
//				var key = $( this ).closest('tr').children().eq(2).text();
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_radiusname_shared_secret_freeradius").select2({
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
				$('#edit_radiusname_shared_secret_freeradius').select2('data', {'id': radiusname, 'text': radiusname});

				var d_data = {'collection': 'shared_secret_freeradius', 'radiusname': radiusname, 'uid': uid, 'fields' : 'shared_secret_info'};

				$.ajax({
					url: "http://"+urlMaster+"/im_get_doc_freeradius",
					dataType: 'jsonp',
					async: false,
					data: d_data,
					success: function(data)
					{
						$('#edit_comment_shared_secret_freeradius').val(data['doc']['comment']);
						$('#edit_key_shared_secret_freeradius').val(data['doc']['key']);
					}
				});

				$('#edit_name_shared_secret_freeradius').val(name);
//				$('#edit_key_shared_secret_freeradius').val(key);
				$('#edit_previous_name_shared_secret_freeradius').val(name);
				$('#edit_previous_radiusname_shared_secret_freeradius').val(radiusname);

				$('#uid_edit_freeradius').val(uid);

				$('#modal_edit_shared_secret_freeradius').modal('show');
			});
		});

		$('.btn_delete_shared_secret').each(function( index ) {
			$( this ).tooltip();
			if (!('click' in $._data( $( this )[0], 'events' ))) 
			{
				$( this ).click(function() {
					$('.shared_secret_name_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
					$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
					
					$('.shared_secret_name_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
					$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());

					$('#uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());

					var radiusname = $('.radiusname_remove_freeradius').val();
					var id_shared_secret = $('.uid_remove_freeradius').val();

					$('#remove_shared_secret_impact_list').empty();
					$('#remove_shared_secret_impact_list').append("Nothing </br>");

					$.ajax({
						url: "http://"+urlMaster+"/im_list_client_for_shared_secret_freeradius",
						contentType: 'application/json; charset=utf-8',
						dataType: 'jsonp',
						data: {'radiusname': radiusname, 'id_shared_secret': id_shared_secret},
						async: false,
						success: function(data)
						{	
							if (data['results'] != null)
							{
								$('#remove_shared_secret_impact_list').empty();
								$('#remove_shared_secret_id_impact_list').empty();
								for (var i = data['results'].length - 1; i >= 0; i--) 
								{
									$('#remove_shared_secret_impact_list').append(data['results'][i]['client_ip']+" - "+data['results'][i]['client_name']+"</br>");
									$('#remove_shared_secret_id_impact_list').append('<input type="hidden" value="'+data['results'][i]['id']+'">');
								}
							}
						}
					});

					$('#modal_delete_shared_secret_freeradius').modal('show');
				});
			}
		});

	}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"createdRow": function(row, data, dataIndex){
			l_shared_secret_name.push(data['radius']+'-'+data['nom']);
		},
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/shared_secret_freeradius/shared_secret/",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
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
		var name = $('#shared_secret_name_remove_freeradius').val();
		var radiusname = $('#radiusname_remove_freeradius').val();
		var uid = $('#uid_remove_freeradius').val();

		var d_data = {'radiusname': radiusname, 'collection': 'shared_secret_freeradius', 'action_type': 'delete_shared_secret', 'shared_secret_name': name, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_shared_secret_freeradius/delete",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				var index = l_shared_secret_name.indexOf(radiusname+'-'+name);
				if (index >= 0)
				{
					l_shared_secret_name.splice( index, 1 );
				}
				$('#modal_delete_shared_secret_freeradius').modal('hide');
				l_shared_secret_name = new Array();
				var table = $('#dataTables-shared_secret_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'shared_secret_freeradius', 'json_field': 'shared_secret', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit' ).click(function() {
		var radiusname = $('#edit_radiusname_shared_secret_freeradius').val();
		var name = $('#edit_name_shared_secret_freeradius').val().trim();
		var key = $('#edit_key_shared_secret_freeradius').val().trim();
		var comment = $('#edit_comment_shared_secret_freeradius').val().trim();

		var name_previous_name = $('#edit_previous_name_shared_secret_freeradius').val();
		var previous_radiusname = $('#edit_previous_radiusname_shared_secret_freeradius').val();

		var uid = $('#uid_edit_freeradius').val();

		var input_errno = false
		input_errno = check_input_form(radiusname, name, key, comment, previous_radiusname, name_previous_name);

		if (input_errno == false)
		{
			$('#edit_alert_input').hide();

			var d_data = {'collection': 'shared_secret_freeradius', 'action_type': 'edit_shared_secret', 'radiusname': radiusname, 'name': name, 'key': key, 'comment': comment, 'uid': uid};

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_shared_secret_freeradius/edit",
				dataType: 'jsonp',
				async: false,
				data: d_data,
				success: function(data)
				{
					console.log('success');
					$('#modal_edit_shared_secret_freeradius').modal('hide');
					l_shared_secret_name = new Array();
					var table = $('#dataTables-shared_secret_list_freeradius').dataTable().api();
					table.ajax.reload();
					var collection_info = [{'collection': 'shared_secret_freeradius', 'json_field': 'shared_secret', 'json_key': 'radiusname'}]
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

///
/// Manage Range
///

	$("#range_radiusname_shared_secret_freeradius").select2({
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

	$( '#add_range_shared_secret_freeradius' ).click(function() {
		var radiusname = $('#range_radiusname_shared_secret_freeradius').val();
		var rangename = $('#range_name_shared_secret_freeradius').val();
		var subnet = $('#range_subnet_shared_secret_freeradius').val();
		var sharedsecret = $('#range_sharedsecret_shared_secret_freeradius').val();

		var input_errno = false
		input_errno = check_input_range_form(radiusname, rangename, sharedsecret, subnet, null, null)

		if (input_errno == false)
		{
			$('#alert_range_input').hide();

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
		}
		else
		{
			$('#alert_range_input').empty();
			$('#alert_range_input').append('<p>Input error on following :</p>');
			for (var i = input_errno.length - 1; i >= 0; i--)
			{
				$('#alert_range_input').append('- '+input_errno[i]+'</br>');
			}
			$('#alert_range_input').show();
		}
	});


	$('#dataTables-range_shared_secret_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_range').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {

				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var rangename = $( this ).closest('tr').children().eq(1).text();
				var subnet = $( this ).closest('tr').children().eq(2).text();
//              var sharedsecret = $( this ).closest('tr').children().eq(1).text()
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_range_radiusname_shared_secret_freeradius").select2({
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
				$('#edit_range_radiusname_shared_secret_freeradius').select2('data', {'id': radiusname, 'text': radiusname});

				var d_data = {'collection': 'range_freeradius', 'rangename': rangename, 'radiusname': radiusname, 'subnet': subnet, 'uid': uid, 'fields' : 'range_info'};

				$.ajax({
					url: "http://"+urlMaster+"/im_get_doc_freeradius",
					dataType: 'jsonp',
					async: false,
					data: d_data,
					success: function(data)
					{
						$('#edit_range_sharedsecret_shared_secret_freeradius').val(data['doc']['sharedsecret']);
					}
				});

				$('#edit_range_name_shared_secret_freeradius').val(rangename);
				$('#edit_range_subnet_shared_secret_freeradius').val(subnet);

				$('#uid_edit_freeradius').val(uid);

				$('#modal_edit_range_shared_secret_freeradius').modal('show');
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

				$('#modal_delete_range_shared_secret_freeradius').modal('show');
			});
		});

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"createdRow": function(row, data, dataIndex){
			l_shared_secret_subnet.push(data['radius']+'-'+data['sous-reseau']);
		},
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/range_freeradius/range/",
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

		var d_data = {'radiusname': radiusname, 'collection': 'range_freeradius', 'action_type': 'delete_range', 'rangename': rangename, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_range_freeradius/delete",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_delete_range_shared_secret_freeradius').modal('hide');
				var table = $('#dataTables-range_shared_secret_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'range_freeradius', 'json_field': 'range', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit_range' ).click(function() {
		var rangename = $('#edit_range_name_shared_secret_freeradius').val();
		var radiusname = $('#edit_range_radiusname_shared_secret_freeradius').val();
		var subnet = $('#edit_range_subnet_shared_secret_freeradius').val();
		var sharedsecret = $('#edit_range_sharedsecret_shared_secret_freeradius').val();
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
				$('#modal_edit_range_shared_secret_freeradius').modal('hide');
				var table = $('#dataTables-range_shared_secret_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'range_freeradius', 'json_field': 'range', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});
});