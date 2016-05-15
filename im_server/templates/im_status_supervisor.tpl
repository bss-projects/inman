{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<div id="page-wrapper">
	<div class="row">
		<div class="col-lg-12">
			<h1 class="page-header">{{ _('Agent status for Supervisor') }}</h1>
		</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
			<div class="panel panel-default">
				<div class="panel-heading">
					<i class="fa fa-map-marker fa-fw"></i> {{ _('Global information') }}
				</div>
				<div class="panel-body">

					<div class="row" style="min-height:400px;">
						<div  class="col-sm-12">
							<h3>Agent list</h3>
							<hr/>
							<div class="col-xs-2"> <!-- required for floating -->
							<!-- Nav tabs -->
								<ul class="nav nav-tabs tabs-left">
									<li class="active"><a href="#home" data-toggle="tab">CRIV</a></li>
									<li><a href="#profile" data-toggle="tab">Visus</a></li>
									<li><a href="#messagess" data-toggle="tab">Thor</a></li>
								</ul>
							</div>

							<div class="col-xs-10">
							<!-- Tab panes -->
								<div class="tab-content">
									<div class="tab-pane active" id="home">
										<div class="col-xs-3">
											<div class="rcornerbox">
												<button id="launch_sync" class="btn btn-success btn-circle btn-lg" type="button">
													<i class="fa fa-link"></i>
												</button>
												Launch Sync
											</div>
											<div class="rcornerbox">
												<button id="launch_reverse" class="btn btn-info btn-circle btn-lg" type="button">
													<i class="fa fa-mail-reply-all"></i>
												</button>
												Back to previous conf
											</div>
										</div>
										<div id="sync_div" class="col-xs-9" style="display:none">
											<i class="fa fa-spin fa-spinner fa-fw"></i> {{ _('Synchronization') }}
											<div class="progress">
												<div id="progressBar" class="default"><div></div></div>
											</div>
										</div>

									</div>
									<div class="tab-pane" id="profile">Profile Tab.</div>
									<div class="tab-pane" id="settings">Messages Tab.</div>
									<div class="tab-pane" id="messagess">Settings Tab.</div>
								</div>
							</div>

							<div class="clearfix"></div>

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
		<script src="/web/js/im_status_supervisor.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}