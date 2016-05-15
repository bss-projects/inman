$(function()
{

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

	$( '#add_user_freeradius' ).click(function() {
		var radiusname = $('#radiusname_user_freeradius').val();
		var username = $('#name_user_freeradius').val();
		var isldap = $('#im_user_local_freeradius').is(':checked');
		var password = $('#password_user_freeradius').val();
		var right = $('#right_user_freeradius').val();

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_user_freeradius/new",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'radiusname': radiusname, 'username': username, 'isldap': isldap, 'password': password, 'right': right},
			async: false,
			success: function(data)
			{
				location.reload(true);
				var collection_info = [{'collection': 'users_freeradius', 'json_field': 'user', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
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
								page_limit: 10
								};
						},
						results: function (data, page) {
							return {results: data.results};
						}
					}
				});
				$('#edit_right_user_freeradius').select2('data', {'id': right, 'text': right});

				$('#edit_name_user_freeradius').val(username);
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
					}
				});

				$('#modal_edit_user_freeradius').modal('show');
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

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/users_freeradius/user/all",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
			{ "data": "utilisateur" },
			{ "data": "droit" },
			{ "data": "connexion" },
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
		var username = $('#edit_name_user_freeradius').val();
		var isldap = $('#im_edit_user_local_freeradius').is(':checked');
		var password = $('#edit_password_user_freeradius').val();
		var right = $('#edit_right_user_freeradius').val();
		var uid = $('#uid_edit_freeradius').val();


		var d_data = {'radiusname': radiusname, 'collection': 'user_freeradius', 'action_type': 'delete_user', 'username': username, 'uid': uid, 'isldap': isldap, 'right': right, 'password': password};

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
				var collection_info = [{'collection': 'users_freeradius', 'json_field': 'user', 'json_key': 'radiusname'}]
				launchSync(radiusname, JSON.stringify(collection_info), 'freeradius');
			}
		});
	});

});
