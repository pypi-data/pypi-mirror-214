<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "morphophonologicalchanges" %>


<h3>${_('Morphophonological change')} ‘${ctx.name}’</h3>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
    </tbody>
</table>

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>

<ul>
    % for token in ctx.tokens:
        <li>${h.link(request, token.formpart.form)}</li>
    % endfor
</ul>