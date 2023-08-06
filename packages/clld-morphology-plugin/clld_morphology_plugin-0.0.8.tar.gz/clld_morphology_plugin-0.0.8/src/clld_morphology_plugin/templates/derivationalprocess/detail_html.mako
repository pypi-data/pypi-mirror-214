<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.util import rendered_form %>
<% from clld_morphology_plugin.util import render_wordforms %>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
% try:
    <%from clld_corpus_plugin.util import rendered_sentence %>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry
<%! active_menu_item = "processes" %>

<h3>${h.link(request, ctx.language)} ${_('derivational process')}: ${ctx.name}</h3>

% if ctx.description:
    ${ctx.description}
% endif

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>

% if ctx.derivations:
    Derivations:
    <ul>
        % for deriv in ctx.derivations:
            <% parts = [] %>
            % for part in deriv.stemparts:
                <% parts.append(h.link(request, part.stempart.morph)) %>
            % endfor
            <li><i>
            % if deriv.source:
                ${h.link(request, deriv.source)}</i> ‘${deriv.source.description}’ →
            %endif
            <i>${h.link(request, deriv.target)}</i> ‘${deriv.   target.description}’ (<i>${", ".join(parts) | n }</i>)</li>
        % endfor
    </ul>
% endif