{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<!-- Modal remove -->
<div class="modal fade" id="modal_delete_right_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="right_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('You are about to delete') }} <strong><span class="right_remove_freeradius"></span></strong> {{ _('for') }}  <strong><span class="vendor_remove_freeradius"></span></strong> {{ _('from') }} <strong><span class="radiusname_remove_freeradius"></span></strong>
				<input type="hidden" id="right_remove_freeradius" name="right_remove_freeradius" class="right_remove_freeradius">
				<input type="hidden" id="radiusname_remove_freeradius" name="radiusname_remove_freeradius" class="radiusname_remove_freeradius">
				<input type="hidden" id="vendor_remove_freeradius" name="vendor_remove_freeradius" class="vendor_remove_freeradius">
				<input type="hidden" id="uid_remove_freeradius" name="uid_remove_freeradius" class="uid_remove_freeradius">
				<div class="horizontallLine"></div>
				<p>{{ _('It will impact') }} : </p>
				<div id="remove_right_impact_list">
					
				</div>
				<div id="remove_right_id_impact_list" style="display: none;">

				</div>
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_remove">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>

<!-- Modal edit -->
<div class="modal fade col-lg-12" id="modal_edit_right_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">

		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit right mod :') }}</h4>
			</div>
			<div class="modal-body">
				<div class="row">
					<div id="edit_alert_input" class="alert alert-warning" style="display: none;">

					</div>
					<form class="form-horizontal col-lg-12" role="form" name="edit_right_freeradius" action="im_crud_right_freeradius/edit" method="post">
									<div class="form-group col-lg-12">
										<label for="edit_radiusname_right_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
										<div class="col-sm-9">
											<input type="edit_radiusname_right_freeradius" class="form-control" id="edit_radiusname_right_freeradius" name="edit_radiusname_right_freeradius" placeholder="{{ _('Radius name') }}">
										</div>
									</div>

									<div class="form-group col-lg-12">
										<label for="edit_label_right_freeradius" class="col-sm-3 control-label">{{ _('Label name') }}</label>
										<div class="col-sm-9">
											<input type="edit_label_right_freeradius" class="form-control" id="edit_label_right_freeradius" name="edit_label_right_freeradius" placeholder="{{ _('Label name') }}">
										</div>
									</div>

									<div class="form-group col-lg-12">
										<label for="edit_vendor_right_freeradius" class="col-sm-3 control-label">{{ _('Select vendor') }}</label>
										<div class="col-sm-9">
											<input type="edit_vendor_right_freeradius" class="form-control" id="edit_vendor_right_freeradius" name="edit_vendor_right_freeradius" placeholder="{{ _('Vendor name') }}">
										</div>
									</div>

									<fieldset class="col-lg-12">
											<legend>{{ _('Specific vendor flag') }}</legend>
									</fieldset>
									<div class="col-lg-12 list_vendor_flag_freeradius">
										<div class="input-group col-lg-12">
											<div class="input-group">
												<span class="input-group-addon">Nom de l\'attribut</span>
												<input class="form-control" type="text" placeholder="Valeur de l\'attribut">
											</div>
										</div>
									</div>
					</form>
				</div>
			</div>
			<div class="modal-footer">
				<input type="hidden" id="uid_edit_freeradius" name="uid_edit_freeradius" class="uid_edit_freeradius">
				<input type="hidden" id="edit_previous_radiusname_right_freeradius" name="edit_previous_radiusname_right_freeradius" class="edit_previous_radiusname_right_freeradius">
				<input type="hidden" id="edit_previous_label_right_freeradius" name="edit_previous_label_right_freeradius" class="edit_previous_label_right_freeradius">
				<input type="hidden" id="edit_previous_vendor_right_freeradius" name="edit_previous_vendor_right_freeradius" class="edit_previous_vendor_right_freeradius">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_edit">{{ _('Proceed') }}</button>
			</div>
		</div>

	</div>
</div>

<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('Rights management for Freeradius') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-unlock-alt fa-fw"></i> {{ _('Rights administration') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-4">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-plus-square-o fa-fw"></i> {{ _('Add right') }}
							</div>
							<div class="panel-body">

								<div id="alert_input" class="alert alert-warning" style="display: none;">
								</div>

								<form class="form-horizontal" role="form" name="create_new_right_freeradius" action="im_crud_right_freeradius/new" method="post">
									<div class="form-group">
										<label for="radiusname_right_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
										<div class="col-sm-9">
											<input type="radiusname_right_freeradius" class="form-control" id="radiusname_right_freeradius" name="radiusname_right_freeradius" placeholder="{{ _('Radius name') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="label_right_freeradius" class="col-sm-3 control-label">{{ _('Label name') }}</label>
<!--										<div class="col-sm-9">
											<input type="label_right_freeradius" class="form-control" id="label_right_freeradius" name="label_right_freeradius" placeholder="{{ _('Label name') }}">
										</div> -->

										<div id="autocomplete_label_right_freeradius" class="col-sm-9">
											<input id="label_right_freeradius" name="label_right_freeradius" class="typeahead" type="label_right_freeradius" placeholder="{{ _('Label name') }}">
										</div>

									</div>

									<div class="form-group">
										<label for="vendor_right_freeradius" class="col-sm-3 control-label">{{ _('Select vendor') }}</label>
										<div class="col-sm-9">
											<input type="vendor_right_freeradius" class="form-control" id="vendor_right_freeradius" name="vendor_right_freeradius" placeholder="{{ _('Vendor name') }}">
										</div>
									</div>

									<fieldset class="col-lg-12">
											<legend>{{ _('Specific vendor flag') }}</legend>
									</fieldset>
									<div class="col-lg-12 list_vendor_flag_freeradius">
									</div>

									<div class="form-group">
										<div class="col-sm-offset-3 col-sm-9">
											<button id="add_vendor_right_freeradius" type="button" class="btn btn-default">{{ _('Add right') }}</button>
										</div>
									</div>
								</form>
							</div>
						</div>
					</div>
					<div class="col-lg-8">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-list fa-fw"></i> {{ _('Right list') }}
							</div>
							<div class="panel-body">
								<div class="table-responsive">
										<!-- ICI DATATABLE -->
									<table class="table table-striped table-bordered table-hover" id="dataTables-right_list_freeradius">
										<thead>
											<tr>
												<th>{{ _('Radius') }}</th>
												<th>{{ _('Label') }}</th>
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
		<script src="/web/js/im_crud_right_freeradius.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}