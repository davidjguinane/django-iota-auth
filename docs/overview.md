# Overview #

Django-Iota-Auth began as an idea to write a custom authentication backend for the Django web framework that would allow a site developer to 'login' a User using their Iota seed, connecting them to the Tangle and allowing them to make purchases, transfer IOTA, etc. Essentially it will allow people to make IOTA web apps with Django. 

It became clear early on in the process that a developer would likely want to keep most of the User model functionality that ships with Django and still store this information in a database, i.e have a users email address, know their name etc. Only authenticating with an IOTA seed would not allow this behaviour. I went through a few attempts and iterations of how to achieve this, before finally settling on the simple solution that I believe is secure but yet to be tested.

Long story short, the IOTA Seed is sort of like a username and password combined. So...

1. I removed the username field by implementing a custom User model
2. I kept the password field which is defined in AbstractBaseUser and use this as the 'seed' field. At the end of the day, it's just terminology. Seed.. password.. you say tom-ay-to, I say tom-ar-to. Just change you labels to say Seed so people know what you are talking about... we don't have to make it hard. I have updated the Password Validators with a custom 'IotaSeedValidator' so it will only accept valid seeds of 81 characters, all uppercase with only the number 9. I am not checking the strength of peoples seed but, that is entirely the users responsibility. 
3. I've implemented an encrpyted cookies sessions rather then the default database sessions. The reason for this is so that I can store the User seed securely to connect to and perform actions on the IOTA Tangle.  
4. Finally, I created a CustomBaseManager that subclasses the Django BaseManager, created a new UserManager that subclasses the new CustomBaseManager, and finally created a new User model that subclasses AbstractBaseUser and removed username functionality, and added the password as the USERNAME_FIELD. During the authentication process, the seed/password is set to the 'request.session['seed']' parameter for use in other code. 

## So how does it work? ##

When a user signs up, they need to enter email, first name, last name, and their IOTA Seed, which is the password. Emails have to be unique, so one account per user. The key part here is that someone may have an IOTA seed and wallet already, but doesn't mean they can use the site immediately. They need to sign up first so the web developer captures the information in the database.

Once you have signed up, to login, the user just enters their email and password/seed and they are logged in to the site and can be connected to the tangle. 