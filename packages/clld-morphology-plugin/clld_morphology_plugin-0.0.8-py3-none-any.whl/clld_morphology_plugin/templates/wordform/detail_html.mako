<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.models import Form%>
<% from clld_morphology_plugin.util import rendered_form %>
<% from clld_morphology_plugin.util import form_representation %>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
% try:
    <%from clld_corpus_plugin.util import rendered_sentence %>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry
<%! active_menu_item = "wordforms" %>


<h3>${_('Wordform')} <i>${ctx.name}</i> ‘${ctx.description}’</h3>

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
        % if ctx.slices:
        <tr>
            <td>Structure:</td>
            <td>
                ${rendered_form(request, ctx) | n}<br>
                ${rendered_form(request, ctx, line="gloss") | n}<br>
                ## ${rendered_form(request, ctx, level="stem") | n}<br>
                ## ${rendered_form(request, ctx, level="stem", line="gloss") | n}
            </td>
        </tr>
        % endif
        % if list(ctx.inflections):
            <tr>
                <td>Inflection:</td>
                <td>
                        % if ctx.lexeme:
                            ${h.link(request, ctx.lexeme)}
                        % else:
                            ${h.link(request, ctx.stem)}
                        % endif
                    <ul>
                    % for formpart in ctx.slices:
                        % if formpart.inflections:
                            <li>
                                % if formpart.morph:
                                    ${h.link(request, formpart.morph)}:
                                % else:
                                    zero-marked:
                                % endif
                                <ul>
                                    % for partinflection in formpart.inflections:
                                        <li>${h.link(request, partinflection.inflection.value.category)}: ${h.link(request,     partinflection.inflection.value, label=partinflection.inflection.value.name)}</li>
                                    % endfor
                                </ul>
                            </li>
                        % endif
                        % for mpchange in formpart.mpchanges:
                            <li>${h.link(request, mpchange.change)}</li>
                            ## (in <i>${formpart.morph}</i>)
                            <ul>
                                    <li>${h.link(request, mpchange.inflection.value.category)}: ${h.link(request,     mpchange.inflection.value, label=mpchange.inflection.value.name)}</li>
                            </ul>
                        % endfor
                    % endfor
                    </ul>
                </td>
            </tr>
        % elif len(ctx.formstems) == 1:
            % if ctx.lexeme:
                <tr>
                    <td>Lexeme:</td>
                    <td>
                    ${h.link(request, ctx.lexeme)}
                    </td>
                </tr>
            % endif
            <tr>
                <td>Stem:</td>
                <td>
                    ${h.link(request, ctx.formstems[0].stem)}
                </td>
            </tr>
        % endif
        % if ctx.meanings:
        <tr>
            <td> Meanings:</td>
            <td>
                <ol>
                    % for meaning in ctx.meanings:
                        <li> ‘${h.link(request, meaning.meaning)}’ </li>
                    % endfor
                </ol>
            </td>
        </tr>
        % endif
        % if ctx.pos:
        <tr>
            <td>Part of speech:</td>
            <td>
                ${h.link(request, ctx.pos)}
            </td>
        </tr>
        % endif
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


% if hasattr(ctx, "sentence_assocs"):
    <% gloss_sentences = {} %>
    % for assoc in ctx.sentence_assocs:
        <%gloss_sentences[assoc.sentence.id] = rendered_sentence(request, assoc.sentence, sentence_link=True)%>
    % endfor
% endif


<div class="tabbable">
    <ul class="nav nav-tabs">
        % if gloss_sentences:
            <li class=${'active' if gloss_sentences else ''}><a href="#corpus" data-toggle="tab"> Corpus tokens </a></li>
        % endif
        % if ctx.multiforms:
            <li class=${'' if gloss_sentences else 'active'}><a href="#multiforms" data-toggle="tab"> Longer forms </a></li>
        % endif
    </ul>

    <div class="tab-content" style="overflow: visible;">

        <div id="multiforms" class="tab-pane ${'' if gloss_sentences or ctx.multiforms else 'active'}">
            % if ctx.multiforms:
                ${request.get_datatable('forms', Form, wordform=ctx).render()}
            % endif
        </div>


        <div id="corpus" class="tab-pane ${'active' if gloss_sentences else ''}">
            <ol class="example">
                % for sentence in gloss_sentences.values():
                    ${sentence}
                % endfor
            </ol>
        </div>
    </div>  
</div>



<script>
var highlight_targets = document.getElementsByName("${ctx.id}");
for (index = 0; index < highlight_targets.length; index++) {
    highlight_targets[index].children[0].classList.add("morpho-highlight");
}
</script>