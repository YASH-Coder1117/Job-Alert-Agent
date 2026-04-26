import unittest
from utils.dedup import generate_hash
from utils.filter import keyword_filter
from config.config import config

class TestPipelineUtils(unittest.TestCase):

    def setUp(self):
        # Override config preferences for testing
        config.PREFERENCES = {
            "keywords": {
                "include": ["python", "ai"],
                "exclude": ["senior", "manager"]
            }
        }

    def test_generate_hash_consistency(self):
        job = {"title": "AI Engineer", "company": "Tech Corp", "location": "Remote"}
        hash1 = generate_hash(job)
        hash2 = generate_hash(job)
        self.assertEqual(hash1, hash2)

    def test_generate_hash_case_insensitivity(self):
        job1 = {"title": "AI Engineer", "company": "Tech Corp", "location": "Remote"}
        job2 = {"title": "ai engineer", "company": "tech corp", "location": "remote"}
        self.assertEqual(generate_hash(job1), generate_hash(job2))

    def test_keyword_filter_include(self):
        job = {"title": "Python AI Developer", "description": "Looking for someone with Python skills."}
        self.assertTrue(keyword_filter(job))

    def test_keyword_filter_exclude(self):
        job = {"title": "Senior AI Engineer", "description": "Looking for a senior developer."}
        self.assertFalse(keyword_filter(job))

    def test_keyword_filter_no_match(self):
        job = {"title": "Java Developer", "description": "Looking for Java Spring Boot."}
        self.assertFalse(keyword_filter(job))

if __name__ == '__main__':
    unittest.main()
