from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.model import tagdb, videodb, comediandb, youtubeLinkdb
from app.model.db import application, db


class VideoModelView(ModelView):
    form_excluded_columns = ('creation_date',)

    form_columns = ('title', 'link', 'description', 'is_active', 'tags',)

    def create_form(self, obj=None):
        form = super(VideoModelView, self).create_form(obj=obj)

        form.tags = SelectMultipleField('Tags', widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
        tags = db.session.query.order_by(tagdb.Tag.name.asc()).all()
        form.tags.choices = [(tag.id, tag.name) for tag in tags]

        return form

    def on_model_change(self, form, model, is_created):
        model.tags = tagdb.Tag.query.filter(tagdb.Tag.id.in_(form.tags.data)).all()

admin = Admin(application)

def start_admin():
    admin.add_view(VideoModelView(videodb.Video, db.session))
    admin.add_view(ModelView(comediandb.Comedian, db.session))
    admin.add_view(ModelView(tagdb.Tag, db.session))
    admin.add_view(ModelView(youtubeLinkdb.YoutubeLink, db.session))

