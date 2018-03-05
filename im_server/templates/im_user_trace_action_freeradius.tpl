{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<link href="/web/css/plugins/daterangepicker/daterangepicker.css" rel="stylesheet">

<!-- Modal remove -->
<div class="modal fade" id="modal_view_user_trace_action_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('View event :') }} <div class="right_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('Date') }} : <strong><span class="date_user_trace_action_freeradius"></span></strong></br>
				{{ _('Radius') }} : <strong><span class="radiusname_user_trace_action_freeradius"></span></strong></br>
				{{ _('User') }} : <strong><span class="username_user_trace_action_freeradius"></span></strong></br>
				{{ _('Event') }} : <strong><span class="event_user_trace_action_freeradius"></span></strong></br>
				{{ _('Info') }} : <div id="action_data_user_trace_action_freeradius"></div></br>
				<input type="hidden" id="right_remove_freeradius" name="right_remove_freeradius" class="right_remove_freeradius">
				<input type="hidden" id="uid_user_trace_action_freeradius" name="uid_user_trace_action_freeradius" class="uid_user_trace_action_freeradius">
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Ok') }}</button>
			</div>
		</div>
	</div>
</div>

<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('User trace action for Freeradius') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-stack-overflow fa-fw"></i> {{ _('Trace') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-12">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-filter fa-fw"></i> {{ _('Filter') }}
							</div>
							<div class="panel-body">

								<div id="alert_input" class="alert alert-warning" style="display: none;">
								</div>

								<form class="form-horizontal" role="form" name="search_user_trace_action_freeradius" action="im_user_trace_action_search_freeradius" method="post">
									<div class="col-lg-4">
										<div class="form-group">
											<label for="radiusname_user_trace_action_freeradius" class="col-sm-4 control-label">{{ _('Radius name') }}</label>
											<div class="col-sm-8">
												<input type="radiusname_user_trace_action_freeradius" class="form-control" id="radiusname_user_trace_action_freeradius" name="radiusname_user_trace_action_freeradius" placeholder="{{ _('Radius name') }}">
											</div>
										</div>
									</div>
									<div class="col-lg-4">
										<div class="form-group">
											<label for="username_user_trace_action_freeradius" class="col-sm-3 control-label">{{ _('User') }}</label>
											<div class="col-sm-9">
												<input type="username_user_trace_action_freeradius" class="form-control" id="username_user_trace_action_freeradius" name="username_user_trace_action_freeradius" placeholder="{{ _('User name') }}">
											</div>
										</div>
									</div>
									<div class="col-lg-4">
										<div class="form-group">
											<label for="date_user_trace_action_freeradius" class="col-sm-3 control-label">{{ _('Date') }}</label>
											<div class="form-group input-group col-sm-9">
												<input type="date_user_trace_action_freeradius" class="form-control" id="date_user_trace_action_freeradius" name="date_user_trace_action_freeradius" placeholder="{{ _('Date') }}">
												<span class="input-group-addon"><i class="glyphicon glyphicon-calendar fa fa-calendar"></i></span>
											</div>
										</div>
									</div>

									<div class="form-group">
										<div class="col-sm-offset-10 col-sm-2">
											<button id="search_user_trace_action_freeradius" type="button" class="btn btn-default">{{ _('Search') }}</button>
										</div>
									</div>
								</form>
							</div>
						</div>
					</div>
					<div class="col-lg-12">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-list-alt fa-fw"></i> {{ _('Event list') }}
							</div>
							<div class="panel-body">
								<div class="table-responsive">
										<!-- ICI DATATABLE -->
									<table class="table table-striped table-bordered table-hover" id="dataTables-user_trace_action_list_freeradius">
										<thead>
											<tr>
												<th>{{ _('Date') }}</th>
												<th>{{ _('Radius') }}</th>
												<th>{{ _('User') }}</th>
												<th>{{ _('Event') }}</th>
												<th>{{ _('Action') }}</th>
											</tr>
										</thead>
										<tbody>
										<!-- ICI AJAX INPUT -->
										</tbody>
									</table>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

	{% endblock container %}
	{% block js %}
		{% include 'im_js.tpl' %}
		<script src="/web/js/im_user_trace_action_freeradius.js"></script>
		<script src="/web/js/plugins/daterangepicker/moment.min.js"></script>
		<script src="/web/js/plugins/daterangepicker/daterangepicker.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}