import requests
from rdflib import Graph, URIRef, RDFS, XSD, Namespace, Literal, RDF
from datetime import datetime

class OntologyPopulator:
    def __init__(self, base_uri, github_token, file_version):
        self.base_uri = base_uri
        self.github_token = github_token
        self.file_version = file_version
        self.g = Graph()
        self.g.parse(f"v{self.file_version}.owl", format="xml")
        self.WEBDEV = Namespace(self.base_uri)

    def safe_string(self, uri_str):
        safe_uri = uri_str.replace(" ", "-").replace("'", "").replace('"', "").replace("#", "_sharp")
        return safe_uri

    def fetch_repos_by_topic(self, topic, min_stars=10000, limit=50):
        url = "https://api.github.com/graphql"
        headers = {"Authorization": f"Bearer {self.github_token}"}

        query_string = f"topic:{topic} stars:>={min_stars} sort:stars-desc"
        graphql_query = """
        query($queryString: String!, $limit: Int!) {
          search(query: $queryString, type: REPOSITORY, first: $limit) {
            edges {
              node {
                ... on Repository {
                  name
                  description
                  url
                  createdAt
                  licenseInfo {
                    name
                  }
                  primaryLanguage {
                    name
                  }
                }
              }
            }
          }
        }
        """
        variables = {"queryString": query_string, "limit": limit}
        response = requests.post(url, json={"query": graphql_query, "variables": variables}, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub GraphQL query failed: {response.status_code}\n{response.text}")

        data = response.json()
        edges = data["data"]["search"]["edges"]
        return [edge["node"] for edge in edges]

    def has_year(self, repo):
        created_at = repo.get("createdAt")
        if created_at:
            dt = datetime.fromisoformat(created_at.replace("Z", ""))
            return str(dt.year)
        return None

    def insert_repos_into_ontology(self, repos, topic):
        for repo in repos:
            safe_name = self.safe_string(repo["name"])
            repo_uri = URIRef(f"{self.base_uri}{topic}#{safe_name}")

            self.g.add((repo_uri, RDF.type, getattr(self.WEBDEV, topic)))
            self.g.add((repo_uri, RDFS.label, Literal(repo["name"], datatype=XSD.string)))

            if repo.get("description"):
                self.g.add((repo_uri, self.WEBDEV.hasDescription, Literal(repo["description"], datatype=XSD.string)))

            if repo.get("url"):
                self.g.add((repo_uri, self.WEBDEV.hasURL, Literal(repo["url"], datatype=XSD.anyURI)))

            year_str = self.has_year(repo)
            if year_str is not None:
                self.g.add((repo_uri, self.WEBDEV.hasReleaseYear, Literal(year_str, datatype=XSD.gYear)))

            license_str = repo.get("licenseInfo", {})
            if license_str:
                license_str = self.safe_string(license_str.get("name"))
                license_uri = URIRef(f"http://example.org/License#{license_str}")
                if not (license_uri, RDF.type, self.WEBDEV.License) in self.g:
                    self.g.add((license_uri, RDF.type, self.WEBDEV.License))
                    self.g.add((license_uri, RDFS.label, Literal(license_str, datatype=XSD.string)))
                self.g.add((repo_uri, self.WEBDEV.isLicenseUnder, license_uri))

            primary_lang_str = repo.get("primaryLanguage", {})
            if primary_lang_str:
                primary_lang_str = self.safe_string(primary_lang_str.get("name"))
                primary_lang_uri = URIRef(f"http://example.org/ProgrammingLanguage#{primary_lang_str}")
                if not (primary_lang_uri, RDF.type, self.WEBDEV.ProgrammingLanguage) in self.g:
                    self.g.add((primary_lang_uri, RDF.type, self.WEBDEV.ProgrammingLanguage))
                    self.g.add((primary_lang_uri, RDFS.label, Literal(primary_lang_str, datatype=XSD.string)))
                self.g.add((repo_uri, self.WEBDEV.usesLanguage, primary_lang_uri))

    def fetch_dbpedia_data(self):
        """Fetch programming languages, paradigms, and operating systems data from DBpedia."""
        endpoint = "https://dbpedia.org/sparql"
        query = """
        SELECT ?entity ?label ?comment ?type WHERE {
          { ?entity rdf:type dbo:ProgrammingLanguage . }
          UNION
          { ?entity rdf:type dbo:ProgrammingParadigm . }
          UNION
          { ?entity rdf:type dbo:OperatingSystem . }
          
          ?entity rdfs:label ?label .
          ?entity rdfs:comment ?comment .
          OPTIONAL { ?entity rdf:type ?type . }
          
          FILTER (lang(?label) = "en" && lang(?comment) = "en")
        }
        """
        params = {"query": query, "format": "json"}
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"DBpedia query failed: {response.status_code}\n{response.text}")

    def add_dbpedia_information(self):
        dbpedia_data = self.fetch_dbpedia_data()
        for result in dbpedia_data["results"]["bindings"]:
            label = result["label"]["value"]
            comment = result["comment"]["value"]
            type_uri = result["type"]["value"] if "type" in result else None

            entity_type = self.WEBDEV.ProgrammingLanguage if "ProgrammingLanguage" in type_uri else \
                          self.WEBDEV.ProgrammingParadigm if "ProgrammingParadigm" in type_uri else \
                          self.WEBDEV.OperatingSystem

            entity_uri_ref = URIRef(f"{self.base_uri}{entity_type}#{self.safe_string(label)}")
            self.g.add((entity_uri_ref, RDF.type, entity_type))
            self.g.add((entity_uri_ref, RDFS.label, Literal(label, datatype=XSD.string)))
            self.g.add((entity_uri_ref, self.WEBDEV.hasDescription, Literal(comment, datatype=XSD.string)))

    def populate_ontology(self):
        #self.add_dbpedia_information()
        print("Done adding DBpedia information.")

        predefined_topics = {
            "programming_language": "ProgrammingLanguage",
            "framework": "Framework",
            "backend": "BackendFramework",
            "frontend": "FrontendFramework",
            "ml": "MachineLearningFramework",
        }

        for key, topic in predefined_topics.items():
            repos = self.fetch_repos_by_topic(key, min_stars=1000, limit=50)
            self.insert_repos_into_ontology(repos, topic)
            print(f"Done processing '{key}' topic.\n")

        new_version = self.file_version + 1
        self.g.serialize(destination=f"v{new_version}.owl", format="xml")
        print(f"Updated ontology saved: {new_version}.owl")
