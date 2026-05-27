# E-Learning-Portal-using-Flask
 A Simple E-Learning website made using Flask and HTML and Bootstrap.
It includes portals for both students and teachers where students can acess or enroll into courses and teachers can create, update or delete courses and check out students enrolled into their courses.

Demo for this project can be checked out here: 

https://drive.google.com/file/d/1L_aoeOAvo1EoxxEJea02WHpomVsnfVcr/view?usp=sharing

You can register/login from the home page. The registration system has a 2 step verification system, where once you enter your details like First name, Last name, Email, password and if you are a teacher or not. Once these details are entered you will 
get a mail for OTP, which you have to enter in the portal. This was made using Flask-Mail.

Once registered you can login. After login you will be redirected to the respective dashboard, depending on whether you are a student or teacher. You can't access the course details without logging into your accounts.

In Student Dashboard, a student can access course material for the courses they have enrolled and can see relevent details of all the courses, but can't access the course material if not enrolled. To enroll the student
has to pay (not really, the payment gateway is in testmode), the student has to hit the enroll button, which will then redirect to a payment gateway, made with Stripe, and complete the payment process with test card details.
Once that completed, the student gets successfully enrolled into the course and can now access all the material. The student can also use search bar to look for any courses in particular.

The Teacher Dashboard on the other hand can see the courses they created only, they can check the enrolled students Name and email address only, they can edit details of the course or delete the course entirely. Teachers
can also add new courses, which when added will send notifications to students who were enrolled into other courses made the teacher in question, to encourage them to check those courses out.

All Students and Teacher records are stored in the User table, all course details are stored in the Courses table and the enrollment of students to their respective courses in the Enrolled table. The tables are made using SQL
and was connected with the program using SQLAlchemy.

### Attributes of USER Table:

- User Id
- First Name
- Last Name
- Email
- Password
- Account (teacher or student)

### Attributes of COURSE Table:

- Course Id
- Title
- Category
- Summary
- Requirements
- Reviews
- Price
- Duration
- Lectures
- Quizzes
- User Id (of teacher)

### Attributes of ENROLLED Table:

- Enroll Id
- User Id (of student)
- Course Id

To run this project first create database, and add that in the SQL URI in main.py, create the tables mentioned, check the details and more specification on each attribute in
the models.py. Install all libraries within a virtual environment as mentioned in the main.py and then run it. Note: dont forget to change the config details in the app.py to get
the notifications on the mail.
