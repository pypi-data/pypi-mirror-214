<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.models import Wordform %>
<% from clld_morphology_plugin.util import render_paradigm %>
<% from clld_morphology_plugin.util import rendered_form %>
<%! active_menu_item = "lexemes" %>

<h3>${_('Lexeme')} <i style="font-variant: small-caps;">${ctx.name}</i> ‘${ctx.description}’</h3>

<table class="table table-nonfluid">
    <tbody>
            <tr>
                <td> Language: </td>
                <td> ${h.link(request, ctx.language)}</td>
            </tr> 
        % if ctx.pos:
            <tr>
                <td> Part of speech: </td>
                <td> ${h.link(request, ctx.pos)} </td>
            </tr> 
        % endif
        % if ctx.stems:
            <tr>
                <td> Stems: </td>
                <td> ${h.text2html(", ".join([h.link(request, stem) for stem in ctx.stems]))}</td>
            </tr>        
        % endif
    </tbody>
</table>

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>

<%def name="print_cell(entity)">
    % if isinstance(entity, str):
        ${entity}
    % else:
        ${h.link(request, entity)}
    % endif
</%def>

<% paradigm = render_paradigm(ctx) %>
% if paradigm:
    Inflected forms:
    <table border="1">
        % for col_idx, colname in enumerate(paradigm["colnames"]):
            <tr>
                % for x in range(len(paradigm["idxnames"])-1):
                    <td> </td>
                % endfor
                <th> ${h.link(request, colname)} </th>
                % for column in paradigm["columns"]:
                    <th> ${print_cell(column[col_idx])} </th>
                % endfor
            </tr>
        % endfor
        <tr>
            % for idxname in paradigm["idxnames"]:
                <th>
                    ${print_cell(idxname)}
                </th>
            % endfor
        </tr>
            <tr>
            % for idxnames, cells in zip(paradigm["index"], paradigm["cells"]):
            <tr>
                % for idxname in idxnames:
                <th>
                    ${print_cell(idxname)}
                    </th>
                % endfor
                % for cell in cells:
                <td>
                    % for form in cell:
                        <i>${h.link(request, form) | n}</i> <br>
                    % endfor
                    </td>
                % endfor
            </tr>
            % endfor
        </tr>
     </table>
% endif
##${render_paradigm(ctx, html=True) | n}

<h4>${_('Wordforms')}:</h4>
${request.get_datatable('wordforms', Wordform, lexeme=ctx).render()}