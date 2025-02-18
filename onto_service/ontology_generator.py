from rdflib import Graph, URIRef, Literal, RDF, RDFS, OWL, XSD

class OntologyGenerator:
    def __init__(self, base_uri, file_version):
        self.base_uri = base_uri
        self.file_version = file_version
        self.g = Graph()
        self.EX = URIRef(self.base_uri)
        self.rdf_ns = RDF
        self.rdfs_ns = RDFS
        self.owl_ns = OWL
        self.xsd_ns = XSD

    def generate_ontology(self):
        self._add_metadata()
        self._add_classes()
        self._add_subclass_relations()
        self._add_object_properties()
        self._add_data_properties()
        self._serialize_ontology()

    def _add_metadata(self):
        self.g.add((self.EX, self.rdf_ns.type, self.owl_ns.Ontology))

    def _add_classes(self):
        classes = [
            "ProgrammingLanguage", "ProgrammingParadigm", "SoftwareArchitecture",
            "License", "OperatingSystem", "Compiler", "Interpreter", "ApplicationServer",
            "Framework", "ORMFramework", "SPAFramework", "FrontendFramework",
            "BackendFramework", "TemplateEngine", "MachineLearningFramework",
            "TestingFramework", "AOPFramework", "SDK", "Library", "IDE", "Organization"
        ]
        for cls in classes:
            self.g.add((self.EX + cls, self.rdf_ns.type, self.owl_ns.Class))
            self.g.add((self.EX + cls, self.rdfs_ns.label, Literal(cls.replace("Framework", " Framework"))))

    def _add_subclass_relations(self):
        framework_subclasses = [
            ("ORMFramework", "Framework"), ("SPAFramework", "Framework"), ("FrontendFramework", "Framework"),
            ("BackendFramework", "Framework"), ("TemplateEngine", "Framework"), ("MachineLearningFramework", "Framework"),
            ("TestingFramework", "Framework"), ("AOPFramework", "Framework")
        ]
        for subclass, superclass in framework_subclasses:
            self.g.add((self.EX + subclass, self.rdf_ns.type, self.owl_ns.Class))
            self.g.add((self.EX + subclass, self.rdfs_ns.subClassOf, self.EX + superclass))

    def _add_object_properties(self):
        object_properties = [
            ("isLicensedUnder", "Framework", "License"), ("hasAuthor", "Framework", "Organization"),
            ("usesLanguage", "Framework", "ProgrammingLanguage"), ("supportsParadigm", "Framework", "ProgrammingParadigm"),
            ("usesArchitecture", "Framework", "SoftwareArchitecture")
        ]
        for prop, domain, range in object_properties:
            self.g.add((self.EX + prop, self.rdf_ns.type, self.owl_ns.ObjectProperty))
            self.g.add((self.EX + prop, self.rdfs_ns.domain, self.EX + domain))
            self.g.add((self.EX + prop, self.rdfs_ns.range, self.EX + range))

    def _add_data_properties(self):
        data_properties = [
            ("hasName", "ProgrammingLanguage", self.xsd_ns.string), ("hasDesigner", "ProgrammingLanguage", self.xsd_ns.string),
            ("hasDeveloper", "ProgrammingLanguage", self.xsd_ns.string), ("hasVersion", "Framework", self.xsd_ns.string),
            ("hasDescription", "Framework", self.xsd_ns.string), ("hasReleaseYear", "Framework", self.xsd_ns.gYear),
            ("hasURL", "Framework", self.xsd_ns.anyURI)
        ]
        for prop, domain, range in data_properties:
            self.g.add((self.EX + prop, self.rdf_ns.type, self.owl_ns.DatatypeProperty))
            self.g.add((self.EX + prop, self.rdfs_ns.domain, self.EX + domain))
            self.g.add((self.EX + prop, self.rdfs_ns.range, range))

    def _serialize_ontology(self):
        rdf_xml_output = self.g.serialize(format='xml').encode('utf-8')
        with open(f"v{self.file_version}.owl", "wb") as file:
            file.write(rdf_xml_output)
        print(f"Ontology generated: 'v{self.file_version}.owl'")
