from sentineltoolbox.hotfix import (
    ConverterDateTime,
    HotfixPath,
    HotfixPathInput,
    HotfixValue,
    HotfixValueInput,
    HotfixWrapper,
    to_int,
    to_lower,
)
from sentineltoolbox.typedefs import Converter, MetadataType_L

#################################################
# WRAPPERS
#################################################
# A wrapper simplifies the user's experience by automatically converting raw data into
# high-level Python types on the fly. For example, a date string is returned as a datetime object.
# It also performs the reverse conversion: if the user sets a datetime object, it is converted
# back to a string to support serialization.

# category / relative path -> Wrapper
WRAPPERS_GENERIC_FUNCTIONS: dict[MetadataType_L, dict[str, Converter]] = {
    "stac_properties": {
        "created": ConverterDateTime(),
        "end_datetime": ConverterDateTime(),
        "start_datetime": ConverterDateTime(),
    },
    "stac_discovery": {},
    "metadata": {},
    "root": {},
}

#################################################
# PATHS FIXES & SHORT NAMES
#################################################
# A "path fix" automatically replaces outdated or incorrect paths with valid ones.
# This is useful for all metadata where the name has changed.

# wrong path -> valid_category, valid_path
HOTFIX_PATHS_GENERIC: HotfixPathInput = {
    # {"name": ("category", None)}  if short name is equal to attribute path relative to category.
    #  This is equivalent to {"name": ("category", "name")}
    # {"short name": ("category", "relative path name")}  if short name is different
    # Ex: {"b0_id": ("stac_properties", "bands/0/name")}
    # {"/absolute/wrong/path": ("category", "relative/path")}
    # Ex: {"other_metadata/start_time": ("stac_properties", None)}
    # short names
    "bands": ("stac_properties", None),
    "eo:bands": ("stac_properties", "bands"),
    "platform": ("stac_properties", None),
    "product:type": ("stac_properties", None),
    "eopf:type": ("stac_properties", "product:type"),
    "product:timeline": ("stac_properties", None),
    "eopf:timeline": ("stac_properties", "product:timeline"),
    "processing:version": ("stac_properties", None),
    "processing:level": ("stac_properties", None),
    "created": ("stac_properties", None),
    "end_datetime": ("stac_properties", None),
    "start_datetime": ("stac_properties", None),
    # wrong paths
    "stac_discovery/properties/eo:bands": ("stac_properties", "bands"),
    "stac_discovery/properties/eopf:type": ("stac_properties", "product:type"),
    "stac_discovery/properties/eopf:timeline": ("stac_properties", "product:timeline"),
}


#################################################
# VALUE FIXES
#################################################
# Function used to fix definitely value

# category / relative path -> fix functions
HOTFIX_VALUES_GENERIC: HotfixValueInput = {
    "stac_properties": {"platform": to_lower, "mission": to_lower, "sat:relative_orbit": to_int},
    "stac_discovery": {},
    "metadata": {},
    "root": {},
}


HOTFIX = [
    HotfixValue(HOTFIX_VALUES_GENERIC),
    HotfixPath(HOTFIX_PATHS_GENERIC),
    HotfixWrapper(WRAPPERS_GENERIC_FUNCTIONS),
]
