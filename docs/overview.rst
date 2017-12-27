# Overview #

Django-Iota-Auth began as an idea to write a custom authentication backend for the Django web framework that would allow a site developer to 'login' a User using their Iota seed, connecting them to the Tangle and allowing them to make purchases, transfer IOTA, etc. Essentially it will allow people to make IOTA web apps with Django. 

It became clear early on in the process that a developer would likely want to keep most of the User model functionality that ships with Django and still store this information in a database, i.e have a users email address, know their name etc. Only authenticating with an IOTA seed would not allow this behaviour. I went through a few attempts and iterations of how to achieve this, before finally settling on the simple solution.

Long story short, the IOTA Seed is sort of like a username and password combined. So...

1. I removed the username field by implementing a custom User model
2. I kept the password field which is defined in AbstractBaseUser and use this as the 'seed' field. At the end of the day, it's just terminology. Seed.. password.. you say tom-ay-to, I say tom-ar-to. Just change you labels to say Seed so people know what you are talking about... we don't have to make it hard. I have updated the Password Validators so it will only accept valid 'passwords' of 81 characters. I am not checking the strength of peoples seed but, that is entirely the users responsibility. 
3. Finally, I created a CustomBaseManager that subclasses the Django BaseManager, rewrite the make_random_unique_password funciton in BaseManager to make an IOTA seed, created a new UserManager that subclasses the new CustomBaseManager, and finally created a new User model that subclasses AbstractBaseUser and removed username functionality, and added the password as the USERNAME_FIELD.

## So how does it work? ##

When a user signs up, they need to enter email, first name, last name, and their IOTA Seed, which is the password. Emails have to be unique, so one account per user. The key part here is that someone may have an IOTA seed and wallet already, but doesn't mean they can use the site immediately. They need to sign up first so the web developer captures the information in the database.

Once you have signed up, to login, the user just enters their email and password/seed and they are connected to the tangle and given access to the site.  