![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) 
# Restaurant POS (Point of Sale)

## CS50X

This is my final project for CS50’s Introduction to Computer Science.

## Features
- **Fastapi**  
- **Uvicorn**
- **Jinja2**
- **SqlAlchemy**
- **Pydantic**
- **Bcrypt**
- **Passlib**

# Description 

This is my final project for CS50X, and it's a comprehensive restaurant application.
To begin, you need to log in as an administrator to add new roles or make changes. There are four types of roles available
- [Administrator](#administrator)
- [Chef](#chef)
- [Waiter](#waiter)
- [Customer](#customers)

All users are initially registered as customers. An administrator must change their roles, and your assigned role determines what actions you can perform.

The next diagrams shows the relation beteewn tables and views

![relational_diagram](/readme_img/relational_diagram.png)
![web_acces_diagram](/readme_img/web_access_diagram.png)

### Administrator
An administrator can perform all tasks, including creating or deleting users, and can also act as a customer or any other role.

### Chef
The chef will have full control over order management. They can change the order status, allowing the customer to track their order effectively.
The chef can manage the entire menu by adding or deleting items. They will also need to start the menu fresh at the beginning of each day to create the daily menu

### Waiter
Waiters can view the menu, create orders, and generate invoices.

### Customers
Finally, customers are limited to viewing the menu and accessing information about the ingredients used in each recipe.

#### Video Demo:  <URL https://www.youtube.com/watch?v=dMzZstF4tUc>
## Documentation
- [Fastapi](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
- [Uvicorn](https://www.uvicorn.org)




