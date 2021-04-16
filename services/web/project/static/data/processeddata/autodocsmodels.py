"""Database models."""
from project import db
from flask_login import UserMixin, _compat
from flask_login._compat import text_type
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


"""Autodoc Object"""
class Autodoc(db.Model):
    """Autodoc model."""
    """Describes table which includes autodocs."""

    __tablename__ = 'autodocs'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    body = db.Column(
        db.String(1000),
        unique=False,
        nullable=True
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    """backreferences Document class on revisions table"""
    documents = relationship(
        'Revision',
        back_populates='autodoc'
        )



"""Association Object - Document Revision of Autodocs"""
class Revision(db.Model):
    """Model for who retains which document"""
    """Associate database."""
    __tablename__ = 'revisions'

    id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True
    )

    document_id = db.Column(
        db.Integer, 
        db.ForeignKey('documents.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    autodoc_id = db.Column(
        db.Integer, 
        db.ForeignKey('documents.id'),
        primary_key=True,
        unique=False,
        nullable=True
    )

    """backreferences to user and document tables"""
    document = db.relationship(
        'Document', 
        back_populates='autodocs'
        )

    autodoc = db.relationship(
        'Autodoc', 
        back_populates='documents'
        )