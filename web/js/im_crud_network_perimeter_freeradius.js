$(function()
{

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

	function perimeterNameAlreadyInUse(radiusname, network_perimetername)
	{
		var flag_return = false;

		$.ajax({
			url: "http://"+urlMaster+"/im_get_network_perimeter_list_freeradius",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'radiusname': radiusname},
			async: false,
			success: function(data)
			{
				for (var i = data['results'].length - 1; i >= 0; i--)
				{
					if (data['results'][i][0]['perimeter'] == network_perimetername)
					{
						flag_return =  true;
					}
				}
			},
			error: function(data)
			{
				console.log(data);
				flag_return =  true;
			}
		});

		return flag_return;
	}

	function compareArrays(arr1, arr2)
	{
		return $(arr1).not(arr2).length == 0 && $(arr2).not(arr1).length == 0
	};

	function perimeterIPAlreadyInUse(radiusname, first_ip, last_ip, ip_list, first_previous_ip, last_previous_ip, ip_previous_list)
	{
		var flag_return = false;

		if (first_previous_ip != null && last_previous_ip != null && first_previous_ip == first_ip && last_previous_ip == last_ip)
		{
			return flag_return;
		}

		if (ip_list != null && ip_previous_list != null && compareArrays(ip_list, ip_previous_list))
		{
			return flag_return;	
		}

		$.ajax({
			url: "http://"+urlMaster+"/im_get_network_perimeter_list_freeradius",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'radiusname': radiusname},
			async: false,
			success: function(data)
			{
				if (ip_list == null)
				{
					for (var i = data['results'].length - 1; i >= 0; i--)
					{
						if (data['results'][i][0]['first_ip'] == first_ip && data['results'][i][0]['last_ip'] == last_ip)
						{
							flag_return =  true;
						}
					}	
				}
				else
				{
					for (var i = data['results'].length - 1; i >= 0; i--)
					{
						if (compareArrays(ip_list, data['results'][i][0]['ip_list']))
						{
							flag_return =  true
						}
					}
				}
				
			},
			error: function(data)
			{
				console.log(data);
				flag_return =  true;
			}
		});

		return flag_return;
	}

	function perimeterLabelIsOK(radiusname, network_perimetername, network_perimeter_previousname)
	{
		if (network_perimetername != '')
		{
			if (perimeterNameAlreadyInUse(radiusname, network_perimetername) == false)
			{
				return true;	
			}
			else if (network_perimeter_previousname != null && network_perimetername == network_perimeter_previousname)
			{
				return true;
			}
			else
			{
				return 'Label already in use. Choose another one';
			}
		}
		else
		{
			return 'Label for perimeter name is missing';
		}
	}

	function ValidateIPaddress(ipaddress) 
	{
		if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress))
		{
			return (true);
		}
	
		return (false);
	}

	function IP2num(dot) 
	{
		var d = dot.split('.');
		return ((((((+d[0])*256)+(+d[1]))*256)+(+d[2]))*256)+(+d[3]);
	}

	function IPIsOK(radiusname, first_ip, last_ip, ip_list, first_previous_ip, last_previous_ip, ip_previous_list)
	{

		if (first_ip != null && first_ip == '')
		{
			return 'First IP is missing';
		}
		if (last_ip != null && last_ip == '')
		{
			return 'Last IP is missing';
		}

		if (first_ip != null && ValidateIPaddress(first_ip) == false)
		{
			return 'Problem on First IP format';
		}
		if (last_ip != null && ValidateIPaddress(last_ip) == false)
		{
			return 'Problem on Last IP format';
		}

		if (last_ip != null && first_ip != null && IP2num(first_ip) >= IP2num(last_ip))
		{
			return 'Problem in order First and Last IP'
		}

		if (ip_list != null && ip_list == '')
		{
			return 'IP is missing in IP List';
		}
		else if (ip_list != null && ip_list != '')
		{
			for (var i = ip_list.length - 1; i >= 0; i--)
			{
				if (ValidateIPaddress(ip_list[i]) == false)
				{
					return 'Problem on IP '+ip_list[i]+' format in IP List';
				}			
			}
		}

		if (perimeterIPAlreadyInUse(radiusname, first_ip, last_ip, ip_list, first_previous_ip, last_previous_ip, ip_previous_list) == true)
		{
			return 'Same IP already define in other perimeter';
		}

		return true;

	}

	function check_input_form(radiusname, network_perimetername, network_perimeter_previousname, first_ip, last_ip, ip_list, first_previous_ip, last_previous_ip, ip_previous_list)
	{
		var flag_input_error = false;
		var ret = '';
		var errno = new Array();

		if ((ret = radiusnameIsOK(radiusname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = perimeterLabelIsOK(radiusname, network_perimetername, network_perimeter_previousname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = IPIsOK(radiusname, first_ip, last_ip, ip_list, first_previous_ip, last_previous_ip, ip_previous_list)) != true)
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

	$('#im_add_subnet_network_perimeter_freeradius').click(function(){
		var radiusname = $('#radiusname_network_perimeter_freeradius').val();
		var network_perimetername = $('#label_subnet_network_perimeter_freeradius').val().trim();
		var first_ip = $('#ip_start_network_perimeter_freeradius').val().trim();
		var last_ip = $('#ip_end_network_perimeter_freeradius').val().trim();

		var input_errno = false
		input_errno = check_input_form(radiusname, network_perimetername, null, first_ip, last_ip, null, null, null, null);

		if (input_errno == false)
		{
			$('#alert_input').hide();

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_network_perimeter_freeradius/new",
				contentType: 'application/json; charset=utf-8',
				dataType: 'jsonp',
				data: {'radiusname': radiusname, 'label': network_perimetername, 'perimeter_type': 'subnet','first_ip': first_ip, 'last_ip': last_ip},
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

	function getListIdUserImpact(id_impact_list)
	{
		var l_id = new Array();

		id_impact_list.children().each(function(){
			l_id.push($( this ).val() );
		});

		return l_id;
	};

	function splitIP(ip)
	{
		var l_ip = new Array();

		l_ip = ip.split(" - ");

		return l_ip;
	};

	function getTabIPList(tab)
	{

		var ip_list = new Array();

		tab.find('tr').each(function (){
			ip = $(this).children('td:first').html();
			ip_list.push(ip);
		});

		return ip_list;
	};

	$('#im_add_listip_network_perimeter_freeradius').click(function(){
		var radiusname = $('#radiusname_network_perimeter_freeradius').val();
		var network_perimetername = $('#label_listip_network_perimeter_freeradius').val().trim();
		var ip_list = getTabIPList($("#tab_list_ip_perimeter_freeradius > tbody"));

		var input_errno = false
		input_errno = check_input_form(radiusname, network_perimetername, null, null, null, ip_list, null, null, null);

		if (input_errno == false)
		{
			$('#alert_input').hide();

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_network_perimeter_freeradius/new",
				contentType: 'application/json; charset=utf-8',
				dataType: 'jsonp',
				data: {'radiusname': radiusname, 'label': network_perimetername, 'perimeter_type': 'ip_list','ip_list': JSON.stringify(ip_list)},
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

	$("#radiusname_network_perimeter_freeradius").select2({
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

	$("#selectip_network_perimeter_freeradius").select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_client_freeradius",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					radiusname: $("#radiusname_network_perimeter_freeradius").val(),
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#selectip_network_perimeter_freeradius").on("select2-selecting",function (e) {
		$("#tab_list_ip_perimeter_freeradius > tbody:last").append('<tr> \
														<td>'+e['val']+'</td> \
														<td><i class="fa fa-times-circle-o fa-fw delete_ip_from_perimeter_freeradius clickable"></i></td>\
													</tr>'); 													

		$(".delete_ip_from_perimeter_freeradius").each(function () {
			$(this).unbind();
			$(this).click(function () {
				$(this).parent().parent().remove();
			});
		});
	});

	$('#dataTables-network_perimeter_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_network_perimeter').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('#edit_alert_input').hide();

				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var network_perimetername = $( this ).closest('tr').children().eq(1).text();
				var type = $( this ).closest('tr').children().eq(2).text();
				var ip = $( this ).closest('tr').children().eq(3).text();
				var uid = $( this ).parent().children('.uid').eq(0).val();
				$('#ip_network_perimeter_edit_freeradius').val($( this ).closest('tr').children().eq(3).text());

				var id_network_perimeter = uid;

				$.ajax({
					url: "http://"+urlMaster+"/im_list_user_for_network_perimeter_freeradius",
					contentType: 'application/json; charset=utf-8',
					dataType: 'jsonp',
					data: {'radiusname': radiusname, 'id_network_perimeter': id_network_perimeter},
					async: false,
					success: function(data)
					{	
						$('#edit_network_perimeter_id_impact_list').empty();
						for (var i = data['results'].length - 1; i >= 0; i--) 
						{
							$('#edit_network_perimeter_id_impact_list').append('<input type="hidden" value="'+data['results'][i]['id']+'">');
						}
					}
				});


				$("#edit_radiusname_network_perimeter_freeradius").select2({
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

				$('#edit_radiusname_network_perimeter_freeradius').select2('data', {'id': radiusname, 'text': radiusname});
				$('#edit_name_network_perimeter_freeradius').val(network_perimetername);
				$('#edit_name_previous_network_perimeter_freeradius').val(network_perimetername);
				$('#edit_type_network_perimeter_freeradius').val(type);
				$('#uid_edit_freeradius').val(uid);
				
				var d_data = {'radiusname': radiusname, 'collection': 'network_perimeter_freeradius', 'action_type': 'edit_network_perimeter', 'network_perimetertoedit': network_perimetername, 'uid': uid};

				if (type == 'subnet')
				{
					$("#edit_subnet_div").show();
					$("#edit_ip_list_div").hide();
					
					var l_ip = splitIP(ip);
					$('#edit_ip_start_network_perimeter_freeradius').val(l_ip[0]);
					$('#edit_ip_end_network_perimeter_freeradius').val(l_ip[1]);

					$('#edit_ip_start_previous_network_perimeter_freeradius').val(l_ip[0]);
					$('#edit_ip_end_previous_network_perimeter_freeradius').val(l_ip[1]);
				}
				else //for IP List edit
				{
					$("#edit_subnet_div").hide();
					$("#edit_ip_list_div").show();
					$.ajax({
						url: "http://"+urlMaster+"/im_get_network_perimeter_Toedit_freeradius",
						dataType: 'jsonp',
						async: false,
						data: d_data,
						success: function(data)
						{
							$("#edit_list_ip_previous_perimeter_freeradius").val(data['ip_list']);

							$("#edit_tab_list_ip_perimeter_freeradius > tbody").empty();
							$("#edit_tab_list_ip_perimeter_freeradius > tbody:last").append(data['data']);

							$('.delete_ip_from_perimeter_freeradius').unbind();
							$('.delete_ip_from_perimeter_freeradius').click(function(){
								$( this ).parent().parent().remove();
							});

							$("#edit_selectip_network_perimeter_freeradius").unbind();
							$("#edit_selectip_network_perimeter_freeradius").select2({
								ajax: {
									url: "http://"+urlMaster+"/im_list_client_freeradius",
									dataType: 'jsonp',
									data: function (term, page) {
										return {
											q: term, // search term
											radiusname: $("#edit_radiusname_network_perimeter_freeradius").val(),
											page_limit: 10
											};
									},
									results: function (data, page) {
										return {results: data.results};
									}
								}
							});

							$("#edit_selectip_network_perimeter_freeradius").on("select2-selecting",function (e) {
								$("#edit_tab_list_ip_perimeter_freeradius > tbody:last").append('<tr> \
																				<td>'+e['val']+'</td> \
																				<td><i class="fa fa-times-circle-o fa-fw delete_ip_from_perimeter_freeradius clickable"></i></td>\
																			</tr>'); 													

								$(".delete_ip_from_perimeter_freeradius").each(function () {
									$(this).unbind();
									$(this).click(function () {
										$(this).parent().parent().remove();
									});
								});
							});

							
						}
					});
				}
				$('#modal_edit_network_perimeter_freeradius').modal('show');
			});

		$('.btn_delete_network_perimeter').each(function( index ) {
			$( this ).tooltip();
			if (!('click' in $._data( $( this )[0], 'events' ))) 
			{
				$( this ).click(function() {
					$('.network_perimeter_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
					$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
					$('.network_perimeter_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
					$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());
					$('.uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());
					$('#ip_network_perimeter_remove_freeradius').val($( this ).closest('tr').children().eq(3).text());

					var radiusname = $('.radiusname_remove_freeradius').val();
					var id_network_perimeter = $('.uid_remove_freeradius').val();

					$('#remove_network_perimeter_impact_list').empty();
					$('#remove_network_perimeter_impact_list').append("Nothing </br>");

					$.ajax({
						url: "http://"+urlMaster+"/im_list_user_for_network_perimeter_freeradius",
						contentType: 'application/json; charset=utf-8',
						dataType: 'jsonp',
						data: {'radiusname': radiusname, 'id_network_perimeter': id_network_perimeter},
						async: false,
						success: function(data)
						{	
							if (data['results'] != null)
							{
								$('#remove_network_perimeter_impact_list').empty();
								$('#remove_network_perimeter_id_impact_list').empty();
								for (var i = data['results'].length - 1; i >= 0; i--) 
								{
									$('#remove_network_perimeter_impact_list').append(data['results'][i]['username']+"</br>");
									$('#remove_network_perimeter_id_impact_list').append('<input type="hidden" value="'+data['results'][i]['id']+'">');
								}
							}
						}
					});

					$('#modal_delete_network_perimeter_freeradius').modal('show');
				});
			}
		});

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/network_perimeter_freeradius/network_perimeter/",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
			{ "data": "perimetre" },
			{ "data": "type" },
			{ "data": "ip" },
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
		var network_perimetername = $('#network_perimeter_remove_freeradius').val();
		var radiusname = $('#radiusname_remove_freeradius').val();
		var type = $('#type_network_perimeter_remove_freeradius').val();
		var uid = $('#uid_remove_freeradius').val();
		var l_user_id_impact = getListIdUserImpact($('#remove_network_perimeter_id_impact_list'));
		var ip = $('#ip_network_perimeter_remove_freeradius').val();

		console.log(l_user_id_impact);
		
		var d_data = {'radiusname': radiusname, 'collection': 'network_perimeter_freeradius', 'action_type': 'delete_network_perimeter', 'label': network_perimetername, 'perimeter_type': type, 'uid': uid, 'list_user_id_impact': JSON.stringify(l_user_id_impact), 'ip': ip};

		$.ajax({
			url: "http://"+urlMaster+"/im_impact_network_perimeter_on_user/delete",
			dataType: 'jsonp',
			async: true,
			data: d_data,
			success: function(data)
			{
				console.log('im_impact_network_perimeter_on_user DELETE');
			}
		});

//		var d_data = {'radiusname': radiusname, 'collection': 'network_perimeter_freeradius', 'action_type': 'delete_network_perimeter', 'label': network_perimetername, 'perimeter_type': type, 'uid': uid};


		$.ajax({
			url: "http://"+urlMaster+"/im_crud_network_perimeter_freeradius/delete",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_delete_network_perimeter_freeradius').modal('hide');
				var table = $('#dataTables-network_perimeter_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'users_freeradius', 'json_field': 'user', 'json_key': 'radiusname'}, {'collection': 'network_perimeter_freeradius', 'json_field': 'network_perimeter', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});

	});

	$( '#proceed_edit' ).click(function() {
		var network_perimetername = $('#edit_name_network_perimeter_freeradius').val().trim();
		var network_perimeter_previousname = $('#edit_name_previous_network_perimeter_freeradius').val();
		var radiusname = $('#edit_radiusname_network_perimeter_freeradius').val();
		var uid = $('#uid_edit_freeradius').val();
		var type = $('#edit_type_network_perimeter_freeradius').val();

		var l_user_id_impact = getListIdUserImpact($('#edit_network_perimeter_id_impact_list'));
		var ip = $('#ip_network_perimeter_edit_freeradius').val();

		var input_errno = false
		if (type == 'subnet')
		{
			var first_ip = $('#edit_ip_start_network_perimeter_freeradius').val().trim();
			var last_ip = $('#edit_ip_end_network_perimeter_freeradius').val().trim();

			var first_previous_ip = $('#edit_ip_start_previous_network_perimeter_freeradius').val();
			var last_previous_ip = $('#edit_ip_end_previous_network_perimeter_freeradius').val();

			input_errno = check_input_form(radiusname, network_perimetername, network_perimeter_previousname, first_ip, last_ip, null, first_previous_ip, last_previous_ip, null);
		}
		else
		{
			var ip_list = getTabIPList($("#edit_tab_list_ip_perimeter_freeradius > tbody"));

			var ip_previous_list = $("#edit_list_ip_previous_perimeter_freeradius").val().split(',');

			input_errno = check_input_form(radiusname, network_perimetername, network_perimeter_previousname, null, null, ip_list, null, null, ip_previous_list);
		}
		
		
		if (input_errno == false)
		{
			$('#edit_alert_input').hide();

			var d_data = {'radiusname': radiusname, 'collection': 'network_perimeter_freeradius', 'action_type': 'edit_network_perimeter', 'label': network_perimetername, 'perimeter_type': type, 'uid': uid, 'list_user_id_impact': JSON.stringify(l_user_id_impact), 'ip': ip};

			$.ajax({
				url: "http://"+urlMaster+"/im_impact_network_perimeter_on_user/edit",
				dataType: 'jsonp',
				async: true,
				data: d_data,
				success: function(data)
				{
					console.log('im_impact_network_perimeter_on_user EDIT');
				}
			});

			if (type == 'subnet')
			{
//				var first_ip = $('#edit_ip_start_network_perimeter_freeradius').val().trim();
//				var last_ip = $('#edit_ip_end_network_perimeter_freeradius').val().trim();

				var d_data = {'radiusname': radiusname, 'collection': 'network_perimeter_freeradius', 'action_type': 'edit_network_perimeter', 'uid': uid, 'label': network_perimetername, 'perimeter_type': 'subnet', 'first_ip': first_ip, 'last_ip': last_ip}
			}
			else
			{
//				var ip_list = getTabIPList($("#edit_tab_list_ip_perimeter_freeradius > tbody"));

				var d_data = {'radiusname': radiusname, 'collection': 'network_perimeter_freeradius', 'action_type': 'edit_network_perimeter', 'uid': uid, 'label': network_perimetername, 'perimeter_type': 'ip_list', 'ip_list': JSON.stringify(ip_list)}
			}

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_network_perimeter_freeradius/edit",
				dataType: 'jsonp',
				async: false,
				data: d_data,
				success: function(data)
				{
					console.log('success');
					$('#modal_edit_network_perimeter_freeradius').modal('hide');
					var table = $('#dataTables-network_perimeter_list_freeradius').dataTable().api();
					table.ajax.reload();
					var collection_info = [{'collection': 'users_freeradius', 'json_field': 'user', 'json_key': 'radiusname'}, {'collection': 'network_perimeter_freeradius', 'json_field': 'network_perimeter', 'json_key': 'radiusname'}]
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