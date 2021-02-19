"""Entry point for TwitOff Flask application"""
__all__ = ['models', 'predict', 'twitter', 'app']

from .app import create_app

APP = create_app()
