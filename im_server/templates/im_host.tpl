{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<textarea id="use_template_list" name="use_template_list" style="display:none">
{{ use_template_list }}
</textarea>
<textarea id="parents_list" name="parents_list" style="display:none">
{{ parents_list }}
</textarea>
<textarea id="group_list" name="group_list" style="display:none">
{{ group_list }}
</textarea>
<textarea id="supervisor_name_arg" name="supervisor_name_arg" style="display:none">
{{ supervisor_name_arg }}
</textarea>

<input id="addtype" type="hidden" name="addtype" value="{{ addtype }}" />
<input id="oid" type="hidden" name="oid" value="{{ oid }}" />
<input id="conf_filepath" type="hidden" name="conf_filepath" value="{{ conf_filepath }}" />

<div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">{{ _('Host definition for : ') }}{{ page_header_name }}</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-12">

                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-desktop fa-fw"></i> {{ _('Host info') }}
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">

							<div class="col-lg-2">
								<div id="iconplace"></div>
                            	<input type="hosticon" class="form-control" id="hosticon" placeholder="{{ _('Choose icon') }}">
							</div>
							<div class="col-lg-4">
								<form class="form-horizontal" role="form">
									<div class="form-group">
										<label for="supervisor_name" class="col-sm-3 control-label">{{ _('Supervisor name') }}</label>
										<div class="col-sm-9">
											<input type="supervisor_name" class="form-control" id="supervisor_name" name="supervisor_name" placeholder="{{ _('Supervisor name') }}">
										</div>
									</div>
									<div class="form-group">
										<label for="use_template" class="col-sm-3 control-label">{{ _('Host template inheritance') }}</label>
											<div class="col-sm-9">
												<input type="use_template" class="form-control" id="use_template" name="use_template" placeholder="{{ _('Host template inheritance (use param)') }}">
											</div>
									</div>
									<div class="form-group">
										<label for="host_parent" class="col-sm-3 control-label">{{ _('Parent\'s Host') }}</label>
											<div class="col-sm-9">
												<input type="host_parent" class="form-control" id="host_parent" name="host_parent" placeholder="{{ _('Parent\'s Host') }}" value="{{ host_parent }}">
											</div>
									</div>
									<div class="form-group">
										<label for="hostname" class="col-sm-3 control-label">{{ _('Hostname') }}</label>
											<div class="col-sm-9">
												<input type="hostname" class="form-control" id="hostname" name="hostname" placeholder="{{ _('Hostname') }}" value="{{ hostname }}">
											</div>
									</div>
									<div class="form-group">
										<label for="ip" class="col-sm-3 control-label">{{ _('IP') }}</label>
											<div class="col-sm-9">
												<input type="ip" class="form-control" id="ip" name="ip" placeholder="{{ _('IP') }}" value="{{ ip }}">
											</div>
									</div>
									<div class="form-group">
										<label for="alias" class="col-sm-3 control-label">{{ _('Alias') }}</label>
											<div class="col-sm-9">
												<input type="alias" class="form-control" id="alias" name="alias" placeholder="{{ _('Alias') }}" value="{{ alias }}">
											</div>
									</div>
									<div class="form-group">
										<label for="group" class="col-sm-3 control-label">{{ _('Group') }}</label>
											<div class="col-sm-9">
												<input type="group" class="form-control" id="group" name="group" placeholder="{{ _('Group') }}">
											</div>
									</div>
								</form>							
							</div>
							<div class="col-lg-6">
								<!-- Nav tabs -->
								<ul class="nav nav-tabs">
									<li class="active"><a href="#services" data-toggle="tab">{{ _('Service list checked') }}</a>
									</li>
									<li><a href="#host_macro" data-toggle="tab">{{ _('Specific macro') }}</a>
									</li>
								</ul>
								<div class="tab-content">
									<div class="tab-pane fade in active" id="services">
										<div id="listservices">
											<table class="table" id="tab_service">
												<thead>
													<tr>
														<th>{{ _('Service name') }}</th>
														<th>{{ _('Service template') }}</th>
														<th>{{ _('Remove') }}</th>
													</tr>
												</thead>
												<tbody>
												{% for service in services %}
													<tr>
														<td>{{ service.name|e }}</td>
														<td>{{ service.template|e }}</td>
														<td class="remove"><button type="button" class="btn btn-default">
														<i class="fa fa-trash-o"></i> {{ _('Remove') }}
														</button>
														</td>
													</tr>
												{% else %}
													<td><div class="no_result_service"></div></td>
													<td><div class="no_result_service"></div>{{ _('No services checked') }}</td>
													<td><div class="no_result_service"></div></td>
												{% endfor %}
												</tbody>
											</table>
											<div class="col-lg-12">
												<div class="col-lg-7 col-lg-offset-2">
													<input type="listservices_select" class="form-control" id="listservices_select" name="listservices_select" placeholder="{{ _('Choose service to check') }}">
												</div>
												<div class="col-lg-2">
													<button id="add_service" class="btn btn-outline btn-info" type="button">{{ _('Add') }}</button>
												</div>
											</div>
										</div>
									</div>
									<div class="tab-pane fade" id="host_macro">
										<div id="listmacros">
											<table class="table" id="tab_macro">
												<thead>
													<tr>
														<th>{{ _('Macro name') }}</th>
														<th>{{ _('Macro value') }}</th>
														<th>{{ _('Remove') }}</th>
													</tr>
												</thead>
												<tbody>
												{% for macro in macros %}
													<tr>
														<td>{{ macro.name|e }}</td>
														<td>{{ macro.value|e }}</td>
														<td class="remove"><button type="button" class="btn btn-default">
														<i class="fa fa-trash-o"></i> {{ _('Remove') }}
														</button>
														</td>
													</tr>
												{% else %}
													<td><div class="no_result_macro"></div></td>
													<td><div class="no_result_macro"></div>{{ _('No macros found') }}</td>
													<td><div class="no_result_macro"></div></td>
												{% endfor %}
												</tbody>
											</table>
											<div class="col-lg-12">
												<div class="col-lg-5">
													<input type="macro_name" class="form-control" id="macro_name" name="macro_name" placeholder="{{ _('Define a macro name') }}">
												</div>
												<div class="col-lg-5">
													<input type="macro_val" class="form-control" id="macro_val" name="macro_val" placeholder="{{ _('Define a macro value') }}">
												</div>
												<div class="col-lg-2">
													<button id="add_macro" class="btn btn-outline btn-info" type="button">{{ _('Add') }}</button>
												</div>
											</div>
										</div>

									</div>
								</div>
							</div>
							<div class="col-lg-4 col-lg-offset-4 col-lg-4 text-center">
								<button id="submit_host" class="btn btn-success" type="button">{{ _('Ok') }}</button>
								<button class="btn btn-warning" type="button">{{ _('Cancel') }}</button>
							</div>
                        </div>
                        <!-- /.panel-body -->
                    </div>
                    <!-- /.panel -->
                </div>
                <!-- /.col-lg-8 -->
            <!-- /.row -->
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
        <!-- /#page-wrapper -->

	{% endblock container %}

	{% block js %}
		{% include 'im_js.tpl' %}
		<script src="/web/js/im_host.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}
