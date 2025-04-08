from typing import List, Dict
from base_dao import BaseDao

class WatchRuleDao(BaseDao):
    def __init__(self):
        super().__init__()
        self.table_name = "watch_rules"
    
    async def create_rule(self, rule_data: Dict) -> Dict:
        """创建监控规则"""
        return await self._supabase.table(self.table_name)\
            .insert(rule_data)\
            .execute()
    
    async def get_user_rules(self, user_id: str) -> List[Dict]:
        """获取用户的所有规则"""
        response = await self._supabase.table(self.table_name)\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("is_active", True)\
            .execute()
        return response.data
    
    async def update_rule(self, rule_id: str, rule_data: Dict) -> Dict:
        """更新规则"""
        return await self._supabase.table(self.table_name)\
            .update(rule_data)\
            .eq("id", rule_id)\
            .execute()
    
    async def update_last_triggered(self, rule_id: str) -> Dict:
        """更新最后触发时间"""
        return await self._supabase.table(self.table_name)\
            .update({"last_triggered_at": "now()"})\
            .eq("id", rule_id)\
            .execute()