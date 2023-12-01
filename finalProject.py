# IMPORTSs

from tkinter.ttk import *
import io
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import sys
from tkinter import filedialog
import random
import sqlite3
import random
from datetime import datetime
import time
from datetime import timedelta
import sqlite3

###########
################################################################

#Create a new window using the Tkinter library.
#- Set the width of the window to 400 pixels.
#- Set the height of the window to 600 pixels.
#- Set the maximum size of the window to the specified width and height.
#- Set the minimum size of the window to the specified width and height.
#- Set the title of the window to 'SPARduct'.
#- Set the window to be displayed without the window manager decorations.
    
window = Tk()
WINDOW_WIDTH = 400
WINDOW_HEIGTH = 600
window.maxsize(WINDOW_WIDTH, WINDOW_HEIGTH)
window.minsize(WINDOW_WIDTH, WINDOW_HEIGTH)
window.title('SPARduct')
window.overrideredirect(True)
#window.wm_attributes("-transparentcolor", "#deb887")

accounts_list = []
################################################################

#The variable `tk_font` is set to the string "Calibre". This is likely used to specify the font to be used in a Tkinter application.
tk_font = "Calibre"
bgcolor = "#eeeeee"
text_color = "red"
user_index = 0

######################### LISTS
user_product_listsaction_list = [] #Create an empty list to store user product lists.
trans_code = "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM"
num = 0
date = datetime.now().date()
_time = time.localtime(time.time()) #Get the current local time and store it in the variable `_time`.
prd_key = 0
product_list = []
transaction_list = []

position = 200
cart_position = 200
search_frame_pos = 200
search_types_id = []
carts_id = []
gap_val = (WINDOW_WIDTH-340)//3
gap_val+=20
x_position = gap_val + 20  #Calculate the x position by adding the value of `gap_val` to 20.

################################################################
def size_check():
    """
    Check the size of the window and update the global variable `WINDOW_WIDTH` with the new width.
    
    """
    global WINDOW_WIDTH
    width = window.winfo_width()
    WINDOW_WIDTH = width
    window.update()


def open_id_image():
    """
    Open a file dialog to allow the user to select an image file for identification purposes.
    global id_picture - the path of the selected image file
    """
    global id_picture
    id_picture = filedialog.askopenfilename()


def upload_image_function():
    """
    This function allows the user to upload an image file. It opens a file dialog to select the image file and stores the file path in the global variable `product_img`.
    
    """
    try:
        global product_img
        product_img = filedialog.askopenfilename()
    except Exception as e:
        messagebox.showerror("Sign in error", "May kulang !\n Ayusin mo")

   
def on_mouse_wheel(event):
    """
    This function is called when a mouse wheel event occurs. It scrolls the view of a product frame by a certain number of units based on the direction and magnitude of the mouse wheel movement.
    event - the mouse wheel event
    
    """
    product_frame.yview_scroll(int(-1 * (event.delta / 120)), "units")


############ ACCOUNTS
class Accounts():
    """
    A class representing user accounts.
    """
    def __init__(self, id_pic, name,address, username, password):
        """
        Initialize a user object with the given attributes.
        id_pic - the ID picture of the user
        name - the name of the user
        address - the address of the user
        username - the username of the user
        password - the password of the user
        None
        """
        self.username = username
        self.password = password
        self.name = name
        self.address = address
        self.id_pic = id_pic
        self.user_product_list = []
        self.product_indx = 0
        self.transaction_list = []

        self.my_container_of_product = []

        self.date = datetime.now().date() #create current date
        
        self.mytransaction_frame = Canvas(user_transaction_frame,width=WINDOW_WIDTH,
                                          height=WINDOW_HEIGTH) #frame for user transaction
        self.my_products_frame = Canvas(product_frame, width=WINDOW_WIDTH,
                                          height=WINDOW_HEIGTH)  # frame for user transaction
        self.my_cart_frame = Canvas(cart_frame, width=WINDOW_WIDTH,
                                          height=WINDOW_HEIGTH)  # frame for user transaction

    def show_info(self):
        """
        Display information about a user in a graphical user interface.
        """
        user_frame = LabelFrame(users_frame)
        user_frame.pack(side='left')

        user_image = Label(user_frame, image=self.id_pic)
        user_image.pack()

        user_name = Label(user_frame, text=f"Name : {self.name}")
        user_name.pack()

        user_address = Label(user_frame, text=f"Address : {self.address}")
        user_address.pack()

        user_DATE = Label(user_frame, text=f"School : {self.date}")
        user_DATE.pack()
        
    # Getter methods to retrieve specific user details
    def get_img(self):
        return self.id_pic

    def get_date(self):
        return self.date

    def get_user_name(self):
        return self.name

    def get_user_address(self):
        return self.address

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id_pic
    ##########
    def add_product(self, product_img, product_name, product_price, product_stock, seller_contact):
        """
        Add a new product to the database.
        product_img - the image of the product
        product_name - the name of the product
        product_price - the price of the product
        product_stock - the stock of the product
        seller_contact - the contact information of the seller
        
        """
        global prd_key
        global user_index
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        key = 0
        for x in c.fetchall():
            key = x[0]
        print("key = ", key)
        if key < prd_key:
            prd_key = key + 1
            print("prd key  change", prd_key)
        conn.commit()
        conn.close()
        print("prd before adding", prd_key)
        with open(product_img, 'rb') as image_file:
            product_img = image_file.read()
        product = Products(sqlite3.Binary(product_img), product_name, product_price, product_stock, seller_contact,
                           user_index, prd_key,
                           self.product_indx)
        product.save()

        current_user().user_product_list.append(product)
        prd_key += 1
        print("prd after adding ", prd_key)
        window.update()
        self.product_indx += 1

    def unshow_my_products(self):
        """
        Hide all products in the user's product list.
        self - the instance of the class
        """
        for items in self.user_product_list:
            items.unshow()

    def show_user_products(self):
        """
        Display the products owned by the user.
       
        """
        global user_index
        for items in self.user_product_list:
            if items == None:
                pass
            else:
                items.show_my_product()
                window.update()

    def show_cart(self):
        """
        Display the cart for the current user and hide the carts for other users.
        """
        pass

    def unshow_cart(self):
        """
        Hide the cart items from the screen by using the `pack_forget()` method on each item in the `cart_list`.
        """
        pass
    def show_my_transaction(self):
        """
        Display the "mytransaction_frame" widget on the screen.
        """
        self.mytransaction_frame.pack(fill=BOTH)


class Products(Accounts):
    """
    This code defines a class named "Products" that inherits from a class named "Accounts".
    """
    def __init__(self, image_of_product, product_type, product_price, product_stock, seller_contact, product_index,id_num,
                 prd_indx):
        #Initialize an instance of a product with the given attributes.
        #image_of_product - the image of the product
        #product_type - the type of the product
        #product_price - the price of the product
        #product_stock - the stock of the product
        #seller_contact - the contact information of the seller
        #product_index - the index of the product
        #id_num - the identification number of the product
        #prd_indx - the index of the product (same as product_index)
        #return None
                 
        self.product_quan_f = None
        global user_index
       # global position_y
        global date
        global product_img
        global window
        global con_bg_img
        
        #Initialize a new object of the current class by calling the superclass's constructor with the following parameters:
        super().__init__(current_user().get_id(),# - The ID obtained from the `accounts_list` at the index `user_index`.
                         current_user().get_user_name(),# - The user name obtained from the `accounts_list` at the index `user_index`.
                         current_user().get_user_address(),#- The user address obtained from the `accounts_list` at the index `user_index`.
                         current_user().get_username(),#  - The username obtained from the `accounts_list` at the index `user_index`.
                         current_user().get_password())#  - The password obtained from the `accounts_list` at the index `user_index`.
        
        ###### quantinty value
        self.new_quan = StringVar()
        # products components
        self.prd_indx = prd_indx
        self.covert_to_img = Image.open(io.BytesIO(image_of_product))
        self.covert_to_img = self.covert_to_img.resize((130, 130))
        convert_to_img = ImageTk.PhotoImage(self.covert_to_img)

        #image for buy frame
        self.img = self.covert_to_img.resize((250,250))
        self.img = ImageTk.PhotoImage(self.img)
        
        self.product_image = convert_to_img
        self.image_of_product = image_of_product
        self.id_num = id_num
        self.product_type = product_type
        self.product_price = int(product_price)
        self.product_stock = int(product_stock)
        self.seller_contact = seller_contact
        self.product_index = product_index

        # time
        self.local_t = time.localtime()
        self.date_posted = datetime.now().date()
        self.time_posted = time.strftime("%H:%M:%S", self.local_t)

        #============================================================ products frame, labels and buttons
        gap_value = 0
        self.product_frame = None
        self.product_container = Canvas(product_frame,  bg='#f3f3f3', scrollregion=(0, 0, 400, 400),)
        self.product_bg_image = None
        self.product_bg_image = self.product_container.create_image(85, 85, image=con_bg_img)  # display container image
        self.product_image_con = Label(self.product_container, image=self.product_image, highlightthickness=2,
                              highlightcolor="black", highlightbackground='black')
        self.product_image_con.place(x=20, y=15) #display product image
        self.price_txt = None
        #============================================================ hOVER
        self.hover_label = Canvas(self.product_container)
        buy_btn = self.hover_label.create_image(85,140,image=buy_img)
        self.price_txt = self.hover_label.create_text(85,85,text=f"Price: PHP {self.product_price}",font=("Arial Black",9,"bold"),fill="black")
        self.hover_label.tag_bind(buy_btn,'<Button>',lambda event:self._add_tocart())
        self.product_container.bind('<Enter>',lambda event:self.hover_product())
        self.product_container.bind('<Leave>',lambda event:self.unhover_product())
        #============================================================
        self.insert_to() #insert to database Products
        #============================================================
        # cart frame
        self.cart_f = Frame(current_user().my_cart_frame)

        # transaction frame
        self.transaction_f = Label(accounts_list[self.product_index].mytransaction_frame)
        # trasaction history list
        #============================================================ create seller profile frame
        self.frame = Canvas(user_frame)
        #self.label = Label(self.frame, image=self.id_pic)
        self.con = Canvas(self.frame,highlightbackground="black",highlightcolor="black",highlightthickness=2,bd=1,width=280,height=350)
        self.con.create_image(200,280,image=wel_bg)
        self.con.create_image(140,100,image=self.id_pic)
        self.back_to_btn = self.frame.create_image(20,20,image=back_to_img)
        self.frame.tag_bind(self.back_to_btn,"<Button>",lambda event: self.profile_unview()) #back button
        self.con.create_text(140,210,font=("monoscape",20,"bold"),text=f"{self.get_user_name()}")
        self.con.create_text(170,240,font=("monoscape",15,"bold"),text=f"{self.get_user_address()}")
        self.con.place(x=60,y=100)
        #self.button_exit_prof = Button(self.frame, command=self.profile_unview, text="X")

        #self.info_label = Label(self.frame,
         #                       text=f"Name:{self.get_user_name()}\nAge:{self.get_age()}\nAddress:{self.get_user_address()}")
        #self.label.pack()
        #self.info_label.pack()
        #self.button_exit_prof.pack()
        #============================================================
        # myproducts frame
        self.myproduct_container = LabelFrame(user_products_frame)
        self.myproduct_image_f = Label(self.myproduct_container, image=self.product_image)
        self.my_Pinfo = Label(self.myproduct_container,
                              text=f"Type: {self.product_type} Price: {self.product_price} Stock: {self.product_stock}")
        self.selfindex = product_index
        self.remove_button = Button(self.myproduct_container, text='remove',
                                    command=lambda: self.remove_product())
        self.my_Pinfo.pack()
        self.myproduct_image_f.pack()
        self.remove_button.pack()

        # date delivever
        self.time_of_deliver = datetime.now().date().today() + timedelta(days=(int(_time.tm_wday) + 7))
        
    def hover_product(self): #show this when enter the cursor to the products container
        """
        Create a hover effect for a product container.
        """
        self.crt_hover_bg = self.product_container.create_window(85,85,window=self.hover_label,width=170,height=170)
        self.product_container.config(highlightbackground="black",highlightcolor="black",highlightthickness=1,bd=1)
         
    def unhover_product(self): #Leave the cursor from the product
        """
        Remove the hover effect from a product container.
        """
        self.product_container.delete(self.crt_hover_bg)
        self.product_container.config(highlightbackground="black",highlightcolor="black",highlightthickness=0,bd=0)
        
    def save(self):
        """
        Save the current product information to a SQLite database.
        """
        global user_index
        global product_img
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()

        product = [self.image_of_product, self.product_type, self.product_price, self.product_stock,
                   self.seller_contact, self.product_index]
        c.executemany(
            "INSERT INTO  products (product_img,product_type,product_price,product_stock,seller_contact,product_index) VALUES (?,?,?,?,?,?)",
            (product,))

        conn.commit()
        conn.close()

    def get_index(self):
        """
        Return the product index of an object.
        """
        return self.product_index

    def show(self):
        """
        Display the product information and handle key events.
        """
        global product_frame
        product_frame.bind("<Key>", self.move)
        index = user_index
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()
        if self.product_stock <= 0:
            """
            Check if the product stock is less than or equal to zero. If so, delete the product from the database, update the UI to indicate that the product is sold out, disable the buy button, and hide the product container. If the product stock is greater than zero, do nothing.
            """
            delete = f"DElETE FROM products WHERE id={self.id_num}"
            c.execute(delete)
            conn.commit()
            conn.close()
            self.my_Pinfo.config(text=f"SOLD OUT")
            self.product_container.pack_forget()
            self.myproduct_container.pack_forget()

        else:
            pass
        conn.commit()
        conn.close()

    def display_to_search_frame(self):
        """
        This method is used to display information about a product in a search frame.
        """
        global search_frame_pos
        # products frame, labels and buttons
        type_container = LabelFrame(search_frame, width=600, height=300, bg='red')

        type_contact = Label(type_container, text=self.seller_contact)
        type_contact.text = self.seller_contact
        type_contact.pack()

        type_stock = Label(type_container, text=str(self.product_stock))
        type_stock.text = str(self.product_stock)
        type_stock.pack()

        type_price = Label(type_container, text=self.product_price)
        type_price.text = self.product_price
        type_price.pack()

        type_img = Label(type_container, image=self.product_image)
        type_img.image = self.product_image
        type_img.pack()

        type_type = Label(type_container, text=self.product_type)
        type_type.pack()

        type_date = Label(type_container,
                          text=f"DATE POSTED: {self.date_posted}\nTIME: {self.time_posted}")
        type_date.pack()

        view_profile = Button(type_container, text='view', command=self.profile_view)
        view_profile.pack()
        # buy button
        buy_button = Button(type_container, text='add to cart')
        buy_button.pack()

        frame_id = search_frame.create_window((220, search_frame_pos), window=type_container, width=350, height=300)
       
        #Check if the `frame_id` is already present in the `search_types_id` list. If it is, remove it using the `delete()` method of the `search_frame` object. Then, add the `frame_id` to the `search_types_id` list. Finally, increment the `search_frame_pos` variable by 300.
        if frame_id in search_types_id:
            search_frame.delete(frame_id)
        search_types_id.append(frame_id)

        search_frame_pos += 300

    def move(self, event):
        """
        Move the product container widget by changing its x and y coordinates.
        event - the event that triggered the move
        """
        self.product_container.place(x=200, y=self.product_container.winfo_y() + 10)
        window.update()

    def insert_to(self):
        """
        This method is used to insert a product frame into a container. It sets the position and size of the product frame, binds events for scrolling, and updates the position variables for the next insertion.
        """
        global x_position
        global position
        global con_bg_img
        global gap_val
       
        self.product_frame = product_frame.create_window((x_position, position), window=self.product_container, width=170, height=170)

        # create binding function for background
        background_of_prod_frame.bind("<Configure>",
                                      lambda e: self.product_container.configure(scrollregion=self.product_container.bbox("all")))
        background_of_prod_frame.bind("<MouseWheel>", self.on_mousewheel_prdcts_F)
        # create binding function for product container
        self.product_container.bind("<Configure>",
                                    lambda e: self.product_container.configure(scrollregion=self.product_container.bbox("all")))
        self.product_container.bind("<MouseWheel>", self.on_mousewheel_prdcts_F)
        self.product_container.bind_all("<Configure>",
                                        lambda e: self.product_container.configure(scrollregion=self.product_container.bbox("all")))
        self.product_container.bind_all("<MouseWheel>", self.on_mousewheel_prdcts_F)

        if x_position == x_position:
            print("eatwyr")
            x_position = 60
            position += 175
        else:
            x_position += (con_bg_img.width +gap_val-20)
        # self.product_container.config(width=WINDOW_WIDTH)
    def on_mousewheel_prdcts_F(self,event):
        """
        This function is an event handler for the mousewheel event in a product frame. It scrolls the view of the product frame based on the delta value of the event.
        """
        product_frame.yview_scroll(-1 * (event.delta // 120), "units")

    def unshow(self):
        """
        Hide the product image, product information, product container, and remove button from the user interface.
        """
        self.myproduct_image_f.pack_forget()
        self.my_Pinfo.pack_forget()
        self.myproduct_container.pack_forget()
        self.remove_button.pack_forget()

    def unpack(self):
        """
        Hide the product container and the myproduct container by removing them from the display.
        """
        self.product_container.pack_forget()
        self.myproduct_container.pack_forget()

    def show_my_product(self):
        """
        Display the product information and image on the screen. If the product is out of stock, remove it from the database and disable the buy button. Otherwise, display the product image, information, and remove button.
        """
        if self.product_stock <= 0:
            conn = sqlite3.connect("Products.db")
            c = conn.cursor()
            delete = f"DElETE FROM products WHERE id={self.id_num}"
            c.execute(delete)
            conn.commit()
            conn.close()
            self.my_Pinfo.config(text=f"SOLD OUT")
            conn.commit()
            conn.close()
        else:
            self.myproduct_image_f.pack()
            self.my_Pinfo.pack()
            self.myproduct_container.pack()
            self.remove_button.pack()

    def _add_tocart(self):
        """
        This method is used to add a product to the user's shopping cart. It updates the GUI to display the product information and allows the user to select the quantity and payment method for the transaction.
        """
        global cart_position
        #global list_p
        global user_index
        unpack_all_frame_in_userframe()

        buy_frame.place(x=10,y=10)
        
        buy_frame.itemconfig(product_info_BF,text=f"\nPrice: PHP{self.product_price}\nType: {self.product_type}\nStock: {self.product_stock}")
        product_picture.config(image=self.img)
        buy_frame.itemconfig(payment_txt,text=f"Payment: 0")
        buy_frame.tag_bind(view_profile_button,"<Button>",lambda event:self.profile_view())
        #amount.config(text=str('PHP' + str(self.product_price)))
        quan_menu.config(textvariable=self.new_quan, from_=0, to=self.product_stock)
        buy_frame.tag_bind(buy_button,"<Button>",lambda event: self.transaction_method(int(quan_menu.get())))#create command for buy button
        self.change_payment()
        
    def change_payment(self):
        """
        This method is used to update the payment amount based on the quantity entered by the user. It handles different scenarios such as when the quantity is greater than the available stock, when the quantity is zero, and when the quantity is a valid number. 
        """
        try:
            """
            Try to perform the following operations:
            - Check if the value entered in `self.new_quan` is greater than the available stock (`self.product_stock`). If it is, display a message indicating that the stock is out of range.
            - Check if the value entered in `self.new_quan` is equal to 0. If it is, display a message indicating that the payment is PHP 0.
            - If neither of the above conditions are met, calculate the payment by multiplying the value entered in `self.new_quan` by `self.product_price` and display it as "Payment: PHP {payment}".
            - If any of the above operations result in a `ValueError`, display a message indicating that the payment is PHP 0
            """
            if int(self.new_quan.get()) > self.product_stock:
                buy_frame.after(100,lambda:self.change_payment())
                buy_frame.itemconfig(payment_txt,text=f"Payment: Stock out of range")
            elif int(self.new_quan.get()) == 0: 
                buy_frame.after(100,lambda:self.change_payment())
                buy_frame.itemconfig(payment_txt,text=f"Payment: PHP 0")
            else:
                buy_frame.itemconfig(payment_txt,text=f"Payment: PHP {int(self.new_quan.get())*self.product_price}")
                buy_frame.after(100,lambda:self.change_payment())

        except ValueError:
            buy_frame.after(100,lambda:self.change_payment())
            buy_frame.itemconfig(payment_txt,text=f"Payment: PHP 0")
            
    def transaction_method(self, new_quantity):
        global carts_id
        global cart_position
        global trans_code
        conn = sqlite3.connect("Products.db")
        conn2 = sqlite3.connect("Transaction.db")
        tran = conn2.cursor()
        c = conn.cursor()
        ask = messagebox.askyesno("info", "are you sure to buy this product?")
        if ask:

            code = ''
            quan = self.product_stock

            for i in range(5):
                code += str(trans_code[random.randint(0, 35)])
            self.product_stock -= new_quantity
            change = f"UPDATE products SET product_stock={self.product_stock} WHERE id={self.id_num}"
            c.execute(change)
            conn.commit()
            #self.product_quan_f.config(text=str(self.product_stock))
            self.my_Pinfo.config(
                text=f"Type: {self.product_type} Price: {self.get_price()} Stock: {self.product_stock}")

            print(self.product_stock)
            window.update()
            if self.product_stock <= 0:
                delete = f"DElETE FROM products WHERE id={self.id_num}"
                c.execute(delete)
                product_frame.delete(self.product_frame)
                conn.commit()
                self.my_Pinfo.config(text=f"SOLD OUT")
            
            # save to the cart
            price = int(self.get_price())
            payment = new_quantity * price
            print("payment",payment)
            product_p_c = Label(self.cart_f, image=self.product_image)
            product_info_c = Label(self.cart_f,
                                   text=f"Seller: {self.get_user_name()}\nProduct: {self.product_type}\nAmount: {self.product_price}\nQuantity: {quan}\nTransaction Code: {str(code)}\nPayment: {payment}\nDATE: {date}\nDATE OF DELIVER:{self.time_of_deliver}")

            product_p_c.pack()
            product_info_c.pack()
            self.cart_f.bind("<Configure>", lambda e: cart_frame.configure(scrollregion=cart_frame.bbox("all")))
            self.cart_f.bind("<MouseWheel>", on_mousewheel_carts_F)
            current_user().my_cart_frame.create_window(200,cart_position,window=self.cart_f,width=WINDOW_WIDTH,heigth=170)

            # add cart to user window
            cart_position += 180

            # save the transaction
            product_p_t = Label(self.transaction_f, image=self.product_image)
            product_info_t = Label(self.transaction_f,
                                   text=f"Buyer: {current_user().get_user_name()}\nProduct: {self.product_type}\nTransaction Code: {str(code)}\nPayment: {payment}\nDATE OF DELIVER:{self.time_of_deliver}")
            button_paid = Button(self.transaction_f, text="paid", command=lambda: (product_info_t.config(text="paid")))
            button_paid.pack()
            product_p_t.pack()
            product_info_t.pack()
            #accounts_list[self.product_index].transaction_list.append(self.transaction_f)
            accounts_list[self.product_index].mytransaction_frame.create_window(200,200,window=self.transaction_f,width=200)

            # send transaction to the admin
            insert_transaction_to_tb = [self.image_of_product, self.get_user_name(),
                                        current_user().get_user_name(), self.product_type, payment,
                                        self.time_of_deliver, code, int(self.product_index), int(user_index)]
            tran.executemany(
                "INSERT INTO transactions (product_img,seller_name,buyer_name,product_type,payment_amount,day_of_deliver,transaction_code,config_user_id,buyer_index) VALUES (?,?,?,?,?,?,?,?,?)",
                (insert_transaction_to_tb,))
            conn2.commit()
            transaction_list.append(
                str(f"Product:{self.product_type} | Seller:{self.get_user_name()} | Price:{self.product_price} >> Buyer:{current_user().get_user_name()} | Payment:{payment} | TRANSACTION CODE:{code}"))
        else:
            pass
        conn.commit()
        conn.close()
        conn2.commit()
        conn2.close()

    def profile_view(self):
        unpack_all_frame_in_userframe()
        self.frame.pack(expand=True, fill=BOTH)

    def profile_unview(self):
        self.frame.pack_forget()
        #product_frame.pack(expand=True, fill=BOTH)
        buy_frame.place(x=10,y=10)

    # Getter methods to retrieve specific user details
    def payment_frame(self):
        pass

    def get_name(self):
        return self.product_type

    def get_pro_date(self):
        return f"{self.date_posted}| {self.time_posted}"

    def get_image(self):
        return self.product_image

    def get_price(self):
        return self.product_price

    def remove_product(self):
        print("prd remove", self.id_num)
        self.myproduct_container.pack_forget()
        conn = sqlite3.connect("Products.db")
        c = conn.cursor()
        delete = f"DElETE FROM products WHERE id={self.id_num}"
        c.execute(delete)
        remove_in_user_product_list(self.product_indx)

        conn.commit()
        conn.close()
        window.update()

    def get_address(self):
        return self.address

    def get_contact(self):
        return self.seller_contact

    def get_quan(self):
        return self.product_stock


################################################################
def current_user():
    return accounts_list[user_index]

def show_user_content_window(user_window):
    return current_user().user_window.pack(fill=BOTH,expand=True)
def pack_window(windo):
    return windo.pack(fill=BOTH,expand=True)
def unpack_window(windo):
    return windo.pack_forget()
def save_product(product_imagee, product_name, product_price, product_quan, seller_contact):
    global product_frame
    global num
    global product_img
    global product_list
    if (
            product_validation(product_imagee, product_name, product_price, product_quan, seller_contact)):
        img = Image.open(product_img)
        img = img.resize((40, 40))
        img = ImageTk.PhotoImage(img)
        current_user().add_product(product_imagee,
                                              product_name,
                                              product_price,
                                              product_quan,
                                              seller_contact,
                                              )

        prd = Label(inven_frame, image=img,
                    text=f"Seller:{current_user().get_user_name()} Type:{product_name} Price:{product_price} Stock:{product_quan}",
                    compound="left")
        prd.image = img
        product_list.append(prd)
        num += 1
        upload_name_of_product.delete(0, END)
        upload_price.delete(0, END)
        upload_stock.delete(0, END)
        upload_contact.delete(0, END)

    else:
        return messagebox.showerror('error', 'error')


def product_validation(product_img, product_type, product_price, product_stock, seller_con):
    if product_img == None and product_type == "" and product_price == '' and product_stock == '' and seller_con == '':
        return False
    else:
        return True


def remove_in_user_product_list(indexx):
    print("remove index", indexx)

    current_user().user_product_list.remove(current_user().user_product_list[indexx])
    for item in current_user().user_product_list:
        if len(current_user().user_product_list) == 0:
            pass
        else:
            item.product_indx -= 1
    print("new len of list", len(current_user().user_product_list))
    window.update()


#######################  SAVE ACCOUNT

def save_account(id_pic, name,address, username, password):
    global sign_in_username
    global accounts_list
    #global age
    try:
        if sign_in_validation(id_pic, name,address, username, password):
            conn = sqlite3.connect('Accounts.db')
            c = conn.cursor()

            img = Image.open(id_pic)
            img = img.resize((60, 60))
            img = ImageTk.PhotoImage(img)
            account = Accounts(id_pic, name,address, username, password)
            accounts_list.append(account)
            with open(id_pic, 'rb') as image_file:
                id_picture = image_file.read()
                c.execute("INSERT INTO accounts (id_pic,name,address,username,password) VALUES (?,?,?,?,?)",
                          (sqlite3.Binary(id_picture), name, address, username, password))
            conn.commit()
            conn.close()
            sign_in_username.delete(0, END)
            sign_user_address.delete(0, END)
            sign_in_password.delete(0, END)
            confirm_pass.delete(0, END)
            show_log_in_frame()
        else:
            show_sign_in_frame()
    except Exception as e:
        messagebox.showerror("Sign in error", "May kulang !\n Ayusin mo")


def sign_in_validation(id_pic, name, address, username, password):
    if not (
            id_pic == None or name == '' or address == '' or username == ''):
        if password == confirm_pass.get():
            return True
    else:
        return False


#######################  ADMIN

def admin():
    size_check()
    global product_list

    unpack_window(log_in_canvas)
    pack_window(admin_frame)

    conn = sqlite3.connect('Accounts.db')
    c = conn.cursor()

    c.execute("SELECT * FROM accounts ")
    for acc in c.fetchall():
        imga = Image.open(io.BytesIO(acc[1]))
        imga = imga.resize((60, 60))
        imgs = ImageTk.PhotoImage(imga)
        container = LabelFrame(users_frame)
        pro_img = Label(container, image=imgs)
        pro_img.image = imgs
        infos = Label(container, text=f"NO# {acc[0]} Name: {acc[2]}Address: {acc[3]}")
        container.pack()
        pro_img.pack()
        infos.pack()

    # user_infos = Label(users_frame,text=f"Name: {ac[1]}\nAge: {ac[2]}\nAddress: {ac[3]}")
    # user_infos.pack()
    conn.commit()
    conn.close()
    for products in product_list:
        products.pack()
    # product_list[0].pack()
    for items in transaction_list:
        Label(admin_tran_frame, text=items).pack()


def users(event):
    size_check()
    admin_menu_frame.pack_forget()
    inven_frame.pack_forget()
    admin_tran_frame.pack_forget()

    users_frame.pack(expand=True, fill=BOTH)


def inventory(event):
    size_check()
    admin_menu_frame.pack_forget()
    users_frame.pack_forget()
    admin_tran_frame.pack_forget()

    inven_frame.pack(expand=True, fill=BOTH)


def admin_log_out():
    pass


def admin_menu(event):
    size_check()
    users_frame.pack_forget()
    inven_frame.pack_forget()
    admin_tran_frame.pack_forget()

    admin_menu_frame.pack(expand=True, fill=BOTH)


def admin_tran(event):
    size_check()
    users_frame.pack_forget()
    inven_frame.pack_forget()
    admin_menu_frame.pack_forget()

    admin_tran_frame.pack(expand=True, fill=BOTH)


#######################   USERS


def user():
    size_check()
    window.update()


def home():
    global product_main_frame
    global cart_position
    global carts_id
    global search_frame_pos
    global search_frame
    size_check()
    unpack_window(log_in_canvas)
    pack_window(user_frame)
    unpack_all_frame_in_userframe()
        
    current_user().mytransaction_frame.pack(fill=BOTH,expand=True) #show user transaction
    current_user().my_cart_frame.pack(fill=BOTH, expand=True)  # show user transaction
    # display user data such as cart,products and transaction hirtory
    for item in current_user().user_product_list:
        item.show_user_products()
        
    current_user().show_user_products()
    # show carts of user
    pack_window(product_main_frame)
    
    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200
    
def unpack_all_frame_in_userframe():
    sell_frame.pack_forget()
    cart_main_frame.pack_forget()
    profile_frame.pack_forget()
    menu_frame.pack_forget()
    buy_frame.pack_forget()
    user_products_frame.pack_forget()
    user_transaction_frame.pack_forget()
    search_frame.pack_forget()
    product_main_frame.pack_forget()

def show_products(event):
    global search_frame_pos
    global products
    size_check()
    unpack_all_frame_in_userframe()
    pack_window(product_main_frame)
    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200


def mysearch(event):
    global search_frame_pos
    size_check()
    unpack_all_frame_in_userframe()

    pack_window(search_frame)

    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200


def myproducts(event):
    global search_frame_pos

    size_check()
    unpack_all_frame_in_userframe()

    for item in current_user().user_product_list:
        item.show_user_products()

    for items in accounts_list:
        if items == current_user() and len(current_user().user_product_list) != 0:
            items.show_user_products()
            window.update()
        else:
            items.unshow_my_products()
    pack_window(user_products_frame)

    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200


def mytransaction(event):
    global search_frame_pos
    size_check()
    unpack_all_frame_in_userframe()

    for item in current_user().user_product_list:
        item.show_my_transaction()

    pack_window(user_transaction_frame)
    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200


def back_to_log_com():
    global search_frame_pos
    size_check()
    unpack_window(sign_in_canvas)
    pack_window(log_in_canvas)

    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200


def add_product(event):
    global search_frame_pos
    size_check()
    unpack_all_frame_in_userframe()
    pack_window(sell_frame)

    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200


def remove_product():
    pass


def menu(event):
    global search_frame_pos
    size_check()
    unpack_all_frame_in_userframe()

    pack_window(menu_frame)
    show_menu_transition()

    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200
    
def show_menu_transition(wid=0):
    if wid == 100:
        pass
    else:
        menu_box.config(width=wid)
        menu_frame.after(5,lambda:show_menu_transition(wid))
        wid+=1

def cart(event):
    global search_frame_pos
    global cart_position
    size_check()
    unpack_all_frame_in_userframe()
    pack_window(cart_main_frame)

    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200


def profile(event):
    global search_frame_pos
    global user_index
    global accounts_list
    size_check()
    unpack_all_frame_in_userframe()
    
    pack_window(profile_frame)
    profile_pic.config(image=current_user().get_img())
    profile_NAME.config(text=current_user().get_user_name())
    profile_ADDRES.config(text=current_user().get_user_address())

    for types in search_types_id:
        search_frame.delete(str(types))
    search_frame_pos = 200

# scroll the products
def on_mousewheel_carts_F(event):
    cart_frame.yview_scroll(-1 * (event.delta // 120), "units")


def change_bg_color():
    log_in_canvas.itemconfig(switch, image=moon_img)
    log_in_canvas.config(bg='#414a4c')

    log_in_canvas.tag_bind(switch, "<Button>", lambda event: change_to_light())


def change_to_light():
    log_in_canvas.itemconfig(switch, image=sun_img)
    log_in_canvas.config(bg=bgcolor)
    log_in_canvas.tag_bind(switch, "<Button>", lambda event: change_bg_color())


def user_log_out(event):
    global carts_id
    global cart_frame
    global cart_position
    unpack_all_frame_in_userframe()
    cart_position = 200
    for items in accounts_list:
        items.unshow_my_products()
        items.unshow_my_transaction()
    for ids in carts_id:
        cart_main_frame.delete(str(ids))
    welcome()


def about():
    pass


################################################################
# center the window
def center_window(window, width, height, ):
    screen_width = window.winfo_screenwidth()
    screen_heigth = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_heigth - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


################################################################
def restore_db_to_list():
    global accounts_list
    global num
    global prd_key
    global product_list


    products_list = []

    conn = sqlite3.connect("Accounts.db")
    conn2 = sqlite3.connect("Products.db")
    conn3 = sqlite3.connect("Transaction.db")

    c = conn.cursor()
    c2 = conn2.cursor()
    c3 = conn3.cursor()
    # c2.execute("CREATE TABLE IF NOT EXISTS products (product_img BLOB,product_type text,product_price INTEGER,product_stock INTEGER,product_index INTEGER)")
    c.execute("SELECT * FROM accounts")
    c2.execute("SELECT * FROM products")

    index = 0
    # RESTORE ACCOUNTS FROM THE DATABASE ACCOUNTS TO LIST OF ACCOUNTS
    for acc in c.fetchall():
        """
        Retrieve account information from a database and create Account objects for each entry. 
        c - the cursor object for executing SQL queries
        accounts_list - a list of Account objects
        """
        img = Image.open(io.BytesIO(acc[1]))
        img = img.resize((150, 150))
        img = ImageTk.PhotoImage(img)
        account = Accounts(img, acc[2], acc[3], acc[4], acc[5])
        accounts_list.append(account)
        print("name user:", accounts_list[index].get_user_name())
        index += 1
    print("account len is ", len(accounts_list))
    products_restore = c2.fetchall()

    # RESTORE PRODUCTS FROM DATABASE PRODUCTS TO ITS OWNERS
    for acc_index in range(len(accounts_list)):
        """
        Iterate over the accounts list and for each account, iterate over the products restore list. If the account index matches the index in the product, create a new product object and add it to the product list. Also, update the user's product list and increment the product index. Finally, commit the changes to the database.
        accounts_list - the list of accounts
        products_restore - the list of products to restore
        """
        print("len(", acc_index, ")")
        for prod in products_restore:
            print("prod[6]", int(prod[6]), "=", acc_index)
            if prod[6] == acc_index:
                print("prod[6]", int(prod[6]))
                img = Image.open(io.BytesIO(prod[1]))
                img = img.resize((60, 60))
                img = ImageTk.PhotoImage(img)
                product = Products(prod[1], prod[2], prod[3], prod[4], prod[5], acc_index, prod[0],
                                   accounts_list[acc_index].product_indx)
                prd = Label(inven_frame, image=img,
                            text=f"Seller:{accounts_list[acc_index].get_user_name()} Type:{prod[2]} Price:{prod[3]} Stock:{prod[4]}",
                            compound="left")
                prd.image = img

                product_list.append(prd)
                print(prod[0])
                accounts_list[acc_index].user_product_list.append(product)

                accounts_list[acc_index].product_indx += 1
                print("prd number before", prd_key)
                if prod[0] > prd_key:
                    prd_key = prod[0]
                    print("prd number after", prd_key)

            conn.commit()
    prd_key += 1
    print("prd last ", prd_key)

    # RESTORE TRANSACTION LIST
    for user_id in range(len(accounts_list)):
        """
        Iterate over the range of the length of the accounts_list.
        accounts_list - the list of user accounts
        """
        c3.execute("SELECT * FROM transactions")
        for _tran in c3.fetchall():
            """
            Iterate over the results fetched from the database query and assign each result to the variable `_tran`.
            """
            if _tran[8] == user_id:
                """
                If the 8th element of the `_tran` list is equal to `user_id`, perform the following actions:
                - Print the value of `_tran[8]`, followed by `'tran'` and `user_index`.
                - Create a `LabelFrame` called `transaction_container` within the `mytransaction_frame` of the `accounts_list` at the index `user_id`.
                - Open the image stored in `_tran[1]` as `tran_img`, resize it to 40x40 pixels, and convert it to a `PhotoImage` object.
                - Create a `Label` called `product_p_t` within `transaction_container` and set its image to `tran_img`.
                - Create a `Label` called `product
                """
                print(_tran[8], 'tran', user_index)
                transaction_container = LabelFrame(accounts_list[user_id].mytransaction_frame)
                tran_img = Image.open(io.BytesIO(_tran[1]))
                tran_img = tran_img.resize((40, 40))
                tran_img = ImageTk.PhotoImage(tran_img)
                product_p_t = Label(transaction_container, image=tran_img)
                product_p_t.image = tran_img
                product_info_t = Label(transaction_container,
                                       text=f"Buyer: {_tran[3]}\nProduct: {_tran[4]}\nTransaction Code: {_tran[7]}\nPayment: {_tran[5]}\nDATE OF DELIVER:{_tran[6]}")
                button_paid = Button(transaction_container, text="paid",
                                     command=lambda: product_info_t.config(text="paid"))
                button_paid.pack()
                product_p_t.pack()
                product_info_t.pack()
                accounts_list[user_id].mytransaction_frame.create_window(200,200,window=transaction_container,width=200)
                print('gwrtygwhg')

    # RESTORE USER CART FROM DB
    for user_id in range(len(accounts_list)):
        """
        Loop through each user ID in the accounts list and execute a SQL query to select all transactions from the "transactions" table.
        accounts_list - a list of user accounts
        """
        c3.execute("SELECT * FROM transactions")
        for _tran in c3.fetchall():
            """
            Iterate over the results fetched from the database. If the value at index 9 of the fetched result is equal to the given user_id, 
            perform the following actions:
            """
            if _tran[9] == user_id:
                """
                If the value at index 9 of the _tran list is equal to the user_id, perform the following actions:
                - Print the value at index 9 and the user_id.
                - Open the image stored at index 1 of the _tran list and resize it to 40x40 pixels.
                - Create a PhotoImage object from the resized image and assign it to the cart_img variable.
                - Create a LabelFrame widget named cart_user_frame.
                - Create a Label widget named product_p_c and set its image attribute to the cart_img.
                - Assign the cart_img to the image attribute of the product_p_c widget.
                - Create a Label widget named product_info_c and set its text attribute to a formatted string containing information from the _tran
                """
                print("9:", _tran[9], "user_id = ", user_id)

                cart_img = Image.open(io.BytesIO(_tran[1]))
                cart_img = cart_img.resize((40, 40))
                cart_img = ImageTk.PhotoImage(cart_img)
                cart_user_frame = Canvas(cart_main_frame)

                product_p_c = Label(cart_user_frame, image=cart_img)
                product_p_c.image = cart_img
                product_info_c = Label(cart_user_frame,
                                       text=f"Seller: {_tran[2]}\nProduct: {_tran[4]}\nTransaction Code: {_tran[7]}\nPayment: {_tran[5]}\nDATE OF DELIVER:{_tran[6]}")
                accounts_list[user_id].my_cart_frame.create_window(200,cart_position,window=cart_user_frame,width=400)

                product_p_c.pack()
                product_info_c.pack()
                print("name", _tran[9])

    conn2.close()
    conn3.close()
    conn.close()


def welcome():
    size_check()
    pack_window(home_canvas)


###############################################################

################################################################

def log_in_validation():
    """
    Validate the login credentials entered by the user.
    """
    global user_index
    conn = sqlite3.connect('Accounts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM accounts")
    if log_in_username.get() == "admin" and log_in_password.get() == 'admin':
        log_in_password.delete(0, END)
        log_in_username.delete(0, END)
        admin()
    else:
        for acc in c.fetchall():
            if log_in_username.get() == acc[4] and log_in_password.get() == acc[5]:
                user_index = acc[0] - 1
                log_in_password.delete(0, END)
                log_in_username.delete(0, END)
                home()
                break

    conn.commit()
    conn.close()


###############################################################
def write_text(index):
    """
    Write a text on a canvas gradually by updating the text with each iteration.
    index - the current index of the text to be written
    """
    if index <= len(tagline):
        partial_text = tagline[:index]
        home_canvas.itemconfig(bsu_tagline, text=partial_text)

        home_canvas.after(40, write_text, index + 1)


def enter_txt_U():
    log_in_canvas.itemconfig(usr_name_line, fill="black", width=1)
    window.update()

    log_in_canvas.itemconfig(usr_p_line, fill="#F3F2ED", width=1)
    window.update()

    print('wrht')


def leave_txt_U():
    pass


def enter_txt_P():
    log_in_canvas.itemconfig(usr_name_line, fill="#F3F2ED", width=1)
    window.update()

    log_in_canvas.itemconfig(usr_p_line, fill="black", width=1)
    window.update()


################################################################

def show_password():
    print("aeg")
    log_in_password.config(show='')
    log_in_password.show = ""
    log_in_canvas.itemconfig(pass_btn_config, image=hide_pass_img)
    log_in_canvas.tag_unbind(pass_btn_config, "<Button>")
    log_in_canvas.tag_bind(pass_btn_config, "<Button>", lambda event: hide_password())
    window.update()


################################################################

def hide_password():
    log_in_password.config(show='*')
    log_in_password.show = "*"
    log_in_canvas.itemconfig(pass_btn_config, image=show_pass_img)
    log_in_canvas.tag_unbind(pass_btn_config, "<Button>")
    log_in_canvas.tag_bind(pass_btn_config, "<Button>", lambda event: show_password())
    window.update()


################################################################
def show_log_in_frame():
    unpack_window(sign_in_canvas)
    unpack_window(home_canvas)
    pack_window(log_in_canvas)

################################################################

def show_sign_in_frame():
    unpack_window(log_in_canvas)
    sign_in_canvas.pack(expand=True, fill=BOTH)


################################################################

def line_move_to_home(event):
    line.place(x=WINDOW_WIDTH - 428, y=27)


def line_move_to_menu(event):
    line.place(x=WINDOW_WIDTH - 49, y=27)


def line_move_to_prof(event):
    line.place(x=WINDOW_WIDTH - 138, y=27)


def line_move_to_search(event):
    line.place(x=WINDOW_WIDTH - 338, y=27)


def line_move_to_cart(event):
    line.place(x=WINDOW_WIDTH - 238, y=27)


# search method
def search_type():
    type = srch_entry.get()
    for acc in accounts_list:
        for prds in acc.user_product_list:
            if type == prds.get_name():
                # search_frame.create_window((220, position), window=type_W,width=350,height=300)
                prds.display_to_search_frame()


############ center the window
center_window(window, WINDOW_WIDTH, WINDOW_HEIGTH)
########################## BSU LOGO

logo_big = Image.open('images/logobsu.png')
logo_big = logo_big.resize((100, 100))
logo_big = ImageTk.PhotoImage(logo_big)

logo_big_super = Image.open('images/logobsu.png')
logo_big_super = logo_big_super.resize((200, 200))
logo_big_super = ImageTk.PhotoImage(logo_big_super)

logo_med = Image.open('images/logobsu.png')
logo_med = logo_med.resize((80, 80))
logo_med = ImageTk.PhotoImage(logo_med)

logo_small = Image.open('images/logobsu.png')
logo_small = logo_small.resize((50, 50))
logo_small = ImageTk.PhotoImage(logo_small)

user_logo = Image.open('images/user.png')
user_logo = user_logo.resize((25, 20))
user_logo = ImageTk.PhotoImage(user_logo)

add_logo = Image.open('images/add.png')
add_logo = add_logo.resize((25, 20))
add_logo = ImageTk.PhotoImage(add_logo)

search_logo = Image.open('images/search logo.png')
search_logo = search_logo.resize((25, 20))
search_logo = ImageTk.PhotoImage(search_logo)

menu_logo = Image.open('images/menu-burger.png')
menu_logo = menu_logo.resize((25, 20))
menu_logo = ImageTk.PhotoImage(menu_logo)

product_logo = Image.open('images/shopping-cart (1).png')
product_logo = product_logo.resize((25, 20))
product_logo = ImageTk.PhotoImage(product_logo)

home_logo = Image.open('images/home.png')
home_logo = home_logo.resize((25, 20))
home_logo = ImageTk.PhotoImage(home_logo)

sign_outl = Image.open('images/sign-out.png')
sign_outl = sign_outl.resize((25, 20))
sign_outl = ImageTk.PhotoImage(sign_outl)

line_logo = Image.open('images/line.png')
line_logo = line_logo.resize((25, 1))
line_logo = ImageTk.PhotoImage(line_logo)

bg_img = Image.open('images/bg_products_F.jpg')
bg_img = bg_img.resize((WINDOW_WIDTH, 700))
bg_img = ImageTk.PhotoImage(bg_img)

bg_2 = Image.open('images/bg2.png')
bg_2 = bg_2.resize((WINDOW_WIDTH, 700))
bg_2 = ImageTk.PhotoImage(bg_2)

########################## ADMIN WINDOW

admin_frame = Canvas(window)
############

admin_label = Label(admin_frame, text="Admin", font=(tk_font, 10), bg=bgcolor)
admin_label.pack(fill=BOTH)

############

admin_frames_but = LabelFrame(admin_frame,
                              bg=bgcolor,
                              highlightcolor='black',
                              highlightthickness=1,
                              highlightbackground='black'
                              )
admin_frames_but.pack(fill=X)

#
inventory_frame_but = Label(admin_frames_but,
                            text='Inventory',
                            width=15
                            )
inventory_frame_but.pack(side='left')
inventory_frame_but.bind('<Button>', inventory)

#
users_frame_but = Label(admin_frames_but,
                        text='Users',
                        width=15
                        )
users_frame_but.pack(side='left')
users_frame_but.bind('<Button>', users)
#
admin_tran_frame_but = Label(admin_frames_but,
                             text='Transaction',
                             width=15
                             )
admin_tran_frame_but.pack(side='left')
admin_tran_frame_but.bind('<Button>', admin_tran)

#
admin_menu_frame_but = Label(admin_frames_but,
                             text='Menu',
                             width=23
                             )
admin_menu_frame_but.pack(side='right')
admin_menu_frame_but.bind('<Button>', admin_menu)

########################## INVENTORY WINDOW FRAME

inven_frame = Canvas(admin_frame, bg='red')

########################## USERS WINDOW FRAME

users_frame = Canvas(admin_frame, bg='blue')

########################## ADMIN MENU WINDOW FRAME

admin_menu_frame = Canvas(admin_frame, bg='green')

########################### ADMIN TRANSACTION WINDOW FRAME

admin_tran_frame = Canvas(admin_frame, bg='black')
###################################################################################### USER WINDOW FRAME


user_frame = Canvas(window)

bottom_can_bar = Canvas(user_frame, width=WINDOW_WIDTH, height=35, bg='white')
bottom_can_bar.pack(side="bottom")
################################################################
user_bg_img = Image.open('images/log-in-bg.png')
user_bg_img = user_bg_img.resize((WINDOW_WIDTH, WINDOW_HEIGTH))
user_bg_img = ImageTk.PhotoImage(user_bg_img)

# sign_in_canvas.create_image(250, 250, image=bg_img)
user_frame_bg = Image.open('images/bg_products_F.jpg')
user_frame_bg = user_frame_bg.resize((WINDOW_WIDTH, 540))

user_frame_bg = ImageTk.PhotoImage(user_frame_bg)

user_frame.create_image(200, 250, image=user_frame_bg)
####################################

bottom_bar_img = Image.open('images/bottom-bar.png')
bottom_bar_img = bottom_bar_img.resize((WINDOW_WIDTH, 40))
bottom_bar_img = ImageTk.PhotoImage(bottom_bar_img)

user_frame.create_image(227, WINDOW_HEIGTH - 20, image=bottom_bar_img)

####################################
gap_value = (WINDOW_WIDTH - (menu_logo.width() + user_logo.width() + product_logo.width() + home_logo.width())) / 7

menu_button_c = bottom_can_bar.create_image(WINDOW_WIDTH - (menu_logo.width() + gap_value), 18, image=menu_logo)
#bottom_can_bar.tag_bind(menu_button_c, "<Enter>", line_move_to_menu)
bottom_can_bar.tag_bind(menu_button_c, "<Button>", menu)
#############
#myprod_button_c = bottom_can_bar.create_image(WINDOW_WIDTH - (menu_logo.width() + gap_value), 18, image=menu_logo)
#bottom_can_bar.tag_bind(myprod_button_c, "<Enter>", line_move_to_menu)
#bottom_can_bar.tag_bind(myprod_button_c, "<Button>", myproducts)

#############
prof_button_c = bottom_can_bar.create_image(WINDOW_WIDTH - (menu_logo.width() + user_logo.width() + (gap_value * 2)),
                                            18, image=user_logo)
bottom_can_bar.tag_bind(prof_button_c, "<Enter>", line_move_to_prof)
bottom_can_bar.tag_bind(prof_button_c, "<Button>", profile)

add_button_c = bottom_can_bar.create_image(
    WINDOW_WIDTH - (menu_logo.width() + user_logo.width() + product_logo.width() + (gap_value * 3)), 18,
    image=add_logo)
#bottom_can_bar.tag_bind(add_button_c, "<Enter>", line_move_to_cart)
bottom_can_bar.tag_bind(add_button_c, "<Button>", add_product)


search_button_c = bottom_can_bar.create_image(WINDOW_WIDTH - (
        menu_logo.width() + user_logo.width() + product_logo.width() + search_logo.width() + (gap_value * 4)), 18,
                                              image=search_logo)
bottom_can_bar.tag_bind(search_button_c, "<Enter>", line_move_to_search)
bottom_can_bar.tag_bind(search_button_c, "<Button>", mysearch)

home_button_c = bottom_can_bar.create_image(WINDOW_WIDTH - (
        menu_logo.width() + user_logo.width() + product_logo.width() + search_logo.width() + home_logo.width() + (
        gap_value * 5)), 18, image=home_logo)
bottom_can_bar.tag_bind(home_button_c, "<Enter>", line_move_to_home)
bottom_can_bar.tag_bind(home_button_c, "<Button>", show_products)

line = Label(bottom_can_bar, image=line_logo, bg="black", highlightcolor="black", highlightbackground="black",
             highlightthickness=0)

####################################

############


#
########################## buy frame

buy_frame = Canvas(user_frame,highlightbackground="black",highlightcolor="black",highlightthickness=2,height=500,bg="white")
#label = Label(buy_frame, text='BUY')
#label.pack(side=TOP)
#product_image_BF = None

##############
buy_frame_bg_img = Image.open('images/bgnanaman.jpg')
buy_frame_bg_img = buy_frame_bg_img.resize((390,510))
buy_frame_bg_img = ImageTk.PhotoImage(buy_frame_bg_img)
#buy_frame.create_image(190,255,image=buy_frame_bg_img) #create background image of buyframe
###############
quan_menu_img = Image.open('images/txt-box.png')
quan_menu_img = quan_menu_img.resize((190,190))
quan_menu_img = ImageTk.PhotoImage(quan_menu_img) 
#buy_frame.create_image(270,270,image=quan_menu_img)

product_info_BF = buy_frame.create_text(110,310,text="",font=("Calibre", 10,"bold"),fill="black") #create text information 
##############
buy_btn_img = Image.open('images/buy.png')
buy_btn_img = buy_btn_img.resize((70,55))
buy_btn_img = ImageTk.PhotoImage(buy_btn_img) #image for buy button 
buy_button = buy_frame.create_image(290,470,image=buy_btn_img) #create button
##############
prof_btn_img = Image.open('images/user.png')
prof_btn_img = prof_btn_img.resize((20,20))
prof_btn_img = ImageTk.PhotoImage(prof_btn_img) #image for buy button 
view_profile_button = buy_frame.create_image(280,310,image=prof_btn_img) #create button
buy_frame.create_text(280,330,text="Profile",font=("Calibre", 6,"bold"),fill="black")#create text 'profile' label
##############
product_picture = Label(buy_frame,highlightbackground="black",highlightcolor="black",highlightthickness=2) #Product image container
buy_frame.create_window(190,140,window=product_picture,width=250,height=250)
buy_frame.create_line(10,280,370,280,width=2,fill="black")

#amount = Label(buy_frame)
#amount.pack(side=LEFT)
############

new_quan = IntVar()
quan_menu = Spinbox(buy_frame,width=15)
quan_menu.place(x=170,y=400)
############ payment text
payment_txt = buy_frame.create_text(40,470,text="Payment: 0")
#buy_button.pack(side=BOTTOM)

########################## MENU WINDOW FRAME

menu_frame = Canvas(user_frame, bg='black')
menu_frame.create_image(200,280,image=bg_img)
menu_frame.create_image(200,280,image=logo_big_super)

menu_box = Canvas(menu_frame,highlightbackground="black",highlightcolor="black",highlightthickness=2,bg=bgcolor,height=500)
menu_box.pack(side='right')

log_out = menu_box.create_text(25,15,text="Log out")
menu_box.tag_bind(log_out,'<Button>', user_log_out)

menu_box.create_line(0,30,100,30,fill="black",width=2)

show_transaction_btn = menu_box.create_text(35,40,text="Transaction")
menu_box.tag_bind(show_transaction_btn,'<Button>', mytransaction)

menu_box.create_line(0,50,100,50,fill="black",width=2)

show_products_btn = menu_box.create_text(37,60,text="My Products")
menu_box.tag_bind(show_products_btn,'<Button>', myproducts)

menu_box.create_line(0,70,100,70,fill="black",width=2)

########################## ADD PRODUCT WINDOW FRAME

sell_frame = Canvas(user_frame, bg='yellow')

upload_image = Button(sell_frame, command=lambda: upload_image_function(), text="Product image")
upload_image.pack()

upload_name_of_product = Entry(sell_frame)
upload_name_of_product.pack()

upload_price = Entry(sell_frame
                     )
upload_price.pack()

upload_stock = Entry(sell_frame)
upload_stock.pack()

upload_contact = Entry(sell_frame)
upload_contact.pack()

upload_product = Button(sell_frame,
                        command=lambda: save_product(product_img, upload_name_of_product.get(), upload_price.get(),
                                                     upload_stock.get(), upload_contact.get()), text="Uplaod")
upload_product.pack()
########################## CART WINDOW FRAME

cart_frame_bg = Image.open('images/bgnanaman.jpg')
cart_frame_bg = cart_frame_bg.resize((470, 610))
cart_frame_bg = ImageTk.PhotoImage(cart_frame_bg)
cart_main_frame = Canvas(user_frame)

cart_bg = Label(cart_main_frame, image=cart_frame_bg,width=WINDOW_WIDTH,height=50)
cart_bg.pack()

cart_frame = Canvas(cart_main_frame,width=WINDOW_WIDTH,height=450)
pack_window(cart_frame)

cart_bg.bind("<Configure>", lambda e: cart_frame.configure(scrollregion=cart_frame.bbox("all")))
cart_bg.bind("<MouseWheel>", on_mousewheel_carts_F)
########################## SEARCH WINDOW FRAME

search_frame_bg = Image.open('images/bgnanaman.jpg')
search_frame_bg = search_frame_bg.resize((470, 610))
search_frame_bg = ImageTk.PhotoImage(search_frame_bg)

search_frame = Canvas(user_frame, bg='red')
# search_bg = Label(search_frame, image = search_frame_bg)
# search_bg.pack()

srch_entry = Entry(search_frame, width=200)
srch_entry.pack()

srch_btn = Button(search_frame, text="Search", command=search_type)
srch_btn.pack()
########################## PROFILE WINDOW FRAME

profile_frame = Canvas(user_frame,
                       bg=bgcolor,

                       )

prof_background_img = Image.open('images/profbg.jpg')
prof_background_img = prof_background_img.resize((470, 610))
prof_background_img = ImageTk.PhotoImage(prof_background_img)

profile_frame.create_image(220, 256, image=prof_background_img)
# bg_prof = Label(profile_frame, image=bg_2)
# bg_prof.pack()

profile_outine = Frame(profile_frame,
                       highlightcolor='black',
                       highlightthickness=1,
                       highlightbackground='black',
                       pady=50,
                       padx=100,
                       bg=bgcolor
                       )
profile_outine.place(x=60, y=20)
profile_pic = Label(profile_outine,
                    highlightcolor='black',
                    highlightthickness=1,
                    highlightbackground='black',
                    borderwidth=2
                    )
profile_pic.pack()

seperator = Label(profile_outine, text="______________________________", bg=bgcolor)
seperator.pack()

profile_name_L = Label(profile_outine,
                       text='NAME',
                       font=(tk_font, 8, 'bold'),
                       bg=bgcolor)
profile_NAME = Label(profile_outine,
                     bg=bgcolor,
                     font=(tk_font, 18, 'bold')
                     )
profile_name_L.pack()
profile_NAME.pack()


profile_address_L = Label(profile_outine,
                          text='ADDRESS',
                          font=(tk_font, 8, 'bold'),
                          bg=bgcolor)
profile_ADDRES = Label(profile_outine,
                       bg=bgcolor,
                       font=(tk_font, 18, 'bold')
                       )
profile_address_L.pack()
profile_ADDRES.pack()

########################## PRODUCTS WINDOW FRAME
product_frame_bg = Image.open('images/bg_products_F.jpg')
product_frame_bg = product_frame_bg.resize((WINDOW_WIDTH, 540))

product_frame_bg = ImageTk.PhotoImage(product_frame_bg)

# container image
con_bg_img = Image.open('images/productcont.jpg')
con_bg_img = con_bg_img.resize((170, 170))
con_bg_img = ImageTk.PhotoImage(con_bg_img)

buy_img = Image.open('images/buy (2).png')
buy_img = buy_img.resize((50,33))
buy_img = ImageTk.PhotoImage(buy_img)
 
product_main_frame = Canvas(user_frame,bg="red")
product_frame = Canvas(product_main_frame, bg='#deb887', scrollregion=(0, 0, 10000, 10000), width=WINDOW_WIDTH,height=450)
product_frame.pack(fill=X,side="bottom")
# Bind mouse wheel event to the canvas
# product_frame.bind("<MouseWheel>", on_mouse_wheel)

# product_frame.create_image(220,256 , image = product_frame_bg)
background_of_prod_frame = Canvas(product_main_frame,width=WINDOW_WIDTH)
background_of_prod_frame.pack(fill=BOTH, expand=True)

#create image bacakground for home
background_of_prod_frame.create_image(200,267,image=product_frame_bg)

######## cart button
cart_button_c = background_of_prod_frame.create_image(380, 18,
    image=product_logo)
background_of_prod_frame.tag_bind(cart_button_c, "<Button>", cart)
########
background_of_prod_frame.create_text(200, 50, text="SPARduct", font=(tk_font,20, "bold"), fill="black")

#product_frame.bind("<Configure>", lambda e: product_frame.configure(scrollregion=product_frame.bbox("all")))
#self.product_containerproduct_frame.bind("<MouseWheel>", on_mousewheel_prdcts_F)

########################## USER PRODUCTS WINDOW FRAME

user_products_frame = Canvas(user_frame, bg='orange')
########################## USER transaction WINDOW FRAME
user_transaction_frame_bg = Image.open('images/bg_ulit.jpg')
user_transaction_frame_bg = user_transaction_frame_bg.resize((470, 610))
user_transaction_frame_bg = ImageTk.PhotoImage(user_transaction_frame_bg)

user_transaction_frame = Canvas(user_frame)
user_transaction_frame.create_image(220, 256, image=user_transaction_frame_bg)

user_transaction_frame = Canvas(user_frame)

########################## SIGN UP WINDOW FRAME

sign_in_canvas = Canvas(window, bg=bgcolor)
######### gaps value

#########
sign_txt_bx = Image.open('images/txt-box.png')
sign_txt_bx = sign_txt_bx.resize((300, 70))
sign_txt_bx = ImageTk.PhotoImage(sign_txt_bx)

sign_img_bx = Image.open('images/txt-box.png')
sign_img_bx = sign_img_bx.resize((100, 50))
sign_img_bx = ImageTk.PhotoImage(sign_img_bx)

back_to_img = Image.open('images/back-arrow.png')
back_to_img = back_to_img.resize((30, 30))
back_to_img = ImageTk.PhotoImage(back_to_img)

sign_to_img = Image.open('images/sign-in.png')
sign_to_img = sign_to_img.resize((160, 80))
sign_to_img = ImageTk.PhotoImage(sign_to_img)

sign_bg_img = Image.open('images/new-.jpg')
sign_bg_img = sign_bg_img.resize((WINDOW_WIDTH, WINDOW_HEIGTH))
sign_bg_img = ImageTk.PhotoImage(sign_bg_img)

sign_out_img = Image.open('images/sign-out.png')
sign_out_img = sign_out_img.resize((725, 616))
sign_out_img = ImageTk.PhotoImage(sign_out_img)

# sign_in_canvas.create_image(250, 250, image=bg_img)

sign_in_canvas.create_image(WINDOW_WIDTH-(sign_bg_img.width()//2), 300, image=sign_bg_img)

back_to_log = sign_in_canvas.create_image(20, 20, image=back_to_img)
sign_in_canvas.tag_bind(back_to_log, "<Button>", lambda event: back_to_log_com())
######## gaps value

sign_txt_box_gap =  (WINDOW_WIDTH-sign_txt_bx.width())//2
########

# outline = sign_in_canvas.create_image(230,300,image=sign_out_img)
#############

######## create logo in log in box and gap value
sign_login_gap_W = (WINDOW_WIDTH-logo_med.width())//2
sign_in_canvas.create_image(sign_login_gap_W+(logo_med.width()//2), 90, image=logo_med)

######## create log in text
sign_in_canvas.create_text(sign_login_gap_W+(logo_med.width()//2), 155, text="Sign up", font=("Segoe UI Black", 24, "bold"))

######## create username label
sign_in_canvas.create_text(120, 210, text="Name", font=("Calibre", 8, "bold"))
######## create username label
sign_in_canvas.create_text(130, 260, text="Address", font=("Calibre", 8, "bold"))
######## create username label
sign_in_canvas.create_text(130, 310, text="Username", font=("Calibre", 8, "bold"))
######## create username label
sign_in_canvas.create_text(130, 360, text="Password", font=("Calibre", 8, "bold"))
######## create username label
sign_in_canvas.create_text(155, 410, text="Confirm Password", font=("Calibre", 8, "bold"))

#############

name_txt_box = sign_in_canvas.create_image(sign_txt_box_gap+(sign_txt_bx.width()//2), 220, image=sign_txt_bx)

address_txt_box = sign_in_canvas.create_image(sign_txt_box_gap+(sign_txt_bx.width()//2), 270, image=sign_txt_bx)

username_txt_box = sign_in_canvas.create_image(sign_txt_box_gap+(sign_txt_bx.width()//2), 320, image=sign_txt_bx)

password_txt_box = sign_in_canvas.create_image(sign_txt_box_gap+(sign_txt_bx.width()//2), 370, image=sign_txt_bx)

confirm_txt_box = sign_in_canvas.create_image(sign_txt_box_gap+(sign_txt_bx.width()//2), 420, image=sign_txt_bx)

#button to open id picture
img_box = sign_in_canvas.create_image((sign_txt_box_gap+((sign_txt_bx.width()//2)-80)), 460, image=sign_img_bx)
sign_in_canvas.tag_bind(img_box, "<Button>", lambda event: open_id_image())

############
# logo
# sign_in_canvas.create_image(220,50,image=logo_med)

# sign label
# sign_in_canvas.create_text(220,90,text="Sign in",font=(tk_font,20,"bold"))

# insert user profile

insert_id = Button(sign_in_canvas, text="Upload id",
                   bg='red',
                   font=(tk_font, 8),
                   command=lambda: open_id_image())
# insert_id.place(x=80,y=150)


######## create name entry
sign_user_name = Entry(sign_in_canvas,
                       width=33,
                       font=(tk_font, 10),
                       bg="#F3F2ED",
                       bd=0)
######## display the name entry
sign_user_name.place(x=(sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, y=227)

######## bind the username entry,this binding appear the line inside of entry box if the cursor enter
# sign_user_name_label.bind("<Enter>",lambda event:enter_txt_U())

######## create line inside of entry box
usr_name_line_S = sign_in_canvas.create_line((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, 246, ((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29)+230, 246, fill="black", width=1)

######## bind the username entry,this binding appear the line inside of entry box if the cursor enter
# sign_user_name_label.bind("<Enter>",lambda event:enter_txt_U())

# create sign address entry
sign_user_address = Entry(sign_in_canvas,
                          width=33,
                          font=(tk_font, 10),
                          bg="#F3F2ED",
                          bd=0)
sign_user_address.place(x=(sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, y=276)

######## create line inside of entry box
address_line_S = sign_in_canvas.create_line((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, 295, ((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29)+230, 295, fill="black", width=1)

######## create sign user username entry
sign_in_username = Entry(sign_in_canvas,
                         width=33,
                         font=(tk_font, 10),
                         bg="#F3F2ED",
                         bd=0)
sign_in_username.place(x=(sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, y=327)

######## create line inside of entry box
username_line_S = sign_in_canvas.create_line((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, 346, ((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29)+230, 346, fill="black", width=1)

####### create sign user password entry
sign_in_password = Entry(sign_in_canvas,
                         width=33,
                         font=(tk_font, 10),
                         bg="#F3F2ED",
                         bd=0)
sign_in_password.place(x=(sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, y=376)

######## create line inside of entry box
pass_line_S = sign_in_canvas.create_line((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, 395, ((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29)+230, 395, fill="black", width=1)

# confirm pass word label / input

# sign confirm password entry
confirm_pass = Entry(sign_in_canvas,
                     width=33,
                     font=(tk_font, 10),
                     bg="#F3F2ED",
                     bd=0,
                     show="*")
confirm_pass.place(x=(sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, y=427)

######## create line inside of entry box
confirm_line_S = sign_in_canvas.create_line((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29, 446, ((sign_txt_box_gap+((sign_txt_bx.width()//2)-80))-29)+230, 446, fill="black", width=1)

# create sign in button
sign_btn_gap =  (WINDOW_WIDTH-sign_to_img.width())//2
sign_in_button = sign_in_canvas.create_image(sign_btn_gap+(sign_to_img.width()//2), 530, image=sign_to_img)
sign_in_canvas.tag_bind(sign_in_button, "<Button>",
                        lambda event: save_account(id_picture, sign_user_name.get(), sign_user_address.get(),
                                                   sign_in_username.get(), sign_in_password.get()))

# try:    # sign_buttton = Button(outline,
# bg=text_color,image=sign_to_img,
# command=lambda: save_account(id_picture, sign_user_name.get(), age.get(), sign_user_address.get(),
# sign_in_username.get(), sign_in_password.get()),
#                 font=(tk_font, 10),
#                 width=10)
#    sign_buttton.pack()
# except Exception as e:
#   messagebox.showerror("Sign in error", "May kulang !\n Ayusin mo")


########################## LOG IN  PRODUCT WINDOW FRAME
# create window for log in
log_in_canvas = Canvas(window)
#########

crt_acc_btn = Image.open('images/crt_acc.png')
crt_acc_btn = crt_acc_btn.resize((230, 60))
crt_acc_btn = ImageTk.PhotoImage(crt_acc_btn)

log_outl = Image.open('images/log_out.png')
log_outl = log_outl.resize((430, 460))
log_outl = ImageTk.PhotoImage(log_outl)

txt_bx = Image.open('images/txt-box.png')
txt_bx = txt_bx.resize((300, 70))
txt_bx = ImageTk.PhotoImage(txt_bx)

log_btn = Image.open('images/log-in.png')
log_btn = log_btn.resize((170, 70))
log_btn = ImageTk.PhotoImage(log_btn)

log_in_b = Image.open('images/log in.png')
log_in_b = log_in_b.resize((60, 20))
log_in_b = ImageTk.PhotoImage(log_in_b)

sign_in_b = Image.open('images/signin.png')
sign_in_b = sign_in_b.resize((60, 20))
sign_in_b = ImageTk.PhotoImage(sign_in_b)

moon_img = Image.open('images/switch (1).png')
moon_img = moon_img.resize((40, 40))
moon_img = ImageTk.PhotoImage(moon_img)

sun_img = Image.open('images/switch.png')
sun_img = sun_img.resize((40, 40))
sun_img = ImageTk.PhotoImage(sun_img)

log_bg_img = Image.open('images/new-.jpg')
log_bg_img = log_bg_img.resize((WINDOW_WIDTH, WINDOW_HEIGTH))
log_bg_img = ImageTk.PhotoImage(log_bg_img)

show_pass_img = Image.open('images/eye2.png')
show_pass_img = show_pass_img.resize((20, 15))
show_pass_img = ImageTk.PhotoImage(show_pass_img)

hide_pass_img = Image.open('images/eye2.png')
hide_pass_img = hide_pass_img.resize((20, 15))
hide_pass_img = ImageTk.PhotoImage(hide_pass_img)

####### gap values
log0_login_gap_W = (WINDOW_WIDTH-logo_med.width())//2
txt_box_gap =  (WINDOW_WIDTH-txt_bx.width())//2
log_btn_gap =  (WINDOW_WIDTH-log_btn.width())//2
crt_btn_gap =  (WINDOW_WIDTH-crt_acc_btn.width())//2

######## background
log_in_canvas.create_image(WINDOW_WIDTH-(log_bg_img.width()//2), 300, image=log_bg_img)
###########
######## password show config
pass_btn_config = log_in_canvas.create_image(txt_box_gap+(txt_bx.width()//2)+150, 325, image=show_pass_img)

log_in_canvas.tag_bind(pass_btn_config, "<Button>", lambda event: show_password())

switch = log_in_canvas.create_image(25, 25, image=sun_img)

log_in_canvas.tag_bind(switch, "<Button>", lambda event: change_bg_color())

######## log in box background
# log_in_canvas.create_image(227,300,image=log_outl)

######## create logo in log in box
log_in_canvas.create_image((log0_login_gap_W+(logo_med.width()//2)), 120, image=logo_med)

######## create log in text
log_in_canvas.create_text((log0_login_gap_W+(logo_med.width()//2)), 185, text="Log in", font=("Segoe UI Black", 24, "bold"))

######## create entry box
txt_boxU = log_in_canvas.create_image(txt_box_gap+(txt_bx.width()//2), 260, image=txt_bx)
txt_boxP = log_in_canvas.create_image(txt_box_gap+(txt_bx.width()//2), 310, image=txt_bx)

######## create username label
username_txt = log_in_canvas.create_text(txt_box_gap+((txt_bx.width()//2)-80), 250, text="Username", font=("Calibre", 8, "bold"))
######## create password label
password_txt = log_in_canvas.create_text(txt_box_gap+((txt_bx.width()//2)-80), 300, text="Password", font=("Calibre", 8, "bold"))

######## create button for log in
btn_log_in = log_in_canvas.create_image(log_btn_gap+(log_btn.width()//2), 390, image=log_btn)
log_in_canvas.tag_bind(btn_log_in, "<Button>", lambda event: log_in_validation())

######## create button for create account
log_in_canvas.create_text(crt_btn_gap+(crt_acc_btn.width()//2), 430, text="Don't have an account?")
btn_crt_acc = log_in_canvas.create_image((log_btn_gap+(log_btn.width()))-76, 470, image=crt_acc_btn)
log_in_canvas.tag_bind(btn_crt_acc, "<Button>", lambda event: show_sign_in_frame())

############
######## create username entry
log_in_username = Entry(log_in_canvas,
                        width=33,

                        font=(tk_font, 10),
                        bg="#F3F2ED",
                        bd=0)
######## display the username entry
log_usernmae_gap_val = (WINDOW_WIDTH-log_in_username.winfo_width())//5
log_in_username.place(x=(txt_box_gap+((txt_bx.width()//2)-80))-29, y=267)
######## create show and hide password button
######## bind the username entry,this binding appear the line inside of entry box if the cursor enter
log_in_username.bind("<Enter>", lambda event: enter_txt_U())

######## create line inside of entry box
usr_name_line = log_in_canvas.create_line((txt_box_gap+((txt_bx.width()//2)-80))-29, 286,((txt_box_gap+((txt_bx.width()//2)-80))-29)+230, 286, fill="#F3F2ED", width=1)

######### create password entry
log_in_password = Entry(log_in_canvas,
                        width=33,
                        show="*",
                        bg="#F3F2ED",
                        font=(tk_font, 10),
                        bd=0)

######## display the password entry
log_password_gap_val = (WINDOW_WIDTH-log_in_password.winfo_width())//2
log_in_password.place(x=(txt_box_gap+((txt_bx.width()//2)-80))-29, y=315)

######## create line inside of entry box
usr_p_line = log_in_canvas.create_line((txt_box_gap+((txt_bx.width()//2)-80))-29, 336, ((txt_box_gap+((txt_bx.width()//2)-80))-29)+230, 336, fill="#F3F2ED", width=1)

######## bind the password entry,this binding appear the line inside of entry box if the cursor enter
log_in_password.bind("<Enter>", lambda event: enter_txt_P())

########################## WELCOCME HOME WINDOW FRAME

con = Image.open('images/icons8-log-in-50.png')
con = ImageTk.PhotoImage(con)

logo_spar = Image.open('images/logo_spar.png')
logo_spar = logo_spar.resize((400, 380))
logo_spar = ImageTk.PhotoImage(logo_spar)

get_start_img = Image.open('images/getstartedbtn.png')
get_start_img = get_start_img.resize((120, 60))
get_start_img = ImageTk.PhotoImage(get_start_img)

wel_bg = Image.open('images/new-.jpg')
wel_bg = wel_bg.resize((WINDOW_WIDTH, WINDOW_HEIGTH))
wel_bg = ImageTk.PhotoImage(wel_bg)

myLogo = Image.open('images/sa.png')
myLogo = myLogo.resize((170, 170))
myLogo = ImageTk.PhotoImage(myLogo)

spar_logo = Image.open('images/spartan.png')
spar_logo = spar_logo.resize((80, 80))
spar_logo = ImageTk.PhotoImage(spar_logo)
#########

home_canvas = Canvas(window, bg=bgcolor)
#gap value
gap_button_start_val = (WINDOW_WIDTH-get_start_img.width())//2
gap_logo_val = (WINDOW_WIDTH-myLogo.width())//2

#welcome background
home_canvas.create_image(WINDOW_WIDTH-(wel_bg.width()//2), WINDOW_HEIGTH-(wel_bg.height()//2), image=wel_bg)

home_canvas.create_image(gap_logo_val+(myLogo.width()//2), 220, image=myLogo)
# home_canvas.create_image(220,100,image=spar_logo)

tagline = f"           A  BatState-U shop that\nleads innovation and transform lives"
gap_tagline_val = (WINDOW_WIDTH-len(tagline))//2
bsu_tagline = home_canvas.create_text(gap_tagline_val+(len(tagline)//2), 330, text="", font=("Bahnschrift Light Condensed", 17), fill="black")
write_text(1)
home_canvas.create_image(30, 30,
                         image=logo_small)

get_started_button = home_canvas.create_image(gap_button_start_val+(get_start_img.width()//2), 495, image=get_start_img)

home_canvas.tag_bind(get_started_button, "<Button>", lambda event: show_log_in_frame())
################################################################

qt = Label(window, height=10, bg='white')
qt.pack(side=TOP, fill=X)
btn_quit = Button(qt, command=lambda: window.quit(), text="X", fg='black', bg='white', font=("monosacpe", 10, 'bold'),
                  relief=FLAT)
btn_quit.pack(side='right', anchor=SW)

if __name__ == '__main__':
    size_check()
    s = ttk.Style()
    s.theme_use('clam')
    restore_db_to_list()
    welcome()
    print(x_position)
    
# Activate the main window
window.mainloop() 

