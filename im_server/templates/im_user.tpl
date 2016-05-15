{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<!-- Modal remove -->
<div class="modal fade" id="modal_delete_user" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="user_remove"></div></h4>
			</div>
			<div class="modal-body">
				{{ _('You are about to delete') }} <strong><span class="user_remove"></span></strong>
				<input type="hidden" id="user_remove" name="user_remove" class="user_remove">
				<input type="hidden" id="uid_remove" name="uid_remove" class="uid_remove">
			</div>
			<div class="modal-footer">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_remove">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>

<!-- Modal edit -->
<div class="modal fade" id="modal_edit_user" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
	<div class="modal-dialog">
		<div class="modal-content">
			<div class="modal-header">
				<button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
				<h4 class="modal-title" id="myModalLabel">{{ _('Edit user mod :') }}</h4>
			</div>

			<div class="modal-body">
				<form class="form-horizontal" role="form" name="edit_user" action="im_crud_user/edit" method="post">

					<div class="form-group">
						<label for="edit_login_user" class="col-sm-3 control-label">{{ _('Login') }}</label>
						<div class="col-sm-9">
							<input type="edit_login_user" class="form-control" id="edit_login_user" name="edit_login_user" placeholder="{{ _('Login') }}">
						</div>
					</div>

					<div class="form-group">
						<label for="edit_password_user" class="col-sm-3 control-label">{{ _('Password') }}</label>
						<div class="col-sm-9">
							<input type="password" class="form-control" id="edit_password_user" name="edit_password_user" placeholder="{{ _('Password') }}">
						</div>
					</div>

					<div class="form-group">
						<label for="edit_firstname_user" class="col-sm-3 control-label">{{ _('Firstname') }}</label>
						<div class="col-sm-9">
							<input type="edit_firstname_user" class="form-control" id="edit_firstname_user" name="edit_firstname_user" placeholder="{{ _('Firstname') }}">
						</div>
					</div>

					<div class="form-group">
						<label for="edit_lastname_user" class="col-sm-3 control-label">{{ _('Lastname') }}</label>
						<div class="col-sm-9">
							<input type="edit_lastname_user" class="form-control" id="edit_lastname_user" name="edit_lastname_user" placeholder="{{ _('Lastname') }}">
						</div>
					</div>

					<div class="form-group">
						<label for="edit_plugin_user" class="col-sm-3 control-label">{{ _('Plugin') }}</label>
						<div class="col-sm-9">
							<input type="edit_plugin_user" class="form-control" id="edit_plugin_user" name="edit_plugin_user" placeholder="{{ _('Plugin') }}">
						</div>
					</div>

					<div class="form-group">
						<table id="edit_tab_plugin_right" class="col-sm-offset-3 col-sm-9">
							<tbody>
								<tr><td></td></tr>
							</tbody>
						</table>
					</div>

				</form>
			</div>

			<div class="modal-footer">
				<input type="hidden" id="uid_edit" name="uid_edit" class="uid_edit">
				<button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
				<button type="button" class="btn btn-primary" id="proceed_edit">{{ _('Proceed') }}</button>
			</div>
		</div>
	</div>
</div>

<div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">{{ _('User management for InMan') }}</h1>
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
										
										<form class="form-horizontal" role="form" name="create_new_user" action="im_crud_user/new" method="post">

											<div class="form-group">
												<label for="login_user" class="col-sm-3 control-label">{{ _('Login') }}</label>
												<div class="col-sm-9">
													<input type="login_user" class="form-control" id="login_user" name="login_user" placeholder="{{ _('Login') }}">
												</div>
											</div>

											<div class="form-group">
												<label for="password_user" class="col-sm-3 control-label">{{ _('Password') }}</label>
												<div class="col-sm-9">
													<input type="password" class="form-control" id="password_user" name="password_user" placeholder="{{ _('Password') }}">
												</div>
											</div>

											<div class="form-group">
												<label for="firstname_user" class="col-sm-3 control-label">{{ _('Firstname') }}</label>
												<div class="col-sm-9">
													<input type="firstname_user" class="form-control" id="firstname_user" name="firstname_user" placeholder="{{ _('Firstname') }}">
												</div>
											</div>

											<div class="form-group">
												<label for="lastname_user" class="col-sm-3 control-label">{{ _('Lastname') }}</label>
												<div class="col-sm-9">
													<input type="lastname_user" class="form-control" id="lastname_user" name="lastname_user" placeholder="{{ _('Lastname') }}">
												</div>
											</div>

											<div class="form-group">
												<label for="plugin_user" class="col-sm-3 control-label">{{ _('Plugin') }}</label>
												<div class="col-sm-9">
													<input type="plugin_user" class="form-control" id="plugin_user" name="plugin_user" placeholder="{{ _('Plugin') }}">
												</div>
											</div>

											<div class="form-group">
													<table id="tab_plugin_right" class="col-sm-offset-3 col-sm-9">
														<tbody>
															<tr><td></td></tr>
														</tbody>
													</table>
											</div>

											<div class="form-group">
												<div class="col-sm-offset-3 col-sm-9">
													<button id="add_user" type="button" class="btn btn-default">{{ _('Add') }}</button>
												</div>
											</div>

										</form>
									</div>
                        		</div>
                    		</div>

                    		<div class="col-lg-8">

                    			<div class="panel panel-default">
									<div class="panel-heading">
										<i class="fa fa-list fa-fw"></i> {{ _('User list') }}
									</div>
									<div class="panel-body">
										<div class="table-responsive">
										<!-- ICI DATATABLE -->
											<table class="table table-striped table-bordered table-hover" id="dataTables-user_list">
												<thead>
													<tr>
														<th>{{ _('Login') }}</th>
														<th>{{ _('Firstname') }}</th>
														<th>{{ _('Lastname') }}</th>
														<th>{{ _('Plugin') }}</th>
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
		<script src="/web/js/im_crud_user.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}
