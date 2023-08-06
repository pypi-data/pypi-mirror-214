import re
from math import floor
import pandas as pd
from clld.web.util.helpers import link
from clld.web.util.htmllib import HTML


GLOSS_ABBR_PATTERN = re.compile(
    "(?P<personprefix>1|2|3)?(?P<abbr>[A-Z]+)(?P<personsuffix>1|2|3)?(?=([^a-z]|$))"
)

empty_pos = HTML.span(
    "empty pos ?",
    **{"class": "pos"},
)


def rendered_gloss_units(request, sentence):  # pylint: disable=too-many-locals
    """This method takes a sentence and returns the interlinear gloss lines as nested divs for displaying.
    If there are ExampleParts present, the associated wordforms will be rendered accordingly."""
    units = []
    if sentence.analyzed and sentence.gloss:
        # g-words associated with this sentence
        slices = {sl.index: sl for sl in sentence.forms}
        g_shift = 0  # to keep up to date with how many g-words there are in total
        pos = False
        for pwc, (pword, pgloss) in enumerate(
            zip(sentence.analyzed.split("\t"), sentence.gloss.split("\t"))
        ):  # iterate p-words
            g_words = []
            morphs = []
            glosses = []
            posses = []
            for gwc, (word, gloss) in enumerate(
                zip(pword.split("="), pgloss.split("="))
            ):  # iterate g-words in p-word
                idx = pwc + gwc + g_shift
                in_clitic_str = False
                if gwc > 0:
                    for glosslist in [morphs, glosses]:
                        glosslist.append("=")
                    posses.append("=")
                    in_clitic_str = True
                if idx not in slices:
                    g_words.append(HTML.span(word.replace("-", "")))
                    morph_list = []
                    if in_clitic_str:
                        morph_list.append("=")
                    morph_list.append(word)
                    morphs.append(HTML.span(*morph_list, class_="morpheme"))
                    glosses.append(HTML.span(gloss))
                    posses.append(" ")
                else:
                    g_words.append(
                        HTML.span(
                            link(request, slices[idx].form),
                            name=slices[idx].form.id,
                        )
                    )
                    r_form = rendered_form(request, slices[idx].form)
                    if r_form:
                        morphs.append(HTML.span(r_form, class_="morpheme"))
                    else:
                        morphs.append(word)

                    rendered_gloss = rendered_form(
                        request, slices[idx].form, line="gloss"
                    )
                    glosses.append(
                        HTML.span(
                            rendered_gloss or gloss,
                            **{"class": "gloss"},
                        )
                    )
                    if slices[idx].form.pos:
                        posses.append(
                            HTML.span(
                                link(
                                    request,
                                    slices[idx].form.pos,
                                    label=slices[idx].form.pos.id,
                                ),
                                **{"class": "pos"},
                            )
                        )
                        pos = True
                    else:
                        posses.append(
                            HTML.span(
                                "?",
                                **{"class": "pos"},
                            )
                        )
            g_shift += gwc
            gloss_divs = []
            if slices:
                gloss_divs.append(HTML.div(*g_words, class_="wordform"))
            gloss_divs.extend(
                [
                    HTML.div(*morphs, class_="morpheme"),
                    HTML.div(*glosses, class_="gloss"),
                ],
            )
            if pos:
                gloss_divs.append(HTML.div(*posses, class_="pos"))
            interlinear_div = HTML.div(
                *gloss_divs,
                class_="gloss-unit",
            )
            units.append(interlinear_div)
    return units


morph_separators = ["-", "~", "<", ">"]
sep_pattern = f"([{''.join(morph_separators)}])"


def form_representation(request, f, level="morphs", line="obj"):
    """Returns a dict of indices and links that make up a given form."""
    parts = dict(enumerate(f.parts))
    slices = {fslice.index: fslice for fslice in f.slices}
    components = {}
    if level == "stem" and hasattr(
        f, "stemforms"
    ):  # returning segmentation and glosses at the stem level
        if line == "obj":
            components[0] = (f, HTML.span(link(request, f)))
        elif line == "gloss":
            components[0] = (
                f,
                HTML.span(".".join([link(request, gloss) for gloss in f.glosses])),
            )
        return components
    if hasattr(f, "formstems"):
        if level == "morphs":  # filling in morph slices from stem into form
            for formstem in f.formstems:
                if len(formstem.index) == 1:
                    for idx, subform in form_representation(
                        request, formstem.stem, level=level, line=line
                    ).items():
                        components[formstem.index[0] + (idx + 0.1) * 0.1] = subform
                        if formstem.index[0] in parts:
                            del parts[formstem.index[0]]
                else:
                    # print(f"{formstem.stem.name} '{formstem.stem.description}', positions {formstem.index} in the wordform {f.name} '{f.description}'")
                    pass
        else:  # filling in links from stem
            for formstem in f.formstems:
                for idx in formstem.index:
                    if line == "obj":
                        components[idx] = (
                            formstem.stem,
                            HTML.span(link(request, formstem.stem, label=parts[idx])),
                        )
                    else:
                        components[idx] = (
                            formstem.stem,
                            HTML.span(
                                ".".join(
                                    [
                                        link(request, gloss)
                                        for gloss in formstem.stem.glosses
                                    ]
                                )
                            ),
                        )
                    if idx in slices:
                        del slices[idx]
    for index, part in parts.items():
        if index in slices:
            if line == "obj" and slices[index].morph:
                components[index] = (
                    slices[index].morph,
                    HTML.span(
                        link(
                            request,
                            slices[index].morph,
                            label=part,
                            name=slices[index].morph.id,
                        )
                    ),
                )
            elif line == "gloss":
                glosslist = []
                for x in slices[index].glosses:
                    glosslist.append(link(request, x.gloss))
                    glosslist.append(".")
                if len(glosslist) > 0:
                    del glosslist[-1]
                for change in slices[index].mpchanges:
                    if change.inflection:
                        glosslist.append("\\")
                        glosslist.append(link(request, change.inflection.value))
                components[index] = (
                    slices[index].morph,
                    HTML.span(*glosslist),
                )
        elif index not in components:
            if line == "obj":
                components[index] = (part, part)
            elif line == "gloss":
                components[index] = ("***", "***")
    return dict(sorted(components.items()))


def rendered_form(request, f, level="morphs", line="obj"):
    """Displays a rendered version of a form or wordform or stem."""
    if hasattr(f, "formslices"):
        if level == "wordforms":
            return HTML.i(*[link(request, x.wordform) + " " for x in f.formslices])
        if level == "forms":
            return HTML.i(link(request, f))
        return HTML.i(
            *[
                rendered_form(request, x.wordform, level, line) + " "
                for x in f.formslices
            ]
        )
    form_components = []
    representation = form_representation(request, f, level, line)
    for index, (part, partlink) in enumerate(representation.values()):
        if index >= 1:
            if form_components[-1] not in morph_separators:
                if isinstance(part, str):
                    form_components.append("-")
                elif part and part.lsep:
                    form_components.append(part.lsep)
                else:
                    form_components.append("-")
        form_components.append(partlink)
        if (
            part
            and index < len(representation)
            and not isinstance(part, str)
            and part.rsep
        ):
            form_components.append(part.rsep)
    if form_components:
        if line != "gloss":
            return HTML.i(*form_components)
        return HTML.span(*form_components)
    return None


def render_paradigm(self, html=False):
    forms = {x.form: {"Form": x.form} for x in self.inflections}
    for inflection in self.inflections:
        if hasattr(inflection.form, "formslices"):
            for fslice in inflection.form.formslices:
                for infl in fslice.wordform.inflections:
                    forms[inflection.form][infl.value.category] = infl.value
        else:
            forms[inflection.form][inflection.value.category] = inflection.value

    df = pd.DataFrame.from_dict(list(forms.values()))
    if len(df) == 0:
        return None
    cut = floor(len(self.inflectionalcategories) / 2) - 1
    y = self.inflectionalcategories[cut + 1 : :]
    x = self.inflectionalcategories[0 : cut + 1]
    df = df.fillna("-")

    if self.paradigm_x:
        x = sorted(
            [cat for cat in self.inflectionalcategories if cat.name in self.paradigm_x],
            key=lambda x: self.paradigm_x,
        )
    if self.paradigm_y:
        y = sorted(
            [cat for cat in self.inflectionalcategories if cat.name in self.paradigm_y],
            key=lambda x: self.paradigm_y,
        )

    def listify(stuff):
        return list(stuff)

    print(df)
    paradigm = pd.pivot_table(df, values="Form", columns=x, index=y, aggfunc=listify)
    paradigm = paradigm.fillna("")
    sort_orders = {cat: cat.ordered_values for cat in self.inflectionalcategories}

    def sorter(s):
        if s.name in sort_orders:
            return s.map({k: v for v, k in enumerate(sort_orders[s.name])})
        return s

    paradigm.sort_index(level=paradigm.index.names, key=sorter, inplace=True)
    paradigm.sort_index(level=paradigm.columns.names, key=sorter, inplace=True, axis=1)
    paradigm.index = pd.MultiIndex.from_frame(paradigm.index.to_frame().fillna(""))

    def cast_list(stuff):
        if not isinstance(stuff, (list, tuple)):
            return [stuff]
        return stuff

    if html:
        return paradigm.to_html()
    if None in paradigm.columns.names:
        colnames = []
    else:
        colnames = paradigm.columns.names

    return {
        "colnames": colnames,
        "columns": [cast_list(x) for x in paradigm.columns.tolist()],
        "idxnames": paradigm.index.names,
        "index": paradigm.index.tolist(),
        "cells": paradigm.values.tolist(),
    }


def dict_to_list(dd):
    for a, b in dd.items():
        yield HTML.li(a)
        if isinstance(b, dict):
            yield HTML.ul(*dict_to_list(b))
        else:
            yield HTML.ul(HTML.li(b))


def build_etymology_tree(request, stem):
    output = {}
    for derivation in stem.derivations:
        output[
            link(request, derivation.target)
            + f" ‘{derivation.target.description}’ ("
            + link(request, derivation.process)
            + ")"
        ] = build_etymology_tree(request, derivation.target)
    return output


def build_etymology_source(request, stem, tree=None):
    if not hasattr(stem, "derived_from"):
        return tree
    if not stem.derived_from:
        return tree or {}
    derivation = stem.derived_from[0]
    parent = derivation.source
    if not parent:
        source_string = ""
    else:
        source_string = link(request, parent) + f" ‘{derivation.source.description}’ + "
    if not tree:
        tree = link(request, stem)
    tree = {
        source_string
        + link(request, derivation.process)
        + ":": tree
    }
    return build_etymology_source(request, parent, tree)


def render_derived_stems(request, stem):
    res = build_etymology_tree(request, stem)
    return HTML.ul(*dict_to_list(res))


def render_derived_from(request, stem):
    res = build_etymology_source(request, stem)
    return HTML.ul(*dict_to_list(res))


def rendered_form_units(request, forms):
    units = []
    keys = ["wordforms", "morphs", "glosses"]
    for form in forms:
        units.append(
            {
                "wordforms": link(request, form),
                "morphs": rendered_form(request, form),
                "glosses": rendered_form(request, form, line="gloss"),
            }
        )
        if form.stem:
            units[-1]["stems"] = rendered_form(request, form.stem)
            keys.append("stems")
    return units, keys


def render_wordforms(request, formlist):
    units, keys = rendered_form_units(request, formlist)
    return units, keys
