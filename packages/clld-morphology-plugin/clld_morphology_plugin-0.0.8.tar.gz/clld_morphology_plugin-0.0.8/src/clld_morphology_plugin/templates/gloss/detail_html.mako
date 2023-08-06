<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.util import rendered_form %>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 
<%! active_menu_item = "glosses" %>

<h3>${_('Gloss')} ‘${ctx.name}’</h3>

<table class="table table-nonfluid">
    <tbody>
        % if ctx.values:
            <tr>
                <td> Inflectional values:</td>
                <td>
                    <ul>
                       % for value in ctx.values:
                           <li>${h.link(request, value, label=value.name)} (${h.link(request, value.category)})</li>
                       % endfor
                    </ul>
                </td>
            </tr>
        % endif
        % if ctx.stempartglosses:
            <% morphstems = {} %>
            % for stemgloss in ctx.stempartglosses:
                <% morphstems.setdefault(stemgloss.stempart.morph, []) %>
                <% morphstems[stemgloss.stempart.morph].append(stemgloss.stempart.stem) %>
            % endfor
            <tr>
                <td> Morphs in stems:</td>
                <td>
                    <ul>
                    % for morph, stems in morphstems.items():
                        <li>${h.link(request, morph)}
                        <ul>
                            % for stem in stems:
                                <li> ${rendered_form(request, stem, level="stem")} ‘${rendered_form(request, stem, line="gloss")}’</li>
                            % endfor
                        </ul>
                        </li>
                    % endfor
                    </ul>
                </td>
            </tr>
        % endif
        % if ctx.formglosses:
            <tr>
                <td> Morphs in wordforms:</td>
                <td>
                    <ul>
                       % for fslice in ctx.formglosses:
                           <li> ${h.link(request, fslice.formpart.form)} ‘${fslice.formpart.form.gloss}’</li>
                       % endfor
                    </ul>
                </td>
            </tr>
        % endif
        ## % if ctx.meanings:
        ##     <tr>
        ##         <td> Meanings:</td>
        ##         <td>
        ##             <ul>
        ##             </ul>
        ##         </td>
        ##     </tr>
        ## % endif
    </tbody>
</table>

<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>