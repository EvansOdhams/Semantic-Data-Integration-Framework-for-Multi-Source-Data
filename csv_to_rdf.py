"""
Convert student_contacts.csv into RDF triples aligned with the ontology.

Usage:
    python csv_to_rdf.py --csv student_contacts.csv --output data/csv_dump.ttl

Dependencies:
    pip install rdflib
"""

import argparse
import csv
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export CSV contacts to RDF.")
    parser.add_argument(
        "--csv",
        default="student_contacts.csv",
        help="Path to the CSV file with contact info.",
    )
    parser.add_argument(
        "--output",
        default="data/csv_dump.ttl",
        help="Path of the Turtle file to create.",
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


def student_uri(ns: Namespace, student_id: str) -> str:
    return ns[f"Student/{student_id}"]


def split_full_name(full_name: str) -> tuple[str, str | None]:
    if not full_name:
        return "", None
    parts = full_name.strip().split(" ", 1)
    first = parts[0]
    last = parts[1] if len(parts) > 1 else None
    return first, last


def main() -> None:
    args = parse_args()
    ns = ensure_namespace(args.base_iri)
    g = Graph()
    g.bind("uni", ns)

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found. Ensure the CSV exists.")

    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            student_id = row["student_id"]
            s_uri = student_uri(ns, student_id)
            g.add((s_uri, RDF.type, ns.Student))
            first, last = split_full_name(row.get("full_name", ""))
            if first:
                g.add((s_uri, ns.firstName, Literal(first)))
            if last:
                g.add((s_uri, ns.lastName, Literal(last)))
            if row.get("email"):
                g.add((s_uri, ns.email, Literal(row["email"])))
            if row.get("phone"):
                g.add((s_uri, ns.phone, Literal(row["phone"])))
            if row.get("country"):
                g.add((s_uri, ns.country, Literal(row["country"])))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(output), format="turtle")
    print(f"Wrote {len(g)} triples to {output}")


if __name__ == "__main__":
    main()


