#!/usr/bin/env python3
# coding: utf-8

import os

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Client(UserMixin, db.Model):
    __tablename__ = "client"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    cnpj = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    passwd = db.Column(db.String(80))
    active = db.Column(db.Boolean)


class DBase:
    version = "1.0.0"

    def __init__(self):
        script_name = os.path.basename(__file__)[:-3]
        script_path = os.path.dirname(os.path.realpath(__file__))
        self.db_name = f"sqlite:///{script_path}{os.sep}{script_name}.sqlite3"
        self.engine = create_engine(
            self.db_name,
            poolclass=StaticPool,
        )
        self.session = sessionmaker(bind=self.engine)
        if not self.engine.has_table("client"):
            Client.__table__.create(self.engine)
        session = self.session()
        old_client = session.query(Client).filter_by(id=999999).first()
        password = generate_password_hash("BestPass", method="sha256")
        if not old_client:
            new_client = Client(
                id=999999,
                name="The Best Client",
                cnpj="12345678000123",
                email="thebestclient@mail.com",
                passwd=password,
                active=1,
            )
            session.add(new_client)
        session.commit()
        session.close()

    def execute_sql(self, sql):
        conn = self.engine.connect()
        trans = conn.begin()
        try:
            result = conn.execute(sql)
            trans.commit()
            conn.close()
            return result
        except Exception:
            trans.rollback()

    def get_client(self, id=None):
        sql = """
            select id, name, cnpj, email, active
            from client
            """
        if id:
            sql += f"where id = {id}"
        data = self.execute_sql(sql)
        if data:
            client = []
            for rec in data:
                client.append(
                    {
                        "id": rec.id,
                        "name": rec.name,
                        "cnpj": rec.cnpj,
                        "email": rec.email,
                        "active": rec.active,
                    }
                )
            return client
        else:
            return []

    def update_client(self, id, name, cnpj, email, passwd, active):
        sql = f"""
            update client
            set name="{name}", cnpj="{cnpj}", email="{email}", passwd="{generate_password_hash(passwd, method="sha256")}", active="{active}" 
            where id="{id}"
            """
        self.execute_sql(sql)

    def add_client(self, name, cnpj, email, passwd, active):
        sql = f"""
            insert into
            client (name, cnpj, email, passwd, active)
            values ("{name}", "{cnpj}", "{email}", "{generate_password_hash(passwd, method="sha256")}", "{active}")
            """
        self.execute_sql(sql)

    def delete_client(self, id):
        sql = f"""
            delete
            from client
            where id="{id}"
            """
        self.execute_sql(sql)
