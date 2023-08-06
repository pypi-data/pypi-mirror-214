# pylint: disable-msg=W0622
"""cubicweb-blog packaging information"""

modname = "blog"
distname = "cubicweb-%s" % modname

numversion = (2, 2, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
description = "blogging component for the CubicWeb framework"
web = "https://forge.extranet.logilab.fr/cubicweb/cubes/%s" % distname
mailinglist = "mailto://cubicweb@lists.logilab.org"
author = "Logilab"
author_email = "contact@logilab.fr"
classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]

__depends__ = {
    "cubicweb": ">= 3.38.0, < 3.39.0",
    "cubicweb-sioc": ">= 0.5.0",
    "six": ">= 1.4.0",
}
__recommends__ = {
    "cubicweb-tag": None,
    "cubicweb-preview": None,
    "cubicweb-comment": ">= 1.6.3",
    "cubicweb-seo": None,
    "feedparser": None,
    "rdflib": None,
}
