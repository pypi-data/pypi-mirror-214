<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%from clld_morphology_plugin import models%>
<%! active_menu_item = "pos" %>


<h3>${ctx.name.capitalize()} (Part of speech, ${ctx.id})</h3>

% if ctx.description:
    <p>${ctx.description}</p>
% endif

<div class="tabbable">
    <ul class="nav nav-tabs">
        % if ctx.wordforms:
            <li class='active'><a href="#forms" data-toggle="tab"> Wordforms </a></li>
        % endif
        % if ctx.lexemes:
            <li class=${'' if ctx.wordforms else 'active'}><a href="#lexemes" data-toggle="tab"> Lexemes </a></li>
        % endif
    </ul>

    <div class="tab-content" style="overflow: visible;">

        <div id="forms" class="tab-pane active">
            ${request.get_datatable('wordforms', models.Wordform, pos=ctx).render()}
        </div>

        <div id="lexemes" class="tab-pane ${'' if ctx.wordforms else 'active'}">
            ${request.get_datatable('lexemes',models.Lexeme, pos=ctx).render()}
        </div>

    </div>  
</div>

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>