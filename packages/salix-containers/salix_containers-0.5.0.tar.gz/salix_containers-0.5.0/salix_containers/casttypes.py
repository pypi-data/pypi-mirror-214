

class CastBase:
    """
    Identical to regular dict/list except on instantiation it performs a
    one-off recursive recasting of all contained items that have a type listed
    in cast_map to the mapped target type.

    Also automatically recasts any list or dict instances to CastList and
    CastDict respectively and recurses them.

    Will only recurse lists and dicts, so if you want to recurse into tuples
    or sets, make sure to include a conversion for these into lists.

    Useful if you have stubborn objects that won't pickle or export to json for
    example.

    cast_map is a dict of conversion types and their recast targets, e.g.:

        {int: str, float: Decimal}

    Conversion types can be a tuple of types:

        {(int, float): str}


    """
    def __init__(self, *args, cast_map, **kwargs):
        # recast keys of cast_map to always be tuples
        cast_map = {(tuple([key]) if not isinstance(key, tuple) else key): value for key, value in cast_map.items()}
        self.cast_map = cast_map
        super().__init__(*args, **kwargs)
        self._recast()

    def _recast(self):
        raise NotImplemented()

    def _recast_item(self, item):
        # Try to recast it first, then recurse
        for src_types, dst_type in self.cast_map.items():
            for src_type in src_types:
                if isinstance(item, src_type):
                    item = dst_type(item)
                    break
        if isinstance(item, list):
            return CastList(item, cast_map=self.cast_map)
        elif isinstance(item, dict):
            return CastDict(item, cast_map=self.cast_map)
        else:
            return item


class CastDictMixin(CastBase):
    def _recast(self):
        for k, v in self.items():
            self[k] = self._recast_item(v)


class CastListMixin(CastBase):
    def _recast(self):
        for i, item in enumerate(self):
            self[i] = self._recast_item(item)


class CastDict(CastDictMixin, dict):
    pass


class CastList(CastListMixin, list):
    pass


