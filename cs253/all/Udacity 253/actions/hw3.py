import json
import re

__author__ = 'dhensche'

from util.handler import Handler
from model.post import Post
from model.base_model import ModelEncoder

class BlogHome(Handler):
    def get(self):
        self.render('blog/index.html', entries=Post.select_all())

class Blog(Handler):
    def render_form(self, content='', subject='', error=''):
        self.render('blog/form.html', content=content, subject=subject, error=error)

    def get(self, id):
        if id == 'newpost':
            self.render_form()
        elif str(id).isdigit():
            p = Post.get_by_id([int(id)])[0]
            self.render('blog/post.html', post=p)
        elif re.match(r'\d+\.json', id):
            p = Post.get_by_id([int(str(id).split('.')[0])])[0]
            self.render_json(p.to_json())
        elif str(id) == '.json':
            self.render_json(json.dumps(list(Post.select_all()), cls=ModelEncoder))
        else:
            self.error(404)

    def post(self, id):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(subject=subject, content=content)
            key = post.put()
            self.redirect('/blog/' + str(key.id()))
        else:
            self.render_form(content, subject, 'Both a subject and content must be present')