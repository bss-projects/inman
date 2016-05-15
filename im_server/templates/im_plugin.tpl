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
                    <h1 class="page-header">{{ _('Plugin management for InMan') }}</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-12">
                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-users fa-fw"></i> {{ _('Plugin administration') }}
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
							<div class="col-lg-3 verticalLine-right">
								<div class="panel panel-default">
									<div class="panel-heading">
										<i class="fa fa-user fa-fw"></i> {{ _('Plugin list') }}
									</div>
									<div class="panel-body">
										<div class="list-group">
											
										</div>
									</div>
                        		</div>
                    		</div>
                    		<div class="col-lg-9 verticalLine-left">
                    			<div class="row">
									<div class="col-lg-12 horizontallLine">
										<h3>{{ _('Plugin info') }}</h3>
									</div>
								</div>
								<div class="row">
									<div class="col-sm-2">
										<label class="control-label">{{ _('Plugin name') }}</label>
									</div>
									<div id="plugin_name" class="col-sm-10">
										
									</div>
								</div>
								<div class="row">
									<div class="col-sm-2">
										<label class="control-label">{{ _('Description') }}</label>
									</div>
									<div id="description" class="col-sm-10">
										
									</div>
								</div>
								<div class="row">
									<div class="col-lg-12 horizontallLine">
										<h3>{{ _('Plugin agent') }}</h3>
									</div>
								</div>
								<div class="row">
									<div class="col-sm-12">
										<div id="accordion" class="panel-group">
									
										</div>
										<div class="row">
											<div class="col-sm-2 col-md-offset-10">
												<p>
													<button class="btn btn-outline btn-info" type="button">{{ _('Edit') }}</button>
													<button class="btn btn-outline btn-warning" type="button">{{ _('Delete') }}</button>
												</p>
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
	</div>

	{% endblock container %}

	{% block js %}
		{% include 'im_js.tpl' %}
		<script src="/web/js/im_crud_plugin.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}
