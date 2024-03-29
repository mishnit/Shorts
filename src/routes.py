from flask import redirect, jsonify, request, abort
from schema import schema
from flask_graphql import GraphQLView

from models import Url
from database import db
from sqlalchemy.schema import Sequence
from helpers import is_valid_url, to_emoji_slug

# Graphql routes instantiated at /graphql/ with GUI.
def create_graphql_route(app):
    app.add_url_rule('/graphql/', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# Routes are instantiated with reference to app, as per the Flask convention.
def create_rest_routes(app):
    # On receiving a GET request for a short-url, reply either with a 404 if it's not found in our database,
    # or a 301 redirect if it is.
    @app.route('/<string:slug>', methods=['GET'])
    def get_redirect(slug):
        url = Url.query.filter(Url.slug == slug).first()

        if url == None:
            abort(404)
        return redirect(url.redirect, code=302)

    # On receiving a long-url to be shortened, we:
    #   1) validate and clean the inputs
    #   2) check if it already exists, if so short-circuit and return the existing shortened url
    #   3) grab the next id out of the database, use it to generate the next smallest available url
    #      save the new instance back to the database.
    #   4) return the new shortened url back to the client.
    @app.route('/', methods=['POST'])
    def create_url():
        if not request.is_json:
            abort(422)

        content = request.json
        redirect_url = content.get('url', '').strip()

        if not is_valid_url(redirect_url):
            abort(422)

        # Check if it already exists
        url = Url.query.filter(Url.redirect==redirect_url).first()

        if url:
            return jsonify({ 'shorter': url.get_full_short() })

        next_id = db.session.execute(Sequence("urls_id_seq"))
        url = Url(id=next_id, redirect=redirect_url, slug=to_emoji_slug(next_id))

        db.session.add(url)
        db.session.commit()

        return jsonify({'shorter': url.get_full_short() })
