# main.py

from ontology_generator import OntologyGenerator
from ontology_populator import OntologyPopulator

FILE_VERSION = 1
BASE_URI = "http://example.org/"
GITHUB_TOKEN = ""

if not GITHUB_TOKEN:
    raise ValueError("Missing GITHUB_TOKEN")

def main():
    # Generate the ontology
    generator = OntologyGenerator(BASE_URI, FILE_VERSION)
    generator.generate_ontology()

    # Populate the ontology with GitHub data
    populater = OntologyPopulator(BASE_URI, GITHUB_TOKEN, FILE_VERSION)
    populater.populate_ontology()


if __name__ == "__main__":
    main()
