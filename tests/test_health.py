import falcon
import unittest
import httpretty
import json
from falcon import testing
from prov.app import init_api
from prov.api.healthcheck import healthcheck_response


class appHealthTest(testing.TestCase):
    """Testing GM prov function and initialize it for that purpose."""

    def setUp(self):
        """Setting the app up."""
        self.app = init_api()

    def tearDown(self):
        """Tearing down the app up."""
        pass


class TestProv(appHealthTest):
    """Testing if there is a health endoint available."""

    def test_create(self):
        """Test GET health message."""
        self.app
        pass

    @httpretty.activate
    def test_health_ok(self):
        """Test GET health is ok."""
        httpretty.register_uri(httpretty.GET, "http://localhost:7030/health", status=200)
        result = self.simulate_get('/health')
        assert(result.status == falcon.HTTP_200)

    @httpretty.activate
    def test_health_response(self):
        """Response to healthcheck endpoint."""
        httpretty.register_uri(httpretty.GET, "http://localhost:3030/{0}/ping".format("$"), "2017-09-18T11:41:19.915+00:00", status=200)
        httpretty.register_uri(httpretty.GET, "http://localhost:7030/health", status=200)
        response = healthcheck_response("Running", True)
        result = self.simulate_get('/health')
        assert(result.content == response)

    def test_actual_health_response(self):
        """Test if json response format."""
        response = healthcheck_response("Running", True)
        json_response = {"graphStore": "Running", "provService": "Running"}
        assert(json_response == json.loads(response))


if __name__ == "__main__":
    unittest.main()