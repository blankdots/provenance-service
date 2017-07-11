import falcon
from prov.utils.logs import app_logger
from prov.api.healthcheck import HealthCheck
from prov.api.provenance import ConstructProvenance, RetrieveProvenance
from prov.api.graph_endpoint import GraphStatistics, GraphList

api_version = "0.1"  # TO DO: Figure out a better way to do versioning


def init_api():
    """Create the API endpoint."""
    provservice = falcon.API()

    provservice.add_route('/health', HealthCheck())

    provservice.add_route('/%s/prov' % (api_version), ConstructProvenance())
    provservice.add_route('/%s/prov/show/{provID}' % (api_version), RetrieveProvenance())

    # provservice.add_route('/%s/graph/query' % (api_version), do_sparql)
    # provservice.add_route('/%s/graph/update' % (api_version), do_graph_update)
    provservice.add_route('/%s/graph/list' % (api_version), GraphList())
    provservice.add_route('/%s/graph/statistics' % (api_version), GraphStatistics())
    # provservice.add_route('/%s/graph/{graphID}' % (api_version), get_graph)

    app_logger.info('App is running.')
    return provservice


if __name__ == '__main__':
    init_api()