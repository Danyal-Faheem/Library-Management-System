
# Library Management System API






## Features

- Permissions managed roles for user, librarian, admin
- Ability to view all books and filter by name
- Can initiate issue request for books by users
- Can handle requests for books by librarians
- Can initiate new book request by users
- Can handle new book requests by librarians
- Automated email reminders for return book
- Manually send email reminders to return book initiated by librarian
- Automated email notification if new book request inititiated and on status change
- Proper validation checks to ensure no more than 3 books are issued to user
- Cross platform


## API Reference

The api contains the following main URLs:

#### /admin
#### /user
#### /books

The following routes are provided:

### Users

#### Create User

```http
  POST /user/create
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user` | `UserProfile` | **Required**. The UserProfile object |

#### Returns the profile of all users if logged in user is a Librarian or just the logged in users profile if the current user is a User

```http
  GET /user/profile/
```



Manage, except create, the profile of user with id
```http
  GET, PUT, PATCH /user/profile/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of user to manage |


### Books

Return the list of books available at the library
```http
  GET /books/books/?name={name}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `name`      | `string` | **Optional**. Name to filter the books with |

Manage books. Only available to Librarians.
```http
  GET, PUT, POST, PATCH, DELETE /books/books/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of book to manage |

### Requests

Return the list of all requests made at the library. If current role is user, only returns the list of requests made by the user.
```http
  GET /books/requests/
```

Manage requests. Only available to Librarians.
```http
  GET, PUT, POST, PATCH, DELETE /books/requests/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of request to manage |

Send email reminder to the user who initiated the book issue request. Only avialable to Librarians.
```http
  GET /books/requests/{id}/reminder
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of request to send email reminder to |

### Tickets

Return the list of all tickets made at the library. If current role is user, only returns the list of requests made by the user.
```http
  GET /books/tickets/
```

Manage tickets. Only available to Librarians.
```http
  GET, PUT, POST, PATCH, DELETE /books/tickets/{id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of ticket to manage |