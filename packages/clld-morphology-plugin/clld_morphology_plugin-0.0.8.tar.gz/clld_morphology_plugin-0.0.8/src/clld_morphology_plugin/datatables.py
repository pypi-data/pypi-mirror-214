from clld.db.models.common import Language
from clld.web.datatables.base import Col
from clld.web.datatables.base import DataTable
from clld.web.datatables.base import LinkCol
from clld.web.util.helpers import icon
from sqlalchemy import and_
from sqlalchemy.orm import joinedload
from clld_morphology_plugin import models


class DescriptionLinkCol(LinkCol):

    """Render a link to the unit using the description as label."""

    def get_attrs(self, item):
        return {"label": item.description}


class FormCountCol(Col):
    def __init__(self, dt, name, **kw):
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        return item.form_count


class AudioCol(Col):
    def __init__(self, dt, name, **kw):
        kw["choices"] = ["yes"]
        kw["input-size"] = "mini"
        kw["model_col"] = models.Wordform_files.id
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        if item.audio:
            return icon("volume-up")
        return None

    def order(self):
        return models.Wordform_files.id

    def search(self, qs):
        if qs == "yes":
            return models.Wordform_files.pk != 0
        return True


class Wordforms(DataTable):

    __constraints__ = [
        Language,
        models.Lexeme,
        models.Morph,
        models.POS,
        models.Inflection,
        models.Stem,
    ]

    def base_query(self, query):
        query = query.join(Language).options(joinedload(models.Wordform.language))

        query = query.outerjoin(
            models.Wordform_files,
            and_(
                models.Wordform_files.object_pk == models.Wordform.pk,
                models.Wordform_files.mime_type.contains("audio/"),
            ),
        ).options(
            joinedload(models.Wordform._files)  # pylint: disable=protected-access
        )

        if self.morph:
            query = query.join(models.WordformPart).options(
                joinedload(models.Wordform.slices)
            )
            return query.filter(
                models.Wordform.slices.any(models.WordformPart.morph == self.morph)
            )
        if self.language:
            return query.filter(models.Wordform.language == self.language)
        if self.stem:
            return query.filter(
                models.Wordform.formstems.any(models.WordformStem.stem == self.stem)
            )
        if self.pos:
            return query.filter(models.Wordform.pos == self.pos)
        if self.lexeme:
            return query.filter(models.Wordform.lexeme == self.lexeme)
        return query

    def col_defs(self):
        cols = [LinkCol(self, "name"), Col(self, "description")]
        if not self.pos:
            cols.append(
                LinkCol(
                    self,
                    "part of speech",
                    model_col=models.POS.name,
                    get_obj=lambda i: i.pos,
                )
            )
        if not self.language:
            cols.append(
                LinkCol(
                    self,
                    "language",
                    model_col=Language.name,
                    get_obj=lambda i: i.language,
                )
            )
        cols.append(AudioCol(self, "Audio"))
        return cols


class Wordforms_noPOS(Wordforms):
    def col_defs(self):
        cols = [LinkCol(self, "name"), Col(self, "description")]
        if not self.language:
            cols.append(
                LinkCol(
                    self,
                    "language",
                    model_col=Language.name,
                    get_obj=lambda i: i.language,
                )
            )
        cols.append(AudioCol(self, "Audio"))
        return cols


class Forms(DataTable):

    __constraints__ = [Language, models.Wordform]

    def base_query(self, query):
        query = query.join(Language).options(joinedload(models.Form.language))

        if self.language:
            return query.filter(models.Form.language == self.language)
        if self.wordform:
            query = query.join(models.FormPart).options(
                joinedload(models.Form.formslices)
            )
            return query.filter(
                models.Form.formslices.any(models.FormPart.wordform == self.wordform)
            )
        return query

    def col_defs(self):
        return [
            LinkCol(self, "name"),
            Col(self, "description"),
            LinkCol(
                self, "language", model_col=Language.name, get_obj=lambda i: i.language
            ),
        ]


class Morphs(DataTable):

    __constraints__ = [Language]

    def base_query(self, query):
        query = query.join(Language).options(joinedload(models.Morph.language))

        if self.language:
            return query.filter(models.Morph.language == self.language)
        return query

    def col_defs(self):
        return [
            LinkCol(self, "name"),
            Col(self, "description"),
            LinkCol(
                self, "language", model_col=Language.name, get_obj=lambda i: i.language
            ),
            Col(self, "morph_type", choices=["prefix", "suffix", "root", "infix"]),
        ]


class Morphemes(DataTable):
    __constraints__ = [Language]

    def base_query(self, query):
        query = query.join(Language).options(joinedload(models.Morpheme.language))

        if self.language:
            return query.filter(models.Morpheme.language == self.language)
        return query

    def col_defs(self):
        return [
            LinkCol(self, "name"),
            Col(self, "description"),
            LinkCol(
                self, "language", model_col=Language.name, get_obj=lambda i: i.language
            ),
        ]


class Stems(DataTable):
    __constraints__ = [Language, models.Morph]

    def base_query(self, query):
        query = query.join(Language).options(joinedload(models.Stem.language))
        query = query.join(models.StemPart).options(joinedload(models.Stem.slices))

        if self.language:
            return query.filter(models.Stem.language == self.language)
        if self.morph:
            return query.filter(
                models.Stem.slices.any(models.StemPart.morph == self.morph)
            )
        return query

    def col_defs(self):
        return [
            LinkCol(self, "name"),
            Col(self, "description"),
            LinkCol(
                self, "language", model_col=Language.name, get_obj=lambda i: i.language
            ),
        ]


class Meanings(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name")]


class DerivationalProcesses(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name")]


class POS(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name"), Col(self, "description")]


class InflectionalCategories(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name"), Col(self, "description")]


class InflectionalValues(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name")]


class Glosses(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name")]


class Lexemes(DataTable):
    __constraints__ = [Language, models.POS]

    def base_query(self, query):
        if self.pos:
            return query.filter(models.Lexeme.pos == self.pos)
        return query

    def col_defs(self):
        cols = [
            LinkCol(self, "name"),
            Col(self, "description"),
            # FormCountCol(self, "Forms", bSortable=False, bSearchable=False),
        ]
        if not self.pos:
            cols.append(
                LinkCol(
                    self,
                    "part of speech",
                    # model_col=models.POS.name,
                    get_obj=lambda i: i.pos,
                )
            )
        return cols


class MorphoPhonoChanges(DataTable):

    __constraints__ = [Language]

    def base_query(self, query):
        query = query.join(Language).options(
            joinedload(models.MorphoPhonologicalChange.language)
        )

        if self.language:
            return query.filter(
                models.MorphoPhonologicalChange.language == self.language
            )
        return query

    def col_defs(self):
        return [
            LinkCol(self, "name"),
            Col(self, "description"),
            LinkCol(
                self, "language", model_col=Language.name, get_obj=lambda i: i.language
            ),
        ]
