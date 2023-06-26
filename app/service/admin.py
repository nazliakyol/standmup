import requests
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from flask_admin import expose
from app.model import db
from app.model.comedian import Comedian
from app.model.product import Product
from app.model.tag import Tag
from app.model.video import Video
from app.model.youtubeLink import YoutubeLink


class VideoModelView(ModelView):
    form_excluded_columns = ('creation_date',)
    form_columns = ('title', 'link', 'description', 'is_active', 'tags',)

    def create_form(self, obj=None):
        form = super(VideoModelView, self).create_form(obj=obj)

        form.tags = SelectMultipleField('Tags', widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
        tags = db.session.query(Tag).order_by(Tag.name.asc()).all()
        form.tags.choices = [(tag.id, tag.name) for tag in tags]

        return form

    def on_model_change(self, form, model, is_created):
        model.tags = Tag.query(Tag).filter(Tag.id.in_(form.tags.data)).all()


class AdminHome(AdminIndexView):
    @expose('/')
    def index(self):
        response = requests.get('http://localhost:5000/api/stat')
        result = response.json()
        return self.render('admin/home.html', result=result)

    default_view = 'index'


admin = None

def start_admin(app):
    global admin
    admin = Admin(app, index_view=AdminHome())
    admin.add_view(VideoModelView(Video, db.session))
    admin.add_view(ModelView(Comedian, db.session))
    admin.add_view(ModelView(Tag, db.session))
    admin.add_view(ModelView(YoutubeLink, db.session))
    admin.add_view(ModelView(Product, db.session))

