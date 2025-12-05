"""
Convert course_catalog.xml into RDF triples aligned with the ontology.

Usage:
    python xml_to_rdf.py --xml course_catalog.xml --output data/xml_dump.ttl

Dependencies:
    pip install rdflib lxml
"""

import argparse
from pathlib import Path

from lxml import etree
from rdflib import Graph, Literal, Namespace, RDF


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export XML catalog to RDF.")
    parser.add_argument(
        "--xml",
        default="course_catalog.xml",
        help="Path to the XML file describing departments and courses.",
    )
    parser.add_argument(
        "--output",
        default="data/xml_dump.ttl",
        help="Path to the Turtle file to generate.",
    )
    parser.add_argument(
        "--base-iri",
        default="http://example.org/university#",
        help="Base IRI for the ontology namespace.",
    )
    return parser.parse_args()


def ensure_namespace(base_iri: str) -> Namespace:
    if not base_iri.endswith(("#", "/")):
        base_iri += "#"
    return Namespace(base_iri)


def department_uri(ns: Namespace, code: str) -> str:
    code = (code or "").strip()
    return ns[f"Department/{code or 'Unknown'}"]


def course_uri(ns: Namespace, code: str) -> str:
    code = (code or "").strip()
    return ns[f"Course/{code or 'Unknown'}"]


def main() -> None:
    args = parse_args()
    ns = ensure_namespace(args.base_iri)
    xml_path = Path(args.xml)
    if not xml_path.exists():
        raise FileNotFoundError(f"{xml_path} not found.")

    tree = etree.parse(str(xml_path))
    g = Graph()
    g.bind("uni", ns)

    for dept in tree.xpath("//department"):
        code = dept.get("code")
        name = dept.get("name")
        d_uri = department_uri(ns, code)

        g.add((d_uri, RDF.type, ns.Department))
        if code:
            g.add((d_uri, ns.departmentCode, Literal(code)))
        if name:
            g.add((d_uri, ns.departmentName, Literal(name)))

        for course in dept.xpath("./course"):
            course_code = course.findtext("courseCode")
            title = course.findtext("title")
            credits = course.findtext("credits")

            c_uri = course_uri(ns, course_code or title or "")
            g.add((c_uri, RDF.type, ns.Course))
            if course_code:
                g.add((c_uri, ns.courseCode, Literal(course_code)))
            if title:
                g.add((c_uri, ns.courseTitle, Literal(title)))
            if credits and credits.isdigit():
                g.add((c_uri, ns.credits, Literal(int(credits))))

            g.add((c_uri, ns.offeredByDepartment, d_uri))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(output), format="turtle")
    print(f"Wrote {len(g)} triples to {output}")


if __name__ == "__main__":
    main()


