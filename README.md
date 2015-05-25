# FindTeammates


## Introduction

“FindTeammates” is a web application, a platform for students to wisely form groups with the help of LinkedIn profile. Each student can demonstrate his or her strengths, while at the same time he or she can look up other students’ profiles to find their ideal teammates.


## Code Structure

This is a Django project. In the root, we have mysite/ directory, FindTeammates/ directory, and manage.py which is used to manage the project (such as running the server, migrate database). In mysite/ directory there are the setting file setting.py and url pattern matching file urls.py, and wsgi.py file. In FindTeammates/ directory, we have all the application-related files. FindTeammates/urls.py is a more detailed url pattern matching file. FindTeammates/views.py included all the views related to each defined url. In FindTeammates/models.py, we have defined all the database classes which are used in our application. In FindTeammates/recommender.py we have defined our recommendation algorithms. In FindTeammates/static/ directory, we have all the static js, css, fonts, images we need in our project. In FindTeammates/templates are the html files of our project. In FindTeammates/migrations are the migrate files we made due to our changes of database schemes.

## Requirement

1. Django (https://www.djangoproject.com/)
2. BeautifulSoup (http://www.crummy.com/software/BeautifulSoup/)

## Installation

Type following commands in shell:

1. git clone https://github.com/zjchen91/FindTeammates.git
2. cd FindTeammates
3. cd mysite
4. python manage.py runserver

Then copy url http://127.0.0.1:8000/FindTeammates/site to your browser.

## Contributors & Maintainers

1. Wendan Kang: wk2269@columbia.edu
2. Yu Wang: yw2684@columbia.edu
3. Zhejiao Chen: zc2291@columbia.edu
4. Enrui Liao: el2756@columbia.edu

