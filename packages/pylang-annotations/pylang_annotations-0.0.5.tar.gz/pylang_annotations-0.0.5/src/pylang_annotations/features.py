from typing import Final


class _Feature:
    """Internal feature flag used by Pylang for special annotations."""
    pass


#: Skip the module to optimize
skip_module: Final[_Feature] = _Feature()
"""
`skip_module` is an annotation used to mark a module that should be skipped during optimization.

To use it, place the following import at the top of your module:
    from pylang.annotations import skip_module
"""
