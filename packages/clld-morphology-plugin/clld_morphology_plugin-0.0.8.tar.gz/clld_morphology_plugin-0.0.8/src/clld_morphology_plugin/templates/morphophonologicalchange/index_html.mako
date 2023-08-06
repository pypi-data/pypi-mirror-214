<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "morphophonologicalchanges" %>
<%block name="title">${_('Morphophonological changes')}</%block>

<h2>${_('Morphophonological changes')}</h2>
<div>
    ${ctx.render()}
</div>