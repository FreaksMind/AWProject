# wado_app/services/ontology_service.py
from rdflib import Graph, Namespace, URIRef, Literal

def build_ontology():
    g = Graph()
    WADO = Namespace("http://wado.org/ontology#")
    g.bind("wado", WADO)
    
    repo1 = URIRef(WADO["Repo1"])
    lang_python = URIRef(WADO["Python"])
    g.add((repo1, WADO.usesLanguage, lang_python))
    
    return g.serialize(format='json-ld')

def convert_to_graph_format(ontology_json_ld):
    g = Graph()
    g.parse(data=ontology_json_ld, format='json-ld')

    nodes = []
    edges = []

    for s, p, o in g:
        nodes.append({"id": str(s), "label": s.split("#")[-1]})
        nodes.append({"id": str(o), "label": o.split("#")[-1]})
        edges.append({"source": str(s), "target": str(o), "relation": p.split("#")[-1]})

    unique_nodes = {node["id"]: node for node in nodes}.values()  # Remove duplicates
    return {"nodes": list(unique_nodes), "edges": edges}
