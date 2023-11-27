## Database model

```
class Question(
    user, [primary key, unique]
    title,
    description,
    what you try and what is your expectation,
    date-created,
    tags(#python, #dart, #django....),
    
)

class Comment (
    question [foreign key]
    user []
    body,
    likes, (one to many relation)

)

class User(
    username,
    image,
    bio,
    phone
)
```

One question can have many answers