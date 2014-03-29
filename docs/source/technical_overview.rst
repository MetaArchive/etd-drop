Technical Overview
==================

ETD Drop is a simple web application for accepting online submissions of
electronic theses and dissertations (ETDs), written in Django.
Submissions are saved to a configurable location on disk in an easy to 
navigate structure, making them easy for your staff (or custom software) to 
review and move into the next stage of your ETD workflow.

A database is only required in order to facilitate user authentication, 
though with a bit of Django expertise it is possible to replace the default 
authentication system with a different one (e.g. using LDAP) potentially
eliminating the need for a database altogether.