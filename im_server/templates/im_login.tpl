{% extends "im_main.tpl" %}
{% block body %}

	<div class="container">
		<div class="row">
			<div class="col-md-4 col-md-offset-4">
				<div class="login-panel panel panel-default">
					<div class="panel-heading">
						<h3 class="panel-title">{{ _('Please Sign In') }}</h3>
					</div>
					{% if login_failed %}
						<div class="alert alert-warning">
							{{ _('Bad Login or Password') }}
						</div>
					{% endif %}
					<div class="panel-body">
						<form role="form" name="auth_local_user" action="/im_login" method="post">
							<fieldset>
								<div class="form-group">
									<input class="form-control" placeholder="{{ _('Login') }}" id="login" name="login" type="login" autofocus>
								</div>
								<div class="form-group">
									<input class="form-control" placeholder="{{ _('Password') }}" id="password" name="password" type="password" value="">
								</div>
									<!-- Change this to a button or input when using this as a form -->
								<button type="submit" class="btn btn-lg btn-success btn-block">{{ _('Submit') }}</button>
							</fieldset>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>

	{% block js %}
		{% include 'im_js.tpl' %}
	{% endblock js %}

{% endblock body %}