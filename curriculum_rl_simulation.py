# PART 1 - Curriculum and Student Simulation

import networkx as nx
import random
import matplotlib.pyplot as plt
import json
from faker import Faker

fake = Faker()

# ---- 1. Create Curriculum Graph ----
courses = [
    "Intro to CS", "Data Structures", "Algorithms", "Databases", "Operating Systems",
    "AI Basics", "Machine Learning", "Computer Vision", "Cybersecurity", "Cryptography",
    "Data Mining", "NLP", "Software Engineering", "Web Dev", "Mobile Dev"
]

prerequisites = {
    "Data Structures": ["Intro to CS"],
    "Algorithms": ["Data Structures"],
    "Databases": ["Data Structures"],
    "Operating Systems": ["Data Structures"],
    "AI Basics": ["Algorithms"],
    "Machine Learning": ["AI Basics"],
    "Computer Vision": ["Machine Learning"],
    "Cybersecurity": ["Operating Systems"],
    "Cryptography": ["Cybersecurity"],
    "Data Mining": ["Databases", "AI Basics"],
    "NLP": ["Machine Learning"],
    "Web Dev": ["Software Engineering"],
    "Mobile Dev": ["Web Dev"]
}

def build_graph():
    G = nx.DiGraph()
    for course in courses:
        G.add_node(course)
    for course, prereqs in prerequisites.items():
        for prereq in prereqs:
            G.add_edge(prereq, course)
    return G

# ---- 2. Generate Students ----
interests = ["AI", "Security", "Data Science"]

def generate_student(id):
    student_courses = set()
    num_courses = random.randint(3, 10)
    while len(student_courses) < num_courses:
        course = random.choice(courses)
        student_courses.add(course)
    grades = {course: random.choice(["A", "B", "C", "D", "F"]) for course in student_courses}
    gpa_map = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}
    gpa = round(sum(gpa_map[g] for g in grades.values()) / len(grades), 2)
    return {
        "id": id,
        "name": fake.name(),
        "completed_courses": list(student_courses),
        "grades": grades,
        "gpa": gpa,
        "interests": random.sample(interests, 1),
        "term": random.randint(1, 8)
    }

students = [generate_student(i) for i in range(100)]

# ---- Optional Visualization ----
G = build_graph()
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, arrowsize=20)
plt.title("University Curriculum Graph")
plt.show()

# ---- Save Sample Data ----
with open("students.json", "w") as f:
    json.dump(students, f, indent=2)

# Sample Cypher Schema (Neo4j)
cypher_schema = '''
CREATE (:Course {name: "Intro to CS"})
CREATE (:Course {name: "Data Structures"})
CREATE (:Course {name: "Algorithms"})
CREATE (:Course {name: "Databases"})
... (repeat for all courses)

MATCH (a:Course {name: "Intro to CS"}), (b:Course {name: "Data Structures"})
CREATE (a)-[:PREREQUISITE_FOR]->(b)
... (repeat for all edges)
'''
with open("cypher_schema.txt", "w") as f:
    f.write(cypher_schema)

# PART 2 - Personalization Strategy (Heuristic-Based Recommendation)
def eligible_courses(student, graph):
    passed_courses = [c for c in student['completed_courses'] if student['grades'][c] != 'F']
    eligible = []
    for course in courses:
        if course in passed_courses:
            continue
        prereqs = list(graph.predecessors(course))
        if all(pr in passed_courses for pr in prereqs):
            eligible.append(course)
    return eligible

def recommend_courses(student, graph, max_load=5):
    interest = student['interests'][0]
    themed_courses = {
        "AI": ["AI Basics", "Machine Learning", "Computer Vision", "NLP"],
        "Security": ["Cybersecurity", "Cryptography"],
        "Data Science": ["Data Mining", "Machine Learning", "Databases"]
    }
    eligible = eligible_courses(student, graph)
    sorted_courses = sorted(eligible, key=lambda c: c in themed_courses[interest], reverse=True)
    return sorted_courses[:random.randint(3, max_load)]

# ---- Run Recommendations for 10 Students ----
recommendations = []
for student in students[:10]:
    recs = recommend_courses(student, G)
    recommendations.append({
        "student_id": student["id"],
        "name": student["name"],
        "interest": student["interests"],
        "recommended_courses": recs
    })

with open("recommendations.json", "w") as f:
    json.dump(recommendations, f, indent=2)

print("Sample Recommendations for 10 students saved to recommendations.json")
