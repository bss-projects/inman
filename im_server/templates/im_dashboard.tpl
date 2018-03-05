{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}
<!-- Modal -->
<div class="modal fade" id="modal_delete_host" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">{{ _('Cancel') }}</span></button>
        <h4 class="modal-title" id="myModalLabel">{{ _('Confirm remove :') }} <div class="hostname_remove"></div></h4>
      </div>
      <div class="modal-body">
        {{ _('You are about to delete') }} <strong><span class="hostname_remove"></span></strong> {{ _('from') }} <strong><span class="supervisor_remove"></span></strong>
        <input type="hidden" id="hostname_remove" name="hostname_remove" class="hostname_remove">
        <input type="hidden" id="supervisor_remove" name="supervisor_remove" class="supervisor_remove">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">{{ _('Cancel') }}</button>
        <button type="button" class="btn btn-primary" id="proceed_remove">{{ _('Proceed') }}</button>
      </div>
      <div id="sync_div" class="row" style="display:none">
			<div class="col-lg-12">
				<!-- /.panel -->
				<div class="panel panel-default">
					<div class="panel-heading">
						<i class="fa fa-spin fa-spinner fa-fw"></i> {{ _('Synchronization') }}
					</div>
					<div class="panel-body">
						<div class="progress">
							<div id="progressBar" class="default"><div></div></div>
						</div>
						<div class="ProgressionContainer">
							<fieldset>
								<legend>{{ _('Progression') }}</legend>
								<div class="ProgressionContent">
								</div>
							</fieldset>
						</div>
					</div>
				</div>
			</div>
		</div>
    </div>
  </div>
</div>


	<div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">{{ _('Dashboard') }}</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-8">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-desktop fa-fw"></i> {{ _('Add host') }}
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <!-- Nav tabs -->
                            <ul class="nav nav-tabs">
                                <li class="active"><a href="#create" data-toggle="tab">{{ _('Create new host') }}</a>
                                </li>
                                <li><a href="#duplicate" data-toggle="tab">{{ _('Create host from model') }}</a>
                                </li>
                                <li><a href="#import" data-toggle="tab">{{ _('Add multiple host') }}</a>
                                </li>
                            </ul>

                            <!-- Tab panes -->
                            <div class="tab-content">
                                <div class="tab-pane fade in active" id="create">
                                    <h4>{{ _('Create new host') }}</h4>
                                    <form class="form-horizontal" role="form" name="create_new_host" action="im_crudhost/newhost" method="post">
                                        <div class="form-group">
                                            <label for="supervisor_newhost" class="col-sm-3 control-label">{{ _('Supervisor name') }}</label>
                                                <div class="col-sm-9">
                                                    <input type="supervisor_newhost" class="form-control" id="supervisor_newhost" name="supervisor_newhost" placeholder="{{ _('Supervisor name') }}">
                                                </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="hostname_newhost" class="col-sm-3 control-label">{{ _('Hostname') }}</label>
                                                <div class="col-sm-9">
                                                    <input type="hostname_newhost" class="form-control create_new_host" id="hostname_newhost" name="hostname_newhost" placeholder="{{ _('Hostname') }}" disabled>
                                                </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="alias_newhost" class="col-sm-3 control-label">{{ _('Alias') }}</label>
                                                <div class="col-sm-9">
                                                    <input type="alias_newhost" class="form-control create_new_host" id="alias_newhost" name="alias_newhost" placeholder="{{ _('Alias') }}" disabled>
                                                </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="ip_newhost" class="col-sm-3 control-label">{{ _('IP') }}</label>
                                            <div class="col-sm-9">
                                                <input type="ip_newhost" class="form-control create_new_host" id="ip_newhost" name="ip_newhost" placeholder="{{ _('IP') }}" disabled>
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <div class="col-sm-offset-3 col-sm-9">
                                                <button type="submit" class="btn btn-default">{{ _('Add') }}</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                                <div class="tab-pane fade" id="duplicate">
                                    <h4>{{ _('Create host from model') }}</h4>
                                    <form class="form-horizontal" role="form" name="create_from_template" action="im_crudhost/template" method="post">
                                        <div class="form-group">
                                            <label for="templatemodel" class="col-sm-2 control-label">{{ _('Choose model') }}</label>
                                                <div class="col-sm-10">
                                                    <input type="templatemodel" class="form-control" id="templatemodel" name="templatemodel" placeholder="{{ _('Choose model') }}">
                                                </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="hostname_template" class="col-sm-2 control-label">{{ _('Hostname') }}</label>
                                                <div class="col-sm-10">
                                                    <input type="hostname_template" class="form-control create_from_template" id="hostname_template" name="hostname_template" placeholder="{{ _('Hostname') }}" disabled>
                                                </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="alias_template" class="col-sm-2 control-label">{{ _('Alias') }}</label>
                                                <div class="col-sm-10">
                                                    <input type="alias_template" class="form-control create_from_template" id="alias_template" name="alias_template" placeholder="{{ _('Alias') }}" disabled>
                                                </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="ip_template" class="col-sm-2 control-label">{{ _('IP') }}</label>
                                            <div class="col-sm-10">
                                                <input type="ip_template" class="form-control create_from_template" id="ip_template" name="ip_template" placeholder="{{ _('IP') }}" disabled>
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <div class="col-sm-offset-2 col-sm-10">
                                                <button type="submit" class="btn btn-default">{{ _('Add') }}</button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                                <div class="tab-pane fade" id="import">
                                    <h4>{{ _('Add multiple host') }}</h4>
                                    <div id="dropzone" class="fade well col-sm-12">{{ _('Drag and drop your file here or select it') }}</div>
                                    <input id="fileupload" class="pull-right" type="file" name="files[]" data-url="server/php/" multiple>
                                </div>
                            </div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-list fa-fw"></i> {{ _('Host list') }}
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="table-responsive">
                                <!-- ICI DATATABLE -->
                                <table class="table table-striped table-bordered table-hover" id="dataTables-hostlist">
                                	<thead>
                                        <tr>
                                            <th>{{ _('Supervisor') }}</th>
                                            <th>{{ _('Host') }}</th>
                                            <th>{{ _('IP') }}</th>
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
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-8 -->
                <div class="col-lg-4">
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bell fa-fw"></i> Notifications Panel
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
                            <div class="list-group">
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-comment fa-fw"></i> New Comment
                                    <span class="pull-right text-muted small"><em>4 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-twitter fa-fw"></i> 3 New Followers
                                    <span class="pull-right text-muted small"><em>12 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-envelope fa-fw"></i> Message Sent
                                    <span class="pull-right text-muted small"><em>27 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-tasks fa-fw"></i> New Task
                                    <span class="pull-right text-muted small"><em>43 minutes ago</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-upload fa-fw"></i> Server Rebooted
                                    <span class="pull-right text-muted small"><em>11:32 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-bolt fa-fw"></i> Server Crashed!
                                    <span class="pull-right text-muted small"><em>11:13 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-warning fa-fw"></i> Server Not Responding
                                    <span class="pull-right text-muted small"><em>10:57 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-shopping-cart fa-fw"></i> New Order Placed
                                    <span class="pull-right text-muted small"><em>9:49 AM</em>
                                    </span>
                                </a>
                                <a href="#" class="list-group-item">
                                    <i class="fa fa-money fa-fw"></i> Payment Received
                                    <span class="pull-right text-muted small"><em>Yesterday</em>
                                    </span>
                                </a>
                            </div>
                            <!-- /.list-group -->
                            <a href="#" class="btn btn-default btn-block">View All Alerts</a>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-bar-chart-o fa-fw"></i> Donut Chart Example
                        </div>
                        <div class="panel-body">
                            <div id="listservices">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>#</th>
                                            <th>Service name</th>
                                            <th>Service template</th>
                                            <th>Remove</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>1</td>
                                            <td>Mark</td>
                                            <td>Otto</td>
                                            <td class="remove"><button type="button" class="btn btn-default">
  <i class="fa fa-trash-o"></i> Remove
</button></td>
                                        </tr>
                                        <tr>
                                            <td>2</td>
                                            <td>Jacob</td>
                                            <td>Thornton</td>
                                            <td class="remove"><button type="button" class="btn btn-default">
  <i class="fa fa-trash-o"></i> Remove
</button></td>
                                        </tr>
                                        <tr>
                                            <td>3</td>
                                            <td>Larry</td>
                                            <td>the Bird</td>
                                            <td class="remove"><button type="button" class="btn btn-default">
  <i class="fa fa-trash-o"></i> Remove
</button></td>
                                        </tr>
                                    </tbody>
                                </table>                            
                            </div>
                            <a href="#" class="btn btn-default btn-block">View Details</a>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-4 -->
            </div>
            <!-- /.row -->
        </div>
        <!-- /#page-wrapper -->
	{% endblock container %}

	{% block js %}
		{% include 'im_js.tpl' %}
<!--		<script src="/web/js/im_dashboard.js"></script> -->
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}	