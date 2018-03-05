{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<!-- Modal remove range -->
<div class="modal fade" id="modal_delete_range_shared_secret_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="rangename_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('You are about to delete') }} <strong><span class="rangename_remove_freeradius"></span></strong> {{ _('subnet') }} <strong><span class="subnet_remove_freeradius"></span></strong> {{ _('from') }} <strong><span class="radiusname_remove_freeradius"></span></strong>
				<input type="hidden" id="rangename_remove_freeradius" name="rangename_remove_freeradius" class="rangename_remove_freeradius">
				<input type="hidden" id="radiusname_remove_freeradius" name="radiusname_remove_freeradius" class="radiusname_remove_freeradius">
				<input type="hidden" id="uid_remove_freeradius" name="uid_remove_freeradius" class="uid_remove_freeradius">
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_remove_range">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>

<!-- Modal edit range-->
<div class="modal fade col-lg-12" id="modal_edit_range_shared_secret_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">

		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit range mod :') }}</h4>
			</div>
			<div class="modal-body">
				<div class="row">
					<form class="form-horizontal" role="form" name="edit_range_shared_secret_freeradius" action="im_crud_range_freeradius/edit" method="post">

						<div class="form-group">
							<label for="edit_range_radiusname_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
							<div class="col-sm-9">
								<input type="edit_range_radiusname_shared_secret_freeradius" class="form-control" id="edit_range_radiusname_shared_secret_freeradius" name="edit_range_radiusname_shared_secret_freeradius" placeholder="{{ _('Radius name') }}">
							</div>
						</div>
						<div class="form-group">
							<label for="edit_range_name_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Range name') }}</label>
							<div class="col-sm-9">
								<input type="edit_range_name_shared_secret_freeradius" class="form-control" id="edit_range_name_shared_secret_freeradius" name="edit_range_name_shared_secret_freeradius" placeholder="{{ _('Name') }}">
							</div>
						</div>
						<div class="form-group">
							<label for="edit_range_subnet_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Subnet') }}</label>
							<div class="col-sm-9">
								<input type="edit_range_subnet_shared_secret_freeradius" class="form-control" id="edit_range_subnet_shared_secret_freeradius" name="edit_range_subnet_shared_secret_freeradius" placeholder="{{ _('Subnet') }}">
							</div>
						</div>
<!--						
						<div class="form-group">
							<label for="edit_range_sharedsecret_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
							<div class="col-sm-9">
								<input type="edit_range_sharedsecret_shared_secret_freeradius" class="form-control" id="edit_range_sharedsecret_shared_secret_freeradius" name="edit_range_sharedsecret_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
							</div>
						</div>
-->
						<div class="form-group">
							<label for="edit_range_sharedsecret_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
							<div class="col-sm-9" align="center">
								<div class="col-sm-12 form-group input-group">
									<input type="password" class="form-control" id="edit_range_sharedsecret_shared_secret_freeradius" name="edit_range_sharedsecret_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
									<span class="input-group-btn">
										<button id="edit_show_hide_range_sharedsecret_freeradius" class="btn btn-default" type="button"><i id="edit_icon_show_hide_range_sharedsecret_freeradius" class="fa fa-eye"></i>
										</button>
									</span>
								</div>
							</div>
						</div>

					</form>
				</div>
			</div>
			<div class="modal-footer">
				<input type="hidden" id="uid_edit_freeradius" name="uid_edit_freeradius" class="uid_edit_freeradius">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_edit_range">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>



<!-- Modal remove -->
<div class="modal fade" id="modal_delete_shared_secret_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="shared_secret_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('You are about to delete') }} {{ _('shared secret') }} <strong><span class="shared_secret_name_remove_freeradius"></span></strong> {{ _('from') }} <strong><span class="radiusname_remove_freeradius"></span></strong>

				<input type="hidden" id="shared_secret_name_remove_freeradius" name="shared_secret_name_remove_freeradius" class="shared_secret_name_remove_freeradius">
				<input type="hidden" id="radiusname_remove_freeradius" name="radiusname_remove_freeradius" class="radiusname_remove_freeradius">
				<input type="hidden" id="uid_remove_freeradius" name="uid_remove_freeradius" class="uid_remove_freeradius">
				<div class="horizontallLine"></div>
				<p>{{ _('It will impact') }} : </p>
				<div id="remove_shared_secret_impact_list">
					
				</div>
				<div id="remove_shared_secret_id_impact_list" style="display: none;">

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
<div class="modal fade col-lg-12" id="modal_edit_shared_secret_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">

		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit shared secret mod :') }}</h4>
			</div>
			<div class="modal-body">
				<div class="row">
					<div id="edit_alert_input" class="alert alert-warning" style="display: none;">

					</div>
					<form class="form-horizontal col-lg-12" role="form" name="edit_shared_secret_freeradius" action="im_crud_shared_secret_freeradius/edit" method="post">

						<div class="form-group col-lg-12">
							<label for="edit_radiusname_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
							<div class="col-sm-9">
								<input type="edit_radiusname_shared_secret_freeradius" class="form-control" id="edit_radiusname_shared_secret_freeradius" name="edit_radiusname_shared_secret_freeradius" placeholder="{{ _('Radius name') }}">
								<input type="hidden" id="edit_previous_radiusname_shared_secret_freeradius" name="edit_previous_radiusname_shared_secret_freeradius">
							</div>
						</div>
						<div class="form-group col-lg-12">
							<label for="edit_name_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Name') }}</label>
							<div class="col-sm-9">
								<input type="edit_name_shared_secret_freeradius" class="form-control" id="edit_name_shared_secret_freeradius" name="edit_name_shared_secret_freeradius" placeholder="{{ _('Name') }}">
								<input type="hidden" id="edit_previous_name_shared_secret_freeradius" name="edit_previous_name_shared_secret_freeradius">
							</div>
						</div>
<!--
						<div class="form-group col-lg-12">
							<label for="edit_key_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
							<div class="col-sm-9">
								<input type="edit_key_shared_secret_freeradius" class="form-control" id="edit_key_shared_secret_freeradius" name="edit_key_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
							</div>
						</div>
-->
						<div class="form-group col-lg-12">
							<label for="edit_key_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
							<div class="col-sm-9" align="center">
								<div class="col-sm-12 form-group input-group">
									<input type="password" class="form-control" id="edit_key_shared_secret_freeradius" name="edit_key_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
									<span class="input-group-btn">
										<button id="edit_show_hide_shared_secret_freeradius" class="btn btn-default" type="button"><i id="edit_icon_show_hide_shared_secret_freeradius" class="fa fa-eye"></i>
										</button>
									</span>
								</div>
							</div>
						</div>

						<div class="form-group col-lg-12">
							<label for="edit_comment_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Comment') }}</label>
							<div class="col-sm-9">
								<input type="edit_comment_shared_secret_freeradius" class="form-control" id="edit_comment_shared_secret_freeradius" name="edit_comment_shared_secret_freeradius" placeholder="{{ _('Comment') }}">
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
			<h1 class="page-header">{{ _('Shared secret management for Freeradius') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-folder-o fa-fw"></i> {{ _('Shared secret administration') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-4">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-folder-open-o fa-fw"></i> {{ _('Add shared secret') }}
							</div>
							<div class="panel-body">

								<div id="alert_input" class="alert alert-warning" style="display: none;">
								</div>
								
								<form class="form-horizontal" role="form" name="create_new_shared_secret_freeradius" action="im_crud_shared_secret_freeradius/new" method="post">
									<div class="form-group">
										<label for="radiusname_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
										<div class="col-sm-9">
											<input type="radiusname_shared_secret_freeradius" class="form-control" id="radiusname_shared_secret_freeradius" name="radiusname_shared_secret_freeradius" placeholder="{{ _('Radius name') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="name_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Name') }}</label>
										<div class="col-sm-9">
											<input type="name_shared_secret_freeradius" class="form-control" id="name_shared_secret_freeradius" name="name_shared_secret_freeradius" placeholder="{{ _('Name') }}">
										</div>
									</div>
<!--
									<div class="form-group">
										<label for="key_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
										<div class="col-sm-9">
											<input type="key_shared_secret_freeradius" class="form-control" id="key_shared_secret_freeradius" name="key_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
										</div>
									</div>
-->
									<div class="form-group">
										<label for="key_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
										<div class="col-sm-9" align="center">
											<div class="col-sm-12 form-group input-group">
												<input type="password" class="form-control" id="key_shared_secret_freeradius" name="key_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
												<span class="input-group-btn">
													<button id="show_hide_shared_secret_freeradius" class="btn btn-default" type="button"><i id="icon_show_hide_shared_secret_freeradius" class="fa fa-eye"></i>
													</button>
												</span>
											</div>
										</div>
									</div>

									<div class="form-group">
										<label for="comment_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Comment') }}</label>
										<div class="col-sm-9">
											<input type="comment_shared_secret_freeradius" class="form-control" id="comment_shared_secret_freeradius" name="comment_shared_secret_freeradius" placeholder="{{ _('Comment') }}">
										</div>
									</div>

									<div class="form-group">
										<div class="col-sm-offset-3 col-sm-9">
											<button id="add_shared_secret_freeradius" type="button" class="btn btn-default">{{ _('Add shared secret') }}</button>
										</div>
									</div>

								</form>

							</div>
						</div>
					</div>
					<div class="col-lg-8">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-list fa-fw"></i> {{ _('Shared secret list') }}
							</div>
							<div class="panel-body">
								<div class="table-responsive">
									<!-- ICI DATATABLE -->
									<table class="table table-striped table-bordered table-hover" id="dataTables-shared_secret_list_freeradius">
										<thead>
											<tr>
												<th>{{ _('Radius') }}</th>
												<th>{{ _('Name') }}</th>
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

	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-sitemap fa-fw"></i> {{ _('Range Shared secret administration') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-4">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-unlink fa-fw"></i> {{ _('Define range') }}
							</div>
							<div class="panel-body">

								<div id="alert_range_input" class="alert alert-warning" style="display: none;">
								</div>

								<form class="form-horizontal" role="form" name="create_new_shared_secret_freeradius" action="im_crud_range_freeradius/new" method="post">

									<div class="form-group">
										<label for="range_radiusname_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
										<div class="col-sm-9">
											<input type="range_radiusname_shared_secret_freeradius" class="form-control" id="range_radiusname_shared_secret_freeradius" name="range_radiusname_shared_secret_freeradius" placeholder="{{ _('Radius name') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="range_name_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Range name') }}</label>
										<div class="col-sm-9">
											<input type="range_name_shared_secret_freeradius" class="form-control" id="range_name_shared_secret_freeradius" name="range_name_shared_secret_freeradius" placeholder="{{ _('Name') }}">
										</div>
									</div>

									<div class="form-group">
										<label for="range_subnet_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Subnet') }}</label>
										<div class="col-sm-9">
											<input type="range_subnet_shared_secret_freeradius" class="form-control" id="range_subnet_shared_secret_freeradius" name="range_subnet_shared_secret_freeradius" placeholder="{{ _('Subnet') }}">
										</div>
									</div>
<!--
									<div class="form-group">
										<label for="range_sharedsecret_shared_secret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
										<div class="col-sm-9">
											<input type="range_sharedsecret_shared_secret_freeradius" class="form-control" id="range_sharedsecret_shared_secret_freeradius" name="range_sharedsecret_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
										</div>
									</div>
-->
									<div class="form-group">
										<label for="range_sharedsecret_freeradius" class="col-sm-3 control-label">{{ _('Shared secret') }}</label>
										<div class="col-sm-9" align="center">
											<div class="col-sm-12 form-group input-group">
												<input type="password" class="form-control" id="range_sharedsecret_shared_secret_freeradius" name="range_sharedsecret_shared_secret_freeradius" placeholder="{{ _('Shared secret') }}">
												<span class="input-group-btn">
													<button id="show_hide_range_sharedsecret_freeradius" class="btn btn-default" type="button"><i id="icon_show_hide_range_sharedsecret_freeradius" class="fa fa-eye"></i>
													</button>
												</span>
											</div>
										</div>
									</div>

									<div class="form-group">
										<div class="col-sm-offset-3 col-sm-9">
											<button id="add_range_shared_secret_freeradius" type="button" class="btn btn-default">{{ _('Add range') }}</button>
										</div>
									</div>

								</form>

							</div>
						</div>
					</div>
					<div class="col-lg-8">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-list fa-fw"></i> {{ _('Range list') }}
							</div>
							<div class="panel-body">
								<div class="table-responsive">
									<!-- ICI DATATABLE -->
									<table class="table table-striped table-bordered table-hover" id="dataTables-range_shared_secret_list_freeradius">
										<thead>
											<tr>
												<th>{{ _('Radius') }}</th>
												<th>{{ _('Range name') }}</th>
												<th>{{ _('Subnet') }}</th>
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
		<script src="/web/js/im_crud_shared_secret_freeradius.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}