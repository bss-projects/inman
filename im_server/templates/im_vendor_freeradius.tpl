{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<!-- Modal remove -->
<div class="modal fade" id="modal_delete_vendor_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="vendor_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('You are about to delete') }} <strong><span class="vendor_remove_freeradius"></span></strong> {{ _('from') }} <strong><span class="radiusname_remove_freeradius"></span></strong>
				<input type="hidden" id="vendor_remove_freeradius" name="vendor_remove_freeradius" class="vendor_remove_freeradius">
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
<div class="modal fade col-lg-12" id="modal_edit_vendor_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit vendor mod :') }}</h4>
			</div>
			<div class="modal-body">
				<div class="row">
					<form class="form-horizontal col-lg-12" role="form" name="edit_vendor_freeradius" action="im_crud_vendor_freeradius/edit" method="post">

						<div class="form-group col-lg-12">
							<label for="edit_radiusname_vendor_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
							<div class="col-sm-9">
								<input type="edit_radiusname_vendor_freeradius" class="form-control" id="edit_radiusname_vendor_freeradius" name="edit_radiusname_vendor_freeradius" placeholder="{{ _('Radius name') }}">
							</div>
						</div>
	
						<div class="form-group col-lg-12">
							<label for="edit_name_vendor_freeradius" class="col-sm-3 control-label">{{ _('Vendor name') }}</label>
							<div class="col-sm-9">
								<input type="edit_name_vendor_freeradius" class="form-control" id="edit_name_vendor_freeradius" name="edit_name_vendor_freeradius" placeholder="{{ _('Vendor name') }}">
							</div>
						</div>
						
						<fieldset class="col-lg-12">
							<legend>{{ _('Specific vendor flag') }}</legend>
						</fieldset>
						<div class="manage_list_bloc col-lg-12">
							<div class="list_bloc col-lg-12">
							</div>
							<div class="input-group col-lg-offset-1 col-lg-10">
								<input type="title_flag_block_freeradius" class="form-control" id="title_flag_block" name="title_flag_block" placeholder="{{ _('Title flag block') }}">
								<span class="input-group-btn">
									<button id="im_add_flag_vendor_bloc" class="btn btn-default" type="button">
										<i class="fa fa-plus-circle"></i>
										{{ _('Add new block') }}
									</button>
								</span>
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
			<h1 class="page-header">{{ _('Vendors management for Freeradius') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-legal fa-fw"></i> {{ _('Vendors administration') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-4">

						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-plus-square-o fa-fw"></i> {{ _('Add vendor') }}
							</div>
							<div class="panel-body">

								<form class="form-horizontal" role="form" name="create_new_vendor_freeradius" action="im_crud_vendor_freeradius/new" method="post">
									<div class="form-group">
										<label for="radiusname_vendor_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
										<div class="col-sm-9">
											<input type="radiusname_vendor_freeradius" class="form-control" id="radiusname_vendor_freeradius" name="radiusname_vendor_freeradius" placeholder="{{ _('Radius name') }}">
										</div>
									</div>
									<div class="form-group">
										<label for="name_vendor_freeradius" class="col-sm-3 control-label">{{ _('Vendor name') }}</label>
										<div class="col-sm-9">
											<input type="name_vendor_freeradius" class="form-control" id="name_vendor_freeradius" name="name_vendor_freeradius" placeholder="{{ _('Vendor name') }}">
										</div>
									</div>

									<div class="form-group">
										<fieldset class="col-lg-12">
											<legend>{{ _('Specific vendor flag') }}</legend>
										</fieldset>
										<div class="col-lg-12">
											<table id="tab_vendor_block_flag_freeradius">
												<tbody>
												<tr><td></td></tr>
												</tbody>
											</table>
										</div>

										<div class="input-group col-lg-offset-1 col-lg-10">
											<input type="title_flag_block_freeradius" class="form-control" id="title_flag_block_freeradius" name="title_flag_block_freeradius" placeholder="{{ _('Title flag block') }}">
											<span class="input-group-btn">
												<button id="im_add_flag_vendor_bloc_freeradius" class="btn btn-default" type="button">
													<i class="fa fa-plus-circle"></i>
														{{ _('Add new block') }}
												</button>
											</span>
										</div>
									</div>

									<div class="form-group">
										<div class="col-sm-offset-3 col-sm-9">
											<button id="add_vendor_freeradius" type="button" class="btn btn-default">{{ _('Add vendor') }}</button>
										</div>
									</div>
								</form>
							</div>
						</div>
					</div>
					<div class="col-lg-8">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-list fa-fw"></i> {{ _('Vendor list') }}
							</div>
							<div class="panel-body">
								<div class="table-responsive">
										<!-- ICI DATATABLE -->
									<table class="table table-striped table-bordered table-hover" id="dataTables-vendor_list_freeradius">
										<thead>
											<tr>
												<th>{{ _('Radius') }}</th>
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
		<script src="/web/js/im_crud_vendor_freeradius.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}