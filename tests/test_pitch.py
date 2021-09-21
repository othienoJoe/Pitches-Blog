import unittest
from app.models import Pitch

class PitchTest(unittest.TestCase):
	'''
	Test Class to test the behavior of the Movie class
	'''

	def setUp(self):
		'''
		Set up method that will run before every Test
		'''
		self.new_pitch = Pitch(title="Test Post Title",body="Test Content body", author_id="Test Post Author", slug="test-post-slug")

	def test_instance(self):
		self.assertTrue(isinstance(self.new_pitch,Pitch))
