# Thack Api List
## Host: <a href="http://192.168.134.163:14010/">http://192.168.134.163:14010/</a>

> 注意：未标明可选的均为必选参数！！！

### 用户相关
#### 登录 /user/user/login [post]
##### 参数:
1. username: 用户名 
2. password: 密码

### 即时通讯类 
#### 发送消息 /im/im/add [post]
##### 参数:
1. from_user_id: 发送者用户id
2. to_user_id: 接收者用户id
3. content: 发送内容

#### 获取目标用户的联系人 /im/im/getContacts [get]
##### 参数:
1. user_id: 用户id

#### 获取聊天内容 /im/im/getContactContent [get]
##### 参数:
1. from_user_id: 发送者用户id
2. to_user_id: 接收者用户id
3. last_id: 最后消息id(可选)

#### 聊天页面 /im/im/index [get]
1. from_user_id: 发送者用户id
2. to_user_id: 接收者用户id

### 资源相关
#### 上传资源 /resource/resource/add [post]
##### 参数:
1. user_id: 用户id
2. url: 资源地址
3. resource_type: 资源类型
4. longitude: 经度
5. latitude: 纬度
6. create_on: 资源创建时间(如2015-01-02 15:04:05)

#### 获取用户资源列表 /resource/resource/list [get]
##### 参数:
1. user_id: 用户id
2. resource_type: 资源类型(可选)

### 说的消息相关
#### 添加消息 /message/message/add [post]
##### 参数:
1. user_id: 用户id
2. latitude: 经度
3. longitude: 纬度
4. content: 文字内容
5. resources: 资源id列表，用逗号隔开(可选)
6. routes: 线路id列表，用逗号隔开(可选)
7. category_id: 分类(可选)
8. tags: 标记(可选)
9. with_sku_id: 推荐景点 id(可选)
10. with_sku_type: 推荐类型(可选)

#### 听消息（查询消息）/message/message/search [get]
1. longitude: 经度
2. latitude: 纬度
3. cateogry_id: 分类id
4. distance: 半径(单位米)

#### 获取我发布的消息 /message/message/list [get]
1. user_id: 用户id

### 旅行轨迹相关
#### 添加轨迹 /route/route/add [post]
1. user_id: 用户id
2. latitude: 经度
3. longitude: 纬度
4. resources: 资源id列表（用逗号隔开）

#### 获取我提交的轨迹列表 /route/route/list [get]
1. user_id: 用户id

#### 获取某条轨迹的详情 /route/route/getById [get]
1. id: 轨迹id

### 景点相关
#### 查询景点 /sku/sku/search
1. keyword: 关键字
2. lat: 纬度
3. lon: 经度
4. distance: 半径
5. page: 页码

#### 获取景点详情 /sku/sku/sight
1. scenic_id: 景点id