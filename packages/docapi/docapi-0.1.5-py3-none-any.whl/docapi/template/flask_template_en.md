## Input

```python
# Get a list of students in a certain grade
@app.route('/users/list', methods=['GET', 'POST'])
def get_users():
    try:
        parmams = request.get_json()
        grade = parmams['grade']
        data = f'List of {grade} students'.split(' ')

        return jsonify(code=0, data=data, error=None)
    except Exception as e:
        return jsonify(code=1, data=None, error=str(e))
```

## Output

### GET|POST - /users/list

##### Update time

{datetime}

##### Description

This interface is used to obtain a list of students in a specified grade. The user needs to provide a grade parameter, and the interface will return a list of students in that grade.

##### Parameters

- `grade` (string): Required, grade name.

##### Return value

- `code` (integer): Return status code, 0 means success.

- `data` (array): Contains a list of students in that grade.

- `error` (string|null): Error message, null if successful.

##### Code example

**curl:**

```bash
curl -X GET http://{{API_BASE}}/users/list -H "Content-Type: application/json" -d '{{"grade": "高一"}}'
```

**python:**

```python
import requests

url = "http://{{API_BASE}}/users/list"
data = {"grade": "高一"}

response = requests.get(url, json=data)

print("status code:", response.status_code)
print("response content:", response.json())
```

**javascript:**

```javascript
const axios = require('axios');

const url = 'http://{{API_BASE}}/users/list';
const data = { grade: '高一' };

axios.get(url, { params: data })
    .then(response => {
        console.log('状态码:', response.status);
        console.log('响应内容:', response.data);
    })
    .catch(error => {
        console.error('错误:', error.response ? error.response.data : error.message);
    });
```
