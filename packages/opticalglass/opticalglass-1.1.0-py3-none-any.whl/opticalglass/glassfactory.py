#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Michael J. Hayford
""" Interfaces for commercial glass catalogs

    The glassfactory module is intended to be the primary method by which glass
    instances are created. The :func:`create_glass` is the public factory
    function for this purpose. The public function :func:`get_glass_catalog`
    returns the glass catalog instance corresponding to the input string.

.. codeauthor: Michael J. Hayford
"""
import logging

from . import glass as cat_glass
from . import glasserror as ge
from . import rindexinfo

from .caselessDictionary import CaselessDictionary

logger = logging.getLogger(__name__)

_catalog_list = CaselessDictionary()

CDGM, Hikari, Hoya, Ohara, Schott, Sumita = range(6)
_cat_names = ["CDGM", "Hikari", "Hoya", "Ohara", "Schott", "Sumita"]
_cat_names_uc = [cat.upper() for cat in _cat_names]


def create_glass(*name_catalog):
    """ Factory function returning a catalog glass instance.

    The input argument list can take several forms:

        - 1 string argument in the form 'glass_name,catalog_name'
        - 2 arguments. The first is a string glass name. The second is a
          string or list of strings of catalog names.
    
    If 2 arguments are used and the catalog is "rindexinfo", the "name" field 
    is taken as a URL or filepath to a material in the `RefractiveIndex.INFO <https://refractiveindex.info>`_ database.

    Arguments:
        *name_catalog: tuple of 1 or 2 input items

    Raises:
        GlassCatalogNotFoundError: if catalog isn't found
        GlassNotFoundError: if name isn't in the specified catalog

    """
    def _create_glass(name, catalog):
        if catalog == "rindexinfo":
            return rindexinfo.create_glass(name)
        else:
            gn_decode = cat_glass.decode_glass_name(name)
            if catalog not in _catalog_list:
                try:
                    cat = get_glass_catalog(catalog)
                except ge.GlassError as gerr:
                    raise gerr
            if catalog in _catalog_list:
                try:
                    # Lookup the decoded glass name. This avoids some problems
                    # with how design programs not exactly matching the
                    # manufacturer's names.
                    gn, gc = _catalog_list[catalog].glass_lookup[gn_decode]
                except KeyError:
                    raise ge.GlassNotFoundError(catalog, name)
                else:
                    return _catalog_list[catalog].create_glass(gn, gc)
            elif "Robb1983" in catalog:
                return cat_glass.Robb1983Catalog().create_glass(name, catalog)
            else:
                logger.info('glass catalog %s not found', catalog)
                raise ge.GlassCatalogNotFoundError(catalog)

    if len(name_catalog) == 2:
        name, catalog = name_catalog
    else:
        name, catalog = name_catalog[0].split(',')
    if isinstance(name, str):
        name = name.strip()

    if isinstance(catalog, str):
        return _create_glass(name, catalog.strip())

    else:  # treat catalog as a list
        for cat in catalog:
            try:
                glass = _create_glass(name, cat.strip())
            except ge.GlassError:
                continue
            else:
                return glass
        logger.info('glass %s not found in %s', name, catalog)
        raise ge.GlassNotFoundError(catalog, name)


def get_glass_catalog(cat_name, mod_name=None, cls_name=None):
    """ Function returning a glass catalog instance.

    Arguments:
        catalog: name of supported catalog (CDGM, Hoya, Ohara, Schott)

    Raises:
        GlassCatalogNotFoundError: if catalog isn't found
    """
    if cat_name in _catalog_list:
        return _catalog_list[cat_name]
    else:
        try:
            if "Robb1983" in cat_name:
                glass_cat = cat_glass.glass_catalog_factory(
                    cat_name,
                    mod_name='opticalglass.glass',
                    cls_name='Robb1983Catalog')
            else:
                glass_cat = cat_glass.glass_catalog_factory(cat_name)
        except ge.GlassError as gerr:
            raise gerr
        else:
            _catalog_list[cat_name] = glass_cat
            return glass_cat


def fill_catalog_list(cat_list=None):
    """ Given a list of catalog names, populate the _catalog_list with them. """
    if cat_list is None:
        cat_list = _cat_names
    for cat in cat_list:
        get_glass_catalog(cat)
    return _catalog_list
