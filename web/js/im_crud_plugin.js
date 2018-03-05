$(function()
{
	var agent_info = new Array();
	var plugin_countnb_agent = new Array();

	$.ajax({
				url: "http://"+urlMaster+"/im_getlistagentinfo/all",
				dataType: 'jsonp',
				async: false,
				success: function(data)
				{
					for (var i = data['results'].length - 1; i >= 0; i--) {
						var plugin_name = data['results'][i]['plugin_name'];
						if (!plugin_countnb_agent[plugin_name])
						{
							plugin_countnb_agent[plugin_name] = 1;
						}
						else
						{
							plugin_countnb_agent[plugin_name] += 1;
						};
						
						if (!agent_info[plugin_name])
						{
							agent_info[plugin_name] = new Array();
						};

						agent_info[plugin_name].push({'agent_name': data['results'][i]['agent_name'], 'agent_hostname': data['results'][i]['agent_hostname'], 'agent_connection_type': data['results'][i]['agent_connection_type'], 'agent_ip': data['results'][i]['agent_ip']});
					};
				}
	});

	$.ajax({
				url: "http://"+urlMaster+"/im_list_plugin_info",
				dataType: 'jsonp',
				async: false,
				success: function(data)
				{

					for (var i = data['results'].length - 1; i >= 0; i--) {
						var plugin_name = data['results'][i]['plugin_name'];
						var short_desc = data['results'][i]['short_desc'];
						var description = data['results'][i]['description'];
						var nb_agent = '*';
						var agent_data = '';

						if (plugin_countnb_agent[plugin_name])
						{
							nb_agent = plugin_countnb_agent[plugin_name];
							agent_data = JSON.stringify(agent_info[plugin_name]);
						};

						$( '.list-group' ).append('<a href="#" class="list-group-item"> \
												<span class="label label-default label-pill pull-right">'+nb_agent+'</span> \
												<h4 class="list-group-item-heading">'+plugin_name+'</h4> \
												<p class="list-group-item-text">'+short_desc+'</p> \
												<input type="hidden" class="description" value="'+description+'"> \
												<div style="display:none" class="agent_data">'+agent_data+'</div> \
											</a>');
					};

				}
	});

	$( '.list-group-item' ).click(function() {
		$( '.list-group-item' ).each(function(){
			$( this ).removeClass('active');
		});

		var plugin_name = $( this ).children('h4').text();
		var description = $( this ).children('.description').val();
		var agent_data = '';

		if ($( this ).children('.agent_data').text() != '')
		{
			agent_data = JSON.parse($( this ).children('.agent_data').text());
		};

		$( this ).addClass('active');
		$( '#plugin_name' ).empty();
		$( '#plugin_name' ).append(plugin_name);

		$( '#description' ).empty();
		$( '#description' ).append(description);

		$( '#accordion' ).empty();
		for (var i = agent_data.length - 1; i >= 0; i--) {
			
			$( '#accordion' ).append('<div class="panel panel-default"> \
		<div class="panel-heading"> \
			<h4 class="panel-title"> \
				<a href="#collapse'+i+'" data-parent="#accordion" data-toggle="collapse" class="">'+agent_data[i]['agent_name']+'</a> \
			</h4> \
		</div> \
		<div id="collapse'+i+'" class="panel-collapse collapse" style="height: 0px;"> \
			<div class="panel-body"> \
				<div class="row"> \
					<div class="col-sm-4"> \
						<div class="row"> \
							<div class="col-sm-4"> \
								<label class="control-label">Agent name</label> \
							</div> \
							<div id="plugin_name" class="col-sm-8"> \
								'+agent_data[i]['agent_name']+' \
							</div> \
						</div> \
						<div class="row"> \
							<div class="col-sm-4"> \
								<label class="control-label">Hostname</label> \
							</div> \
							<div id="plugin_name" class="col-sm-8"> \
								'+agent_data[i]['agent_hostname']+' \
							</div> \
						</div> \
					</div> \
					<div class="col-sm-4"> \
						<div class="row"> \
							<div class="col-sm-4"> \
								<label class="control-label">IP</label> \
							</div> \
							<div id="plugin_name" class="col-sm-8"> \
								'+agent_data[i]['agent_ip']+' \
							</div> \
						</div> \
						<div class="row"> \
							<div class="col-sm-4"> \
								<label class="control-label">Connection type</label> \
							</div> \
							<div id="plugin_name" class="col-sm-8"> \
								'+agent_data[i]['agent_connection_type']+' \
							</div> \
						</div> \
					</div> \
					<div class="col-sm-4"> \
						\
					</div> \
				</div> \
			</div> \
		</div> \
	</div>');

		};

		if (plugin_name == 'Administration')
		{
			$( '.btn' ).addClass('disabled');
		}
		else
		{
			$( '.btn' ).removeClass('disabled');
		};
	});

});
