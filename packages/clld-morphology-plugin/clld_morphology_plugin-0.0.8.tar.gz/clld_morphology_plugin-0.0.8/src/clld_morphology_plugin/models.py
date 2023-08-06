from clld.db.meta import Base
from clld.db.meta import PolymorphicBaseMixin
from clld.db.models.common import Contribution
from clld.db.models.common import FilesMixin
from clld.db.models.common import HasFilesMixin
from clld.db.models.common import HasSourceMixin
from clld.db.models.common import IdNameDescriptionMixin
from clld.db.models.common import Language
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy import Unicode
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
from zope.interface import implementer
from clld_morphology_plugin import interfaces


@implementer(interfaces.IMeaning)
class Meaning(Base, PolymorphicBaseMixin, IdNameDescriptionMixin):
    """Placeholder for meaning."""


@implementer(interfaces.IGloss)
class Gloss(Base):
    """A gloss is a word in the metalanguage or a `glossing abbreviation <https://en.m.wikipedia.org/wiki/List_of_glossing_abbreviations>`_ that is used to represent a semantic or functional aspect of an object language element."""

    id = Column(String, unique=True)
    name = Column(String, unique=False)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=True)
    """The meaning associated with this gloss."""
    # todo: this should maybe be a many-to-many mapping?
    meaning = relationship(Meaning, innerjoin=True, backref="glosses")

    @property
    def morphs(self):
        """A list of all morphs that have this gloss"""
        return list(
            dict.fromkeys(
                [s.formpart.morph for s in self.formglosses if s.formpart.morph]
            )
        )


@implementer(interfaces.IMorpheme)
class Morpheme(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    """A morpheme is a set of morphs."""

    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="morphemes")
    comment = Column(Unicode)

    @property
    def glosses(self):
        """A list of sets of glosses used for the morphs of this morpheme"""
        glosslist = []
        for m in self.allomorphs:
            for glosses in m.glosses:
                if glosses not in glosslist:
                    glosslist.append(glosses)
        return glosslist

    @property
    def forms(self):
        """A list of wordforms in which morphs belonging to this morpheme occur."""
        formlist = []
        for m in self.allomorphs:
            for fslice in m.formslices:
                formlist.append(fslice.form)
        return list(set(formlist))

    @property
    def formslices(self):
        """A list of positions in wordforms in which morphs belonging to this morpheme occur."""
        slicelist = []
        for m in self.allomorphs:
            for fslice in m.formslices:
                slicelist.append(fslice)
        return slicelist

    @property
    def stemslices(self):
        """A list of positions in stems in which morphs belonging to this morpheme occur."""
        slicelist = []
        for m in self.allomorphs:
            for fslice in m.stemslices:
                slicelist.append(fslice)
        return slicelist

    @property
    def inflectionalvalues(self):
        """A list of inflectional values expressed with morphs belonging to this morpheme."""
        vallist = []
        for m in self.allomorphs:
            for val in m.inflectionalvalues:
                vallist.append(val)
        return list(set(vallist))


@implementer(interfaces.IMorph)
class Morph(Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin):
    """A morph is a pairing of a sequence of segments and function, which can not be further segmented."""

    __table_args__ = (
        UniqueConstraint("language_pk", "id"),
        UniqueConstraint("morpheme_pk", "id"),
    )

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)
    morpheme_pk = Column(Integer, ForeignKey("morpheme.pk"), nullable=True)
    morpheme = relationship(Morpheme, innerjoin=True, backref="allomorphs")
    """The right-hand separator for this morph (e.g.: ``-`` or ``>``)"""
    rsep = Column(String, nullable=True)
    """The right-hand separator for this morph (e.g.: ``-`` or ``>``)"""
    lsep = Column(String, nullable=True)
    """The morph type (e.g.: ``root`` or ``prefix``)"""
    morph_type = Column(String, nullable=True)

    @property
    def glosses(self):
        """A list of gloss sets that tokens of this morph have."""
        glosslist = []
        for fslice in self.formslices:
            g = [x.gloss for x in fslice.glosses]
            if g not in glosslist:
                glosslist.append(g)
        return glosslist

    @property
    def inflectionalvalues(self):
        """A list of inflectional values marked by tokens of this morph."""
        infllist = []
        for fslice in self.formslices:
            for partinflection in fslice.inflections:
                if partinflection.inflection.value not in infllist:
                    infllist.append(partinflection.inflection.value)
        return infllist

    @property
    def wordforms(self):
        """A list of wordforms this morph occurs in."""
        formlist = [x.form for x in self.formslices]
        for x in self.stemslices:
            for form in x.stem.wordforms:
                if form not in formlist:
                    formlist.append(form)
        return formlist


@implementer(interfaces.IPOS)
class POS(Base, IdNameDescriptionMixin):
    """A part of speech is a language-specific open or closed set of wordforms (or lexemes)"""

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)


@implementer(interfaces.IWordform)
class Wordform(
    Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin, HasFilesMixin
):
    """A wordform is a grammatical or morphosyntactic word. It can have a stem and bear inflectional morphology."""

    __table_args__ = (
        UniqueConstraint("language_pk", "id"),
        UniqueConstraint("pos_pk", "id"),
    )

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="wordforms")

    pos_pk = Column(Integer, ForeignKey("pos.pk"))
    """The part of speech of this wordform."""
    pos = relationship(POS, backref="wordforms", innerjoin=True)

    """The parts into which this wordform can be segmented. Note that these are not necessarily morphs, as 1) there may be segments that have no meaning attached to them, 2) parts may be stems which could be further segmentable, and 3) morphs split by infixation appear as two separate parts."""
    parts = Column(MutableList.as_mutable(PickleType), default=[])

    @property
    def lexeme(self):
        """The lexeme to which this wordform belongs."""
        for infl in self.inflections:
            if infl.stem:
                return infl.stem.lexeme
        for formstem in self.formstems:
            return formstem.stem.lexeme
        return None

    @property
    def audio(self):
        """The audio file associated with this wordform."""
        for f in self._files:
            if f.mime_type.split("/")[0] == "audio":
                return f
        return None

    @property
    def inflections(self):
        """A list of inflections (linking to stems and inflectional values) found in this wordform."""
        for s in self.slices:
            for infl in s.inflections:
                yield infl.inflection

    @property
    def stem(self):
        """The stem of this wordform."""
        for infl in self.inflections:
            if infl.stem:
                return infl.stem
        if self.formstems:
            return self.formstems[0].stem
        return None

    @property
    def gloss(self):
        """Parts of this wordform represented as a gloss (string)"""
        return "-".join(
            [".".join([y.gloss.name for y in x.glosses]) for x in self.slices]
        )


class WordformPart(Base):
    """The association table between wordforms and morphs. ``index`` corresponds to the ``parts`` of the wordform."""

    id = Column(String, unique=True, nullable=False)
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    morph_pk = Column(Integer, ForeignKey("morph.pk"), nullable=True)
    form = relationship(Wordform, innerjoin=True, backref="slices")
    morph = relationship(Morph, innerjoin=True, backref="formslices")
    index = Column(Integer, nullable=True)


class WordformPartGloss(Base):
    """The association table between wordformparts (bound morph tokens) and glosses."""

    formpart_pk = Column(Integer, ForeignKey("wordformpart.pk"), nullable=False)
    formpart = relationship(WordformPart, innerjoin=True, backref="glosses")
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=False)
    gloss = relationship(Gloss, innerjoin=True, backref="formglosses")


class WordformMeaning(Base):
    """The association table between wordforms and meanings."""

    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    meaning_pk = Column(Integer, ForeignKey("meaning.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="meanings")
    meaning = relationship(Meaning, innerjoin=True, backref="forms")


@implementer(interfaces.IForm)
class Form(
    Base, PolymorphicBaseMixin, IdNameDescriptionMixin, HasSourceMixin, HasFilesMixin
):
    """An arbitrarily long form, from suffix to entire sentence. Work in progress."""

    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True, backref="forms")

    contribution_pk = Column(Integer, ForeignKey("contribution.pk"))
    contribution = relationship(Contribution, backref="forms")

    parts = Column(MutableList.as_mutable(PickleType), default=[])

    @property
    def link_form(self):
        if len(self.formslices) > 1:
            return self
        return self.formslices[0].wordform

    @property
    def audio(self):
        for f in self._files:
            if f.mime_type.split("/")[0] == "audio":
                return f
        return None


class FormPart(Base):
    id = Column(String, unique=True)
    form_pk = Column(Integer, ForeignKey("form.pk"), nullable=False)
    wordform_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    form = relationship(Form, innerjoin=True, backref="formslices")
    wordform = relationship(Wordform, innerjoin=True, backref="multiforms")
    index = Column(Integer, nullable=True)


class Form_files(Base, FilesMixin):  # noqa: N801
    pass


class Wordform_files(Base, FilesMixin):  # noqa: N801
    pass


@implementer(interfaces.ILexeme)
class Lexeme(Base, IdNameDescriptionMixin):
    """ "A lexeme is a 'dictionary entry'."""

    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    pos_pk = Column(Integer, ForeignKey("pos.pk"), nullable=True)
    pos = relationship(POS, backref="lexemes", innerjoin=True)

    comment = Column(Unicode)

    """What inflectional categories should be shown on the x-axis of the inflectional paradigm?"""
    paradigm_x = Column(MutableList.as_mutable(PickleType), default=[])
    """What inflectional categories should be shown on the y-axis of the inflectional paradigm?"""
    paradigm_y = Column(MutableList.as_mutable(PickleType), default=[])

    @hybrid_property
    def inflections(self):
        """A list of all inflections (linking stems of the lexeme with wordforms and inflectional values) associated with this lexeme."""
        infl_list = []
        for stem in self.stems:
            infl_list.extend(stem.inflections)
        return infl_list

    @property
    def inflectionalcategories(self):
        """The inflectional categories stems of this lexeme are inflected for."""
        infl_list = []
        for stem in self.stems:
            infl_list.extend(stem.inflectionalcategories)
        return list(dict.fromkeys(infl_list))


@implementer(interfaces.IStem)
class Stem(Base, IdNameDescriptionMixin):
    """A stem is the part of a wordform that is not inflected. It is associated with a lexeme, and is potentially morphologically complex."""

    __table_args__ = (UniqueConstraint("language_pk", "id"),)

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)

    lexeme_pk = Column(Integer, ForeignKey("lexeme.pk"))
    lexeme = relationship(Lexeme, innerjoin=True, backref="stems")
    comment = Column(Unicode)

    """The parts into which this stem can be segmented. Note that these are not necessarily morphs, as 1) there may be segments that have no meaning attached to them, 2) parts may be other stems which could be further segmentable, and 3) morphs split by infixation appear as two separate parts."""
    parts = Column(MutableList.as_mutable(PickleType), default=[])

    rsep = Column(String, nullable=True)
    lsep = Column(String, nullable=True)

    @property
    def inflectionalcategories(self):
        """The inflectional categories this stem is inflected for in wordforms."""
        return list(dict.fromkeys([x.value.category for x in self.inflections]))

    @property
    def gloss(self):
        """A string representation of the glosses (e.g., ``burn.INTR``)"""
        if self.glosses:
            return ".".join([x.name for x in self.glosses])
        return self.description

    @property
    def wordforms(self):
        """A list of inflected wordforms of this stem."""
        return [x.form for x in self.stemforms]


class StemPart(Base):
    """The association table between stems and morphs. ``index`` corresponds to the ``parts`` of the stem."""

    id = Column(String, unique=True)
    stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    morph_pk = Column(Integer, ForeignKey("morph.pk"), nullable=False)
    stem = relationship(Stem, innerjoin=True, backref="slices")
    morph = relationship(Morph, innerjoin=True, backref="stemslices")
    index = Column(Integer, nullable=True)


class StemPartGloss(Base):
    """The association table between stemparts (bound morph tokens) and glosses."""

    stempart_pk = Column(Integer, ForeignKey("stempart.pk"), nullable=False)
    stempart = relationship(StemPart, innerjoin=True, backref="glosses")
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=False)
    gloss = relationship(Gloss, innerjoin=True, backref="stempartglosses")


class WordformStem(Base):
    """The association table between stems and inflected forms. ``ìndex`` represents the position(s) in the ``parts`` of the stem."""

    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    form = relationship(Wordform, innerjoin=True, backref="formstems")
    stem = relationship(Stem, innerjoin=True, backref="stemforms")
    index = Column(MutableList.as_mutable(PickleType), default=[])


@implementer(interfaces.IInflCategory)
class InflectionalCategory(Base, IdNameDescriptionMixin):
    """An inflectional category like person or tense."""

    value_order = Column(MutableList.as_mutable(PickleType), default=[])
    """The order in which the inflectional values of this category should be ordered. For instance, person should be 1,2,3."""

    @property
    def ordered_values(self):
        """A sorted list of inflectional values associated with this category."""
        order = {val: pos for pos, val in enumerate(self.value_order)}
        sort_count = len(order)
        for plus, val in enumerate(self.values):
            if val.id not in order:
                order[val.id] = sort_count + plus
        if len(self.value_order) > 0 and self.value_order[0] == "-":
            return ["-"] + sorted(self.values, key=lambda x: order[x.id])
        return sorted(self.values, key=lambda x: order[x.id]) + ["-"]


@implementer(interfaces.IInflValue)
class InflectionalValue(Base, IdNameDescriptionMixin):
    category_pk = Column(Integer, ForeignKey("inflectionalcategory.pk"), nullable=False)
    category = relationship(InflectionalCategory, innerjoin=True, backref="values")
    gloss_pk = Column(Integer, ForeignKey("gloss.pk"), nullable=True)
    gloss = relationship(Gloss, innerjoin=True, backref="values")

    def __str__(self):
        if self.gloss:
            return self.gloss.name
        return self.name

    def __lt__(self, other):
        if isinstance(other, str):
            return self.name < other
        return self.name < other.name

    @property
    def exponents(self):
        """A dict of morphs (exponents) expressing this inflectional value, values are wordforms."""
        res = {}
        for inflection in self.inflections:
            key = [formpart.formpart.morph for formpart in inflection.formparts]
            for mpchange in inflection.mpchanges:
                key.append(mpchange.change)
            key = tuple(key)
            res.setdefault(key, [])
            res[key].append(inflection.form)
        return res


class Inflection(Base):
    """An inflection links an inflectional value with a stem, as well as morphs in a wordform."""

    value_pk = Column(Integer, ForeignKey("inflectionalvalue.pk"), nullable=False)
    stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    value = relationship(InflectionalValue, innerjoin=True, backref="inflections")
    stem = relationship(Stem, innerjoin=True, backref="inflections")

    @property
    def form(self):
        if self.formparts:
            if self.formparts[0].form:
                return self.formparts[0].form
            return self.formparts[0].formpart.form
        if self.mpchanges:
            return self.mpchanges[0].formpart.form
        raise ValueError(f"Inflection {self} has no associated forms")

    @property
    def morphs(self):
        return [x.formpart.morph for x in self.formparts]


class WordformPartInflection(Base):
    """The association table between form morphs and inflections. This allows modeling things like an inflectional value being expressed by two distinct morphs."""

    form_pk = Column(Integer, ForeignKey("form.pk"), nullable=True)
    form = relationship(Form, innerjoin=True, backref="inflections")
    formpart_pk = Column(Integer, ForeignKey("wordformpart.pk"), nullable=False)
    formpart = relationship(WordformPart, innerjoin=True, backref="inflections")
    infl_pk = Column(Integer, ForeignKey("inflection.pk"), nullable=False)
    inflection = relationship(Inflection, innerjoin=True, backref="formparts")


@implementer(interfaces.IDerivProcess)
class DerivationalProcess(Base, IdNameDescriptionMixin):
    """A derivational process derives new stems from roots or other stems."""

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)


class Derivation(Base):
    """A derivation links a source stem or root with a derivational process and a target stem."""

    process_pk = Column(Integer, ForeignKey("derivationalprocess.pk"), nullable=False)
    process = relationship(DerivationalProcess, innerjoin=True, backref="derivations")
    source_root_pk = Column(Integer, ForeignKey("morph.pk"), nullable=True)
    source_root = relationship(
        Morph, innerjoin=True, backref="derivations", foreign_keys=[source_root_pk]
    )
    source_stem_pk = Column(Integer, ForeignKey("stem.pk"), nullable=True)
    source_stem = relationship(
        Stem, innerjoin=True, backref="derivations", foreign_keys=[source_stem_pk]
    )
    target_pk = Column(Integer, ForeignKey("stem.pk"), nullable=False)
    target = relationship(
        Stem, innerjoin=True, backref="derived_from", foreign_keys=[target_pk]
    )

    @property
    def source(self):
        if self.source_stem:
            return self.source_stem
        if self.source_root:
            return self.source_root
        return None


class StemPartDerivation(Base):
    """The association table between stem morphs and derivations. This allows modeling things like a derivational process adding two distinct morphs to a stem."""

    stempart_pk = Column(Integer, ForeignKey("stempart.pk"), nullable=False)
    stempart = relationship(StemPart, innerjoin=True, backref="derivations")
    derivation_pk = Column(Integer, ForeignKey("derivation.pk"), nullable=False)
    derivation = relationship(Derivation, innerjoin=True, backref="stemparts")


@implementer(interfaces.IMorphoPhonoChange)
class MorphoPhonologicalChange(Base, IdNameDescriptionMixin):
    """A morphophonological change."""

    language_pk = Column(Integer, ForeignKey("language.pk"), nullable=False)
    language = relationship(Language, innerjoin=True)


class MorphoPhonoInstance(Base):
    """An instance of a morphophonological change, connecting it with part of a form, and optionally an inflection."""

    change_pk = Column(
        Integer, ForeignKey("morphophonologicalchange.pk"), nullable=False
    )
    inflection_pk = Column(Integer, ForeignKey("inflection.pk"), nullable=True)
    formpart_pk = Column(Integer, ForeignKey("wordformpart.pk"), nullable=True)
    stempart_pk = Column(Integer, ForeignKey("stempart.pk"), nullable=True)

    change = relationship(MorphoPhonologicalChange, innerjoin=True, backref="tokens")
    inflection = relationship(Inflection, innerjoin=True, backref="mpchanges")
    formpart = relationship(WordformPart, innerjoin=True, backref="mpchanges")
    stempart = relationship(StemPart, innerjoin=True, backref="mpchanges")
