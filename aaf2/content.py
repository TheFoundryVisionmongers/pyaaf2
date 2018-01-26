from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

from uuid import UUID

from . import core
from .utils import register_class
from . import mobs
from . import mxf
from . import ama

@register_class
class Header(core.AAFObject):
    class_id = UUID("0d010101-0101-2f00-060e-2b3402060101")
    __slots__ = ()

@register_class
class ContentStorage(core.AAFObject):
    class_id = UUID("0d010101-0101-1800-060e-2b3402060101")
    __slots__ = ()

    @property
    def mobs(self):
        return self['Mobs']

    def toplevel(self):
        for mob in self.compositionmobs():
            if mob.usage == 'Usage_TopLevel':
                yield mob

    def mastermobs(self):
        for mob in self.mobs:
            if isinstance(mob, mobs.MasterMob):
                yield mob

    def compositionmobs(self):
        for mob in self.mobs:
            if isinstance(mob, mobs.CompositionMob):
                yield mob

    def sourcemobs(self):
        for mob in self.mobs:
            if isinstance(mob, mobs.SourceMob):
                yield mob

    def link_external_mxf(self, path):
        m = mxf.MXFFile(path)
        if m.operation_pattern != "OPAtom":
            raise Exception("can only link OPAtom mxf files")
        return m.link(self.root)

    def create_ama_link(self, path, metadata):
        return ama.create_ama_link(self.root, path, metadata)

    @property
    def essencedata(self):
        return self["EssenceData"]
