import unittest
from rdflib import Graph, URIRef
from prov.utils.prefixes import bind_prefix, ATTXBase, create_uri


class PrefixTestCase(unittest.TestCase):
    """Test for Prefixes connection."""

    def setUp(self):
        """Set up test fixtures."""
        self.graph = Graph()

    def test_bind_prefix(self):
        """Test for Namespaces."""
        bind_prefix(self.graph)
        self.assertTrue(list(self.graph.namespaces()) != [], "Test if there are namespaces.")

    def test_create_URI_2vars(self):
        """Test creating an URI with 2 variables."""
        test_uri = create_uri(ATTXBase, "test")
        assert(test_uri == URIRef("{0}{1}".format(ATTXBase, "test")))

    def test_create_URI_3vars(self):
        """Test creating an URI with 3 variables."""
        test_uri = create_uri(ATTXBase, "test", "add")
        assert(test_uri == URIRef("{0}{1}_{2}".format(ATTXBase, "test", "add")))


if __name__ == "__main__":
    unittest.main()
