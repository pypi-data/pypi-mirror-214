<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

<%! active_menu_item = "inflectionalvalues" %>

<h3>${_('Inflectional value')} '${ctx.name}'</h3>

<table class="table table-nonfluid">
    <tbody>
    <tr>
        <td>Category:</td>
        <td>${h.link(request, ctx.category)}</td>
    </tr>
    % if ctx.gloss:
        <tr>
            <td>Gloss:</td>
            <td>${h.link(request, ctx.gloss)}</td>
        </tr>
    % endif
    % if ctx.exponents:
    <td> Exponents: </td>
    <td>
        <ul>
            % for morphs, forms in ctx.exponents.items():
                <% morph_list = [] %>
                <% label = [] %>
                % for morph in morphs:
                    % if morph:
                        <% morph_list.append(h.link(request, morph)) %>
                        <% label.append(morph.id) %>
                    % else:
                        <% morph_list.append("zero-marked") %>
                        <% label.append("zero") %>                      
                    % endif
                % endfor
                <% label = ",".join(label) %>
                <li>
                    ${", ".join(morph_list) |n} (<a data-toggle="collapse" data-target="#${label}">🞃 forms</a>)
                </li>
                    <div id="${label}" class="collapse out">
                        <ul>
                            % for form in forms:
                                <li>${h.link(request, form)}</li>
                            % endfor
                        </ul>
                    </div>
            % endfor
        </ul>
    </td>
    % endif
    </tbody>
</table>

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>
