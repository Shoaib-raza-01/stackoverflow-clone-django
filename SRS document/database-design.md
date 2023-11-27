## Database model

```
class User(
    image (url/image)
    bio (String)
    phone (number, Unique, Not Null)
    UserID (Primary Key, Auto-increment, Integer)
    UserName (String, Unique, Not Null)
    Email (String, Unique, Not Null)
    Password (String, Not Null)
)

class Question(
    QuestionID (Primary Key, Auto-increment, Integer)
    UserID (Foreign Key referencing Users.UserID)
    Title (String, Not Null)
    Description (Text, Not Null)
    CreatedAt (Timestamp)
    what you try and what is your expectation (Text, Not Null),
    Tags (Text, [#python, #dart, #django....]),
    
)

class Answer (
    AnswerID (Primary Key, Auto-increment, Integer)
    QuestionID (Foreign Key referencing Questions.QuestionID)
    UserID (Foreign Key referencing Users.UserID)
    Content (Text, Not Null)
    CreatedAt (Timestamp)
    Likes
)

class Comment (
    CommentID (Primary Key, Auto-increment, Integer)
    QuestionID (Foreign Key referencing Questions.QuestionID)
    AnswerID (Foreign Key referencing Answer.AnswerID)
    UserID (Foreign Key referencing Users.UserID)
    Content (Text, Not Null)
    CreatedAt (Timestamp)
    Likes
)

```

- Each User can ask multiple Questions. (One-to-Many: Users -> Questions)
- Each Question can have multiple Answers. (One-to-Many: Questions -> Answers)
- Each User can provide multiple Answers. (One-to-Many: Users -> Answers)
- Each User can comment on both questions and answers. (One-to-Many: Users -> Comments)
- Each question has a unique ID that references the user who asked it. (One-to-Many: Questions -> Users)
- Each answer has a unique ID that references the user who provided it. (One-to-Many: Answers -> Users)
- Each comment has a unique ID that references the user who made it. (One-to-Many: Comments -> Users)
