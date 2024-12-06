__all__ = [
    "AUXILIARY_TREE",
    "DPR_SEMANTIC_WITH_SAT_PRODUCTS",
    "FIELDS_DESCRIPTION",
    "LIST_DPR_ADFS_FROM_MERGED_LEGACY",
    "LIST_DPR_ADFS_FROM_SPLIT_LEGACY",
    "LIST_DPR_WITH_SAT_ADFS_FROM_MERGED_LEGACY",
    "MAPPING_DPR_SEMANTIC_TO_LEGACY",
    "MAPPING_DPR_WITH_SAT_SEMANTIC_TO_LEGACY",
    "MAPPING_LEGACY_SEMANTIC_TO_DPR",
    "MAPPING_LEGACY_SEMANTIC_TO_DPR_WITH_SAT",
    "PRODUCT_DATA",
    "PRODUCT_DESCRIPTION",
    "PRODUCT_DOCUMENTATION",
    "PRODUCT_FORMATS",
    "PRODUCT_LEVEL",
    "PRODUCT_PATTERNS",
    "TERM_DATA",
    "TERM_DESCRIPTION",
    "TERM_DOCUMENTATION",
    "TERM_LINKS",
]

from typing import Any, Iterable

from sentineltoolbox.readers.resources import load_resource_file
from sentineltoolbox.stacutils import STAC_PROPERTIES

MAPPING_LEGACY_SEMANTIC_TO_DPR_WITH_SAT: dict[str, Any] = load_resource_file("metadata/mapping_legacy_dpr.json")
MAPPING_LEGACY_SEMANTIC_TO_DPR: dict[str, Any] = {}

PRODUCT_FORMATS: dict[str, Any] = load_resource_file("metadata/product_formats.json")
MAPPING_DPR_WITH_SAT_SEMANTIC_TO_LEGACY: dict[str, Any] = {}
MAPPING_DPR_SEMANTIC_TO_LEGACY: dict[str, Any] = {}

LIST_DPR_ADFS_FROM_SPLIT_LEGACY: list[str] = []
for legacy, dpr_outputs in MAPPING_LEGACY_SEMANTIC_TO_DPR_WITH_SAT.items():
    if isinstance(dpr_outputs, str):
        dpr_outputs = [dpr_outputs]
    for dpr_sat in dpr_outputs:
        dpr = dpr_sat[3:]
        if len(dpr_outputs) > 1:
            MAPPING_LEGACY_SEMANTIC_TO_DPR.setdefault(legacy, []).append(dpr)
            LIST_DPR_ADFS_FROM_SPLIT_LEGACY.append(dpr)
        else:
            MAPPING_LEGACY_SEMANTIC_TO_DPR[legacy] = dpr
        MAPPING_DPR_WITH_SAT_SEMANTIC_TO_LEGACY.setdefault(dpr_sat, []).append(legacy)
        MAPPING_DPR_SEMANTIC_TO_LEGACY.setdefault(dpr, []).append(legacy)

LIST_DPR_ADFS_FROM_MERGED_LEGACY: list[str] = []
LIST_DPR_WITH_SAT_ADFS_FROM_MERGED_LEGACY: list[str] = []
for dpr_sat, legacies in MAPPING_DPR_WITH_SAT_SEMANTIC_TO_LEGACY.items():
    dpr = dpr_sat[3:]
    if len(legacies) > 1:
        LIST_DPR_ADFS_FROM_MERGED_LEGACY.append(dpr)
        LIST_DPR_WITH_SAT_ADFS_FROM_MERGED_LEGACY.append(dpr_sat)

FIELDS_DESCRIPTION = load_resource_file("metadata/fields_description.json")

TERM_DESCRIPTION = load_resource_file("metadata/term_description.json")
TERM_LINKS = load_resource_file("metadata/term_links.json")
TERM_DOCUMENTATION = load_resource_file("metadata/term_documentation.json")

for stac_id, stac_prop in STAC_PROPERTIES.items():
    FIELDS_DESCRIPTION[stac_id] = stac_prop.get("title", stac_id.capitalize())
    TERM_DESCRIPTION[stac_id] = stac_prop.get("description", FIELDS_DESCRIPTION[stac_id])

PRODUCT_DESCRIPTION = load_resource_file("metadata/product_description.json")
PRODUCT_LEVEL = load_resource_file("metadata/product_level.json")
PRODUCT_DOCUMENTATION = load_resource_file(
    "metadata/product_documentation.toml",
    fmt=".toml",
)

PRODUCT_DATA = dict(
    description=PRODUCT_DESCRIPTION,
    level=PRODUCT_LEVEL,
    documentation=PRODUCT_DOCUMENTATION,
    legacy=MAPPING_DPR_SEMANTIC_TO_LEGACY,
)

TERM_DATA = dict(description=TERM_DESCRIPTION, documentation=TERM_DOCUMENTATION, link=TERM_LINKS)

PRODUCT_PATTERNS = load_resource_file("product_patterns.json")

DPR_SEMANTIC_WITH_SAT_PRODUCTS = {
    "S02MSIL1A",
    "S02MSIL1B",
    "S02MSIL1C",
    "S02MSIL2A",
    "S03OLCEFR",
    "S03OLCERR",
    "S03OLCLFR",
    "S03SLSFRP",
    "S03SLSLST",
    "S03SLSRBT",
    "S03SYNAOD",
    "S03SYNSDR",
    "S03SYNV10",
    "S03SYNVG1",
    "S03SYNVGK",
}

AUXILIARY_TREE = load_resource_file("auxiliary_tree.json")
PRODUCT_TREE = load_resource_file("product_tree.json")


def fields_headers(fields: Iterable[str]) -> list[Any]:
    return [FIELDS_DESCRIPTION.get(item, item) for item in fields]


def product_summaries(
    dpr_names: Iterable[str],
    fields: Iterable[str] = ("name", "description"),
) -> list[list[str]]:
    """
    >>> product_summaries(["OLCEFR", "OLCERR"]) # doctest: +ELLIPSIS
    [['OLCEFR', 'Full Resolution ...'], ['OLCERR', 'Reduced Resolution ...']]
    """
    from sentineltoolbox.models.filename_generator import extract_semantic

    lst: list[list[str]] = []
    for name in dpr_names:
        identifier = extract_semantic(name)
        item = []
        for field in fields:
            if field == "name":
                item.append(name)
            else:
                item.append(PRODUCT_DATA.get(field, {}).get(identifier, ""))
        lst.append(item)
    return lst


def term_summaries(
    dpr_names: Iterable[str],
    fields: Iterable[str] = ("name", "description"),
) -> list[list[str]]:
    from sentineltoolbox.models.filename_generator import extract_semantic

    lst: list[list[str]] = []
    for name in dpr_names:
        name = extract_semantic(name)
        item = []
        for field in fields:
            if field == "name":
                item.append(name)
            else:
                item.append(TERM_DATA.get(field, {}).get(name, ""))
        lst.append(item)
    return lst
