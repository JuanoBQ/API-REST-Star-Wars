import os
from flask_admin import Admin
from models import db, User, Planets, People, Starship, Favorites
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Juan Admin', template_mode='bootstrap3')

    # Define your custom ModelViews
    class UserModelView(ModelView):
        # Ajusta las columnas que deseas mostrar
        column_list = ('id', 'name', 'email', 'is_active')

    class PlanetsModelView(ModelView):
        column_list = ('id', 'name')

    class PeopleModelView(ModelView):
        column_list = ('id', 'name')

    class StarshipModelView(ModelView):
        column_list = ('id', 'name')

    class FavoritesModelView(ModelView):
        column_list = ('id', 'user_id', 'planet_id',
                       'people_id', 'starship_id')

    # Add your models to the admin panel
    admin.add_view(UserModelView(User, db.session))
    admin.add_view(PlanetsModelView(Planets, db.session))
    admin.add_view(PeopleModelView(People, db.session))
    admin.add_view(StarshipModelView(Starship, db.session))
    admin.add_view(FavoritesModelView(Favorites, db.session))
