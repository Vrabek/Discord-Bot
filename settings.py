import os
import logging

from dotenv import load_dotenv


load_dotenv()
"""Static token retrival"""
DISCORD_API_SECRET = os.getenv('DISCORD_API_TOKEN')



