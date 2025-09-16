#-----------------LIBRARY MANAGEMENT SYSTEM--------------

import psycopg2
conn = psycopg2.connect(
  host = "localhost",
  user = "postgres",
  password = "trisha123",
  database = "postgres",
  port = 5432
)
def create_table():
  with conn.cursor() as cursor:
    cursor.execute("create table if not exists authors(id serial primary key,name TEXT NOT NULL)")
    cursor.execute("create table if not exists books(id serial primary key,title TEXT NOT NULL,author_id int references authors(id),available boolean default TRUE)")
    cursor.execute("create table if not exists borrowers(id serial primary key,name TEXT NOT NULL)")
    cursor.execute("create table if not exists borrow_record(id serial primary key,book_id int references books(id),borrower_id int references borrowers(id),returned boolean default FALSE);")
  conn.commit()

create_table()
def add_author(name):
  with conn.cursor() as cursor:
    cursor.execute("insert into authors(name) values(%s);",(name,))
  conn.commit()
def add_book(title,author_id):
  with conn.cursor() as cursor:
    cursor.execute("insert into books(title,author_id) values(%s ,%s);",(title,author_id))
  conn.commit()
def  add_borrower(name):
  with conn.cursor() as cursor:
    cursor.execute("insert into borrowers(name) values(%s);",(name,))
  conn.commit()
def borrow_book(book_id,borrower_id):
  with conn.cursor() as cursor:
    cursor.execute("select available from books where id = %s;",(book_id,))
    available = cursor.fetchone()
    if available and available[0]:
      cursor.execute("update books set available = FALSE where id = %s;",(book_id,))
      cursor.execute("insert into borrow_record(book_id,borrower_id) values(%s,%s);",(book_id,borrower_id))
    else:
      print("BOOK UNAVAILABLE FOR BORROW")
  conn.commit()
def return_book(book_id):
  with conn.cursor() as cursor:
    cursor.execute("update borrow_record set returned = TRUE where book_id = %s;",(book_id,))
    cursor.execute("update books set available = TRUE where id = %s",(book_id,))
  conn.commit()
def available_book():
  with conn.cursor() as cursor:
    cursor.execute("select * from books where available = TRUE;")
    result = cursor.fetchall()
    for r in result:
      print(f"{r[0]} |  {r[1]} | {r[2]} | {r[3]}")
  conn.commit()
def borrowed_by_user(borrower_id):
  with conn.cursor() as cursor:
    cursor.execute("select count(*) from borrow_record where borrower_id = %s;",(borrower_id,))
    result = cursor.fetchone()[0]
    print(f"no of books borrowed by {borrower_id} is {result}")
  conn.commit()

welcome = "WELCOME TO LIBRARY MANAGEMENT SYSTEM"
print(welcome)
menu = """   
1. Add Author
2. Add Book
3. Add Borrower
4. Borrow Book
5. Return Book
6. Show Available Books
7. Show Books Borrowed by User
8. Exit
"""
while (user_input := input(menu)) != "8":
  if user_input == "1":
    name = input("ENTER THE NAME:")
    add_author(name)
    print(f"{name} IS ADDED ")
  elif user_input == "2":
    title = input("ENTER THE TITLE:")
    author_id  =  int(input("ENTER THE ID:"))
    add_book(title,author_id)
    print(f"{title} BOOK ADDED SUCCESSFULLY")
  elif  user_input == "3":
    name = input("ENTER THE NAME OF THE BORROWER")
    add_borrower(name)
  elif user_input == "4":
    book_id = int(input("ENTER THE BOOK ID"))
    borrower_id = int(input("ENTER THE BORROWER ID:"))
    borrow_book(book_id,borrower_id)
  elif user_input == "5":
    book_id = int(input("ENTER THE BOOK TO RETURN :"))
    return_book(book_id)
    print("BOOK RETURNED SUCCESSFULLY")
  elif user_input == "6":
    print("showing available books :")
    available_book()
  elif user_input == "7":
     borrower_id = int(input("ENTER THE BOrrower ID"))
     borrowed_by_user(borrower_id)
  else:
    print("INVALID INPUT")












