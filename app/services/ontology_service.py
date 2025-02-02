# wado_app/services/ontology_service.py
from rdflib import Graph, Namespace, URIRef, Literal
from .github_service import fetch_repos

def build_ontology(org="mozilla"):
    g = Graph()
    WADO = Namespace("http://wado.org/ontology#")
    SCHEMA = Namespace("http://schema.org/")
    DBPEDIA = Namespace("http://dbpedia.org/ontology/")
    g.bind("wado", WADO)
    g.bind("schema", SCHEMA)
    g.bind("dbpedia", DBPEDIA)
    
    repos = fetch_repos(org)
    for repo in repos:
        repo_uri = URIRef(WADO[repo["name"]])
        g.add((repo_uri, WADO.hasURL, Literal(repo["url"])))
        g.add((repo_uri, WADO.hasDescription, Literal(repo["description"])))
        g.add((repo_uri, SCHEMA.dateCreated, Literal(repo["createdAt"])))
        g.add((repo_uri, SCHEMA.dateModified, Literal(repo["updatedAt"])))

        # Add programming languages
        if repo["primaryLanguage"]:
            lang_uri = URIRef(DBPEDIA[repo["primaryLanguage"]["name"]])
            g.add((repo_uri, WADO.usesLanguage, lang_uri))

        for lang in repo["languages"]["nodes"]:
            lang_uri = URIRef(DBPEDIA[lang["name"]])
            g.add((repo_uri, WADO.usesLanguage, lang_uri))

        # Add topics (frameworks, tools, OS, methodologies)
        for topic in repo["repositoryTopics"]["nodes"]:
            topic_name = topic["topic"]["name"]
            topic_uri = URIRef(WADO[topic_name.replace(" ", "_")])
            g.add((repo_uri, WADO.hasTopic, topic_uri))

        # Extract keywords from README to detect runtime platforms, IDEs, compilers, etc.
        if repo["readme"]:
            readme_text = repo["readme"]["text"].lower()
            if "docker" in readme_text:
                g.add((repo_uri, WADO.usesPlatform, URIRef(WADO["Docker"])))
            if "linux" in readme_text or "ubuntu" in readme_text:
                g.add((repo_uri, WADO.supportsOS, URIRef(DBPEDIA["Linux"])))
            if "visual studio code" in readme_text:
                g.add((repo_uri, WADO.usesIDE, URIRef(WADO["VSCode"])))
            if "compiler" in readme_text:
                g.add((repo_uri, WADO.usesTool, URIRef(WADO["Compiler"])))

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
