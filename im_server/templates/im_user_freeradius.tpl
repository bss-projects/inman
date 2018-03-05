{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<!-- Modal remove -->
<div class="modal fade" id="modal_delete_user_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="user_remove_freeradius"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('You are about to delete') }} <strong><span class="user_remove_freeradius"></span></strong> {{ _('from') }} <strong><span class="radiusname_remove_freeradius"></span></strong>
				<input type="hidden" id="user_remove_freeradius" name="user_remove_freeradius" class="user_remove_freeradius">
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
<div class="modal fade" id="modal_edit_user_freeradius" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit user mod :') }}</h4>
			</div>

			<div class="modal-body">
				<div id="edit_alert_input" class="alert alert-warning" style="display: none;">

				</div>
				<form class="form-horizontal" role="form" name="edit_user_freeradius" action="im_crud_user_freeradius/edit" method="post">

					<div id="edit_expiration_status" class="form-group" style="display: none;">
						<label class="col-sm-3 label label-warning label-pill">{{ _('Account expired') }}</label>
						<div class="col-sm-9"></div>
					</div>

					<div class="form-group">
						<label for="edit_radiusname_user_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
						<div class="col-sm-9">
							<input type="edit_radiusname_user_freeradius" class="form-control" id="edit_radiusname_user_freeradius" name="edit_radiusname_user_freeradius" placeholder="{{ _('Radius name') }}">
							<input type="hidden" id="edit_previous_radiusname_user_freeradius" name="edit_previous_radiusname_user_freeradius">
						</div>
					</div>

					<div class="form-group">
						<div class="col-sm-offset-3 col-sm-9">
							<input id="im_edit_user_local_freeradius" type="checkbox" name="im_edit_user_local_freeradius" checked>
						</div>
					</div>

					<div class="form-group">
						<label for="edit_name_user_freeradius" class="col-sm-3 control-label">{{ _('Username') }}</label>
						<div class="col-sm-9">
							<input type="edit_name_user_freeradius" class="form-control" id="edit_name_user_freeradius" name="edit_name_user_freeradius" placeholder="{{ _('Username') }}">
							<input type="hidden" id="edit_previous_name_user_freeradius" name="edit_previous_name_user_freeradius">
						</div>
					</div>

					<div id="div_edit_password_user_freeradius" class="form-group" style="display:none">
						<label for="edit_password_user_freeradius" class="col-sm-3 control-label">{{ _('Password') }}</label>
						<div class="col-sm-9">
							<input type="edit_password_user_freeradius" class="form-control" id="edit_password_user_freeradius" name="edit_password_user_freeradius" placeholder="{{ _('Password') }}">
						</div>
					</div>

					<div class="form-group">
						<label for="edit_right_user_freeradius" class="col-sm-3 control-label">{{ _('Right') }}</label>
						<div class="col-sm-9">
							<input type="edit_right_user_freeradius" class="form-control" id="edit_right_user_freeradius" name="edit_right_user_freeradius" placeholder="{{ _('Right') }}">
						</div>
					</div>

					<div class="form-group">
						<label for="edit_expiration_date_user_freeradius" class="col-sm-3 control-label">{{ _('Expire on') }}</label>
						<div class="col-sm-9">
							<input type="edit_expiration_date_user_freeradius" class="form-control" id="edit_expiration_date_user_freeradius" name="edit_expiration_date_user_freeradius" placeholder="">
						</div>
					</div>

					<div class="form-group">
						<label for="edit_perimeter_user_freeradius" class="col-sm-3 control-label">{{ _('Perimeter') }}</label>
						<div class="col-sm-9 im_relative">
							<input type="edit_perimeter_user_freeradius" class="form-control" id="edit_perimeter_user_freeradius" name="edit_perimeter_user_freeradius" placeholder="{{ _('Perimeter') }}">
							<div id="edit_perimeter_select_freeradius" class=" overlay">
								<ul class="list-unstyled">

								</ul>
							</div>
						</div>
												
					</div>

					<div class="form-group">
						<div class="col-sm-12 edit_perimeter_list_user_freeradius">
							<div class="table-responsive">
								<table id="edit_tab_list_perimeter_user_freeradius" class="table table-hover">
									<thead>
										<tr>
											<th>Perimeter</th>
											<th><i class="fa fa-gear"></i></th>
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

			<div class="modal-footer">
				<input type="hidden" id="uid_edit_freeradius" name="uid_edit_freeradius" class="uid_edit_freeradius">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_edit">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>

<input id="conf_filepath" type="hidden" name="conf_filepath" value="{{ conf_filepath }}" />

<div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">{{ _('User management for Freeradius') }}</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-12">

                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-users fa-fw"></i> {{ _('Users administration') }}
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">

							<div class="col-lg-4">

								<div class="panel panel-default">
									<div class="panel-heading">
										<i class="fa fa-user fa-fw"></i> {{ _('Add user') }}
									</div>
									<div class="panel-body">
										
										<div id="alert_input" class="alert alert-warning" style="display: none;">
										</div>

										<form class="form-horizontal" role="form" name="create_new_user_freeradius" action="im_crud_user_freeradius/new" method="post">

											<div class="form-group">
												<label for="radiusname_user_freeradius" class="col-sm-3 control-label">{{ _('Radius name') }}</label>
												<div class="col-sm-9">
													<input type="radiusname_user_freeradius" class="form-control" id="radiusname_user_freeradius" name="radiusname_user_freeradius" placeholder="{{ _('Radius name') }}">
												</div>
											</div>

											<div class="form-group">
												<div class="col-sm-offset-3 col-sm-9">
													<input id="im_user_local_freeradius" type="checkbox" name="im_user_local_freeradius" checked>
												</div>
											</div>

											<div class="form-group">
												<label for="name_user_freeradius" class="col-sm-3 control-label">{{ _('Username') }}</label>
												<div class="col-sm-9">
													<input type="name_user_freeradius" class="form-control" id="name_user_freeradius" name="name_user_freeradius" placeholder="{{ _('Username') }}">
												</div>
											</div>

											<div id="div_password_user_freeradius" class="form-group" style="display:none">
												<label for="password_user_freeradius" class="col-sm-3 control-label">{{ _('Password') }}</label>
												<div class="col-sm-9">
													<input type="password_user_freeradius" class="form-control" id="password_user_freeradius" name="password_user_freeradius" placeholder="{{ _('Password') }}">
												</div>
											</div>

											<div class="form-group">
												<label for="right_user_freeradius" class="col-sm-3 control-label">{{ _('Right') }}</label>
												<div class="col-sm-9">
													<input type="right_user_freeradius" class="form-control" id="right_user_freeradius" name="right_user_freeradius" placeholder="{{ _('Right') }}">
												</div>
											</div>

											<div class="form-group">
												<label for="expiration_date_user_freeradius" class="col-sm-3 control-label">{{ _('Expire on') }}</label>
												<div class="col-sm-9">
													<input type="expiration_date_user_freeradius" class="form-control" id="expiration_date_user_freeradius" name="expiration_date_user_freeradius" placeholder="">
												</div>
											</div>

											<div class="form-group">


												<label for="perimeter_user_freeradius" class="col-sm-3 control-label">{{ _('Perimeter') }}</label>
												<div class="col-sm-9 im_relative">
													<input type="perimeter_user_freeradius" class="form-control" id="perimeter_user_freeradius" name="perimeter_user_freeradius" placeholder="{{ _('Perimeter') }}">
													<div id="perimeter_select_freeradius" class=" overlay">
														<ul class="list-unstyled">

														</ul>
													</div>
												</div>
												
											</div>

											<div class="form-group">
												<div class="col-sm-12 perimeter_list_user_freeradius">
													<div class="table-responsive">
														<table id="tab_list_perimeter_user_freeradius" class="table table-hover">
															<thead>
																<tr>
																	<th>Perimeter</th>
																	<th><i class="fa fa-gear"></i></th>
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
													<button id="add_user_freeradius" type="button" class="btn btn-default">{{ _('Add') }}</button>
												</div>
											</div>

										</form>
									</div>
                        		</div>
<!-- Bloc prevu pour le duplication d'un user existant pour faciliter la creation d'un user en prenant exemple sur un connu
                        		<div class="panel panel-default">
									<div class="panel-heading">
										<i class="fa fa-copy fa-fw"></i> {{ _('Duplicate user') }}
									</div>
									<div class="panel-body">
										<form class="form-horizontal" role="form" name="duplicate_user_freeradius" action="im_crud_user_freeradius/duplicate" method="post">

											<div class="form-group">
												<label for="model_user_freeradius" class="col-sm-3 control-label">{{ _('Model') }}</label>
												<div class="col-sm-9">
													<input type="model_user_freeradius" class="form-control" id="model_user_freeradius" name="model_user_freeradius" placeholder="{{ _('Model') }}">
												</div>
											</div>

											<div class="form-group">
												<div class="col-sm-offset-3 col-sm-9">
													<input id="im_model_user_local_freeradius" type="checkbox" name="im_model_user_local_freeradius" checked>
												</div>
											</div>

											<div class="form-group">
												<label for="name_model_user_freeradius" class="col-sm-3 control-label">{{ _('Username') }}</label>
												<div class="col-sm-9">
													<input type="name_model_user_freeradius" class="form-control" id="name_model_user_freeradius" name="name_model_user_freeradius" placeholder="{{ _('Username') }}" disabled>
												</div>
											</div>

											<div id="div_password_model_user_freeradius" class="form-group" style="display:none">
												<label for="password_model_user_freeradius" class="col-sm-3 control-label">{{ _('Password') }}</label>
												<div class="col-sm-9">
													<input type="password_model_user_freeradius" class="form-control" id="password_user_model_freeradius" name="password_user_model_freeradius" placeholder="{{ _('Password') }}" disabled>
												</div>
											</div>

											<div class="form-group">
												<div class="col-sm-offset-3 col-sm-9">
													<button id="duplicate_user_freeradius" type="button" class="btn btn-default">{{ _('Add') }}</button>
												</div>
											</div>

										</form>
									</div>
                        		</div>
-->
                    		</div>

                    		<div class="col-lg-8">

                    			<div class="panel panel-default">
									<div class="panel-heading">
										<i class="fa fa-list fa-fw"></i> {{ _('User list') }}
									</div>
									<div class="panel-body">
										<div class="table-responsive">
										<!-- ICI DATATABLE -->
											<table class="table table-striped table-bordered table-hover" id="dataTables-user_list_freeradius">
												<thead>
													<tr>
														<th>{{ _('Radius') }}</th>
														<th>{{ _('Username') }}</th>
														<th>{{ _('Right') }}</th>
														<th>{{ _('Connection') }}</th>
														<th>{{ _('Status') }}</th>
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
		<script src="/web/js/plugins/inputmask/inputmask.js"></script>
		<script src="/web/js/plugins/inputmask/inputmask.extensions.js"></script>
		<script src="/web/js/plugins/inputmask/inputmask.numeric.extensions.js"></script>
		<script src="/web/js/plugins/inputmask/inputmask.date.extensions.js"></script>
		<script src="/web/js/plugins/inputmask/jquery.inputmask.js"></script>
		<script src="/web/js/im_crud_user_freeradius.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}
