$(function()
{

	$("#templatemodel").select2({
		minimumInputLength: 1,
		ajax: {
			url: "http://"+urlMaster+"/getlisthost",
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

	$("#supervisor_newhost").select2({
		minimumInputLength: 1,
		ajax: {
			url: "http://"+urlMaster+"/getlistsupervisor",
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

	$("#hostname_newhost").change(function(){
		var allHost = "";

		//il faut passer en param le nom du superviseur choisi
		/////Il faut mettre en place un select avec indication du superviseur pour choix modele en cas de doublon sur des superviseurs différents

		$.ajax({
			url: "http://"+urlMaster+"/getallhost",
			dataType: 'jsonp',
			async: false,
			success: function(data)
			{
				allHost = data;
				console.log(allHost);
				if ($.inArray($("#hostname_newhost").val(), allHost) == -1)
				{
					$("#hostname_newhost").parent().parent().removeClass("has-error");
					$("#hostname_newhost").parent().parent().addClass("has-success");
				}
				else
				{
					$("#hostname_newhost").parent().parent().removeClass("has-success");
					$("#hostname_newhost").parent().parent().addClass("has-error");
				};
			}
		});
	});

	$("#hostname_template").change(function(){

			var allHost = "";

		//il faut passer en param le nom du superviseur choisi
		/////Il faut mettre en place un select avec indication du superviseur pour choix modele en cas de doublon sur des superviseurs différents

		$.ajax({
			url: "http://"+urlMaster+"/getallhost",
			dataType: 'jsonp',
			async: false,
			success: function(data)
			{
				allHost = data;
				console.log(allHost);
				if ($.inArray($("#hostname_template").val(), allHost) == -1)
				{
					$("#hostname_template").parent().parent().removeClass("has-error");
					$("#hostname_template").parent().parent().addClass("has-success");
				}
				else
				{
					$("#hostname_template").parent().parent().removeClass("has-success");
					$("#hostname_template").parent().parent().addClass("has-error");
				};
			}
		});
	});

	$('#filterlevelview').bootstrapSwitch({
		onText: 'Simple',
		offText: 'Complet',
		size: 'normal'
	});

	$('#fileupload').fileupload({
		dataType: 'json',
		dropZone: $('#dropzone'),
		done: function (e, data) {
			$.each(data.result.files, function (index, file) {
				$('<p/>').text(file.name).appendTo(document.body);
			});
		}
	});

	$('#dataTables-hostlist').dataTable(
	{
		"processing": true,
		"serverSide": false,
		"ajax": {
					"url": "http://"+urlMaster+"/getlisthostinfo",
					"dataType": "jsonp",
					"async": false
		},
		"columns": [
			{ "data": "superviseur" },
			{ "data": "hote" },
			{ "data": "ip" },
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
	
});
