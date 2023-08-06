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
<%! active_menu_item = "wordforms" %>

<h3>${_('Form')} <i>${ctx.name}</i> ‘${ctx.description}’</h3>

% if ctx.formslices:
% endif
<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Form:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        % if ctx.formslices:
            <tr>
                <td>
                    Structure:
                </td>
                <td>
<% formtuples, keys = render_wordforms(request, [fslice.wordform for fslice in ctx.formslices]) %>
<div class="sentence">
        <div class="body">
            <div class="gloss-box">
                <div class="gloss-unit">
                    % for key in keys:
                        <div>${key}:</div>    
                    % endfor
                </div>
                % for formtuple in formtuples:
                    <div class="gloss-unit">
                        % for key in keys:
                            % if key in formtuple:
                                <div class="${key}"><text>${formtuple[key]|n}</text></div>
                            % else:
                                <div class="${key}">-</div>                            
                            % endif
                        % endfor
                    </div>
                % endfor
            </div>
            ## <div class="translation">Then the next day Ituimano went, Takyimano.
            </div>
        </div>
    </div>
                </td>
            </tr>
        % endif
        ## % if ctx.meanings:
        ## <tr>
        ##     <td> Meanings:</td>
        ##     <td>
        ##         <ol>
        ##             % for meaning in ctx.meanings:
        ##                 <li> ‘${h.link(request, meaning.meaning)}’ </li>
        ##             % endfor
        ##         </ol>
        ##     </td>
        ## </tr>
        ## % endif
        % if getattr(ctx, "segments", None):
            <tr>
                <td>Segments:</td>
                <td>
                % for segment in ctx.segments:
                ${h.link(request, segment.phoneme)}
                    % endfor</td>
            </tr>
        % endif
        % if ctx.source:
            <tr>
                <td>Source:</td>
                <td>${h.link(request, ctx.source)}</td>
            </tr>
        % endif
    </tbody>
</table>

<p>${h.text2html(h.Markup(ctx.markup_description or ""))}</p>

% if ctx.audio:
    <audio controls="controls"><source src="/audio/${ctx.audio}" type="audio/x-wav"></source></audio>
% endif 

<script>
var highlight_targets = document.getElementsByName("${ctx.id}");
for (index = 0; index < highlight_targets.length; index++) {
    highlight_targets[index].children[0].classList.add("morpho-highlight");
}
</script>