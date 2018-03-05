{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<!-- Modal remove -->
<div class="modal fade" id="modal_delete_network_perimeter_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="network_perimeter_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				<p> {{ _('You are about to delete') }} <strong><span class="network_perimeter_remove_freeradius"></span></strong> {{ _('from') }} <strong><span class="radiusname_remove_freeradius"></span></strong> </p>
				<input type="hidden" id="network_perimeter_remove_freeradius" name="network_perimeter_remove_freeradius" class="network_perimeter_remove_freeradius">
				<input type="hidden" id="radiusname_remove_freeradius" name="radiusname_remove_freeradius" class="radiusname_remove_freeradius">
				<input type="hidden" id="type_network_perimeter_remove_freeradius" name="type_network_perimeter_remove_freeradius" class="type_network_perimeter_remove_freeradius">
				<input type="hidden" id="ip_network_perimeter_remove_freeradius" name="ip_network_perimeter_remove_freeradius" class="ip_network_perimeter_remove_freeradius">
				<input type="hidden" id="uid_remove_freeradius" name="uid_remove_freeradius" class="uid_remove_freeradius">
				<div class="horizontallLine"></div>
				<p>{{ _('It will impact') }} : </p>
				<div id="remove_network_perimeter_impact_list">
					
				</div>
				<div id="remove_network_perimeter_id_impact_list" style="display: none;">

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
<div class="modal fade col-lg-12" id="modal_edit_network_perimeter_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit network perimeter mod :') }}</h4>
			</div>
			<div class="modal-body">
				<div class="row">
					<div id="edit_alert_input" class="alert alert-warning" style="display: none;">

					</div>
					<form class="form-horizontal col-lg-12" role="form" name="edit_network_perimeter_freeradius" action="im_crud_network_perimeter_freeradius/edit" method="post">

						<div class="form-group col-lg-12">
							<label for="edit_radiusname_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
							<div class="col-sm-9">
								<input type="edit_radiusname_network_perimeter_freeradius" class="form-control" id="edit_radiusname_network_perimeter_freeradius" name="edit_radiusname_network_perimeter_freeradius" placeholder="{{ _('Radius name') }}">
							</div>
						</div>
	
						<div class="form-group col-lg-12">
							<label for="edit_name_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Perimeter name') }}</label>
							<div class="col-sm-9">
								<input type="edit_name_network_perimeter_freeradius" class="form-control" id="edit_name_network_perimeter_freeradius" name="edit_name_network_perimeter_freeradius" placeholder="{{ _('Perimeter name') }}">
								<input type="hidden" id="edit_name_previous_network_perimeter_freeradius" name="edit_name_previous_network_perimeter_freeradius">
							</div>
						</div>

						<div id="edit_subnet_div" class="form-group col-lg-12" style="display: none;">
							<fieldset class="col-lg-12">
								<legend>{{ _('Subnet perimeter') }}</legend>
							</fieldset>

							<label for="edit_ip_start_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('First IP') }}</label>
							<div class="col-sm-9">
								<input type="edit_ip_start_network_perimeter_freeradius" class="form-control" id="edit_ip_start_network_perimeter_freeradius" name="edit_ip_start_network_perimeter_freeradius" placeholder="{{ _('First IP') }}">
								<input type="hidden" id="edit_ip_start_previous_network_perimeter_freeradius" name="edit_ip_start_previous_network_perimeter_freeradius">
							</div>

							<label for="edit_ip_end_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Last IP') }}</label>
							<div class="col-sm-9">
								<input type="edit_ip_end_network_perimeter_freeradius" class="form-control" id="edit_ip_end_network_perimeter_freeradius" name="edit_ip_end_network_perimeter_freeradius" placeholder="{{ _('Last IP') }}">
								<input type="hidden" id="edit_ip_end_previous_network_perimeter_freeradius" name="edit_ip_end_previous_network_perimeter_freeradius">
							</div>

						</div>
						

						<div id="edit_ip_list_div" class="form-group col-lg-12" style="display: none;">
							<fieldset class="col-lg-12">
								<legend>{{ _('IP list perimeter') }}</legend>
							</fieldset>

							<label for="edit_selectip_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Select an IP') }}</label>
							<div class="col-sm-9">
								<input type="edit_selectip_network_perimeter_freeradius" class="form-control" id="edit_selectip_network_perimeter_freeradius" name="edit_selectip_network_perimeter_freeradius" placeholder="{{ _('Select an IP') }}">
							</div>

							<div class="col-sm-12 limit_list_ip_perimeter_freeradius">
								<input type="hidden" id="edit_list_ip_previous_perimeter_freeradius" name="edit_list_ip_previous_perimeter_freeradius">
								<div class="table-responsive">
									<table id="edit_tab_list_ip_perimeter_freeradius" class="table table-hover">
										<thead>
											<tr>
												<th>IP</th>
												<th>Action</th>
											</tr>
										</thead>
										<tbody>
												
										</tbody>
									</table>
								</div>
							</div>
						</div>
					</form>
				</div>
			</div>
			<div class="modal-footer">
				<input type="hidden" id="uid_edit_freeradius" name="uid_edit_freeradius" class="uid_edit_freeradius">
				<input type="hidden" id="edit_type_network_perimeter_freeradius" name="edit_type_network_perimeter_freeradius" class="edit_type_network_perimeter_freeradius">
				<input type="hidden" id="ip_network_perimeter_edit_freeradius" name="ip_network_perimeter_edit_freeradius" class="ip_network_perimeter_edit_freeradius">
				<div id="edit_network_perimeter_id_impact_list" style="display: none;">

				</div>
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_edit">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>

<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('Network perimeter management for Freeradius') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-sitemap fa-fw"></i> {{ _('Network perimeter administration') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-4">

						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-plus-square-o fa-fw"></i> {{ _('Add perimeter') }}
							</div>
							<div class="panel-body">

								<div id="alert_input" class="alert alert-warning" style="display: none;">
								</div>

								<form class="form-horizontal" role="form" name="create_new_network_perimeter_freeradius" action="im_crud_network_perimeter_freeradius/new" method="post">
									<div class="form-group">
										<label for="radiusname_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
										<div class="col-sm-9">
											<input type="radiusname_network_perimeter_freeradius" class="form-control" id="radiusname_network_perimeter_freeradius" name="radiusname_network_perimeter_freeradius" placeholder="{{ _('Radius name') }}">
										</div>
									</div>

									<div class="form-group">
										<fieldset class="col-lg-12">
											<legend>{{ _('Subnet perimeter') }}</legend>
										</fieldset>

										<label for="label_subnet_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Label') }}</label>
										<div class="col-sm-9">
											<input type="label_subnet_network_perimeter_freeradius" class="form-control" id="label_subnet_network_perimeter_freeradius" name="label_subnet_network_perimeter_freeradius" placeholder="{{ _('Subnet label') }}">
										</div>

										<label for="ip_start_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('First IP') }}</label>
										<div class="col-sm-9">
											<input type="ip_start_network_perimeter_freeradius" class="form-control" id="ip_start_network_perimeter_freeradius" name="ip_start_network_perimeter_freeradius" placeholder="{{ _('First IP') }}">
										</div>

										<label for="ip_end_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Last IP') }}</label>
										<div class="col-sm-9">
											<input type="ip_end_network_perimeter_freeradius" class="form-control" id="ip_end_network_perimeter_freeradius" name="ip_end_network_perimeter_freeradius" placeholder="{{ _('Last IP') }}">
										</div>

										<div class="col-sm-offset-3 col-sm-9">
											<button id="im_add_subnet_network_perimeter_freeradius" class="btn btn-default" type="button">
												<i class="fa fa-plus-circle"></i>
													{{ _('Add new perimeter') }}
											</button>
										</div>

									</div>

									<div class="form-group">
										<fieldset class="col-lg-12">
											<legend>{{ _('IP list perimeter') }}</legend>
										</fieldset>

										<label for="label_listip_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Label') }}</label>
										<div class="col-sm-9">
											<input type="label_listip_network_perimeter_freeradius" class="form-control" id="label_listip_network_perimeter_freeradius" name="label_listip_network_perimeter_freeradius" placeholder="{{ _('IP list label') }}">
										</div>

										<label for="selectip_network_perimeter_freeradius" class="col-sm-3 control-label">{{ _('Select an IP') }}</label>
										<div class="col-sm-9">
											<input type="selectip_network_perimeter_freeradius" class="form-control" id="selectip_network_perimeter_freeradius" name="selectip_network_perimeter_freeradius" placeholder="{{ _('Select an IP') }}">
										</div>

										<div class="col-sm-12 limit_list_ip_perimeter_freeradius">
											<div class="table-responsive">
												<table id="tab_list_ip_perimeter_freeradius" class="table table-hover">
													<thead>
														<tr>
															<th>IP</th>
															<th>Action</th>
														</tr>
													</thead>
													<tbody>
														
													</tbody>
												</table>
											</div>
										</div>
                            

									</div>

									<div class="form-group">
										<div class="col-sm-offset-3 col-sm-9">
											<button id="im_add_listip_network_perimeter_freeradius" class="btn btn-default" type="button">
												<i class="fa fa-plus-circle"></i>
													{{ _('Add new perimeter') }}
											</button>
										</div>
									</div>
								</form>
							</div>
						</div>
					</div>
					<div class="col-lg-8">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-list fa-fw"></i> {{ _('Perimeter list') }}
							</div>
							<div class="panel-body">
								<div class="table-responsive">
										<!-- ICI DATATABLE -->
									<table class="table table-striped table-bordered table-hover" id="dataTables-network_perimeter_list_freeradius">
										<thead>
											<tr>
												<th>{{ _('Radius') }}</th>
												<th>{{ _('Perimeter') }}</th>
												<th>{{ _('Type') }}</th>
												<th>{{ _('IP') }}</th>
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
		<script src="/web/js/im_crud_network_perimeter_freeradius.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}