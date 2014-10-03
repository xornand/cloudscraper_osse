Usage
=====

At this point you system is ready for crawling and searching, but it's empty.

Power up your wsgi web server and proceed with the initial setup. Open you browser and
go to `http://127.0.0.1/adminpanel <http://127.0.0.1/adminpanel>`_. Login with the default username `admin` and password
`admin`. Do not forget to change this later via Administration->auth->users page for security reasons!

Let's add a single directory which resides on your local drive (on the same machine where you installed Cloudscraper OSSE).

Open `http://127.0.0.1/adminpanel/locals/directory <http://127.0.0.1/adminpanel/locals/directory>`_. and click on `Add`. Enter
a non-empty directory path, and choose one of the predefined schedules. If you're not satisfied with them, you can always create
new ones on the cores->schedules page ordirectly by clicking on the + button. Additionaly, set description, owner and permissions
and click on `Save`. After a few moments (depends on directory size), your index will be ready for searching.

At this time your directory is added into the system and it will be crawled and updated by the schedule you have set during creation.