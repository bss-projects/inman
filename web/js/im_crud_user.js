$(function()
{

	$('#plugin_user').select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_plugin",
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

function onselect2_select(select2_elem, dest_tab)
{
	$(select2_elem).unbind();
	$(select2_elem).on('select2-selecting', function(e){
		var plugin_name = e.val;

		console.log(dest_tab);

		$(dest_tab+' > tbody:last').append('<tr> \
														<td> \
															<div class="info_frame info_frame-dismissable" class="col-sm-12"> \
																<h4>'+plugin_name+'</h4> \
																<button class="close" aria-hidden="true"type="button" data-dismiss="alert">×</button> \
																<div class="form-group"> \
																	<label for="agent_user" class="col-sm-3 control-label">Agent</label> \
																	<div class="col-sm-8"> \
																		<input class="plugin_name" type="hidden" value="'+plugin_name+'"> \
																		<input type="agent_user" class="form-control agent_user" id="agent_user" name="agent_user" placeholder="Agent"> \
																	</div> \
																</div> \
															</div> \
														</td> \
													</tr>');

		$(".agent_user").each(function(index, e){
			plugin_name = $(this).parent().children('.plugin_name').val();

			var pre_selectval = $(this).val();
			var ret_pre_selectval = new Array();

			$(this).select2({
				multiple: true,
				ajax: {
					url: "http://"+urlMaster+"/im_getlistagent/"+plugin_name,
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

			if (pre_selectval)
			{
				pre_selectval = pre_selectval.split(',');
				for (i = 0; i < pre_selectval.length; i++)
				{
					ret_pre_selectval[i] = {'id': pre_selectval[i], 'text': pre_selectval[i]}
				};

				$(this).select2('data', ret_pre_selectval);
			};

		});
	});

};

	function getTabPluginRights(tab) {
		var tab_rights = new Array();

		tab.each(function(){
			var plugin_name = $( this ).find('h4').eq(0).text();
			var list_agent = new Array();

			if (plugin_name) {
				var agents = $( this ).find('.agent_user').eq(1).val().split(',');
				var right = new Object();
				right['agent'] = agents;
				right['plugin_name'] = plugin_name;
				tab_rights.push(right);
			};

		});

		return tab_rights;
	}

	onselect2_select('#plugin_user', '#tab_plugin_right');

	$( '#add_user' ).click(function() {
		var login = $('#login_user').val();
		var password = $('#password_user').val();
		var firstname = $('#firstname_user').val();
		var lastname = $('#lastname_user').val();

		var rights = getTabPluginRights($('#tab_plugin_right td'));

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_user/new",
			contentType: 'application/json; charset=utf-8',
			dataType: 'jsonp',
			data: {'login': login, 'password': password, 'firstname': firstname, 'lastname': lastname, 'rights': JSON.stringify(rights)},
			async: false,
			success: function(data)
			{
				location.reload(true);
			}
		});
	});

	$('#filterlevelview').bootstrapSwitch({
		onText: 'Simple',
		offText: 'Complet',
		size: 'small'
	});

	$('#dataTables-user_list').on('draw.dt', function () {
		$('.btn_edit').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {

				var login = $( this ).closest('tr').children().eq(0).text();
				var firstname = $( this ).closest('tr').children().eq(1).text();
				var lastname = $( this ).closest('tr').children().eq(2).text()
				var plugin = $( this ).closest('tr').children().eq(3).text()
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_plugin_user").select2({
					ajax: {
						url: "http://"+urlMaster+"/im_list_plugin",
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

				onselect2_select('#edit_plugin_user', '#edit_tab_plugin_right');

				$('#edit_login_user').val(login);
				$('#edit_firstname_user').val(firstname);
				$('#edit_lastname_user').val(lastname);
				$('#uid_edit').val(uid);

				var d_data = {'collection': 'users', 'action_type': 'edit_user', 'login': login, 'uid': uid};

				$.ajax({
						url: "http://"+urlMaster+"/im_get_user_Toedit",
						dataType: 'jsonp',
						async: false,
						data: d_data,
						success: function(data)
						{
							if (data['data'] == '')
							{
								data['data'] = '<tbody><tr><td></td></tr></tbody>';
							};


							$('#modal_edit_user .modal-dialog .modal-content .modal-body .form-horizontal #edit_tab_plugin_right').empty()
							$('#modal_edit_user .modal-dialog .modal-content .modal-body .form-horizontal #edit_tab_plugin_right').append(data['data']);

							$(".agent_user").each(function(index, e){
								plugin_name = $(this).parent().children('.plugin_name').val();

								var pre_selectval = $(this).val();
								var ret_pre_selectval = new Array();

								$(this).select2({
									multiple: true,
									ajax: {
											url: "http://"+urlMaster+"/im_getlistagent/"+plugin_name,
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

								if (pre_selectval)
								{
									pre_selectval = pre_selectval.split(',');
									for (i = 0; i < pre_selectval.length; i++)
									{
										ret_pre_selectval[i] = {'id': pre_selectval[i], 'text': pre_selectval[i]}
									};
					
									$(this).select2('data', ret_pre_selectval);
								};
					
							});
						}
				});

				$('#modal_edit_user').modal('show');
			});

		$('.btn_delete').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.user_remove').html($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove').html($( this ).closest('tr').children().eq(0).text());
				$('.user_remove').val($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove').val($( this ).closest('tr').children().eq(0).text());

				$('#uid_remove').val($( this ).parent().children('.uid').eq(0).val());

				$('#modal_delete_user').modal('show');
			});
		});

	});}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlist_user",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "login" },
			{ "data": "prenom" },
			{ "data": "nom" },
			{ "data": "plugin" },
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
		var login = $('#user_remove').val();
		var uid = $('#uid_remove').val();

		var d_data = {'collection': 'users', 'action_type': 'delete_user', 'login': login, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_user/delete",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_delete_user').modal('hide');
				var table = $('#dataTables-user_list').dataTable().api();
				table.ajax.reload();
			}
		});
	});

	$( '#proceed_edit' ).click(function() {
		var login = $('#edit_login_user').val();
		var password = $('#edit_password_user').val();
		var firstname = $('#edit_firstname_user').val();
		var lastname = $('#edit_lastname_user').val();
		var uid = $('#uid_edit').val();

		var rights = getTabPluginRights($('#edit_tab_plugin_right td'));

		var d_data = {'collection': 'user', 'action_type': 'edit_user', 'uid': uid, 'password': password, 'login': login, 'firstname': firstname, 'lastname': lastname, 'rights': JSON.stringify(rights)};

		$.ajax({
			url: "http://"+urlMaster+"/im_crud_user/edit",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				$('#modal_edit_user').modal('hide');
				var table = $('#dataTables-user_list').dataTable().api();
				table.ajax.reload();
			}
		});
	});

});
