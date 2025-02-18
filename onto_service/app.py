from flask import Flask, request, jsonify, send_file, render_template
from ontology_generator import OntologyGenerator
from ontology_populator import OntologyPopulator
from rdflib import Graph, RDF, URIRef, OWL
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
cors = CORS(app, origins='*')

BASE_URI = "http://example.org/"
FILE_VERSION = 1
GITHUB_TOKEN = ""
ONTOLOGY_FILE = f"v{FILE_VERSION}.owl"

generator = OntologyGenerator(BASE_URI, FILE_VERSION)
populator = OntologyPopulator(BASE_URI, GITHUB_TOKEN, FILE_VERSION)

def generate_ontology():
    generator.generate_ontology()
    populator.populate_ontology()
    return ONTOLOGY_FILE

@app.route('/generate_ontology', methods=['POST'])
def generate():
    generated_file = generate_ontology()
    return jsonify({"message": "Ontology generated successfully", "file": generated_file})

@app.route('/download_ontology', methods=['GET'])
def download_ontology():
    return send_file(ONTOLOGY_FILE, as_attachment=True)

@app.route('/list_repos', methods=['GET'])
def list_repos():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({"error": "Topic parameter is required"}), 400
    
    repos = populator.fetch_repos_by_topic(topic, limit=10)
    return jsonify(repos)

@app.route('/query_ontology', methods=['GET'])
def query_ontology():
    query = request.args['query']
    if not query:
        return jsonify({"error": "SPARQL query is required"}), 400
    print(query)
    g = Graph()
    g.parse("teste.owl", format="xml")
    results = g.query(query)
    response = []
    for row in results:
        response.append([str(item) for item in row])
    #print(response)
    return jsonify({"results": response})

def rdf_to_cytoscape(graph):
    elements = []
    for subj, pred, obj in graph:
        subj_id = str(subj)
        obj_id = str(obj)
        elements.append({"data": {"id": subj_id, "label": subj_id}})
        elements.append({"data": {"id": obj_id, "label": obj_id}})
        elements.append({"data": {"source": subj_id, "target": obj_id, "label": str(pred)}})
    return elements

@app.route('/graph', methods=['GET'])
def graph():
    g = Graph()
    g.parse("teste.owl", format="xml")
    elements = rdf_to_cytoscape(g)
    return jsonify(elements)



@app.route('/classes', methods=['GET'])
def get_classes():
    g = Graph()
    g.parse("teste.owl", format="xml")
    classes = []
    for s in g.subjects(RDF.type, OWL.Class):
        classes.append(s.n3(g.namespace_manager).replace('<', '').replace('>', ''))
    return jsonify(classes)

@app.route('/individuals', methods=['GET'])
def get_individuals():
    g = Graph()
    g.parse("teste.owl", format="xml")
    query = request.args['class_uri']
    target_class = URIRef(query.replace("#", "/"))

    individuals = set(g.subjects(RDF.type, target_class))
    test = []
    for lala in individuals:
        test.append(lala.n3(g.namespace_manager).replace('<', '').replace('>', ''))
    #print(test)
    return jsonify(test)

@app.route('/properties', methods=['GET'])
def get_individual_properties():
    g = Graph()
    g.parse("teste.owl", format="xml")
    query = request.args['individual_uri']
    target_ind = URIRef(query)
    print(target_ind)
    properties = {}
    for p, o in g.predicate_objects(target_ind):
        properties[p.n3(g.namespace_manager)] = o.n3(g.namespace_manager)
    return jsonify(properties)

if __name__ == '__main__':
    app.run(debug=True)
