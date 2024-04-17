# Creating Your First User

In order to use the member facing page of the server, we will need to create a test user we can login with. 

1. Create a test card. From the `/admin` page, navigate to _Membership->Card_, then click _Create_. Enter 0 as the serial for now. This is an integer, but everything else uses the hexadecimal representation. Enter 123 for the _Number On Front_, leave everything else as it is and click _Save_.
2. Create a test member. From the `/admin` page, navigate to _Membership->Member_, then click _Create_. Enter anything you want into the name and email fields. In the _Cards_ field, type the number 123 then select the entry that appears. Click _Save_ to finish.

## Logging In

You should now be able to navigate to `http://127.0.0.1:5000`. This will show the login page that's displayed on the member portal in the Hackspace.

Behind the scenes, this page listens for keyboard input and will log you in when a valid card serial is "typed" in. To login with the test card, type _0 then Enter_. You will have to be quick as there is a 0.5s timeout after the page loads!