from flask import Flask, request
from werkzeug import security
import sqlite3
import os
import random

app = Flask(__name__)


try:
    MANAGE_PASSWORD = os.environ['MANAGE_PASSWORD']
except KeyError:
    MANAGE_PASSWORD = None


def get_random_ip(seed) -> str:
    random.seed(seed)
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


def get_password_hash(domain_id) -> str:
    conn = sqlite3.connect("database.db")

    password_hash = conn.execute(
        "SELECT password_hash FROM domains WHERE id == ?",
        domain_id).fetchone()

    if not password_hash:
        return ""
    password_hash = password_hash[0]
    return password_hash


@app.route("/")
def get_domains():
    conn = sqlite3.connect("database.db")
    domains = conn.execute("SELECT id, domain from domains").fetchall()

    ans = "".join(f"id: {row[0]}, name: {row[1]}<br>" for row in domains)
    print(ans)

    return ans


@app.route("/get/")
def get_ip():
    domain_id = request.args.get("domain_id")
    password = request.args.get("password")
    if not domain_id or not password:
        return get_random_ip(domain_id)

    password_hash = get_password_hash(domain_id)

    if not security.check_password_hash(password_hash, password):
        return get_random_ip(domain_id)
    conn = sqlite3.connect("database.db")
    ip = conn.execute(
        "SELECT ip FROM domains WHERE id == ?", domain_id).fetchone()
    ip = ip[0]
    return ip


@app.route("/add")
def add_address():
    domain = request.args.get("domain_name")
    ip = request.args.get("ip")
    password = request.args.get("password")
    manage_password = request.args.get("manage_password")

    if not (domain and ip and password and manage_password):
        return "ais4Ab6E"

    if not MANAGE_PASSWORD:
        return "Nope"

    if MANAGE_PASSWORD != manage_password:
        return "Eeng8iTh"

    conn = sqlite3.connect("database.db")
    conn.execute("INSERT INTO domains (domain, ip, password_hash) VALUES (?, ?, ?)",
                 (domain, ip, security.generate_password_hash(password)))
    conn.commit()

    return "OK"


@app.route("/set/")
def set_ip():
    domain_id = request.args.get("domain_id")
    password = request.args.get("password")
    new_ip = request.args.get("new_ip")
    new_pass = request.args.get("new_pass")

    if not (domain_id and password):
        return "bo8ieZaz"

    password_hash = get_password_hash(domain_id)

    if not security.check_password_hash(password_hash, password):
        return "No"

    conn = sqlite3.connect("database.db")
    if new_ip:
        conn.execute(
            "UPDATE domains SET ip = ? WHERE id = ?", (new_ip, domain_id))
    if new_pass:
        conn.execute(
            "UPDATE domains SET password_hash = ? WHERE id = ?",
            (security.generate_password_hash(new_pass), domain_id)
        )
    conn.commit()

    return "OK"
