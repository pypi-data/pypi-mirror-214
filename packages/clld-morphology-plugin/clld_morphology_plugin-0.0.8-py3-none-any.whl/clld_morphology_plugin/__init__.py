from clld_morphology_plugin import datatables
from clld_morphology_plugin import interfaces
from clld_morphology_plugin import models


__author__ = "Florian Matter"
__email__ = "florianmatter@gmail.com"
__version__ = "0.0.8"


def includeme(config):
    config.registry.settings["mako.directories"].insert(
        1, "clld_morphology_plugin:templates"
    )
    config.add_static_view(
        "clld-morphology-plugin-static", "clld_morphology_plugin:static"
    )

    config.register_resource("morph", models.Morph, interfaces.IMorph, with_index=True)
    config.register_resource(
        "morpheme", models.Morpheme, interfaces.IMorpheme, with_index=True
    )
    config.register_resource(
        "meaning", models.Meaning, interfaces.IMeaning, with_index=True
    )
    config.register_resource("pos", models.POS, interfaces.IPOS, with_index=True)
    config.register_resource(
        "lexeme", models.Lexeme, interfaces.ILexeme, with_index=True
    )
    config.register_resource(
        "wordform", models.Wordform, interfaces.IWordform, with_index=True
    )

    config.register_resource("gloss", models.Gloss, interfaces.IGloss, with_index=False)
    config.register_resource("stem", models.Stem, interfaces.IStem, with_index=True)
    config.register_resource(
        "inflectionalvalue",
        models.InflectionalValue,
        interfaces.IInflValue,
        with_index=True,
    )
    config.register_resource(
        "inflectionalcategory",
        models.InflectionalCategory,
        interfaces.IInflCategory,
        with_index=True,
    )
    config.register_resource(
        "form",
        models.Form,
        interfaces.IForm,
        with_index=True,
    )
    config.register_resource(
        "derivationalprocess",
        models.DerivationalProcess,
        interfaces.IDerivProcess,
        with_index=True,
    )
    config.register_resource(
        "morphophonologicalchange",
        models.MorphoPhonologicalChange,
        interfaces.IMorphoPhonoChange,
        with_index=True,
        route="morphophonologicalchanges",
    )

    config.register_datatable(
        "morphophonologicalchanges", datatables.MorphoPhonoChanges
    )
    config.register_datatable("lexemes", datatables.Lexemes)
    config.register_datatable("pos", datatables.POS)
    config.register_datatable("meanings", datatables.Meanings)
    config.register_datatable("morphs", datatables.Morphs)
    if config.registry.settings.get("clld_morphology_plugin", {}).get("pos", True):
        config.register_datatable("wordforms", datatables.Wordforms)
    else:
        config.register_datatable("wordforms", datatables.Wordforms_noPOS)
    config.register_datatable("morphemes", datatables.Morphemes)
    config.register_datatable("glosses", datatables.Glosses)
    config.register_datatable("stems", datatables.Stems)
    config.register_datatable("forms", datatables.Forms)
    config.register_datatable("derivationalprocesses", datatables.DerivationalProcesses)
    config.register_datatable(
        "inflectionalcategorys", datatables.InflectionalCategories
    )
    config.register_datatable("inflectionalvalues", datatables.InflectionalValues)
