$(function()
{
	$("#radiusname_log_freeradius").select2({
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

	function onchallenge (session, method, extra) {
		if (method === "wampcra") {
			return autobahn.auth_cra.sign(Ckey, extra.challenge);
		}
		console.log('Crossbar on challenge');
	}

	function updateScrollToEnd(div_name){
		$(div_name).scrollTop($(div_name)[0].scrollHeight);
	}

	function unsubscribe(session)
	{
		for (var i = Object.keys(session._subscriptions).length - 1; i >= 0; i--) {
			sub_id = Object.keys(session._subscriptions)[i];
			if (session._subscriptions[sub_id][0])
			{
				session.unsubscribe(session._subscriptions[sub_id][0]);	
			};
		};
	}

	var connection = new autobahn.Connection({
		url: 'ws://'+urlCrossbar+':8080/ws',
		realm: realmCrossbar,
		authmethods: ["wampcra"],
		authid: Cuser,
		onchallenge: onchallenge}
	);
 
	connection.onopen = function (session) {

 		console.log('Crossbar on open');
		console.log(uriTopicLiveLog_freeradius);

 		session.subscribe(uriTopicLiveLog_freeradius, onevent1);

 		console.log('Crossbar subscribe');

		$('#file_view_log_freeradius').click(function() {

			var radiusname = $('#radiusname_log_freeradius').val();
			console.log('File log view');
			unsubscribe(session);

			/*
			** Replace follow radiusname with the radius name selected
			*/

			console.log('Call RPC listLogFileFreeradius');
			$('#frame_view_log_freeradius').empty();

			if (radiusname)
			{
				session.call('im.freeradius.list.file.log', [radiusname]).then(
					function (res) {
						
						console.log("listLogFileFreeradius() success");

						$('#frame_view_log_freeradius').empty();
						for (var len = res.length - 1, i = 0; i <= len; i++)
						{
							console.log('Call RPC readLogFreeradius');
							session.call('im.freeradius.file.log', [radiusname, res[i]]).then(
								function (res) {
									$('#frame_view_log_freeradius').append(res);
									updateScrollToEnd('#frame_view_log_freeradius');
									console.log("readLogFreeradius() success");
								},
								function (err) {
									console.log("readLogFreeradius() error:", err);
								}
							)
						}
					},
					function (err) {
						console.log("listLogFileFreeradius() error:", err);
					}
				)
			}
			else
			{
				$('#frame_view_log_freeradius').append('You have to choose a RADIUS to watch');
			}
		});

		$('#live_view_log_freeradius').click(function() {
			var radiusname = $('#radiusname_log_freeradius').val();
			console.log('Live log view');
			$('#frame_view_log_freeradius').empty();
			unsubscribe(session);
			console.log(session);

			if (radiusname)
			{
				session.subscribe(uriTopicLiveLog_freeradius, onevent1);
			}
			else
			{
				$('#frame_view_log_freeradius').append('You have to choose a RADIUS to watch');
			}
		});

		function onevent1(args) {
			console.log(args);
			var radiusname = $('#radiusname_log_freeradius').val();

			if (radiusname == args[0][0])
			{
				$('#frame_view_log_freeradius').append(args[0][1]+'</br>');
				updateScrollToEnd('#frame_view_log_freeradius')
				//	connection.close();				
			}

		}

	};
	console.log('Login into Crossbar');
	connection.open();
});
