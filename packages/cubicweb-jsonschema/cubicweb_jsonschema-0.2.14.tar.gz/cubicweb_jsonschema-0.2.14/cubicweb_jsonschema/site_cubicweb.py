# copyright 2017-2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""cubicweb-jsonschema's site configuration."""


def add_mappers_to_cube_appobject_path() -> None:
    """Add "mappers" to `cube_appobject_path` class attribute of CubicWeb
    configuration classes.
    """
    import importlib
    import logging

    LOGGER = logging.getLogger("cubicweb-jsonschema")
    LOGGER.info('adding "mappers" to cube appobjects path')

    # See cubicweb.cwconfig.CubicWebConfiguration.load_available_configs()
    # where all known configuration modules are listed.
    # TODO: We should have a better way to discovered registered
    # configuration classes.
    CONFS = (
        ("cubicweb.pyramid.config", "AllInOneConfiguration"),
        ("cubicweb.cw_config", "CubicWebConfiguration"),
        ("cubicweb.devtools.apptest_config", "ApptestConfiguration"),
        ("cubicweb_web.devtools.testlib", "WebApptestConfiguration"),
        (
            "cubicweb_web.devtools.testlib",
            "WebPostgresApptestConfiguration",
        ),
        ("cubicweb_web.webconfig", "WebAllInOneConfiguration"),
    )

    for modname, configclsname in CONFS:
        try:
            mod = importlib.import_module(modname)
        except ImportError:
            LOGGER.warning(
                'failed to import %s, "mappers" appobjects will not '
                "loaded for this configuration",
                modname,
            )
            continue
        configcls = getattr(mod, configclsname)
        configcls.cube_appobject_path.add("mappers")


add_mappers_to_cube_appobject_path()
del add_mappers_to_cube_appobject_path
