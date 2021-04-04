![](https://github.com/ThiagoKoster/FPSOEquipmentManager/workflows/Project%20Tests/badge.svg)
# FPSOEquipmentManager 

Backend to manage different equipment of an FPSO (Floating Production, Storage and Offloading)

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#set-up">Set Up</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

### Built With
* [Flask](https://palletsprojects.com/p/flask/) - Micro web framework.
* [flask-restx](https://github.com/python-restx/flask-restx) - Extension for flask that adds decorators to describe the 
  API and expose its documentation properly using *Swagger*. 
* [marshmallow](https://marshmallow.readthedocs.io/en/stable/) - Creates schemas for *validation* and *serialize/deserialize* data.
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM (Object Relational mapper) for database access.
* [SQLite](https://sqlite.org/index.html) - Data persistence and in memory database for unit tests. 




<!-- SET UP -->
## Set up
### Prerequisites
Python 3

### Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/ThiagoKoster/FPSOEquipmentManager
    ```
2. Setup virtual environment:
    ```sh
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
## Usage
### Run the application
```sh
 python app.py
```
This will start the application at <http://localhost:5000/api>

### Test the application
1. The swagger doc can be accessed at <http://localhost:5000/api/doc> when it is running.
![alt text](docs/resources/swagger-usage.gif)
   
<!-- CONTACT -->
## Contact
Thiago Koster Lago - thiagokoster@gmail.com


