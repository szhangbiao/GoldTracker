"""
This module provides a Supabase client implementation for database operations.
It handles the connection and interaction with a Supabase backend using environment variables
for authentication.
"""
import os
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件中的环境变量

# Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

class SupabaseClient:
    """
    A client class for interacting with Supabase database.
    
    This class provides a wrapper around the Supabase client to handle
    database operations and connections.
    """
    def __init__(self):
        self.supabase = create_client(url, key)