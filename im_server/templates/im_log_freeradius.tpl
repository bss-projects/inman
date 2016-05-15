{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('Log view for Freeradius') }}</h1>
		</div>
                <!-- /.col-lg-12 -->
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-file-text-o fa-fw"></i> {{ _('Log view') }}
				</div>
				<div class="panel-body">
					<div class="col-lg-2">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-hand-o-up fa-fw"></i> {{ _('Type') }}
							</div>
							<div class="panel-body">
								<button id="live_view_log_freeradius" type="button" class="btn btn-outline btn-primary btn-lg btn-block">{{ _('Live view') }}</button>
								<button id="file_view_log_freeradius" type="button" class="btn btn-outline btn-primary btn-lg btn-block">{{ _('File view') }}</button>
							</div>
						</div>
					</div>
					<div class="col-lg-10">
						<div class="panel panel-default">
							<div class="panel-heading">
								<i class="fa fa-eye fa-fw"></i> {{ _('View') }}
							</div>
							<div class="panel-body">
								<div id="frame_view_log_freeradius" class="log_view">
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
		<script src="/web/js/autobahn.min.jgz"></script>
		<script src="/web/js/im_websocket_log_freeradius.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}
