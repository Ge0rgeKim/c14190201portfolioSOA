# Simple Cloud Storage

## Register New User

### Request
```bash
POST /user/register
```

### Respone
#### add user
![Response](https://img.shields.io/badge/Created-200-brightgreen)
```bash
{
    "status": "success",
    "message": "Success to add user"
}
```

#### add user (user password below 8 characters)
![Response](https://img.shields.io/badge/Bad%20Request-400-red)
```bash
{
    "status": "error",
    "message": "Password must contain 8 characters or more"
}
```

#### add user (user username already exist)
![Response](https://img.shields.io/badge/Bad%20Request-400-red)
```bash
{
    "status": "error",
    "message": "Username already exists"
}
```

## Login User

### Request
```bash
POST /user/register
```

### Respone
#### add user
![Response](https://img.shields.io/badge/Created-200-brightgreen)
```bash
{
    "status": "success",
    "message": "Success add User ..."
}
```

#### add user (user password below 8 characters)
![Response](https://img.shields.io/badge/Bad%20Request-400-red)
```bash
{
    "status": "error",
    "message": "password must be at least 8 characters"
}
```

#### add user (user username already exist)
![Response](https://img.shields.io/badge/Bad%20Request-400-red)
```bash
{
    "status": "error",
    "message": "username .... already exist"
}
```
