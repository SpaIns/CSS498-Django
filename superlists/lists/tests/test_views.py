class MyListsTest(TestCase):

	def test_my_lists_url_renders_my_lists_template(self):
		response = self.client.get('/lists/users/a@b.com/')
		self.assertTemplateUsed(response, 'my_lists.html')