{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('Command management for Supervisor') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-map-marker fa-fw"></i> {{ _('Command Control') }}
				</div>
				<div class="panel-body">

					<div class="row">
						<div class="col-lg-4">
							<div class="panel panel-default">
								<div class="panel-heading">
									<i class="fa fa-plus-square-o fa-fw"></i> {{ _('Add command') }}
								</div>
								<div class="panel-body">


									<form class="form-horizontal" role="form" name="create_new_command_supervisor" action="im_crud_command_supervisor/newcommand" method="post">
										<div class="form-group">
											<label for="supervisorname_command_supervisor" class="col-sm-3 control-label">{{ _('Supervisor name') }}</label>
											<div class="col-sm-9">
												<input type="supervisorname_command_supervisor" class="form-control" id="supervisorname_command_supervisor" name="supervisorname_command_supervisor" placeholder="{{ _('Supervisor name') }}">
											</div>
										</div>
										<div class="form-group">
											<label for="name_command_supervisor" class="col-sm-3 control-label">{{ _('Command name') }}</label>
											<div class="col-sm-9">
												<input type="name_command_supervisor" class="form-control" id="name_command_supervisor" name="name_command_supervisor" placeholder="{{ _('Command name') }}">
											</div>
										</div>
										<div class="form-group">
											<label for="probe_command_supervisor" class="col-sm-3 control-label">{{ _('Probe') }}</label>
											<div class="col-sm-9">
												<input type="probe_command_supervisor" class="form-control" id="probe_command_supervisor" name="probe_command_supervisor" placeholder="{{ _('Probe') }}">
											</div>
										</div>
										<div class="form-group">
											<label for="args_command_supervisor" class="col-sm-3 control-label">{{ _('Arguments') }}</label>
											<div class="col-sm-9">



										<div id="listargs_supervisor">
											<table class="table" id="tab_args_supervisor">
												<thead>
													<tr>
														<th>{{ _('Option') }}</th>
														<th>{{ _('Value') }}</th>
														<th>{{ _('R') }}</th>
													</tr>
												</thead>
												<tbody>

												</tbody>
											</table>
											<div class="col-lg-12">
												<div class="col-lg-5">
													<input type="option_command_supervisor" class="form-control" id="option_command_supervisor" name="option_command_supervisor" placeholder="{{ _('Option') }}">
												</div>
												<div class="col-lg-5">
													<input type="value_command_supervisor" class="form-control" id="value_command_supervisor" name="value_command_supervisor" placeholder="{{ _('Value') }}">
												</div>
												<div class="col-lg-2">
													<button id="add_args" class="btn btn-outline btn-info" type="button">{{ _('Add') }}</button>
												</div>
											</div>
										</div>





											</div>
										</div>
										<div class="form-group">
											<div class="col-sm-offset-3 col-sm-9">
													<button id="add_command_supervisor" type="button" class="btn btn-default">{{ _('Add command') }}</button>
											</div>
										</div>
									</form>


								</div>
							</div>
						</div>
						<div class="col-lg-8">
							<div class="panel panel-default">
								<div class="panel-heading">
									<i class="fa fa-plus-square-o fa-fw"></i> {{ _('Command list') }}
								</div>
								<div class="panel-body">
									<div class="table-responsive">
											<!-- ICI DATATABLE -->
										<table class="table table-striped table-bordered table-hover" id="dataTables-command_list_supervisor">
											<thead>
												<tr>
													<th>{{ _('Supervisor') }}</th>
													<th>{{ _('Name') }}</th>
													<th>{{ _('Bin') }}</th>
													<th>{{ _('Actions') }}</th>
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
</div>

	{% endblock container %}
	{% block js %}
		{% include 'im_js.tpl' %}
		<script src="/web/js/autobahn.min.jgz"></script>
		<script src="/web/js/im_command_supervisor.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}