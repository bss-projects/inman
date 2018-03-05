$(function()
{
	var l_user = new Array();

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

	function dateIsOK(date)
	{

		split_date = date.split('/');
		date_iso_format = split_date[2]+'-'+split_date[1]+'-'+split_date[0];

		expiration_date_input = Date.parse(date_iso_format);
		expiration_date_input = expiration_date_input - Date.now();

		if (expiration_date_input > 0)
		{
			return true;
		}
		else
		{
			return 'Invalid expiration date';
		}
	}

	function usernameIsOK(radiusname, username, previous_radiusname, username_previousname)
	{
		if (username != '')
		{
			if (username_previousname && radiusname+'-'+username == previous_radiusname+'-'+username_previousname)
			{
				return true;
			}

			if (! /^[a-z0-9_-]+$/i.test(username))
			{
				return 'Name format incorrect. Use only alphanum and "-" or "_"';
			}

			if (l_user.includes(radiusname+'-'+username))
			{
				return 'Username already in use';
			}

			return true;
		}
		else
		{
			return 'Name is missing for user';
		}
	}

	function passwordIsOK(password, isldap)
	{

		if (isldap)
		{
			return true;
		}

		if (password != '')
		{
			if (! /^[a-z0-9!"#$%&'()*+,.\/:;<=>?@\[\] ^_`{|}~-]*$/i.test(password))
			{
				return 'Password format incorrect. Use only a-z0-9!"#$%&\'()*+,./:;<=>?@[] ^_`{|}~-';
			}

			return true;
		}
		else
		{
			return 'Password is missing for user';
		}
	}

	function check_input_form(radiusname, username, password, date, right, isldap, previous_radiusname, username_previousname)
	{
		var flag_input_error = false;
		var ret = '';
		var errno = new Array();

		if ((ret = radiusnameIsOK(radiusname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = usernameIsOK(radiusname, username, previous_radiusname, username_previousname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = passwordIsOK(password, isldap)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = dateIsOK(date)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if (!right)
		{
			flag_input_error = true;
			errno.push('No right selected')
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

	function search_n_select_network_perimeter(perimeter_user_input, radiusname_input, perimeter_select_overlay, tab_list_perimeter)
	{
		$(perimeter_user_input).keyup(function(){
			if ($(radiusname_input).val())
			{
			
				var radiusname = $(radiusname_input).val();
				var perimeter_user_freeradius = $(perimeter_user_input).val().trim();

				if (perimeter_user_freeradius == '')
				{
					$(perimeter_select_overlay).hide();
					$(perimeter_select_overlay+"> ul").empty();
				}
				else
				{
					$.ajax({
						url: "http://"+urlMaster+"/im_list_network_perimeter_freeradius",
						contentType: 'application/json; charset=utf-8',
						dataType: 'jsonp',
						data: {'radiusname': radiusname, 'plugin': 'freeradius', 'collection_info': 'network_perimeter_freeradius', 'q': perimeter_user_freeradius},
						async: false,
						success: function(data)
						{
							console.log('Success sync');
							$(perimeter_select_overlay+" > ul").empty();
							var class_even_odd = 'even'
							for (var i = 0; i < data.results.length; i++) {
								if (class_even_odd == 'odd')
								{
									class_even_odd = 'even';
								}
								else
								{
									class_even_odd = 'odd';
								}
								$(perimeter_select_overlay+"> ul:last").append('<li class="clickable select_perimeter_user_freeradius '+class_even_odd+'">'+data.results[i]['text']+'\
																					</li>\
																					<input class="select_perimeter_uid_user_freeradius" type="hidden" value="'+data.results[i]['id']+'">');
							}
							$('.select_perimeter_user_freeradius').each(function(){
								$(this).click(function(){

									$(tab_list_perimeter+" > tbody:last").append('<tr> \
																					<td>'+$(this).text()+'</td> \
																					<td><i class="fa fa-times-circle-o fa-fw delete_perimeter_user_freeradius clickable"></i></td>\
																					<input class="selected_perimeter_uid_user_freeradius" type="hidden" value="'+$(this).next().val()+'">\
																				</tr>');

									$(perimeter_select_overlay).hide();
									$(perimeter_select_overlay+"> ul").empty();
									$(perimeter_user_input).val('');

									$(".delete_perimeter_user_freeradius").each(function () {
										$(this).unbind();
										$(this).click(function () {
											$(this).parent().parent().remove();
										});
									});

								});
							});
							$(perimeter_select_overlay).show();
						},
						error: function(data)
						{
							console.log('Error sync');
						}
					});
				}
			}
		});
	}

	search_n_select_network_perimeter("#perimeter_user_freeradius", '#radiusname_user_freeradius', '#perimeter_select_freeradius', '#tab_list_perimeter_user_freeradius');

	search_n_select_network_perimeter("#edit_perimeter_user_freeradius", '#edit_radiusname_user_freeradius', '#edit_perimeter_select_freeradius', '#edit_tab_list_perimeter_user_freeradius');

	$("#radiusname_user_freeradius").select2({
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

	$("#right_user_freeradius").select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_right_freeradius",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					radiusname: $("#radiusname_user_freeradius").val(),
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	var timestamp_next_year = $.now() + 31540000000;
	var dt = new Date(timestamp_next_year);
	var day = dt.getDate();
	var month = dt.getMonth() + 1;
	var year = dt.getFullYear();

	if (day < 10)
	{
		day = '0' + day;
	}

	if (month < 10)
	{
		month = '0' + month;
	}

	var next_year_expire_date = day + "/" + month + "/" + year;

	$('#expiration_date_user_freeradius').inputmask('99/99/9999',{ 'placeholder': 'dd/mm/yyyy' });

	$('#expiration_date_user_freeradius').val(next_year_expire_date);

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

	function getTabPerimeterList(tab)
	{

		var perimeter_list = new Array();
		var perimeter_name = '';
		var perimeter_id = 0;

		tab.find('tr').each(function (){
			perimeter_name = $(this).children('td:first').text();
			perimeter_id = parseInt($(this).children('input').val());

			if (perimeter_id)
			{
				perimeter_list.push({'perimeter_name': perimeter_name.trim(), 'uid': perimeter_id});
			}
		});

		return perimeter_list;
	};

	$( '#add_user_freeradius' ).click(function() {
		var radiusname = $('#radiusname_user_freeradius').val();
		var username = $('#name_user_freeradius').val().trim();
		var isldap = $('#im_user_local_freeradius').is(':checked');
		var password = $('#password_user_freeradius').val().trim();
		var expiration_date = $('#expiration_date_user_freeradius').val();
		var expiration_status = 'ok';
		var right = $('#right_user_freeradius').val();
		var perimeter_list = getTabPerimeterList($("#tab_list_perimeter_user_freeradius"));

		var input_errno = false
		input_errno = check_input_form(radiusname.toLowerCase(), username.toLowerCase(), password, expiration_date, right, isldap, null, null);

		if (input_errno == false)
		{
			$('#alert_input').hide();

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_user_freeradius/new",
				contentType: 'application/json; charset=utf-8',
				dataType: 'jsonp',
				data: {'radiusname': radiusname, 'username': username, 'isldap': isldap, 'password': password, 'right': right, 'perimeter_list': JSON.stringify(perimeter_list), 'expiration_date': expiration_date, 'expiration_status': expiration_status},
				async: false,
				success: function(data)
				{
					location.reload(true);
					var collection_info = [{'collection': 'users_freeradius', 'json_field': 'user', 'json_key': 'radiusname'}, {'collection': 'network_perimeter_freeradius', 'json_field': 'network_perimeter', 'json_key': 'radiusname'}]
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

	$('#im_user_local_freeradius').bootstrapSwitch({
			onText: 'Oui',
			offText: 'Non',
			labelText: 'Utilisateur LDAP',
			size: 'normal'
	});

	$('#im_user_local_freeradius').on('switchChange.bootstrapSwitch', function(event, state) {
		if (state == false)
		{
			$("#div_password_user_freeradius").show();
		};
		if (state == true)
		{
			$("#div_password_user_freeradius").hide();
		};
	});

	$('#im_edit_user_local_freeradius').bootstrapSwitch({
			onText: 'Oui',
			offText: 'Non',
			labelText: 'Utilisateur LDAP',
			size: 'normal'
	});

	$('#im_edit_user_local_freeradius').on('switchChange.bootstrapSwitch', function(event, state) {
		if (state == false)
		{
			$("#div_edit_password_user_freeradius").show();
		};
		if (state == true)
		{
			$("#div_edit_password_user_freeradius").hide();
		};
	});

	$('#im_model_user_local_freeradius').bootstrapSwitch({
			onText: 'Oui',
			offText: 'Non',
			labelText: 'Utilisateur LDAP',
			size: 'normal'
	});

	$('#im_model_user_local_freeradius').on('switchChange.bootstrapSwitch', function(event, state) {
		if (state == false)
		{
			$("#div_password_model_user_freeradius").show();
		};
		if (state == true)
		{
			$("#div_password_model_user_freeradius").hide();
		};
	});

	$('#filterlevelview').bootstrapSwitch({
		onText: 'Simple',
		offText: 'Complet',
		size: 'small'
	});

	$('#dataTables-user_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_user').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {

				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var username = $( this ).closest('tr').children().eq(1).text();
				var right = $( this ).closest('tr').children().eq(2).text()
				var connection_type = $( this ).closest('tr').children().eq(3).text()
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_radiusname_user_freeradius").select2({
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
				$('#edit_radiusname_user_freeradius').select2('data', {'id': radiusname, 'text': radiusname});

				$("#edit_right_user_freeradius").select2({
					ajax: {
						url: "http://"+urlMaster+"/im_list_right_freeradius",
						dataType: 'jsonp',
						data: function (term, page) {
							return {
								q: term, // search term
								radiusname: $("#edit_radiusname_user_freeradius").val(),
								page_limit: 10
								};
						},
						results: function (data, page) {
							return {results: data.results};
						}
					}
				});
				$('#edit_right_user_freeradius').select2('data', {'id': right, 'text': right});

				$('#edit_expiration_date_user_freeradius').inputmask('99/99/9999',{ 'placeholder': 'dd/mm/yyyy' });

				$('#edit_name_user_freeradius').val(username);
				$('#edit_previous_name_user_freeradius').val(username);
				$('#edit_previous_radiusname_user_freeradius').val(radiusname);
				$('#uid_edit_freeradius').val(uid);

				if (connection_type == 'LDAP')
				{
					$('#im_edit_user_local_freeradius').bootstrapSwitch('state', true);
				}
				else
				{
					$('#im_edit_user_local_freeradius').bootstrapSwitch('state', false);
				};


				var d_data = {'collection': 'users_freeradius', 'username': username, 'radiusname': radiusname, 'uid': uid, 'fields' : 'user_info'};

				$.ajax({
					url: "http://"+urlMaster+"/im_get_doc_freeradius",
					dataType: 'jsonp',
					async: false,
					data: d_data,
					success: function(data)
					{
						$('#edit_password_user_freeradius').val(data['doc']['password']);
						if (data['doc']['expiration_date'])
						{
							$('#edit_expiration_date_user_freeradius').val(data['doc']['expiration_date']);
						}
						else
						{
							$('#edit_expiration_date_user_freeradius').val('');
						}

						if (data['doc']['expiration_status'] != 'ok')
						{
							$('#edit_expiration_status').show();
						}
						else
						{
							$('#edit_expiration_status').hide();
						}

						$("#edit_tab_list_perimeter_user_freeradius > tbody").empty();
						if (data['doc']['network_perimeter'])
						{
							for (var i = data['doc']['network_perimeter'].length - 1; i >= 0; i--)
							{
								var network_perimeter_data = data['doc']['network_perimeter'][i];

								$("#edit_tab_list_perimeter_user_freeradius > tbody:last").append('<tr> \
																					<td>'+network_perimeter_data['perimeter_name']+'</td> \
																					<td><i class="fa fa-times-circle-o fa-fw delete_perimeter_user_freeradius clickable"></i></td>\
																					<input class="selected_perimeter_uid_user_freeradius" type="hidden" value="'+network_perimeter_data['uid']+'">\
																				</tr>');
							}

							$(".delete_perimeter_user_freeradius").each(function () {
									$(this).unbind();
									$(this).click(function () {
									$(this).parent().parent().remove();
								});
							});
						}
					}
				});

				$('#modal_edit_user_freeradius').modal('show');
			});
		});

		$('.btn_delete_user').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.user_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
				$('.user_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());

				$('#uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());

				$('#modal_delete_user_freeradius').modal('show');
			});
		});

	}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"createdRow": function(row, data, dataIndex){
			l_user.push(data['radius'].toLowerCase()+'-'+data['utilisateur'].toLowerCase());
		},
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/users_freeradius/user/",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
			{ "data": "utilisateur" },
			{ "data": "droit" },
			{ "data": "connexion" },
			{ "data": "statut" },
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
		var username = $('#user_remove_freeradius').val();
		var radiusname = $('#radiusname_remove_freeradius').val();
		var uid = $('#uid_remove_freeradius').val();

		var d_data = {'radiusname': radiusname, 'collection': 'user_freeradius', 'action_type': 'delete_user', 'username': username, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_user_freeradius/delete",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				var index = l_user.indexOf(radiusname.toLowerCase()+'-'+username.toLowerCase());
				if (index >= 0)
				{
					l_user.splice( index, 1 );
				}
				$('#modal_delete_user_freeradius').modal('hide');
				var table = $('#dataTables-user_list_freeradius').dataTable().api();
				table.ajax.reload();
				var collection_info = [{'collection': 'users_freeradius', 'json_field': 'user', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

	$( '#proceed_edit' ).click(function() {
		var radiusname = $('#edit_radiusname_user_freeradius').val();
		var username = $('#edit_name_user_freeradius').val().trim();
		var username_previousname = $('#edit_previous_name_user_freeradius').val();
		var previous_radiusname = $('#edit_previous_radiusname_user_freeradius').val();
		var isldap = $('#im_edit_user_local_freeradius').is(':checked');
		var password = $('#edit_password_user_freeradius').val().trim();
		var expiration_date = $('#edit_expiration_date_user_freeradius').val();
		var expiration_status = 'ok';
		var right = $('#edit_right_user_freeradius').val();
		var uid = $('#uid_edit_freeradius').val();
		var perimeter_list = getTabPerimeterList($("#edit_tab_list_perimeter_user_freeradius"));

		var input_errno = false
		input_errno = check_input_form(radiusname.toLowerCase(), username.toLowerCase(), password, expiration_date, right, isldap, previous_radiusname.toLowerCase(), username_previousname.toLowerCase());

		if (input_errno == false)
		{
			$('#edit_alert_input').hide();

			var d_data = {'radiusname': radiusname, 'collection': 'user_freeradius', 'action_type': 'edit_user', 'username': username, 'uid': uid, 'isldap': isldap, 'right': right, 'password': password, 'perimeter_list': JSON.stringify(perimeter_list), 'expiration_date': expiration_date, 'expiration_status': expiration_status};

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_user_freeradius/edit",
				dataType: 'jsonp',
				async: false,
				data: d_data,
				success: function(data)
				{
					console.log('success');
					$('#modal_edit_user_freeradius').modal('hide');
					var table = $('#dataTables-user_list_freeradius').dataTable().api();
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