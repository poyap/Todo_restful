### Django Todo app

#### In this project I built a rest api using django restframework to serialize our todo app models.


**We had two roles:** \n
    - developers
    - project managers

I used django User model to create a custom user that has additional field called "role". Which users had two options. In addition I used this field to give permissions to the users. So I created custom permissions based on built-in permission classes and baseclasses to extend the usability of them.
  