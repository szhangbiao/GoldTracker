from storage.supabase_client import SupabaseClient

class BaseDao:
    def __init__(self):
        self._client = SupabaseClient()
        self._supabase = self._client.supabase