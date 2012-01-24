from pyramid.config import Configurator
from pyramid.exceptions import NotFound
from pyramid.exceptions import Forbidden
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from defpage.lib.authentication import AuthenticationPolicy
from defpage.lib.interfaces import IUser
from defpage.lib.util import is_int
from defpage.base.config import system_params
from defpage.base.security import User

def main(global_config, **settings):
    system_params.update(settings)
    session_factory = UnencryptedCookieSessionFactoryConfig("7oDVDSuJ")
    authentication_policy = AuthenticationPolicy()
    config = Configurator()
    config.setup_registry(settings=settings, session_factory=session_factory, authentication_policy=authentication_policy)

    config.registry.registerUtility(factory=User, provided=IUser)

    config.add_subscriber("defpage.base.layout.renderer_add_globals", "pyramid.events.BeforeRender")
    config.add_subscriber("defpage.lib.authentication.authenticate", "pyramid.events.NewRequest")

    # misc
    config.add_view("defpage.base.views.forbidden", "", context=Forbidden)
    config.add_view("defpage.base.views.empty", "", renderer="defpage.base:templates/notfound.pt", context=NotFound)
    config.add_view("defpage.base.views.empty", "error", renderer="defpage.base:templates/error.pt")
    config.add_view("defpage.base.views.default", "")

    # collection
    config.add_view("defpage.base.views.create_collection", "create_collection", renderer="defpage.base:templates/collection/create.pt")

    config.add_route("display_collection", "/collection/{name}", custom_predicates=(is_int,))
    config.add_view("defpage.base.views.display_collection", route_name="display_collection", renderer="defpage.base:templates/collection/display.pt")

    config.add_route("collection_properties", "/collection/{name}/properties", custom_predicates=(is_int,))
    config.add_view("defpage.base.views.collection_properties", route_name="collection_properties", renderer="defpage.base:templates/collection/properties.pt")

    config.add_route("delete_collection", "/collection/{name}/delete", custom_predicates=(is_int,))
    config.add_view("defpage.base.views.delete_collection", route_name="delete_collection", renderer="defpage.base:templates/collection/delete.pt")

    config.add_route("collection_permissions", "/collection/{name}/permissions", custom_predicates=(is_int,))
    config.add_view("defpage.base.views.collection_permissions", route_name="collection_permissions", renderer="defpage.base:templates/collection/permissions.pt")

    # source
    config.add_route("source_overview", "/collection/{name}/source", custom_predicates=(is_int,))
    config.add_view("defpage.base.views.source_overview", route_name="source_overview", renderer="defpage.base:templates/source/overview.pt")

    # transmission
    config.add_route("transmission_overview", "/collection/{name}/transmission", custom_predicates=(is_int,))
    config.add_view("defpage.base.views.transmission_overview", route_name="transmission_overview", renderer="defpage.base:templates/transmission/overview.pt")

    return config.make_wsgi_app()
