-- 启用必要的扩展
create extension if not exists "uuid-ossp";

-- 用户表 (使用 Supabase auth.users)
-- Supabase 已经提供了内置的用户认证系统，我们只需要创建用户配置表
create table user_profiles (
    id uuid references auth.users on delete cascade,
    username text,
    updated_at timestamp with time zone default timezone('utc'::text, now()),
    primary key (id)
);

-- 启用 RLS (Row Level Security)
alter table user_profiles enable row level security;

-- 设置 RLS 策略
create policy "用户只能访问自己的配置"
    on user_profiles for all
    using (auth.uid() = id);

-- 监控目标表
create table watch_targets (
    id uuid primary key default uuid_generate_v4(),
    name text not null,
    type text not null, -- 'GOLD', 'STOCK' 等
    symbol text not null, -- 股票代码或黄金品种代码
    current_price numeric,
    last_updated_at timestamp with time zone default timezone('utc'::text, now()),
    created_at timestamp with time zone default timezone('utc'::text, now()),
    unique(type, symbol)
);

-- 价格历史记录表
create table price_history (
    id uuid primary key default uuid_generate_v4(),
    target_id uuid references watch_targets on delete cascade,
    price numeric not null,
    volume numeric,
    timestamp timestamp with time zone default timezone('utc'::text, now()),
    source text
);

-- 用户关注规则表
create table watch_rules (
    id uuid primary key default uuid_generate_v4(),
    user_id uuid references auth.users on delete cascade,
    target_id uuid references watch_targets on delete cascade,
    price_threshold numeric not null, -- 价格变动阈值
    threshold_type text not null check (threshold_type in ('PERCENTAGE', 'ABSOLUTE')),
    direction text not null check (direction in ('UP', 'DOWN', 'BOTH')),
    is_active boolean default true,
    notification_method text not null,  -- 'EMAIL', 'SMS', 'PUSH' 等
    created_at timestamp with time zone default timezone('utc'::text, now()),
    last_triggered_at timestamp with time zone,
    unique(user_id, target_id, threshold_type, direction)
);

-- 提醒历史记录表
create table alert_history (
    id uuid primary key default uuid_generate_v4(),
    rule_id uuid references watch_rules on delete cascade,
    user_id uuid references auth.users on delete cascade,
    target_id uuid references watch_targets on delete cascade,
    old_price numeric not null,
    new_price numeric not null,
    change_percentage numeric,
    triggered_at timestamp with time zone default timezone('utc'::text, now()),
    notification_status text -- 'SENT', 'FAILED' 等
);

-- 添加索引
create index idx_watch_targets_type_symbol on watch_targets(type, symbol);
create index idx_price_history_target_timestamp on price_history(target_id, timestamp);
create index idx_watch_rules_user_target on watch_rules(user_id, target_id);
create index idx_alert_history_user on alert_history(user_id);

-- 设置 RLS
alter table watch_rules enable row level security;
alter table alert_history enable row level security;

-- 添加 RLS 策略
create policy "用户只能访问自己的监控规则"
    on watch_rules for all
    using (auth.uid() = user_id);

create policy "用户只能查看自己的提醒历史"
    on alert_history for select
    using (auth.uid() = user_id);