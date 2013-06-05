import mock
import unittest
import datetime

from jenkinsapi.jenkins import Jenkins

class TestJenkins(unittest.TestCase):

	DATA = {}

	@mock.patch.object(Jenkins, '_poll')
	def setUp(self, _poll):
		_poll.return_value = self.DATA
		self.J = Jenkins('http://localhost:8080', username='foouser', password='foopassword')

	def testClone(self):
		JJ = self.J._clone()
		self.assertNotEquals(id(JJ), id(self.J))
		self.assertEquals(JJ, self.J)

if __name__ == '__main__':
	unittest.main()