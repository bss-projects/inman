{% extends "im_frame.tpl" %}

	{% block menu %}
		{% include 'im_menu.tpl' %}
	{% endblock menu %}
	{% block container %}

<div id="page-wrapper">
            <div class="row">
                <div class="col-lg-12">
                    <h1 class="page-header">{{ _('Request registration for InMan') }}</h1>
                </div>
                <!-- /.col-lg-12 -->
            </div>
            <!-- /.row -->
            <div class="row">
                <div class="col-lg-12">

                    <!-- /.panel -->
                    <div class="panel panel-default">
                        <div class="panel-heading">
                            <i class="fa fa-info fa-fw"></i> {{ _('Info') }}
                        </div>
                        <!-- /.panel-heading -->
                        <div class="panel-body">
				Envoyer un email a l'equipe support ESSI
			</div>
</div>

	{% endblock container %}

	{% block js %}
		{% include 'im_js.tpl' %}
		<script src="/web/js/im_crud_user.js"></script>
	{% endblock js %}

{# Faire un include pour les JS globaux et IF pour ne prendre que le JS spec a la page #}
