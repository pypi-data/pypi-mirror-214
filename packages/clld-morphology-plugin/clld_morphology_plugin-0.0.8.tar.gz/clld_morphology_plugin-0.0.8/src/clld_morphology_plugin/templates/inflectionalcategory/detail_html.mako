<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

<%! active_menu_item = "inflectionalcategories" %>

<h3>${_('Inflectional category')} ${ctx.name}</h3>
% if ctx.description:
    ${ctx.description}<br>
% endif

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>

Values:
<ul>
% for val in ctx.values:
    <li>${h.link(request, val)} (${val.name})</li>
% endfor
</ul>