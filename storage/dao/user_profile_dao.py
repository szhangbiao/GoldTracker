from typing import Optional, Dict
from base_dao import BaseDao

class UserProfileDao(BaseDao):
    def __init__(self):
        super().__init__()
        self.table_name = "user_profiles"
    
    async def get_profile(self, user_id: str) -> Optional[Dict]:
        """获取用户配置"""
        response = await self._supabase.table(self.table_name)\
            .select("*")\
            .eq("id", user_id)\
            .execute()
        return response.data[0] if response.data else None
    
    async def upsert_profile(self, profile_data: Dict) -> Dict:
        """创建或更新用户配置"""
        return await self._supabase.table(self.table_name)\
            .upsert(profile_data)\
            .execute()