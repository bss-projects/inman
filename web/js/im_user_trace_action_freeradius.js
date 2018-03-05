$(function()
{

	$("#radiusname_user_trace_action_freeradius").select2({
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

	$("#username_user_trace_action_freeradius").select2({
		ajax: {
			url: "http://"+urlMaster+"/im_list_user_freeradius",
			dataType: 'jsonp',
			data: function (term, page) {
				return {
					q: term, // search term
					radiusname: $("#radiusname_user_trace_action_freeradius").val(),
					page_limit: 10
					};
			},
			results: function (data, page) {
				return {results: data.results};
			}
		}
	});

	$("#date_user_trace_action_freeradius").daterangepicker();

	$('#dataTables-user_trace_action_list_freeradius').on('draw.dt', function () {
		$('.btn_view').each(function( index ) {
			$( this ).tooltip();
			$( this ).click(function() {
				var date = $( this ).closest('tr').children().eq(0).text();
				var radiusname = $( this ).closest('tr').children().eq(1).text();
				var username = $( this ).closest('tr').children().eq(2).text();
				var event = $( this ).closest('tr').children().eq(3).text();
				var uid = $( this ).parent().children('.uid').eq(0).val();

				$('.date_user_trace_action_freeradius').html(date);
				$('.radiusname_user_trace_action_freeradius').html(radiusname);
				$('.username_user_trace_action_freeradius').html(username);
				$('.event_user_trace_action_freeradius').html(event);
				$('#uid_user_trace_action_freeradius').val(uid);

				$.ajax({
					url: "http://"+urlMaster+"/im_get_action_user_trace/"+uid,
					dataType: 'jsonp',
					async: false,
					success: function(data)
					{
						$('#action_data_user_trace_action_freeradius').empty();
						if (typeof data === 'object')
						{
							var keys = Object.keys(data);
							for (var i = keys.length - 1; i >= 0; i--)
							{
								$('#action_data_user_trace_action_freeradius').append('<strong><span>'+keys[i]+': '+data[keys[i]]+'</span></strong></br>');
							}
						}
						else 
						{
							$('#action_data_user_trace_action_freeradius').append('<strong><span>'+data+'</span></strong></br>');
						}
					}
				});

				$('#modal_view_user_trace_action_freeradius').modal('show');
			});

		});

	}).dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/im_get_list_user_trace/freeradius",
					"dataType": "jsonp",
					"async": false
		},
		"order": [[ 0, "desc" ]],
		"columns": [
			{ "data": "date" },
			{ "data": "radius" },
			{ "data": "utilisateur" },
			{ "data": "événement" },
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

	$( '#search_user_trace_action_freeradius' ).click(function() {
		var radiusname = $('#radiusname_user_trace_action_freeradius').val();
		var username = $('#username_user_trace_action_freeradius').val();
		var date = $('#date_user_trace_action_freeradius').val();
		var l_date = date.split(' - ');

		var datePartsBegin = l_date[0].split('/');
		var datePartsEnd = l_date[1].split('/');

		var date_begin = new Date(datePartsBegin[2], parseInt(datePartsBegin[0], 10) - 1, datePartsBegin[1]);
		var timestamp_begin = date_begin.getTime() / 1000;

		var date_end = new Date(datePartsEnd[2], parseInt(datePartsEnd[0], 10) - 1, datePartsEnd[1]);
		var timestamp_end = date_end.getTime() / 1000;

		var d_data = {'agent': radiusname, 'username': username, 'timestamp_begin': timestamp_begin, 'timestamp_end': timestamp_end};

		console.log(d_data);

		$.ajax({
			url: "http://"+urlMaster+"/im_get_list_user_trace/freeradius",
			dataType: 'jsonp',
			async: false,
			data: d_data,
			success: function(data)
			{
				var table = $('#dataTables-user_trace_action_list_freeradius').dataTable().api();
				table.clear();
				table.rows.add(data['data']);
				table.draw();
			}
		});

	});

});