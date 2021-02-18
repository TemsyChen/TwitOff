"""Entry point for TwitOff Flask application"""
__all__ = ['models', 'predict', 'twitter']

from .app import create_app

APP = create_app()
