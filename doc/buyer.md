## 买家下单

#### URL：
POST http://[address]/buyer/new_order

#### Request

##### Header:

key | 类型 | 描述 | 是否可为空
---|---|---|---
token | string | 登录产生的会话标识 | N

##### Body:
```json
{
  "user_id": "buyer_id",
  "store_id": "store_id",
  "books": [
    {
      "id": "1000067",
      "count": 1
    },
    {
      "id": "1000134",
      "count": 4
    }
  ]
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
store_id | string | 商铺ID | N
books | class | 书籍购买列表 | N

books数组：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
id | string | 书籍的ID | N
count | string | 购买数量 | N


#### Response

Status Code:

码 | 描述
--- | ---
200 | 下单成功
512 | 买家用户ID不存在
513 | 商铺ID不存在
515 | 购买的图书不存在
517 | 商品库存不足

##### Body:
```json
{
  "order_id": "uuid"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
order_id | string | 订单号，只有返回200时才有效 | N


## 买家付款

#### URL：
POST http://[address]/buyer/payment

#### Request

##### Body:
```json
{
  "user_id": "buyer_id",
  "order_id": "order_id",
  "password": "password"
}
```

##### 属性说明：

变量名 | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
order_id | string | 订单ID | N
password | string | 买家用户密码 | N 


#### Response

Status Code:

码 | 描述
--- | ---
200 | 付款成功
512 | 用户ID不存在
513 | 商铺ID不存在
518 | 无效订单
519 | 账户余额不足
401 | 授权失败 


## 买家充值

#### URL：
POST http://[address]/buyer/add_funds

#### Request



##### Body:
```json
{
  "user_id": "user_id",
  "password": "password",
  "add_value": 10
}
```

##### 属性说明：

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
password | string | 用户密码 | N
add_value | int | 充值金额，以分为单位 | N


Status Code:

码 | 描述
--- | ---
200 | 充值成功
401 | 授权失败


## 买家取消订单

#### URL：
POST http://[address]/buyer/close_order

#### Request

##### Body:
```json
{
  "user_id": "buyer_id",
  "password": "password",
  "order_id": "order_id"
}
```

##### 属性说明：

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
password | string | 用户密码 | N
order_id | string | 订单ID | N


Status Code:

码 | 描述
--- | ---
200 | 取消订单成功
401 | 授权失败
512 | 用户ID不存在
513 | 商铺ID不存在
518 | 无效订单
521 | 订单已关闭
524 | 订单不能取消


## 买家确认收货

#### URL：
POST http://[address]/buyer/receive_books

#### Request

##### Body:

```json
{
  "buyer_id": "$buyerer id$",
  "order_id": "$order id$"
}
```

| key      | 类型   | 描述       | 是否可为空 |
| -------- | ------ | ---------- | ---------- |
| buyer_id | string | 买家用户ID | N          |
| order_id | string | 订单ID     | N          |

#### Response

Status Code:

| 码   | 描述               |
| ---- | ------------------ |
| 200  | 成功               |
| 522  | 未发货             |
| 523  | 已收货             |
| 401  | 授权失败           |
| 518  | 用户id，订单不匹配 |


## 买家查询订单

#### URL：
POST http://[address]/buyer/close_order

#### Request

##### Body:
```json
{
  "user_id": "buyer_id",
  "password": "password"
}
```

##### 属性说明：

key | 类型 | 描述 | 是否可为空
---|---|---|---
user_id | string | 买家用户ID | N
password | string | 用户密码 | N


Status Code:

码 | 描述
--- | ---
200 | 查询订单成功
401 | 授权失败