# 功能

此脚本将一个Notion Database的一个Date属性列中所有日期改为CST时区

# 使用方法

## 本地使用

1. 创建Notion Integration，获取secret
2. 修改`properties.py`将secret赋值给`NOTION_TOKEN`
3. 在需要使用该脚本的Notion Database中Share - Invite第一步中创建好的Integration
4. 获取`database_id`，`database_id`的值为在需要使用该脚本的Notion Database的页面网址中`notion.so/`和`?v=`中间的字符串
5. 修改`properties.py`将`database_id`赋值给`NOTION_DATABASE_ID`
6. 修改`properties.py`将需要修改的列的名称(Property Name)赋值给`DATE_COLUMN_NAME`
7. `pip install requests`
8. `python notion_timezone_setter.py`

# 限制条件

1. 只支持修改一个Database
2. 只支持修改一列
3. 需要确保列中每个元素都具有日期与时间
4. 只支持修改时区为CST
5. 修改的列类型必须已经为Date