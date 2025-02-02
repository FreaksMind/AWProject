# app/routes.py
from flask import Blueprint, jsonify, request
from .services.github_service import fetch_repos
from .services.ontology_service import build_ontology, convert_to_graph_format

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Welcome to WADO API"})

@main.route('/repos', methods=['GET'])
def get_repos():
    org = request.args.get('org', 'mozilla')  # Default to 'mozilla'
    repos = fetch_repos(org)
    return jsonify(repos)

@main.route('/ontology', methods=['GET'])
def ontology():
    org = request.args.get('org', 'facebook')
    ontology_data = build_ontology()
    return jsonify(ontology_data)

@main.route('/graph', methods=['GET'])
def graph_data():
    ontology_data = build_ontology()  # Get ontology
    graph_json = convert_to_graph_format(ontology_data)  # Convert to nodes/edges
    return jsonify(graph_json)

from flask import render_template

@main.route('/graph-view', methods=['GET'])
def graph_view():
    return render_template("graph.html")
