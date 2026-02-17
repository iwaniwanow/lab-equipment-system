(^) © SoftUni – about.softuni.bg. Copyrighted document. Unauthorized copy, reproduction or use is not permitted.

Django Basics Regular Exam
Individual Project
Project Requirements for Django Basics Course @ SoftUni
Your project is an opportunity to demonstrate your understanding of Django fundamentals by developing a
functional and visually appealing web application. You are expected to apply everything you have learned - from
setting up models, forms, and views, to creating dynamic templates and maintaining clean, modular code. The
project should showcase your ability to design and implement a real-world solution independently, following
Django's best practices and conventions. Focus on building a cohesive, original concept that reflects both technical
proficiency and thoughtful design.
1. Project Requirements
Important Notes :

Authentication and Django User management are explicitly excluded from the following requirements. You
are not supposed to implement login, logout, registration, or user-related functionality.
The submitted project must be downloadable , installable , and runnable without modifications. After
installing dependencies and applying migrations, the application should start successfully using the default
configuration.
All environment variables and credentials required for local testing must be clearly documented in your
README file.
Your Web Application must use the following technologies, frameworks, and development techniques:

The application must be implemented using the Django Framework (latest stable version).
o Your project must consist of at least three (3) Django apps , each with clearly defined
responsibilities.
o The application must define at least three (3) database models.
▪ Models created via inheritance or one-to-one relationships count as one model (for
example: Person <-> Employee counts as one model).
▪ Your database architecture must include at least one many-to-one and one many-to-many
relationship.
o The application must have at least three ( 3 ) forms with proper data validations.
▪ When validating data, display appropriate and user-friendly error messages.
▪ Implement validations both in forms and/or models where suitable.
▪ Customize error messages, help texts, labels, and placeholders.
▪ Include read-only or disabled fields in at least one form.
▪ Exclude unnecessary fields when rendering forms.
▪ Provide a confirmation step before deleting an object.
(^) © SoftUni – about.softuni.bg. Copyrighted document. Unauthorized copy, reproduction or use is not permitted.
o Implement views to handle business logic:
▪ You may use function-based views (FBVs) or class-based views (CBVs).
▪ Handle forms correctly (GET and POST methods, validation, saving).
▪ Use redirects after successful form submissions or updates.
o The application must include at least ten ( 10 ) web pages / templates built using the Django
Template Engine :
▪ At least seven (7) of them must display dynamic data from the database.
▪ Implement full CRUD functionality for at least two ( 2 ) models.
▪ Include pages that display all objects , filtered/sorted objects, and single-object details.
▪ Showcase your skills using built-in and custom template filters / tags.
▪ A custom 404 error page is required.
▪ A base template is mandatory (not counted among the 10 templates).
▪ Apply template inheritance and reusable partial templates (e.g., for headers, cards, or
lists).
▪ Ensure that navigation links connect all pages consistently, and every page includes a
footer.
▪ Templates can be reused across different views when appropriate.
▪ Implement a Web Page Design using Bootstrap , AI-generated layout , or your own custom
design.

All pages in the application must be accessible through navigation links.
o Avoid "orphan" pages that can only be reached by typing a URL manually.
o Ensure consistent navigation menus and footers across the site.
o Failure to implement a working navigation structure will negatively impact your assessment result ,
as any inaccessible pages will not be counted or evaluated.
Use a PostgreSQL Database Management System.
Use GitHub as your version control platform.
o Submit a public GitHub repository link.
o There must be a minimum of 3 ( three ) commits on 3 ( three ) separate days.
Showcase your project's functionality through well-structured project documentation.
o GitHub README file.
Follow Object-Oriented Programming (OOP) and clean code best practices :
o Apply data encapsulation and proper exception handling.
o Demonstrate inheritance, abstraction, and polymorphism where relevant.
o Follow strong cohesion and loose coupling principles.
o Maintain readable, consistently formatted code with clear naming conventions.
(^) © SoftUni – about.softuni.bg. Copyrighted document. Unauthorized copy, reproduction or use is not permitted.

Disclaimer
It is NOT permissible to use any of the following in your project:
o Ideas , Models , HTML , CSS , or entire Django apps taken from workshops , exercises , or
lectures / presentations.
o HTML / CSS / JS from JS modules , or any other SoftUni-related courses.
o AI-generated code (except HTML/CSS for layout and styling and project documentation).
If your project's codebase is mostly AI-generated (> 60%), your project will be disqualified and graded with
zero points (0 points).
Focus on developing a unique , original idea , and ensure your implementation reflects your own work and
understanding.
o Failure to do so will negatively affect your final assessment.
2. Submission Deadline
You must submit a GitHub link to your project before 15 :59 on 24 February 2026 using the submission
button in the Regular Exam section, available from 1 7 February 2026.
You may continue improving your project after assessment ( after 13 March 2026 )
o Do not push new commits until evaluation is finalized ; work locally until then.
Projects not submitted before the deadline will NOT be evaluated.
The assessment is performed manually and usually takes around 14 days.
3. Assessment Criteria
Originality and Concept (unique idea, relevance, creativity) - maximum 15 points
Database Design and Relationships (model structure, M2M, FKs, constraints, fields, methods, Meta, query
usage) - maximum 5 points
Implementing forms (customization, read-only, excludes, etc.) - maximum 15 points
Data validation (in forms and/or models, meaningful messages) - maximum 10 points
Views Implementation (CBVs/FBVs, redirects, handling forms, error handling) - maximum 15 points
Templates (links, dynamic data, inheritance, filters, tags, reusability) - maximum 15 points
Project Documentation (README clarity, setup instructions, structure overview) - maximum 5 points
Version Control (Git discipline: commits, structure, descriptive messages) - maximum 5 points
Advanced Features or Extra Functionality (not demonstrated by lecturer) - maximum 10 points
Code Quality and Structure (readability, OOP principles, modularity, cohesion) - maximum 5 points