from django.test import TestCase
from django.urls import reverse
from .models import BlogPost, Comment


class BlogTests(TestCase):

    def setUp(self):
        self.blog_post = BlogPost.objects.create(title="Test Post", content="Test Content")
        self.comment = Comment.objects.create(post=self.blog_post, author="Test", text="Test Comment")

    # 1. Test: création d'un blog
    def test_create_blog_post(self):
        response = self.client.post(reverse('add_post'), {
            'title': 'New Post',
            'content': 'New Content'
        })
        self.assertEqual(BlogPost.objects.count(), 2)  # Vérifie que deux posts existent
        self.assertEqual(BlogPost.objects.last().title, 'New Post')  # Vérifie le titre du dernier post
        self.assertEqual(response.status_code, 302)  # Vérifie la redirection après la création

    # 2. Test: edition d'un blog
    def test_edit_blog_post(self):
        response = self.client.post(reverse('edit_post', kwargs={'pk': self.blog_post.pk}), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updated Title')
        self.assertEqual(self.blog_post.content, 'Updated Content')

    # 3. Test: suppression d'un blgo
    def test_delete_blog_post(self):
        response = self.client.post(reverse('delete_post', kwargs={'pk': self.blog_post.pk}))
        self.assertEqual(BlogPost.objects.count(), 0)
        self.assertRedirects(response, reverse('post_list'))

    # 4. Test: ajout d'un comentaire
    def test_add_comment(self):
        response = self.client.post(reverse('add_comment', kwargs={'pk': self.blog_post.pk}), {
            'author': 'Bob',
            'text': 'Another Test Comment'
        })
        self.assertEqual(self.blog_post.comment_set.count(), 2)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.blog_post.pk}))

    # 5. Test: editer un comentaire
    def test_edit_comment(self):
        response = self.client.post(reverse('edit_comment', kwargs={'pk': self.comment.pk}), {
            'author': 'Alice',
            'text': 'Edited Comment'
        })
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Edited Comment')

    # 6. Test: suprimer un commentaire
    def test_delete_comment(self):
        response = self.client.post(reverse('delete_comment', kwargs={'pk': self.comment.pk}))
        self.assertEqual(self.blog_post.comment_set.count(), 0)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.blog_post.pk}))

    # 7. Test: test d'une requette http pour la liste des post
    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_list.html')

    # 8. Test: test d'une requette http pour le detail d'un post
    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.blog_post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')

    # 9. Test: verifie que le bon templatz est utilisé
    def test_correct_template_for_add_comment(self):
        response = self.client.get(reverse('add_comment', kwargs={'pk': self.blog_post.pk}))
        self.assertTemplateUsed(response, 'add_comment.html')

    # 10. Test: test de la redirection apres un edit de post
    def test_redirection_after_editing_post(self):
        response = self.client.post(reverse('edit_post', kwargs={'pk': self.blog_post.pk}), {
            'title': 'Updated Title',
            'content': 'Updated Content'
        })
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.blog_post.pk}))
