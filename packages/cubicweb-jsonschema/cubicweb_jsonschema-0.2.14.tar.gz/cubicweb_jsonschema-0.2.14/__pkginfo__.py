# pylint: disable=W0622
"""cubicweb-jsonschema application packaging information"""


cubename = "jsonschema"
modname = "cubicweb_" + cubename
distname = "cubicweb-" + cubename

numversion = (0, 2, 14)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "JSON Schema for CubicWeb"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/" + cubename

__depends__ = {
    "cubicweb": ">= 4.5.2, < 5.0.0",
    "cubicweb-web": ">= 1.3.1, < 2.0.0",
    "iso8601": None,
    "jsl": None,
    "pyramid": ">= 1.10.8",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: JavaScript",
]
