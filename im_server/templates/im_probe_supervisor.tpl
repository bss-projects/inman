{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('Probe management for Supervisor') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-map-marker fa-fw"></i> {{ _('Probe Control') }}
				</div>
				<div class="panel-body">

					<div class="row">
						<div class="col-lg-4">
							<div class="panel panel-default">
								<div class="panel-heading">
									<i class="fa fa-plus-square-o fa-fw"></i> {{ _('Add probe') }}
								</div>
								<div class="panel-body">


									<form class="form-horizontal" role="form" name="create_new_probe_supervisor" action="im_crud_probe_supervisor/newprobe" method="post">
										<div class="form-group">
											<label for="supervisorname_probe_supervisor" class="col-sm-3 control-label">{{ _('Supervisor name') }}</label>
											<div class="col-sm-9">
												<input type="supervisorname_probe_supervisor" class="form-control" id="supervisorname_probe_supervisor" name="supervisorname_probe_supervisor" placeholder="{{ _('Supervisor name') }}">
											</div>
										</div>
										<div class="form-group">
											<label for="name_probe_supervisor" class="col-sm-3 control-label">{{ _('Probe name') }}</label>
											<div class="col-sm-9">
												<input type="name_probe_supervisor" class="form-control" id="name_probe_supervisor" name="name_probe_supervisor" placeholder="{{ _('Probe name') }}">
											</div>
										</div>
										<div class="form-group">
											<label for="file_probe_supervisor" class="col-sm-3 control-label">{{ _('Probe upload') }}</label>
											<div class="col-sm-9">
												<div id="dropzone" class="fade well col-sm-12">{{ _('Drag and drop your file here or select it') }}</div>
												<table id="fileupload_list">
												</table>
												<input id="fileupload" class="pull-right" type="file" name="files[]" data-url="/upload_supervisor" multiple>
											</div>
										</div>
										<div class="form-group">
											<div class="col-sm-offset-3 col-sm-9">
												<button id="add_probe_supervisor" type="button" class="btn btn-default">{{ _('Add probe') }}</button>
											</div>
										</div>
									</form>


								</div>
							</div>
						</div>
						<div class="col-lg-8">
							<div class="panel panel-default">
								<div class="panel-heading">
									<i class="fa fa-plus-square-o fa-fw"></i> {{ _('Probe list') }}
								</div>
								<div class="panel-body">
									<div class="table-responsive">
											<!-- ICI DATATABLE -->
										<table class="table table-striped table-bordered table-hover" id="dataTables-probe_list_supervisor">
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
		<script src="/web/js/im_probe_supervisor.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}