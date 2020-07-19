<!-- Generator: Widdershins v4.0.1 -->

<h1 id="fastapi">FastAPI v0.1.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

# Authentication

- oAuth2 authentication. 

    - Flow: password

    - Token URL = [/api/v1/login](/api/v1/login)

|Scope|Scope Description|
|---|---|

<h1 id="fastapi-default">Default</h1>

## root__get

<a id="opIdroot__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/', headers = headers)

print(r.json())

```

`GET /`

*Root*

> Example responses

> 200 Response

```json
null
```

<h3 id="root__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="root__get-responseschema">Response Schema</h3>

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-user">user</h1>

## logout_api_v1_logout_get

<a id="opIdlogout_api_v1_logout_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/api/v1/logout', headers = headers)

print(r.json())

```

`GET /api/v1/logout`

*Logout*

> Example responses

> 200 Response

```json
null
```

<h3 id="logout_api_v1_logout_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="logout_api_v1_logout_get-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## edit_api_v1_user_edit_post

<a id="opIdedit_api_v1_user_edit_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/user/edit', headers = headers)

print(r.json())

```

`POST /api/v1/user/edit`

*Edit*

> Body parameter

```json
{
  "id": 0,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string",
  "password": "string"
}
```

<h3 id="edit_api_v1_user_edit_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UserInDB](#schemauserindb)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string"
}
```

<h3 id="edit_api_v1_user_edit_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[User](#schemauser)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## login_api_v1_login_post

<a id="opIdlogin_api_v1_login_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json'
}

r = requests.post('/api/v1/login', headers = headers)

print(r.json())

```

`POST /api/v1/login`

*Login*

> Body parameter

```yaml
username: string
password: string

```

<h3 id="login_api_v1_login_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_login_api_v1_login_post](#schemabody_login_api_v1_login_post)|true|none|

> Example responses

> 200 Response

```json
{
  "access_token": "string",
  "token_type": "string",
  "user": {
    "id": 0,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "role": "string"
  }
}
```

<h3 id="login_api_v1_login_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Token](#schematoken)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## create_user_api_v1_users_create__post

<a id="opIdcreate_user_api_v1_users_create__post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/users/create/', headers = headers)

print(r.json())

```

`POST /api/v1/users/create/`

*Create User*

> Body parameter

```json
{
  "id": 0,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string",
  "password": "string"
}
```

<h3 id="create_user_api_v1_users_create__post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UserInDB](#schemauserindb)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="create_user_api_v1_users_create__post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="create_user_api_v1_users_create__post-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="fastapi-server">server</h1>

## servers_all_api_v1_server_all_get

<a id="opIdservers_all_api_v1_server_all_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/api/v1/server/all', headers = headers)

print(r.json())

```

`GET /api/v1/server/all`

*Servers All*

> Example responses

> 200 Response

```json
[
  {
    "id": 0,
    "address": "string",
    "v6_address": "string",
    "subnet": 0,
    "v6_subnet": 0,
    "interface": "string",
    "listen_port": 0,
    "endpoint": "string",
    "private_key": "string",
    "public_key": "string",
    "is_running": true,
    "configuration": "string",
    "post_up": "string",
    "post_down": "string",
    "dns": "string",
    "peers": []
  }
]
```

<h3 id="servers_all_api_v1_server_all_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<h3 id="servers_all_api_v1_server_all_get-responseschema">Response Schema</h3>

Status Code **200**

*Response Servers All Api V1 Server All Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Servers All Api V1 Server All Get|[[WGServer](#schemawgserver)]|false|none|none|
|» WGServer|[WGServer](#schemawgserver)|false|none|none|
|»» id|integer|false|none|none|
|»» address|string|false|none|none|
|»» v6_address|string|false|none|none|
|»» subnet|integer|false|none|none|
|»» v6_subnet|integer|false|none|none|
|»» interface|string|true|none|none|
|»» listen_port|integer|false|none|none|
|»» endpoint|string|false|none|none|
|»» private_key|string|false|none|none|
|»» public_key|string|false|none|none|
|»» is_running|boolean|false|none|none|
|»» configuration|string|false|none|none|
|»» post_up|string|false|none|none|
|»» post_down|string|false|none|none|
|»» dns|string|false|none|none|
|»» peers|[[WGPeer](#schemawgpeer)]|false|none|none|
|»»» WGPeer|[WGPeer](#schemawgpeer)|false|none|none|
|»»»» id|integer|false|none|none|
|»»»» name|string|false|none|none|
|»»»» address|string|false|none|none|
|»»»» v6_address|string|false|none|none|
|»»»» private_key|string|false|none|none|
|»»»» public_key|string|false|none|none|
|»»»» shared_key|string|false|none|none|
|»»»» server_id|string|true|none|none|
|»»»» dns|string|false|none|none|
|»»»» allowed_ips|string|false|none|none|
|»»»» configuration|string|false|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## add_interface_api_v1_server_add_post

<a id="opIdadd_interface_api_v1_server_add_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/server/add', headers = headers)

print(r.json())

```

`POST /api/v1/server/add`

*Add Interface*

> Body parameter

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="add_interface_api_v1_server_add_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGServerAdd](#schemawgserveradd)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="add_interface_api_v1_server_add_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGServer](#schemawgserver)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## stop_server_api_v1_server_stop_post

<a id="opIdstop_server_api_v1_server_stop_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/server/stop', headers = headers)

print(r.json())

```

`POST /api/v1/server/stop`

*Stop Server*

> Body parameter

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="stop_server_api_v1_server_stop_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGServer](#schemawgserver)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="stop_server_api_v1_server_stop_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGServer](#schemawgserver)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## start_server_api_v1_server_start_post

<a id="opIdstart_server_api_v1_server_start_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/server/start', headers = headers)

print(r.json())

```

`POST /api/v1/server/start`

*Start Server*

> Body parameter

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="start_server_api_v1_server_start_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGServer](#schemawgserver)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="start_server_api_v1_server_start_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGServer](#schemawgserver)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## restart_server_api_v1_server_restart_post

<a id="opIdrestart_server_api_v1_server_restart_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/server/restart', headers = headers)

print(r.json())

```

`POST /api/v1/server/restart`

*Restart Server*

> Body parameter

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="restart_server_api_v1_server_restart_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGServer](#schemawgserver)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="restart_server_api_v1_server_restart_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGServer](#schemawgserver)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## delete_server_api_v1_server_delete_post

<a id="opIddelete_server_api_v1_server_delete_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/server/delete', headers = headers)

print(r.json())

```

`POST /api/v1/server/delete`

*Delete Server*

> Body parameter

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="delete_server_api_v1_server_delete_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGServer](#schemawgserver)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="delete_server_api_v1_server_delete_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGServer](#schemawgserver)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## stats_server_api_v1_server_stats_post

<a id="opIdstats_server_api_v1_server_stats_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/server/stats', headers = headers)

print(r.json())

```

`POST /api/v1/server/stats`

*Stats Server*

> Body parameter

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="stats_server_api_v1_server_stats_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGServer](#schemawgserver)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="stats_server_api_v1_server_stats_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="stats_server_api_v1_server_stats_post-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## edit_server_api_v1_server_edit_post

<a id="opIdedit_server_api_v1_server_edit_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/server/edit', headers = headers)

print(r.json())

```

`POST /api/v1/server/edit`

*Edit Server*

> Body parameter

```json
{}
```

<h3 id="edit_server_api_v1_server_edit_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}
```

<h3 id="edit_server_api_v1_server_edit_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGServer](#schemawgserver)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## server_config_api_v1_server_config__server_id__get

<a id="opIdserver_config_api_v1_server_config__server_id__get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/api/v1/server/config/{server_id}', headers = headers)

print(r.json())

```

`GET /api/v1/server/config/{server_id}`

*Server Config*

<h3 id="server_config_api_v1_server_config__server_id__get-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|server_id|path|integer|true|none|

> Example responses

> 200 Response

```json
"string"
```

<h3 id="server_config_api_v1_server_config__server_id__get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|string|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="fastapi-peer">peer</h1>

## add_peer_api_v1_peer_add_post

<a id="opIdadd_peer_api_v1_peer_add_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/peer/add', headers = headers)

print(r.json())

```

`POST /api/v1/peer/add`

*Add Peer*

> Body parameter

```json
{
  "server_interface": "string"
}
```

<h3 id="add_peer_api_v1_peer_add_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGPeerAdd](#schemawgpeeradd)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "address": "string",
  "v6_address": "string",
  "private_key": "string",
  "public_key": "string",
  "shared_key": "string",
  "server_id": "string",
  "dns": "string",
  "allowed_ips": "string",
  "configuration": "string"
}
```

<h3 id="add_peer_api_v1_peer_add_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGPeer](#schemawgpeer)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## delete_peer_api_v1_peer_delete_post

<a id="opIddelete_peer_api_v1_peer_delete_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/peer/delete', headers = headers)

print(r.json())

```

`POST /api/v1/peer/delete`

*Delete Peer*

> Body parameter

```json
{
  "id": 0,
  "name": "string",
  "address": "string",
  "v6_address": "string",
  "private_key": "string",
  "public_key": "string",
  "shared_key": "string",
  "server_id": "string",
  "dns": "string",
  "allowed_ips": "string",
  "configuration": "string"
}
```

<h3 id="delete_peer_api_v1_peer_delete_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGPeer](#schemawgpeer)|true|none|

> Example responses

> 200 Response

```json
{
  "id": 0,
  "name": "string",
  "address": "string",
  "v6_address": "string",
  "private_key": "string",
  "public_key": "string",
  "shared_key": "string",
  "server_id": "string",
  "dns": "string",
  "allowed_ips": "string",
  "configuration": "string"
}
```

<h3 id="delete_peer_api_v1_peer_delete_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[WGPeer](#schemawgpeer)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## edit_peer_api_v1_peer_edit_post

<a id="opIdedit_peer_api_v1_peer_edit_post"></a>

> Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/api/v1/peer/edit', headers = headers)

print(r.json())

```

`POST /api/v1/peer/edit`

*Edit Peer*

> Body parameter

```json
{
  "id": 0,
  "name": "string",
  "address": "string",
  "v6_address": "string",
  "private_key": "string",
  "public_key": "string",
  "shared_key": "string",
  "server_id": "string",
  "dns": "string",
  "allowed_ips": "string",
  "configuration": "string"
}
```

<h3 id="edit_peer_api_v1_peer_edit_post-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[WGPeer](#schemawgpeer)|true|none|

> Example responses

> 200 Response

```json
null
```

<h3 id="edit_peer_api_v1_peer_edit_post-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="edit_peer_api_v1_peer_edit_post-responseschema">Response Schema</h3>

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="fastapi-wg">wg</h1>

## generate_psk_api_v1_wg_generate_psk_get

<a id="opIdgenerate_psk_api_v1_wg_generate_psk_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/api/v1/wg/generate_psk', headers = headers)

print(r.json())

```

`GET /api/v1/wg/generate_psk`

*Generate Psk*

> Example responses

> 200 Response

```json
{
  "psk": "string"
}
```

<h3 id="generate_psk_api_v1_wg_generate_psk_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[PSK](#schemapsk)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## generate_key_pair_api_v1_wg_generate_keypair_get

<a id="opIdgenerate_key_pair_api_v1_wg_generate_keypair_get"></a>

> Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/api/v1/wg/generate_keypair', headers = headers)

print(r.json())

```

`GET /api/v1/wg/generate_keypair`

*Generate Key Pair*

> Example responses

> 200 Response

```json
{
  "public_key": "string",
  "private_key": "string"
}
```

<h3 id="generate_key_pair_api_v1_wg_generate_keypair_get-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[KeyPair](#schemakeypair)|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|Not found|None|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

# Schemas

<h2 id="tocS_Body_login_api_v1_login_post">Body_login_api_v1_login_post</h2>
<!-- backwards compatibility -->
<a id="schemabody_login_api_v1_login_post"></a>
<a id="schema_Body_login_api_v1_login_post"></a>
<a id="tocSbody_login_api_v1_login_post"></a>
<a id="tocsbody_login_api_v1_login_post"></a>

```json
{
  "username": "string",
  "password": "string"
}

```

Body_login_api_v1_login_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|username|string|true|none|none|
|password|string|true|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>
<!-- backwards compatibility -->
<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_KeyPair">KeyPair</h2>
<!-- backwards compatibility -->
<a id="schemakeypair"></a>
<a id="schema_KeyPair"></a>
<a id="tocSkeypair"></a>
<a id="tocskeypair"></a>

```json
{
  "public_key": "string",
  "private_key": "string"
}

```

KeyPair

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|public_key|string|true|none|none|
|private_key|string|true|none|none|

<h2 id="tocS_PSK">PSK</h2>
<!-- backwards compatibility -->
<a id="schemapsk"></a>
<a id="schema_PSK"></a>
<a id="tocSpsk"></a>
<a id="tocspsk"></a>

```json
{
  "psk": "string"
}

```

PSK

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|psk|string|true|none|none|

<h2 id="tocS_Token">Token</h2>
<!-- backwards compatibility -->
<a id="schematoken"></a>
<a id="schema_Token"></a>
<a id="tocStoken"></a>
<a id="tocstoken"></a>

```json
{
  "access_token": "string",
  "token_type": "string",
  "user": {
    "id": 0,
    "username": "string",
    "email": "string",
    "full_name": "string",
    "role": "string"
  }
}

```

Token

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|access_token|string|true|none|none|
|token_type|string|true|none|none|
|user|[User](#schemauser)|true|none|none|

<h2 id="tocS_User">User</h2>
<!-- backwards compatibility -->
<a id="schemauser"></a>
<a id="schema_User"></a>
<a id="tocSuser"></a>
<a id="tocsuser"></a>

```json
{
  "id": 0,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string"
}

```

User

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|none|none|
|username|string|true|none|none|
|email|string|false|none|none|
|full_name|string|false|none|none|
|role|string|false|none|none|

<h2 id="tocS_UserInDB">UserInDB</h2>
<!-- backwards compatibility -->
<a id="schemauserindb"></a>
<a id="schema_UserInDB"></a>
<a id="tocSuserindb"></a>
<a id="tocsuserindb"></a>

```json
{
  "id": 0,
  "username": "string",
  "email": "string",
  "full_name": "string",
  "role": "string",
  "password": "string"
}

```

UserInDB

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|none|none|
|username|string|true|none|none|
|email|string|false|none|none|
|full_name|string|false|none|none|
|role|string|false|none|none|
|password|string|true|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>
<!-- backwards compatibility -->
<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[string]|true|none|none|
|msg|string|true|none|none|
|type|string|true|none|none|

<h2 id="tocS_WGPeer">WGPeer</h2>
<!-- backwards compatibility -->
<a id="schemawgpeer"></a>
<a id="schema_WGPeer"></a>
<a id="tocSwgpeer"></a>
<a id="tocswgpeer"></a>

```json
{
  "id": 0,
  "name": "string",
  "address": "string",
  "v6_address": "string",
  "private_key": "string",
  "public_key": "string",
  "shared_key": "string",
  "server_id": "string",
  "dns": "string",
  "allowed_ips": "string",
  "configuration": "string"
}

```

WGPeer

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|none|none|
|name|string|false|none|none|
|address|string|false|none|none|
|v6_address|string|false|none|none|
|private_key|string|false|none|none|
|public_key|string|false|none|none|
|shared_key|string|false|none|none|
|server_id|string|true|none|none|
|dns|string|false|none|none|
|allowed_ips|string|false|none|none|
|configuration|string|false|none|none|

<h2 id="tocS_WGPeerAdd">WGPeerAdd</h2>
<!-- backwards compatibility -->
<a id="schemawgpeeradd"></a>
<a id="schema_WGPeerAdd"></a>
<a id="tocSwgpeeradd"></a>
<a id="tocswgpeeradd"></a>

```json
{
  "server_interface": "string"
}

```

WGPeerAdd

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|server_interface|string|true|none|none|

<h2 id="tocS_WGServer">WGServer</h2>
<!-- backwards compatibility -->
<a id="schemawgserver"></a>
<a id="schema_WGServer"></a>
<a id="tocSwgserver"></a>
<a id="tocswgserver"></a>

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}

```

WGServer

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|none|none|
|address|string|false|none|none|
|v6_address|string|false|none|none|
|subnet|integer|false|none|none|
|v6_subnet|integer|false|none|none|
|interface|string|true|none|none|
|listen_port|integer|false|none|none|
|endpoint|string|false|none|none|
|private_key|string|false|none|none|
|public_key|string|false|none|none|
|is_running|boolean|false|none|none|
|configuration|string|false|none|none|
|post_up|string|false|none|none|
|post_down|string|false|none|none|
|dns|string|false|none|none|
|peers|[[WGPeer](#schemawgpeer)]|false|none|none|

<h2 id="tocS_WGServerAdd">WGServerAdd</h2>
<!-- backwards compatibility -->
<a id="schemawgserveradd"></a>
<a id="schema_WGServerAdd"></a>
<a id="tocSwgserveradd"></a>
<a id="tocswgserveradd"></a>

```json
{
  "id": 0,
  "address": "string",
  "v6_address": "string",
  "subnet": 0,
  "v6_subnet": 0,
  "interface": "string",
  "listen_port": 0,
  "endpoint": "string",
  "private_key": "string",
  "public_key": "string",
  "is_running": true,
  "configuration": "string",
  "post_up": "string",
  "post_down": "string",
  "dns": "string",
  "peers": []
}

```

WGServerAdd

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|integer|false|none|none|
|address|string|true|none|none|
|v6_address|string|false|none|none|
|subnet|integer|false|none|none|
|v6_subnet|integer|false|none|none|
|interface|string|true|none|none|
|listen_port|integer|true|none|none|
|endpoint|string|false|none|none|
|private_key|string|false|none|none|
|public_key|string|false|none|none|
|is_running|boolean|false|none|none|
|configuration|string|false|none|none|
|post_up|string|false|none|none|
|post_down|string|false|none|none|
|dns|string|false|none|none|
|peers|[[WGPeer](#schemawgpeer)]|false|none|none|

