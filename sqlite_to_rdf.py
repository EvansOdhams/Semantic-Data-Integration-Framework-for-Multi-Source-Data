"""
Convert the SQLite source (university.db) into RDF triples aligned with the ontology.

Usage:
    python sqlite_to_rdf.py --db university.db --output data/sqlite_dump.ttl

Requirements:
    pip install rdflib
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from rdflib import Graph, Literal, Namespace, RDF, URIRef, XSD


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export SQLite data to RDF.")
    parser.add_argument(
        "--db",
        default="university.db",
        help="Path to the SQLite database created from setup_university.sql",
    )
    parser.add_argument(
        "--output",
        default="sqlite_dump.ttl",
        help="Path to the Turtle file that will be generated.",
    )
    parser.add_argument(
        "--base-iri",
        default="http://example.org/university#",
        help="Base IRI for the ontology namespace.",
    )
    return parser.parse_args()


def ensure_namespace(base_iri: str) -> Namespace:
    if not base_iri.endswith(("#", "/")):
        base_iri = base_iri + "#"
    return Namespace(base_iri)


def build_graph(ns: Namespace) -> Graph:
    g = Graph()
    g.bind("uni", ns)
    return g


def student_uri(ns: Namespace, student_id: int) -> URIRef:
    return ns[f"Student/{student_id}"]


def course_uri(ns: Namespace, course_id: int) -> URIRef:
    return ns[f"Course/{course_id}"]


def enrollment_uri(ns: Namespace, enrollment_id: int) -> URIRef:
    return ns[f"Enrollment/{enrollment_id}"]


def department_uri(ns: Namespace, name: str) -> URIRef:
    slug = name.strip().replace(" ", "_")
    return ns[f"Department/{slug}"]


def export_students(conn: sqlite3.Connection, g: Graph, ns: Namespace) -> None:
    cursor = conn.execute(
        """
        SELECT student_id, first_name, last_name, date_of_birth, major
        FROM Students
        """
    )
    for row in cursor:
        sid, first_name, last_name, dob, major = row
        s_uri = student_uri(ns, sid)
        g.add((s_uri, RDF.type, ns.Student))
        g.add((s_uri, ns.firstName, Literal(first_name)))
        g.add((s_uri, ns.lastName, Literal(last_name)))
        if dob:
            g.add((s_uri, ns.dateOfBirth, Literal(dob, datatype=XSD.date)))
        if major:
            g.add((s_uri, ns.major, Literal(major)))


def export_courses(conn: sqlite3.Connection, g: Graph, ns: Namespace) -> None:
    cursor = conn.execute(
        """
        SELECT course_id, course_code, course_title, department, credits
        FROM Courses
        """
    )
    for row in cursor:
        cid, code, title, department, credits = row
        c_uri = course_uri(ns, cid)
        g.add((c_uri, RDF.type, ns.Course))
        g.add((c_uri, ns.courseCode, Literal(code)))
        g.add((c_uri, ns.courseTitle, Literal(title)))
        if isinstance(credits, int):
            g.add((c_uri, ns.credits, Literal(credits, datatype=XSD.integer)))
        if department:
            d_uri = department_uri(ns, department)
            g.add((d_uri, RDF.type, ns.Department))
            g.add((d_uri, ns.departmentName, Literal(department)))
            g.add((c_uri, ns.offeredByDepartment, d_uri))


def export_enrollments(conn: sqlite3.Connection, g: Graph, ns: Namespace) -> None:
    cursor = conn.execute(
        """
        SELECT enrollment_id, student_id, course_id, semester, year, grade
        FROM Enrollments
        """
    )
    for row in cursor:
        eid, sid, cid, semester, year, grade = row
        e_uri = enrollment_uri(ns, eid)
        g.add((e_uri, RDF.type, ns.Enrollment))
        if semester:
            g.add((e_uri, ns.semester, Literal(semester)))
        if isinstance(year, int):
            g.add((e_uri, ns.year, Literal(year, datatype=XSD.integer)))
        if grade:
            g.add((e_uri, ns.grade, Literal(grade)))

        s_uri = student_uri(ns, sid)
        c_uri = course_uri(ns, cid)
        g.add((s_uri, ns.hasEnrollment, e_uri))
        g.add((e_uri, ns.enrolledInCourse, c_uri))


def main() -> None:
    args = parse_args()
    db_path = Path(args.db)
    if not db_path.exists():
        raise FileNotFoundError(
            f"{db_path} does not exist. Run setup_university.sql to create it."
        )

    ns = ensure_namespace(args.base_iri)
    graph = build_graph(ns)

    with sqlite3.connect(db_path) as conn:
        export_students(conn, graph, ns)
        export_courses(conn, graph, ns)
        export_enrollments(conn, graph, ns)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(output_path), format="turtle")
    print(f"Wrote {len(graph)} triples to {output_path}")


if __name__ == "__main__":
    main()


