<nav class="navbar navbar-default navbar-fixed-top" role="navigation" style="margin-bottom: 0">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".sidebar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.html">InMan</a>
            </div>
            <!-- /.navbar-header -->

            <ul class="nav navbar-top-links navbar-right">
                <li class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-eye-slash fa-fw"></i>  <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-alerts">
                        <li>
                            <a href="#">
                            <div>
                                <i class="fa fa-adjust fa-fw"></i> {{ _('Display Filter') }}
                                <span class="pull-right">
                                    <input id="filterlevelview" type="checkbox" name="filterlevelview" checked>
                                </span>
                            </div>
                            </a>
                        </li>
                        <li class="divider"></li>
                        <li>
                            <a href="#">
                                <div>
                                    <i class="fa fa-comment fa-fw"></i> New Comment
                                    <span class="pull-right text-muted small">4 minutes ago</span>
                                </div>
                            </a>
                        </li>
                    </ul>
                    <!-- /.dropdown-alerts -->
                </li>
                <!-- /.dropdown -->
                <li class="dropdown">
                    <a class="dropdown-toggle" data-toggle="dropdown" href="#">
                        <i class="fa fa-user fa-fw"></i>  <i class="fa fa-caret-down"></i>
                    </a>
                    <ul class="dropdown-menu dropdown-user">
                        <li><a href="#"><i class="fa fa-user fa-fw"></i> {{ _('User profile') }}</a>
                        </li>
                        <li><a href="#"><i class="fa fa-gear fa-fw"></i> {{ _('Settings') }}</a>
                        </li>
                        <li class="divider"></li>
                        <li><a href="cas_logout"><i class="fa fa-sign-out fa-fw"></i> {{ _('Logout') }}</a>
                        </li>
                    </ul>
                    <!-- /.dropdown-user -->
                </li>
                <!-- /.dropdown -->
            </ul>
            <!-- /.navbar-top-links -->

            <div class="navbar-default navbar-static-side" role="navigation">
                <div class="sidebar-collapse">
                    <ul class="nav" id="side-menu">
                        <li>
                            <a href="/"><i class="fa fa-list-alt fa-fw"></i> {{ _('Dashboard') }}</a>
                        </li>
                        
                        {% if 'supervisor' in plugin_list %}
                        <li>
                            <a href="#"><i class="fa fa-dashboard fa-fw"></i> {{ _('Supervisor configuration') }}<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="/im_host_supervisor">{{ _('Host') }}</a>
                                </li>
                                <li>
                                    <a href="/im_model_supervisor">{{ _('Model') }}</a>
                                </li>
                                <li>
                                    <a href="/im_command_supervisor">{{ _('Command') }}</a>
                                </li>
                                <li>
                                    <a href="/im_probe_supervisor">{{ _('Probe') }}</a>
                                </li>
                                <li>
                                    <a href="/im_status_supervisor">{{ _('Status') }}</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>
						{% endif %}

						{% if 'freeradius' in plugin_list %}
                        <li>
                            <a href="#"><i class="fa fa-key fa-fw"></i> {{ _('Freeradius configuration') }}<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="/im_user_freeradius">{{ _('Users management') }}</a>
                                </li>
                                <li>
                                    <a href="/im_client_freeradius">{{ _('Clients management') }}</a>
                                </li>
                                <li>
                                    <a href="/im_shared_secret_freeradius">{{ _('Shared secret') }}</a>
                                </li>
                                <li>
                                    <a href="/im_vendor_freeradius">{{ _('Vendors management') }}</a>
                                </li>
                                <li>
                                    <a href="/im_right_freeradius">{{ _('Rights management') }}</a>
                                </li>
                                <li>
                                    <a href="/im_network_perimeter_freeradius">{{ _('Network perimeter') }}</a>
                                </li>
                                <li>
                                    <a href="/im_user_trace_action_freeradius">{{ _('User action') }}</a>
                                </li>
                                <li>
                                    <a href="/im_log_freeradius">{{ _('View log') }}</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>
                        {% endif %}

                        {% if 'Administration' in plugin_list %}
                        <li>
                            <a href="#"><i class="fa fa-gears fa-fw"></i> {{ _('Administration') }}<span class="fa arrow"></span></a>
                            <ul class="nav nav-second-level">
                                <li>
                                    <a href="/im_user">{{ _('User') }}</a>
                                </li>
                                <li>
                                    <a href="/im_plugin">{{ _('Plugin') }}</a>
                                </li>
                            </ul>
                            <!-- /.nav-second-level -->
                        </li>
                        {% endif %}
                        
                    </ul>
                    <!-- /#side-menu -->
                </div>
                <!-- /.sidebar-collapse -->
            </div>
            <!-- /.navbar-static-side -->
        </nav>		
