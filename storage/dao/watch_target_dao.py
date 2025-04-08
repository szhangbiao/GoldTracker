from typing import Optional, Dict
from base_dao import BaseDao

class WatchTargetDao(BaseDao):
    def __init__(self):
        super().__init__()
        self.table_name = "watch_targets"
    
    async def create_target(self, target_data: Dict) -> Dict:
        """创建监控目标"""
        return await self._supabase.table(self.table_name)\
            .insert(target_data)\
            .execute()
    
    async def get_target(self, target_id: str) -> Optional[Dict]:
        """获取单个监控目标"""
        response = await self._supabase.table(self.table_name)\
            .select("*")\
            .eq("id", target_id)\
            .execute()
        return response.data[0] if response.data else None
    
    async def get_target_by_symbol(self, type: str, symbol: str) -> Optional[Dict]:
        """根据类型和代码获取监控目标"""
        response = await self._supabase.table(self.table_name)\
            .select("*")\
            .eq("type", type)\
            .eq("symbol", symbol)\
            .execute()
        return response.data[0] if response.data else None
    
    async def update_price(self, target_id: str, price: float) -> Dict:
        """更新当前价格"""
        return await self._supabase.table(self.table_name)\
            .update({"current_price": price, "last_updated_at": "now()"})\
            .eq("id", target_id)\
            .execute()