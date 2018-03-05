$(function()
{
	l_vendor = new Array();

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

	function notassocIsOK(radiusname, vendorname, previous_radiusname, previous_vendorname) {
		if (radiusname != '' && vendorname != '')
		{
			if (previous_radiusname != null && previous_vendorname != null)
			{
				if (radiusname.toLowerCase()+'-'+vendorname.toLowerCase() == previous_radiusname.toLowerCase()+'-'+previous_vendorname.toLowerCase()) 
				{
					return true;
				}
			}
			if (l_vendor.includes(radiusname.toLowerCase()+'-'+vendorname.toLowerCase()))
			{
				return vendorname+' already associate to '+radiusname;
			}
		}
		return true;
	}

	function vendor_flagIsOK(tab_flag)
	{
		var errno = new Array();
		var flag_attribute_missing = true;
		var block_name = Object.keys(tab_flag);
		var nb_block = block_name.length

		console.log(block_name);

		for (var i = 0; i < nb_block; i++)
		{
			var t_list_attribute = Object.values(tab_flag[block_name[i]]);

			if (t_list_attribute.length && flag_attribute_missing == true)
			{
				flag_attribute_missing = false
			}

			for (var j = 0; j < t_list_attribute.length; j++)
			{
				if ((ret = stringIsOK(t_list_attribute[j], 'Attribute in '+block_name[i], true)) != true)
				{
					errno.push(ret+'<br/>')
				}
			}
		}

		if (!block_name.length)
		{
			return 'Vendor flag block is missing';
		}
		else if (!errno.length)
		{
			return true;
		}
		else
		{
			return errno;
		}
	}

	function check_input_form(radiusname, vendorname, tab_flag, previous_radiusname, previous_vendorname)
	{
		var flag_input_error = false;
		var ret = '';
		var errno = new Array();

		if ((ret = radiusnameIsOK(radiusname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ((ret = stringIsOK(vendorname, 'Vendor name', true)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}
		
		if ((ret = notassocIsOK(radiusname, vendorname, previous_radiusname, previous_vendorname)) != true)
		{
			flag_input_error = true;
			errno.push(ret)
		}

		if ( (ret = vendor_flagIsOK(tab_flag)) != true)
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

	$("#im_add_flag_vendor_bloc_freeradius").click(function(){

		var block_title = $('#title_flag_block_freeradius').val().trim();
		$('#alert_input').hide();

		if ((ret = stringIsOK(block_title, 'Block title ', true)) != true)
		{
			$('#alert_input').empty();
			$('#alert_input').append('<p>Input error on following :</p>');
			$('#alert_input').append('- '+ret+'</br>');
			$('#alert_input').show();
			return;
		}

		$('#tab_vendor_block_flag_freeradius > tbody:last').append('<tr> \
																		<td> \
																			<div class="info_frame info_frame-dismissable col-lg-12"> \
																				<h4>'+block_title+'</h4> \
																				<button class="close" aria-hidden="true"type="button" data-dismiss="alert">×</button> \
																				<div class="manage_flag_spec_vendor_bloc_freeradius"> \
																					<div class="list_flag_spec_vendor_bloc_freeradius"> \
																						<div class="input-group"> \
																							<div class="input-group"> \
																								<span class="input-group-addon">Attribut</span> \
																								<input class="form-control" type="text" placeholder="Nom de l\'attribut"> \
																							</div> \
																						</div> \
																					</div> \
																					<div class="link_add_flag_freeradius"> \
																						<span class="fake-link new-flag_freeradius"> \
																							<i class="fa fa-plus"></i> \
																							Ajout nouvel attribut \
																						</span> \
																					</div> \
																				</div> \
																			</div> \
																		</td> \
																	</tr>');

		$(".new-flag_freeradius").unbind();
		$(".new-flag_freeradius").click(function(){
			var list = $( this ).parent().parent().children()[0];

			list.insertAdjacentHTML('beforeEnd','<div class="input-group"> \
													<div class="input-group"> \
														<span class="input-group-addon">Attribut</span> \
														<input class="form-control" type="text" placeholder="Nom de l\'attribut"> \
													</div> \
												</div>');
		});

	});

	$("#im_add_flag_vendor_bloc").click(function(){
		var block_title = $('#title_flag_block').val().trim();
		var list_block = $( this ).parent().parent().parent().eq(0).children('.list_bloc');

		list_block.append('<div class="info_frame info_frame-dismissable col-lg-12"> \
								<h4>'+block_title+'</h4>  \
								<button class="close" aria-hidden="true" type="button" data-dismiss="alert">×</button> \
								<div class="list_flag col-lg-12"> \
								</div> \
								<div class="input-group col-lg-12"> \
									<input type="flag_name_freeradius" class="form-control flag_name" name="flag_name_freeradius" placeholder="Nom de l\'attribut"> \
									<span class="input-group-btn"> \
										<button class="btn btn-default add_flag" type="button"> \
											<i class="fa fa-plus"></i> \
											Ajout nouvel attribut \
										</button> \
									</span> \
								</div> \
							</div>');


		$('.add_flag').unbind();
		$('.add_flag').click(function(){
			var flag_name = $( this ).parent().parent().children().eq(0).val();
			var list_flag = $( this ).parent().parent().parent().eq(0).children('.list_flag');

			list_flag.append('<div class="entry_list_flag col-lg-12"> \
								<div class="col-lg-11">'+ 
									flag_name 
								+'</div> \
								<div class="col-lg-1"> \
									<i class="fa fa-trash-o fake-link remove_flag"></i> \
								</div> \
							</div>');

			$('.remove_flag').unbind();
			$('.remove_flag').click(function(){
				$( this ).parent().parent().remove();
			});
		});

	});

	$('.add_flag').click(function(){
		var flag_name = $( this ).parent().parent().children().eq(0).val();
		var list_flag = $( this ).parent().parent().parent().eq(0).children('.list_flag');

		list_flag.append('<div class="entry_list_flag col-lg-12"> \
							<div class="col-lg-11">'+ 
								flag_name 
							+'</div> \
							<div class="col-lg-1"> \
								<i class="fa fa-trash-o fake-link remove_flag"></i> \
							</div> \
						</div>');

		$('.remove_flag').unbind();
		$('.remove_flag').click(function(){
			$( this ).parent().parent().remove();
		});
	});

	$('.remove_flag').click(function(){
		$( this ).parent().parent().remove();
	});

	function getTabVendorFlag(tab) {
		var tab_flag = new Object();

		tab.each(function(){
			var block_title = $( this ).find('h4').eq(0).text();
			var list_flag = new Array();

			if (block_title) {
				$( this ).find('.list_flag_spec_vendor_bloc_freeradius').children().each(
					function(){
						var flag = $( this ).find('input').eq(0).val();
						if (flag) {
							list_flag.push(flag);
						};
					});
				tab_flag[block_title] = list_flag;
			};
		});
		return tab_flag;
	}

	$('#add_vendor_freeradius').click(function(){
		var radiusname = $('#radiusname_vendor_freeradius').val();
		var vendorname = $('#name_vendor_freeradius').val();
		var tab_flag = getTabVendorFlag($('#tab_vendor_block_flag_freeradius td'));

		var input_errno = false
		input_errno = check_input_form(radiusname, vendorname, tab_flag, null, null)

		if (input_errno == false)
		{
			$('#alert_input').hide();

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_vendor_freeradius/new",
				contentType: 'application/json; charset=utf-8',
				dataType: 'jsonp',
				data: {'radiusname': radiusname, 'vendorname': vendorname, 'l_flag': JSON.stringify(tab_flag)},
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

	$("#radiusname_vendor_freeradius").select2({
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

	$('#dataTables-vendor_list_freeradius').on('draw.dt', function () {
		$('.btn_edit_vendor').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {

				var radiusname = $( this ).closest('tr').children().eq(0).text();
				var vendorname = $( this ).closest('tr').children().eq(1).text();
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$("#edit_radiusname_vendor_freeradius").select2({
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

				$('#edit_radiusname_vendor_freeradius').select2('data', {'id': radiusname, 'text': radiusname});
				$('#edit_name_vendor_freeradius').val(vendorname);
				$('#uid_edit_freeradius').val(uid);

				$('#edit_previous_name_vendor_freeradius').val(vendorname);
				$('#edit_previous_radiusname_vendor_freeradius').val(radiusname);
				
				var d_data = {'radiusname': radiusname, 'collection': 'vendor_freeradius', 'action_type': 'edit_vendor', 'vendortoedit': vendorname, 'uid': uid};

				$.ajax({
						url: "http://"+urlMaster+"/im_get_vendor_Toedit_freeradius",
						dataType: 'jsonp',
						async: false,
						data: d_data,
						success: function(data)
						{
							$('#modal_edit_vendor_freeradius .modal-dialog .modal-content .modal-body .row .manage_list_bloc .list_bloc').empty()
							$('#modal_edit_vendor_freeradius .modal-dialog .modal-content .modal-body .row .manage_list_bloc .list_bloc').append(data['data']);

							$('.remove_flag').unbind();
							$('.remove_flag').click(function(){
								$( this ).parent().parent().remove();
							});

							$('.add_flag').unbind();
							$('.add_flag').click(function(){
								var flag_name = $( this ).parent().parent().children().eq(0).val();
								var list_flag = $( this ).parent().parent().parent().eq(0).children('.list_flag');
					
								list_flag.append('<div class="entry_list_flag col-lg-12"> \
													<div class="col-lg-11">'+ 
														flag_name 
													+'</div> \
													<div class="col-lg-1"> \
														<i class="fa fa-trash-o fake-link remove_flag"></i> \
													</div> \
												</div>');

								$('.remove_flag').unbind();
								$('.remove_flag').click(function(){
									$( this ).parent().parent().remove();
								});
							});
						}
				});
				$('#modal_edit_vendor_freeradius').modal('show');
			});

		});

		$('.btn_delete_vendor').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				$('.vendor_remove_freeradius').html($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').html($( this ).closest('tr').children().eq(0).text());
				$('.vendor_remove_freeradius').val($( this ).closest('tr').children().eq(1).text());
				$('.radiusname_remove_freeradius').val($( this ).closest('tr').children().eq(0).text());
				$('.uid_remove_freeradius').val($( this ).parent().children('.uid').eq(0).val());
				$('#modal_delete_vendor_freeradius').modal('show');

				var radiusname = $('.radiusname_remove_freeradius').val();
				var vendorname = $('.vendor_remove_freeradius').val();

				$('#remove_vendor_impact_list').empty();
				$('#remove_vendor_impact_list').append("Nothing </br>");

				$.ajax({
					url: "http://"+urlMaster+"/im_list_right_for_vendor_freeradius",
					contentType: 'application/json; charset=utf-8',
					dataType: 'jsonp',
					data: {'radiusname': radiusname, 'vendorname': vendorname},
					async: false,
					success: function(data)
					{	
						if (data['results'] != null)
						{
							$('#remove_vendor_impact_list').empty();
							$('#remove_vendor_id_impact_list').empty();
							for (var i = data['results'].length - 1; i >= 0; i--) 
							{
								$('#remove_vendor_impact_list').append(data['results'][i]['right_label']+"</br>");
								$('#remove_vendor_id_impact_list').append('<input type="hidden" value="'+data['results'][i]['id']+'">');
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
			l_vendor.push(data['radius'].toLowerCase()+'-'+data['vendeur'].toLowerCase());
		},
		"ajax": {
					"url": "http://"+urlMaster+"/im_getlistinfo_freeradius/vendor_freeradius/vendor/",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "radius" },
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
		var vendorname = $('#vendor_remove_freeradius').val();
		var radiusname = $('#radiusname_remove_freeradius').val();
		var uid = $('#uid_remove_freeradius').val();

		var d_data = {'radiusname': radiusname, 'collection': 'vendor_freeradius', 'action_type': 'delete_vendor', 'vendortodelete': vendorname, 'uid': uid};

		$.ajax({
			url: "http://"+urlMaster+"/im_delete_entry_freeradius",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				console.log('success');
				l_vendor = []
				$('#modal_delete_vendor_freeradius').modal('hide');
				var table = $('#dataTables-vendor_list_freeradius').dataTable().api();
				table.ajax.reload();
			}
		});
	});

	function getDivVendorFlag(div) {
		var tab_flag = new Object();

		div.children().each(function(){

			var block_title = $( this ).find('h4').eq(0).text();
			var list_flag = new Array();

			if (block_title) {
				$( this ).find('.list_flag').children().each(
					function(){
						var flag = $( this ).children('.col-lg-11').eq(0)[0].innerHTML;
						if (flag) {
							list_flag.push(flag);
						};
					});
				tab_flag[block_title] = list_flag;
			};
		});
		return tab_flag;
	}

	$( '#proceed_edit' ).click(function() {
		var vendorname = $('#edit_name_vendor_freeradius').val();
		var radiusname = $('#edit_radiusname_vendor_freeradius').val();
		var previous_vendorname = $('#edit_previous_name_vendor_freeradius').val();
		var previous_radiusname = $('#edit_previous_radiusname_vendor_freeradius').val();
		var uid = $('#uid_edit_freeradius').val();
		var tab_flag = getDivVendorFlag($('#modal_edit_vendor_freeradius .modal-dialog .modal-content .modal-body .row .manage_list_bloc .list_bloc'));

		var input_errno = false
		input_errno = check_input_form(radiusname, vendorname, tab_flag, previous_radiusname, previous_vendorname)

		if (input_errno == false)
		{
			$('#edit_alert_input').hide();

			var d_data = {'radiusname': radiusname, 'collection': 'vendor_freeradius', 'action_type': 'edit_vendor', 'vendorname': vendorname, 'uid': uid, 'l_flag': JSON.stringify(tab_flag)};

			$.ajax({
				url: "http://"+urlMaster+"/im_crud_vendor_freeradius/edit",
				dataType: 'jsonp',
				async: false,
				data: d_data,
				success: function(data)
				{
					console.log('success');
					l_vendor = []
					$('#modal_edit_vendor_freeradius').modal('hide');
					var table = $('#dataTables-vendor_list_freeradius').dataTable().api();
					table.ajax.reload();
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
