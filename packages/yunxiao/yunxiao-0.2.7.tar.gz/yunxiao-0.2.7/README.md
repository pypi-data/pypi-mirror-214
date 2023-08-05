
# YunXiao API
An API tool for YunXiao Education Institution Management System.


# Copyright Statement
YunXiao software is owned by XiaoGuanJia. This project is for learning purposes only. If there is any infringement, please contact me to delete.


# Contact
admin@sqkkyzx.com


# API Endpoint

## App

- ### arrange

` 排课管理。 ` 

| Parameter | Description |
|-----------|-------------|
| starttime | 查询起始时间 |
| endtime | 查询截止时间 |


- ### become_history

` 设为曾就读学生。 ` 

| Parameter | Description |
|-----------|-------------|
| studentlist | 学生ID |


- ### class_arrange

` 查询指定班级排课。 ` 

| Parameter | Description |
|-----------|-------------|
| classid | 班级id |


- ### class_info

` 查询指定班级信息 ` 

| Parameter | Description |
|-----------|-------------|
| classid | 班级id |


- ### class_info_page

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### class_student

` 查询指定班级的学员 ` 

| Parameter | Description |
|-----------|-------------|
| classid |     班级id |
| inout |       [1]当前在班学员 [2]历史学员 |


- ### company_course

` [教务管理/课表点名/全部课表] ` 

| Parameter | Description |
|-----------|-------------|


- ### course_absent

` [教务管理/缺勤管理] ` 

| Parameter | Description |
|-----------|-------------|
| starttime | 起始时间 |
| endtime | 结束时间 |
| pagesize | 单页项目数量 |


- ### curriculum

` 查询所有在开的课程 ` 

| Parameter | Description |
|-----------|-------------|
| searchname | 查找关键字。 |
| haltsalelist | 是否在售。0>在售 1>停售 |


- ### find_course_money

` 课消数据。 ` 

| Parameter | Description |
|-----------|-------------|
| date | 月份，格式示例： 2023-02 |


- ### find_data_report

` 每日简报。 ` 

| Parameter | Description |
|-----------|-------------|
| date | 日期，格式示例 2023-02-01 |


- ### find_data_report_list

` 某日到某日数据。 ` 

| Parameter | Description |
|-----------|-------------|
| startdate | 起始日期 |
| enddate | 截至日期 |


- ### find_now_data_report

` [数据/当前数据] ` 

| Parameter | Description |
|-----------|-------------|


- ### find_refund_money

` 学费退费数据 ` 

| Parameter | Description |
|-----------|-------------|
| date | 月份，格式示例： 2023-02 |


- ### find_student_course_amount

` 学生数据 - 课时报表。 ` 

| Parameter | Description |
|-----------|-------------|
| curriculumids | 课程ID列表 |
| status | 学生状态列表 |
| studentname | 按学生姓名检索 |


- ### find_student_course_fee

` 学生数据 - 费用报表。 ` 

| Parameter | Description |
|-----------|-------------|
| curriculumids | 课程ID列表 |
| status | 学生状态列表 |
| studentname | 按学生姓名检索 |


- ### find_tuition

` 学费收入数据。 ` 

| Parameter | Description |
|-----------|-------------|
| date | 月份，格式示例： 2023-02 |


- ### get_teacher_list

` 查询老师 ` 

| Parameter | Description |
|-----------|-------------|
| querykey | 关键词检索 |


- ### list_campus

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### operation_record_list

` [工作台][学员][就读课程][出入班记录] ` 

| Parameter | Description |
|-----------|-------------|
| campus_ids_index | 实例中选择的校区列表索引，必须从中列表中选择一个。 |


- ### order

` [收银管理/订单管理] ` 

| Parameter | Description |
|-----------|-------------|
| ordertype | 订单类型 |
| searchname | 查询姓名 |
| starttime | 起始时间 |
| endtime | 截至时间 |
| pagesize | 每页数量 |


- ### order_info

` [收银管理/订单管理/订单详情] ` 

| Parameter | Description |
|-----------|-------------|


- ### refund_order

` [收银管理/订单管理/退费] ` 

| Parameter | Description |
|-----------|-------------|
| searchname | 查询姓名 |
| starttime | 起始时间 |
| endtime | 结束时间 |
| pagesize | 项目数 |


- ### renew_cookie

` 刷新 cookie.tmp 配置中存储的 cookie ` 

| Parameter | Description |
|-----------|-------------|


- ### renew_token

` 刷新 token.tmp 配置中存储的 token ` 

| Parameter | Description |
|-----------|-------------|


- ### request

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### student_attend_course

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### student_card

` 查看学员的课程卡包 ` 

| Parameter | Description |
|-----------|-------------|
| studentid | 学生ID |


- ### student_info

` [教务管理/学员/学员详情] ` 

| Parameter | Description |
|-----------|-------------|
| studentid | 学生ID |


- ### student_list

` [教务管理/学员] ` 

| Parameter | Description |
|-----------|-------------|
| curriculumids | 课程筛选 |
| classids | 班级筛选 |
| name | 姓名查询关键字 |
| status | 学员状态 0>未收费 1>在读 6>曾就读 7>停课 99>无效学员 |
| class_student_status | 0>不筛选 1>未入班 2>已入班 |


- ### student_suspend_course

` 设为停课状态。 ` 

| Parameter | Description |
|-----------|-------------|
| student_id | 学生ID |
| suspend_course_date | 停课时间。0000-00-00 |
| remove_class | 是否从班级中移除 |


- ### update_curriculum_price_item

` ⚠ 编辑课程，谨慎使用 ` 

| Parameter | Description |
|-----------|-------------|


## Web

- ### find_course_sign_charge

` 查询课消记录 ` 

| Parameter | Description |
|-----------|-------------|
| sort_field | 时间筛选模式。 <operationTime> - 操作时间 |


- ### find_order_item_all

` 查询订单明细。 ` 

| Parameter | Description |
|-----------|-------------|
| starttime | 起始时间 |
| endtime | 结束时间 |
| orderstatus | 订单状态。 |


- ### find_payment_list

` 收入明细报表。 ` 

| Parameter | Description |
|-----------|-------------|
| group_no | 收据编号 |
| pay_start_date | 支付起始时间 |
| pay_end_date | 支付结束时间 |
| order_status | 订单状态 1>已付款 4>已作废 |
| page_num | 页数 |
| page_size | 每页项目数 |


- ### find_receipt

` 收据。 ` 

| Parameter | Description |
|-----------|-------------|
| order_id | 订单 ID |
| payment_group_id | 支付 ID |


- ### find_student_course_amount

` 取得所有学员的课时统计数据。 ` 

| Parameter | Description |
|-----------|-------------|
| page_num | 页数。 |
| page_size | 每页记录数。 |


- ### find_student_course_fee

` 取得所有学员的课时统计数据。 ` 

| Parameter | Description |
|-----------|-------------|
| student_name | 学员姓名。 |
| status | 学员状态。[0:"未收费"][1:"在读"][7:"停课"] |
| display_history | 是否显示曾就读。<True:显示><False:不显示> |
| page_num | 页数。 |
| page_size | 每页记录数。 |


- ### receipt

` 收据。 ` 

| Parameter | Description |
|-----------|-------------|
| order_id | 订单 ID |
| payment_group_id | 支付 ID |


- ### renew_cookie

` 刷新 cookie.tmp 配置中存储的 cookie ` 

| Parameter | Description |
|-----------|-------------|


- ### renew_token

` 刷新 token.tmp 配置中存储的 token ` 

| Parameter | Description |
|-----------|-------------|


- ### request

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### snap_info_by_payment_group_id

` 收据。 ` 

| Parameter | Description |
|-----------|-------------|
| order_id | 订单 ID |
| payment_group_id | 支付 ID |


- ### student_course_card

` 取得所有学员的课程卡片。 ` 

| Parameter | Description |
|-----------|-------------|
| page_num | 页数。 |
| page_size | 每页记录数。 |


- ### teacher_arrange

` 取得指定老师的课表。 ` 

| Parameter | Description |
|-----------|-------------|
| teacher_id | 查询的老师ID |
| start_date | 起始日期，默认为本周一 |
| end_date | 结束日期，默认为本周日 |
| page_num | 页数。 |
| page_size | 每页记录数。 |


## V2

- ### arrange_list_date

` 列出日期范围全部排课[最大9999条] ` 

| Parameter | Description |
|-----------|-------------|


- ### arrange_list_daterange

` 列出全部排课[最大99999条] ` 

| Parameter | Description |
|-----------|-------------|


- ### arrange_queery_date

` ⚠ 未完成，无法使用 查询指定日期排课 ` 

| Parameter | Description |
|-----------|-------------|


- ### arrange_query_daterange

` 排课管理。 ` 

| Parameter | Description |
|-----------|-------------|
| displayCompletedClass | 显示已结班排课 |
| starttime | 查询起始时间 |
| endtime | 查询截止时间 |


- ### campus_list_all

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### campus_todaymoney_list_all

` 分校区列出指定日期的费用数据。 ` 

| Parameter | Description |
|-----------|-------------|
| date | 日期 |


- ### card_list_all

` 列出所有课程卡 ` 

| Parameter | Description |
|-----------|-------------|


- ### charge_detail_list_daterange

` :param startdate: YY-MM-DD ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |


- ### charge_record_list_daterange

` :param startdate: YY-MM-DD ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |


- ### class_list_all

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### curriculum_list_all

` 列出全部课程[最大9999条] ` 

| Parameter | Description |
|-----------|-------------|


- ### curriculum_query

` 查询所有在开的课程 ` 

| Parameter | Description |
|-----------|-------------|
| searchname | 查找关键字。 |
| haltsalelist | 是否在售。0>在售 1>停售 |


- ### money_list_month

` :param yy_mm: 月份，格式示例： 2023-02 ` 

| Parameter | Description |
|-----------|-------------|


- ### order_item_list_all

` 列出指定操作日期范围的所有订单记录 ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |
| startdate | YY-MM-DD |


- ### payment_item_list_all

` 列出指定操作日期范围的所有订单记录 ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |
| startdate | YY-MM-DD |


- ### payment_record_list_all

` 列出指定操作日期范围的所有订单记录 ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |
| startdate | YY-MM-DD |


- ### payment_refund_list_all

` 列出指定操作日期范围的所有订单记录 ` 

| Parameter | Description |
|-----------|-------------|
| enddate | YY-MM-DD |
| startdate | YY-MM-DD |


- ### renew_cookie

` 刷新 cookie.tmp 配置中存储的 cookie ` 

| Parameter | Description |
|-----------|-------------|


- ### renew_token

` 刷新 token.tmp 配置中存储的 token ` 

| Parameter | Description |
|-----------|-------------|


- ### request

`  ` 

| Parameter | Description |
|-----------|-------------|


- ### student_listall

` 列出全部学生[最大99999条] ` 

| Parameter | Description |
|-----------|-------------|


- ### student_query

` [教务管理/学员] ` 

| Parameter | Description |
|-----------|-------------|
| size | 项目数量 |
| curriculumids | 课程筛选 |
| classids | 班级筛选 |
| name | 姓名查询关键字 |
| status | 学员状态 0>未收费 1>在读 6>曾就读 7>停课 99>无效学员 |
| class_student_status | 0>不筛选 1>未入班 2>已入班 |


- ### teacher_list_all

` 列出全部老师<MAX-9999> ` 

| Parameter | Description |
|-----------|-------------|


- ### teacher_query

` :return: ` 

| Parameter | Description |
|-----------|-------------|


