import json
import falcon
from prov.schemas import load_schema
from prov.utils.validate import validate
from prov.utils.logs import app_logger
from prov.applib.construct_prov import prov_task


class ConstructProvenance(object):
    """Construct Provenance based on provided request."""

    @validate(load_schema('provschema'), load_schema('altprovschema'))
    def on_post(self, req, resp, parsed):
        """Respond on GET request to map endpoint."""
        if isinstance(parsed, dict):
            response = prov_task.delay(parsed["provenance"], parsed["payload"])
            result = {'taskID': response.id}
            resp.body = json.dumps(result)
            resp.content_type = 'application/json'
        elif isinstance(parsed, list):
            tasks = []
            for obj in parsed:
                response = prov_task.delay(obj["provenance"], obj["payload"])
                tasks.append(response.id)
            result = {'taskID': tasks}
            resp.body = json.dumps(result)
            resp.content_type = 'application/json'
        # result = construct_provenance(parsed["provenance"], parsed["payload"])
        # resp.body = result
        # resp.content_type = 'text/turtle'
        resp.status = falcon.HTTP_200
        app_logger.info('Accepted POST Request for /prov.')


class RetrieveProvenance(object):
    """Update Provenance on request."""

    @validate(load_schema('idtype'))
    def on_get(self, req, resp, provID):
        """Respond on GET request to map endpoint."""
        resp.status = falcon.HTTP_200
        app_logger.info('Finished operations on /prov/{0} GET Request.'.format(provID))
