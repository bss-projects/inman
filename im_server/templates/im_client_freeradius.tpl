{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<!-- Modal client import file result -->
<div class="modal fade" id="modal_client_import_file_result_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Close') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Client file import return :') }} </h4>
			</div>
			<div class="modal-body">
				<div class="panel panel-danger">
					<div class="panel-heading">
						{{ _('Error in file') }}
					</div>
					<div class="panel-body">
						<div class="table-responsive">
							<table id="table_client_file_import_error" class="table">
								<thead>
									<tr>
										<th>#</th>
										<th>{{ _('Error') }}</th>
									</tr>
								</thead>
								<tbody>
								</tbody>
							</table>
						</div>
					</div>
				</div>
				<div class="panel panel-info">
					<div class="panel-heading">
						{{ _('Action') }}
					</div>
					<div class="panel-body">
						<p>{{ _('Number of line to insert : ') }}<span id="import_file_number_of_line"></span></p>
						<div id="import_file_sync_state">
							<ul>
								
							</ul>
						</div>
					</div>
				</div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Close') }}</button>
			</div>
		</div>
	</div>
</div>

<!-- Modal remove -->
<div class="modal fade" id="modal_delete_client_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="client_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('You are about to delete') }} <strong><span class="client_remove_freeradius"></span></strong> {{ _('vendor') }} <strong><span class="vendor_remove_freeradius"></span></strong> {{ _('from') }} <strong><span class="radiusname_remove_freeradius"></span></strong>
				<input type="hidden" id="client_remove_freeradius" name="client_remove_freeradius" class="client_remove_freeradius">
				<input type="hidden" id="client_ip_remove_freeradius" name="client_ip_remove_freeradius" class="client_ip_remove_freeradius">
				<input type="hidden" id="radiusname_remove_freeradius" name="radiusname_remove_freeradius" class="radiusname_remove_freeradius">
				<input type="hidden" id="uid_remove_freeradius" name="uid_remove_freeradius" class="uid_remove_freeradius">
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_remove">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>

<!-- Modal edit -->
<div class="modal fade col-lg-12" id="modal_edit_client_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">

		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit client mod :') }}</h4>
			</div>
			<div class="modal-body">
				<div class="row">
					<div id="edit_alert_input" class="alert alert-warning" style="display: none;">

					</div>
					<form class="form-horizontal col-lg-12" role="form" name="edit_client_freeradius" action="im_crud_client_freeradius/edit" method="post">

						<div class="form-group col-lg-12">
							<label for="edit_radiusname_client_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
							<div class="col-sm-9">
								<input type="edit_radiusname_client_freeradius" class="form-control" id="edit_radiusname_client_freeradius" name="edit_radiusname_client_freeradius" placeholder="{{ _('Radius name') }}">
								<input type="hidden" id="edit_previous_radiusname_client_freeradius" name="edit_previous_radiusname_client_freeradius">
							</div>
						</div>
						<div class="form-group col-lg-12">
							<label for="edit_name_client_freeradius" class="col-sm-3 control-label">{{ _('Name') }}</label>
							<div class="col-sm-9">
								<input type="edit_name_client_freeradius" class="form-control" id="edit_name_client_freeradius" name="edit_name_client_freeradius" placeholder="{{ _('Name') }}">
							</div>
						</div>
						<div class="form-group col-lg-12">
							<label for="edit_shortname_client_freeradius" class="col-sm-3 control-label">{{ _('Shortname') }}</label>
							<div class="col-sm-9">
								<input type="edit_shortname_client_freeradius" class="form-control" id="edit_shortname_client_freeradius" name="edit_shortname_client_freeradius" placeholder="{{ _('Shortname') }}">
							</div>
						</div>
						<div class="form-group col-lg-12">
							<label for="edit_ip_client_freeradius" class="col-sm-3 control-label">{{ _('IP') }}</label>
							<div class="col-sm-9">
								<input type="edit_ip_client_freeradius" class="form-control" id="edit_ip_client_freeradius" name="edit_ip_client_freeradius" placeholder="{{ _('IP') }}">
								<input type="hidden" id="edit_previous_ip_client_freeradius" name="edit_previous_ip_client_freeradius">
							</div>
						</div>
						<div class="form-group col-lg-12">
							<label for="edit_vendor_client_freeradius" class="col-sm-3 control-label">{{ _('Select vendor') }}</label>
							<div class="col-sm-9">
								<input type="edit_vendor_client_freeradius" class="form-control" id="edit_vendor_client_freeradius" name="edit_vendor_client_freeradius" placeholder="{{ _('Vendor name') }}">
							</div>
						</div>
						<div class="form-group col-lg-12">
							<label for="edit_secret_client_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
							<div class="col-sm-9">
								<input type="edit_secret_client_freeradius" class="form-control" id="edit_secret_client_freeradius" name="edit_secret_client_freeradius" placeholder="{{ _('Shared secret') }}">
							</div>
						</div>

						<div class="form-group col-lg-12">
							<div class="col-sm-3"></div>
							<div class="col-sm-9">
								<button type="button" class="btn btn-outline btn-default btn-xs" id="clear_secret_client_freeradius">{{ _('Clear Shared secret') }}</button>
							</div>
						</div>

					</form>
				</div>
			</div>
			<div class="modal-footer">
				<input type="hidden" id="uid_edit_freeradius" name="uid_edit_freeradius" class="uid_edit_freeradius">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_edit">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>



<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('Clients management for Freeradius') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-folder-o fa-fw"></i> {{ _('Clients administration') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-4">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-folder-open-o fa-fw"></i> {{ _('Add client') }}
							</div>
							<div class="panel-body">

								<div id="alert_input" class="alert alert-warning" style="display: none;">
								</div>
								
								<form class="form-horizontal" role="form" name="create_new_client_freeradius" action="im_crud_client_freeradius/new" method="post">
									<div class="form-group">
										<label for="radiusname_client_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
										<div class="col-sm-9">
											<input type="radiusname_client_freeradius" class="form-control" id="radiusname_client_freeradius" name="radiusname_client_freeradius" placeholder="{{ _('Radius name') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="name_client_freeradius" class="col-sm-3 control-label">{{ _('Name') }}</label>
										<div class="col-sm-9">
											<input type="name_client_freeradius" class="form-control" id="name_client_freeradius" name="name_client_freeradius" placeholder="{{ _('Name') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="shortname_client_freeradius" class="col-sm-3 control-label">{{ _('Shortname') }}</label>
										<div class="col-sm-9">
											<input type="shortname_client_freeradius" class="form-control" id="shortname_client_freeradius" name="shortname_client_freeradius" placeholder="{{ _('Shortname') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="ip_client_freeradius" class="col-sm-3 control-label">{{ _('IP') }}</label>
										<div class="col-sm-9">
											<input type="ip_client_freeradius" class="form-control" id="ip_client_freeradius" name="ip_client_freeradius" placeholder="{{ _('IP') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="vendor_client_freeradius" class="col-sm-3 control-label">{{ _('Select vendor') }}</label>
										<div class="col-sm-9">
											<input type="vendor_client_freeradius" class="form-control" id="vendor_client_freeradius" name="vendor_client_freeradius" placeholder="{{ _('Vendor name') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="secret_client_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
										<div class="col-sm-9">
											<input type="secret_client_freeradius" class="form-control" id="secret_client_freeradius" name="secret_client_freeradius" placeholder="{{ _('Shared secret') }}">
										</div>
									</div>

									<div class="form-group">
										<div class="col-sm-offset-3 col-sm-9">
											<button id="add_client_freeradius" type="button" class="btn btn-default">{{ _('Add client') }}</button>
										</div>
									</div>

								</form>

							</div>
						</div>

						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-upload fa-fw"></i> {{ _('Upload client file') }}
							</div>
							<div class="panel-body">
								<div id="dropzone" class="fade well col-sm-12">{{ _('Drag and drop your file here or select it') }}</div>
								<table id="fileupload_list">
								</table>
								<input id="fileupload" class="pull-right" type="file" name="files[]" data-url="/upload_freeradius" multiple>
							</div>
						</div>

					</div>
					<div class="col-lg-8">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-list fa-fw"></i> {{ _('Client list') }}
							</div>
							<div class="panel-body">
								<div class="table-responsive">
										<!-- ICI DATATABLE -->
									<table class="table table-striped table-bordered table-hover" id="dataTables-client_list_freeradius">
										<thead>
											<tr>
												<th>{{ _('Radius') }}</th>
												<th>{{ _('Client') }}</th>
												<th>{{ _('IP') }}</th>
												<th>{{ _('Vendor') }}</th>
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

	{% endblock container %}
	{% block js %}
		{% include 'im_js.tpl' %}
		<script src="/web/js/im_crud_client_freeradius.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}