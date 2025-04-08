from typing import List, Dict
from base_dao import BaseDao

class AlertHistoryDao(BaseDao):
    def __init__(self):
        super().__init__()
        self.table_name = "alert_history"
    
    async def create_alert(self, alert_data: Dict) -> Dict:
        """创建提醒记录"""
        return await self._supabase.table(self.table_name)\
            .insert(alert_data)\
            .execute()
    
    async def get_user_alerts(self, user_id: str, limit: int = 50) -> List[Dict]:
        """获取用户的提醒历史"""
        response = await self._supabase.table(self.table_name)\
            .select("*")\
            .eq("user_id", user_id)\
            .order("triggered_at", desc=True)\
            .limit(limit)\
            .execute()
        return response.data