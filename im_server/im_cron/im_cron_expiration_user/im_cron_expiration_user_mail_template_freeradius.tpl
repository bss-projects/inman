<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	</head>
	<body>
		<div>
			<p>Bonjour,</p>
		</div>
		<div>
			<p>Les comptes suivants vont bientot arriver a expiration :</p>
		</div>
		<div>
			{% if l_one_day %}
				<p>Expiration dans les 24h:</p>
				<ul>
					{% for item in l_one_day %}
						<li>{{ item.username }}</li>
					{% endfor %}
				</ul>
			{% endif %}
		</div>
		<div>
			{% if l_one_week %}
				<p>Expiration dans la semaine:</p>
				<ul>
					{% for item in l_one_week %}
						<li>{{ item.username }}</li>
					{% endfor %}
				</ul>
			{% endif %}
		</div>
		<div>
			{% if l_one_month %}
				<p>Expiration dans le mois:</p>
				<ul>
					{% for item in l_one_month %}
						<li>{{ item.username }}</li>
					{% endfor %}
				</ul>
			{% endif %}
		</div>
	</body>
</html>