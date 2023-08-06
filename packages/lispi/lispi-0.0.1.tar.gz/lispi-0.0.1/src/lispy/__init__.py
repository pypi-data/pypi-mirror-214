try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


__all__ = [
        'slideEdit',
        'text2audio',
        'revealjs_template',
        ]

# Version of the ppr package
__version__ = "0.0.01"