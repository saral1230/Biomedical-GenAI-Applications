import unittest
from unittest.mock import patch, MagicMock
from src.data_ingestion.pubmed_api import search_pubmed, fetch_pubmed_abstracts
from src.data_ingestion.pubtator_api import fetch_pubtator_annotations


class TestDataIngestion(unittest.TestCase):
    @patch("src.data_ingestion.pubmed_api.Entrez.esearch")
    def test_search_pubmed(self, mock_esearch):
        """Test searching PubMed for PMIDs."""
        mock_esearch.return_value.read.return_value = {"IdList": ["12345", "67890"]}
        pmids = search_pubmed("TP53 AND lung cancer", max_results=2)
        self.assertEqual(pmids, ["12345", "67890"])

    @patch("src.data_ingestion.pubmed_api.Entrez.efetch")
    def test_fetch_pubmed_abstracts(self, mock_efetch):
        """Test retrieving abstracts from PubMed."""
        mock_efetch.return_value.read.return_value = "This is a sample abstract."
        abstract = fetch_pubmed_abstracts(["12345"])
        self.assertIn("sample abstract", abstract.lower())

    @patch("requests.get")
    def test_fetch_pubtator_annotations(self, mock_get):
        """Test retrieving annotations from PubTator."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"12345": {"annotations": ["Gene", "Disease"]}}
        mock_get.return_value = mock_response
        annotations = fetch_pubtator_annotations(["12345"])
        self.assertIn("12345", annotations)
        self.assertIn("annotations", annotations["12345"])


if __name__ == "__main__":
    unittest.main()
