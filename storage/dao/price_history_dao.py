from typing import List, Dict
from base_dao import BaseDao

class PriceHistoryDao(BaseDao):
    def __init__(self):
        super().__init__()
        self.table_name = "price_history"
    
    async def add_price_record(self, record_data: Dict) -> Dict:
        """添加价格记录"""
        return await self._supabase.table(self.table_name)\
            .insert(record_data)\
            .execute()
    
    async def get_target_history(self, target_id: str, limit: int = 100) -> List[Dict]:
        """获取目标的价格历史"""
        response = await self._supabase.table(self.table_name)\
            .select("*")\
            .eq("target_id", target_id)\
            .order("timestamp", desc=True)\
            .limit(limit)\
            .execute()
        return response.data