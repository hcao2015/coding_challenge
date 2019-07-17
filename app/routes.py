import logging

import flask
from flask import Response, jsonify
from app import api

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/api/v1/teams/<team_name>", methods=["GET"])
def get_team(team_name):
    """
    Endpoint to merged team profile API
    :param team_name
    """
    team = api.MainAPI(team_name=team_name)
    team_data = team.get_individual_team()
    return jsonify(**team_data['data']), team_data['status']


@app.route("/api/v1/orgs/<org_name>/teams/<team_name>", methods=["GET"])
def get_info(org_name, team_name):
    """
    Enpoint to merged profile from Github organization and Bitbucket team API
    :param org_name, team_name
    """
    team = api.MainAPI(team_name=team_name, organization_name=org_name)
    team_data = team.get_team_in_org_info()
    return jsonify(**team_data['data']), team_data['status']
