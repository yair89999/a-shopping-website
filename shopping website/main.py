from typing_extensions import final
from flask import Flask, redirect,url_for, render_template, request, session, flash
import os,json

from search_algorithm import get_results_algorithm,split_list

if os.getcwd().split("\\")[-1] != "shopping website": # os.getcwd() gets the folder the file runs on
    try:
        os.chdir("shopping website") # change the diractory it works on to discord bot(now it start it from the "games and projects" directory)
    except: # can cause a error if it starts it from the folder
        pass

app = Flask(__name__)
app.secret_key = "shopping website.com 131t5$^~#^&@#"
upload_folder = "static//product pictures//"
users = {} # "username": {password:"password", credit card num:"1234567891234567", items in cart:[], items ordered: [], items selling: [] }
products = {} # username: [{title:"Product name", description: "short product description", price:"1009", "pic path":"static/product pictures/name.png"},{title:"Product name", description: "short product description", price:"1009", "pic path":"static/product pictures/name.png"}]
def reload_users():
    global users
    with open("static/users.json","r") as file:
        data = json.load(file) # load the json file
    for user in data["people"]:
        username = user["username"]
        del user["username"]
        users[username] = user
reload_users()
def save_user(username,password,credit_card): # create a user in the file
    if username in users:
        return False
    else: # can use this username
        # saves in users
        users[username] = {"password":password, "credit card":credit_card, "items in cart":[], "items ordered":[], "items selling":[]}
        # saves in file
        people = []
        for user in users:
            user_dict = {}
            user_dict["username"] = user
            for user_data in users[user].items(): # append every value
                user_dict[user_data[0]] = user_data[1]
            people.append(user_dict)
        people = {"people":people}
        with open("static/users.json","w") as f: # opens the json file
            json.dump(people, f, indent=4) # write to the json file everything(the indent=4 is like the if that it starts 4 space after te other line(change to see))
        return True
def resave_data(username,password,credit_card): # resave the data the user gave(password,credit card) and save it in the file
    try:
        users[username]["credit card"] = credit_card
        users[username]["password"] = password
        people = []
        for user in users:
            user_dict = {}
            user_dict["username"] = user
            for user_data in users[user].items(): # append every value
                user_dict[user_data[0]] = user_data[1]
            people.append(user_dict)
        people = {"people":people}
        with open("static/users.json","w") as f:
            json.dump(people, f, indent=4) # json.jump(what to write, filename, optional)
        return True
    except: return False
def save_all_users():
    people = []
    for user in users:
        user_dict = {}
        user_dict["username"] = user
        for user_data in users[user].items(): # append every value
            user_dict[user_data[0]] = user_data[1]
        people.append(user_dict)
    people = {"people":people}
    with open("static/users.json","w") as f:
        json.dump(people, f, indent=4) # json.jump(what to write, filename, optional)

def reload_products():
    global products
    products = {}
    with open("static/products.json") as file:
        data = json.load(file)
    for product in data["products"]:
        username = product["username"]
        title,description,price,pic_path = product["title"],product["description"],product["price"],product["pic path"]
        try:
            products[username].append({"title":title,"description":description, "price":price, "pic path":pic_path})
        except:
            products[username] = [{"title":title,"description":description, "price":price, "pic path":pic_path}]
reload_products()
def save_product(title,description,price,pic_path): # append a perticular product and saves all
    # username: [{title:"title", description: "short product description", price:"1009", "pic path":"static/product pictures/name.png"}]
    username = session["username"]
    try:
        products[username].append({"title":title,"description":description, "price":price, "pic path":pic_path})
    except:
        products[username] = [{"title":title,"description":description, "price":price, "pic path":pic_path}]
    products_list = []
    for user in products:
        for user_product in products[user]:
            user_dict = {"username":user}
            title,description,price,path = user_product["title"],user_product["description"],user_product["price"],user_product["pic path"]
            user_dict["title"] = title
            user_dict["description"] = description
            user_dict["price"] = price
            user_dict["pic path"] = path
            products_list.append(user_dict)
    products_dict = {"products":products_list}
    with open("static/products.json","w") as file:
        json.dump(products_dict, file, indent=4)
def save_all_products(): # just save every product that in products dict
    products_list = []
    for user in products:
        for user_product in products[user]:
            user_dict = {"username":user}
            title,description,price,path = user_product["title"],user_product["description"],user_product["price"],user_product["pic path"]
            user_dict["title"] = title
            user_dict["description"] = description
            user_dict["price"] = price
            user_dict["pic path"] = path
            products_list.append(user_dict)
    products_dict = {"products":products_list}
    with open("static/products.json","w") as file:
        json.dump(products_dict, file, indent=4)

def return_products_names(): # just open the products.json file and puts everything as a dict like this: product_name:{info}
    with open("static//products.json") as file:
        data = json.load(file)["products"]
    products2 = {}
    for product in data:
        product_name = product["title"]
        del product["title"]
        products2[product_name] = product
    return products2
"""changing the variable logged(defins in the functions) in the functions: login,create_user,logout
in every other function the logged variable will be T/F by if there is "logged" key in the session(check the functions if you dont understand) """

top_4_products = []
products_saw_rate = {}

for user in products:
    for product in products[user]:
        if len(top_4_products) < 4:
            top_4_products.append(product["title"])
        products_saw_rate[product["title"]] = 0
def reload_top4_products_file():
    """opens(the top4 file) and change the list of the top4"""
    global top_4_products
    file = open("static//top4_products.txt","r").read()
    top_4_products = file.split("<~!--!~>")
    print(top_4_products)
reload_top4_products_file()
def reload_products_saw_rate():
    global products_saw_rate
    with open("static//products_saw_rate.json","r") as f:
        data = json.load(f)
    products_saw_rate = data["saws"][0]
    for user in products:
        for product in products[user]:
            if not product["title"] in products_saw_rate:
                products_saw_rate[product["title"]] = 0
reload_products_saw_rate()
def save_products_saw_rate():
    saving = {"saws":[products_saw_rate]}
    with open("static//products_saw_rate.json","w") as f:
        json.dump(saving,f, indent=4)

def save_top4_in_file():
    file = open("static//top4_products.txt","w")
    text = "<~!--!~>".join(top_4_products)
    file.write(text)
def update_top_4():
    # updates the top 4 list
    for product in products_saw_rate:
        rate = products_saw_rate[product] # gets the rate from the products_saw_rate
        for top4_product in top_4_products:
            top4_product_rate = products_saw_rate[top4_product] # gets the rate of the top_4 list product
            if rate > top4_product_rate and not product in top_4_products:
                top_4_products.remove(top4_product)
                top_4_products.append(product)
                break # only the inside loop
    print("top 4 products:",top_4_products)

if len(top_4_products) < 4:
    for user in products:
        for product in products[user]:
            if len(top_4_products) < 4 and not product in top_4_products:
                top_4_products.append(product["title"])
            else:
                break
        if len(top_4_products) == 4:
            break
for product in top_4_products: 
    if product == "": top_4_products.remove("")
if len(top_4_products) < 4:
    for user in products:
        for product in products[user]:
            if len(top_4_products) < 4 and not product in top_4_products:
                top_4_products.append(product["title"])
            else:
                break
        if len(top_4_products) == 4:
            break
print(top_4_products)
save_top4_in_file()


def return_top4_with_info(): # reads the top4 list and returns a list with all of the info about this product(dict for product)
    products_list = []
    for product in top_4_products:
        for user in products:
            for product2 in products[user]:
                if product == product2["title"]:
                    product2["username"] = user
                    products_list.append(product2)
    print(len(products_list))
    return products_list

@app.route("/",methods=["POST","GET"])
@app.route("/home",methods=["POST","GET"])
def home():
    logged,items_in_cart = "F",""
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
            items_in_cart = len(users[session["username"]]["items in cart"])
    if request.method == "POST":
        what_to_search = request.form["what to search"]
        print("searched:",what_to_search)
        if what_to_search == "":
            flash("Text box cannot be empty")
            return render_template("home.html", logged=logged, in_cart=items_in_cart,top4 = return_top4_with_info())
        else: # going to the page
            items_to_show = get_results_algorithm(return_products_names(), what_to_search)
            session["option items"] =  items_to_show=items_to_show
            return redirect(url_for("show_searched_products_options",searched=what_to_search))
    else:
        return render_template("home.html", logged=logged, in_cart=items_in_cart,top4 = return_top4_with_info())


@app.route("/profile",methods=["POST","GET"])
def profile():
    """you can change the user data in the profile"""
    logged = "F"
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
            items_in_cart = len(users[session["username"]]["items in cart"])            
    if logged == "T":
        try:
            user_selling_items = products[session["username"]]
        except: user_selling_items = []

        try:
            items_bought = [] # [{'title': "name", 'description': 'blablabla', 'price': '1,000,000', 'pic path': "path", 'username': 'name'}]
            items_bought_names = users[session["username"]]["items ordered"]
            for user in products:
                user_products = products[user]
                for usr_product in user_products:
                    if usr_product["title"] in items_bought_names:
                        usr_product["username"] = user
                        items_bought.append(usr_product)
        except: items_bought = []
        if request.method == "POST":
            """what can the user change in the profile:  credit card num"""
            try: # if the user searched for something
                what_to_search = request.form["what to search"]
                print("searched:",what_to_search)
                if what_to_search == "":
                    flash("Text box cannot be empty")
                    return render_template("profile.html", logged=logged, in_cart=items_in_cart,  selling_items=user_selling_items,bought_items=items_bought)
                else: # going to the page
                    items_to_show = get_results_algorithm(return_products_names(), what_to_search)
                    session["option items"] =  items_to_show=items_to_show
                    return redirect(url_for("show_searched_products_options",searched=what_to_search))
            except:pass
            username = session["username"]
            # resave the credit card
            past_credit_card,new_credit_card = request.form["past credit card num"],request.form["new credit card num"]
            problem = ""
            if len(past_credit_card) != 16 or len(new_credit_card) != 16: # too short/long
                problem = "Credit card numbers must be 16 long"
            elif past_credit_card != users[username]["credit card"]: # past credit card and the one he putted are not the same
                problem = "Wrong past credit card"
            for number in past_credit_card: # illegal characters
                try: int(number)
                except: 
                    problem = "credit card number has illegal characters"
                    break
            for number in new_credit_card: # illegal characters
                try: int(number)
                except: 
                    problem = "credit card number has illegal characters"
                    break
            if problem == "": # will save+reload the file+dict
                good = resave_data(username,users[username]["password"], new_credit_card) # True = went good, False = error in function
                reload_users()
                if good == False: problem = "Couldn't update the credit card please try again" # there was an error in the function
                elif good == True: problem = "Credit card changed successfully!" # went good
            return render_template("profile.html",logged=logged,user = username, in_cart=items_in_cart, selling_items=user_selling_items,bought_items=items_bought,username=session["username"],   problem=problem)
        else:
            return render_template("profile.html", logged=logged, in_cart=items_in_cart,selling_items=user_selling_items,bought_items=items_bought,username=session["username"])
    else:
        return redirect(url_for("home"))

@app.route("/del product/<product_name>")
def delete_product(product_name):
    try:
        username = session["username"]
    except: return redirect(url_for("home"))
    try:
        for product in products[username]:
            if product["title"] == product_name: # same title
                products[username].remove(product) # removes product from user products list that in products dict
                try:
                    os.remove("static/"+product["pic path"]) # removes product pic from PC
                except: pass
                for user in users:
                    in_cart = users[user]["items in cart"]
                    bought = users[user]["items ordered"]
                    if product["title"] in in_cart:
                        in_cart.remove(product["title"])
                        users[user]["items in cart"] = in_cart
                    if product["title"] in bought:
                        bought.remove(product["title"])
                        users[user]["items ordered"] = bought
                save_all_users()
                reload_users()
        with open("static//top4_products.txt","w") as f:
            f.write("")
        del products_saw_rate[product_name]
        save_products_saw_rate()
        reload_products_saw_rate()
        global top_4_products
        top_4_products = []
        reload_top4_products_file()
        if len(top_4_products) < 4:
            for user in products:
                for product in products[user]:
                    if len(top_4_products) < 4 and not product in top_4_products:
                        top_4_products.append(product["title"])
                    else:
                        break
                if len(top_4_products) == 4:
                    break
        for product in top_4_products: 
            if product == "": top_4_products.remove("")
        if len(top_4_products) < 4:
            for user in products:
                for product in products[user]:
                    if len(top_4_products) < 4 and not product in top_4_products:
                        top_4_products.append(product["title"])
                    else:
                        break
                if len(top_4_products) == 4:
                    break
        save_top4_in_file()
    except: flash("You can't delete a product that not yours") # will show this below the search textbox
    save_all_products()
    reload_products()
    return redirect(url_for("profile"))


@app.route("/my cart",methods=["POST","GET"])
def my_cart():
    logged = "F"
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
            items_in_cart = len(users[session["username"]]["items in cart"])
    else:
        return redirect(url_for("home"))
            
    if logged == "T":
        user_cart = [] # [[title,description,price,pic path],  [title,description,price,pic path],  [title,description,price,pic path]]
        for product in users[session["username"]]["items in cart"]:
            product_name = product
            appended = False
            for username in products:
                for product2 in products[username]:
                    if product2["title"] == product_name:
                        description,price,pic_path = product2["description"], product2["price"],product2["pic path"]
                        user_cart.append({"title":product_name,"description":description,"price":price,"pic path":pic_path})
                        appended = True
                        break
                if appended==True:break

        if request.method == "POST":
            try:
                what_to_search = request.form["what to search"]
                print("searched:",what_to_search)
                if what_to_search == "":
                    flash("Text box cannot be empty")
                    return render_template("my cart.html", logged=logged, in_cart=items_in_cart,  cart=user_cart)
                else: # going to the page
                    items_to_show = get_results_algorithm(return_products_names(), what_to_search)
                    session["option items"] =  items_to_show=items_to_show
                    return redirect(url_for("show_searched_products_options",searched=what_to_search))
            except:pass
            
        else:
            return render_template("my cart.html", logged=logged, in_cart=items_in_cart,  cart=user_cart)
    else:
        return redirect(url_for("home"))

@app.route("/remove/<product_name>")
def remove_product(product_name): # removes the product from cart and return to my cart page
    try:
        users[session["username"]]["items in cart"].remove(product_name)
        save_all_users()
        reload_users()
        return redirect(url_for("my_cart"))
    except:
        return redirect(url_for("home"))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {"jpg","png"}
illegal_signs_in_price = ["..",",,",".,",",."] # using to check for illegal characters in the price
illegal_characters = """abcdefghijklmnopqrstuvwxyz:;!@#$%^&*()_-=+[]{}\|""''/?`~""" # using to check for illegal characters in the price
illegal_start_characters = ".," # using to check for illegal characters in the price
def get_files():
    files = []
    for (dirpath, dirnames, filenames) in os.walk("static/product pictures"):
        files.extend(filenames)
        break
    return files
@app.route("/upload product",methods=["POST","GET"])
def upload_product():
    print(products)
    logged = "F"
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
            items_in_cart = len(users[session["username"]]["items in cart"])
            
    if logged == "T":
        if request.method == "POST":
            try:
                what_to_search = request.form["what to search"]
                print("searched:",what_to_search)
                if what_to_search == "":
                    flash("Text box cannot be empty")
                    return render_template("upload product.html", logged=logged, in_cart=items_in_cart)
                else: # going to the page
                    items_to_show = get_results_algorithm(return_products_names(), what_to_search)
                    session["option items"] =  items_to_show=items_to_show
                    return redirect(url_for("show_searched_products_options",searched=what_to_search))
            except:pass

            # get text+check text
            problem = ""
            title = request.form["title"]
            description = request.form["description"]
            price = request.form["price"]
            info = [title,description,price]
            if "" in info:
                problem = "One or more textboxes are empty"
            
            if len(title) == 0 or len(description) == 0 or len(price) == 0:
                problem = "You didnt fill up one or more textboxes"
            if problem == "": # check for mistakes/illegal characters in everything
                # illegal characters: price
                for illegal in illegal_signs_in_price:
                    if illegal in price:
                        problem = "price can not have " + illegal + " in it"
                        break
                for character in price:
                    if character in illegal_characters:
                        problem = "Price has illegal character"
                        break
                if price[0] in illegal_start_characters:
                    problem = "Price has illegal start character"
                # 

            # get file+check file
            flash_msg = ""
            file_path = ""
            if problem == "": # if there wasnt any problems at the text it will check for problems in the file(dont have a reason to check before(waste of time))
                try:
                    if "file" in request.files: # if selected a file
                        file = request.files["file"] # gets the file
                        if allowed_file(file.filename) == True and file.filename != "":
                            file.filename = ".".join([title,file.filename.split(".")[1]]) # change the filename to the title string+pic type
                            if file.filename in get_files():
                                problem = "That product name(title) is catch, please choose other title/name"
                            else:
                                file.save(os.path.join(upload_folder, file.filename)) # saves the file in the current user directory
                                file_path = "product pictures//" + file.filename
                        elif file.filename == "":
                            return render_template("upload product.html", flash_msg="No file was selected" , logged=logged, in_cart=items_in_cart,  title=title,description=description,price=price)
                        else: 
                            return render_template("upload product.html", flash_msg="Can only upload jpg/png pictures" , logged=logged, in_cart=items_in_cart,  title=title,description=description,price=price)
                    else: # if just pressed submit without uploading
                        flash_msg = "No file was selected"
                except: 
                    flash_msg = "No file was selected"
                    return render_template("upload product.html", flash_msg=flash_msg , logged=logged, in_cart=items_in_cart,  title=title,description=description,price=price)
            
            if problem == "": 
                # saves everything
                # save_product(title,description,price,pic_path)
                save_product(title,description,price,file_path)
                reload_products()
                problem = "Product uploaded"
                products_saw_rate[title] = 0
                title,description,price = "","",""
            return render_template("upload product.html", flash_msg=flash_msg , logged=logged, in_cart=items_in_cart,  problem=problem,title=title,description=description,price=price)
        else:
            return render_template("upload product.html", logged=logged, in_cart=items_in_cart)
    else:
        return redirect(url_for("home"))

@app.route("/search options/<searched>",methods=["POST","GET"])
def show_searched_products_options(searched):
    logged,items_in_cart = "F",""
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
            items_in_cart = len(users[session["username"]]["items in cart"])
    try:
        session["option items"]
    except:
        return redirect(url_for("home"))
    if request.method == "POST":
        what_to_search = request.form["what to search"]
        print("searched:",what_to_search)
        if what_to_search == "":
            flash("Text box cannot be empty")
            products_options = session["option items"]
            final_products_options = []
            for products_list in products_options:
                for product in products_list: # goes over the 4 long lists
                    for username in products:
                        for product_dict in products[username]:
                            if product_dict["title"] == product: # same name
                                product_dict["username"] = username
                                final_products_options.append(product_dict)
            final_products_options = split_list(final_products_options,4)
            print(final_products_options)
            return render_template("show products options.html", searched=searched,items_to_show=final_products_options,  logged=logged, in_cart=items_in_cart)
        
        else: # going to the page
            items_to_show = get_results_algorithm(return_products_names(), what_to_search)
            session["option items"] =  items_to_show=items_to_show
            return redirect(url_for("show_searched_products_options",searched=what_to_search))
    else:
        products_options = session["option items"]
        final_products_options = []
        for products_list in products_options:
            for product in products_list: # goes over the 4 long lists
                for username in products:
                    for product_dict in products[username]:
                        if product_dict["title"] == product: # same name
                            product_dict["username"] = username
                            final_products_options.append(product_dict)
        
        final_products_options = split_list(final_products_options,4)
        print(final_products_options)
        return render_template("show products options.html", searched=searched,items_to_show=final_products_options,  logged=logged, in_cart=items_in_cart)


@app.route("/product/<product_name>",methods=["POST","GET"])
def show_product(product_name):
    if not product_name in products_saw_rate:
        return redirect(url_for("home"))
    
    products_saw_rate[product_name] += 1
    update_top_4()
    save_top4_in_file()
    reload_top4_products_file()
    save_products_saw_rate()
    reload_products_saw_rate()
    
    logged = "F"
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
            items_in_cart = len(users[session["username"]]["items in cart"])
    else:
        items_in_cart = 0
    product_dict = {}
    for user in products: # gets the product
        user_products = products[user]
        for product in user_products:
            if product_name == product["title"]:
                product_dict = product
                product_dict["username"] = user
                break
        if product_dict != {}: break

    if request.method == "POST":
            try:
                what_to_search = request.form["what to search"]
                print("searched:",what_to_search)
                if what_to_search == "":
                    flash("Text box cannot be empty")
                    return render_template("show product.html",product=product_dict, logged=logged, in_cart=items_in_cart)
                else: # going to the page
                    items_to_show = get_results_algorithm(return_products_names(), what_to_search)
                    session["option items"] =  items_to_show=items_to_show
                    return redirect(url_for("show_searched_products_options",searched=what_to_search))
            except:pass
            return render_template("show product.html",product=product_dict, logged=logged, in_cart=items_in_cart)
    else:
        return render_template("show product.html",product=product_dict, logged=logged, in_cart=items_in_cart)

@app.route("/add/<product_name>", methods=["POST","GET"])
def add_product(product_name): # append to the list the item(if dont have it in cart) 
    # add product function does not show anything on the screen its just a backend URL function
    if "logged" in session:
        pass
    else:
        return redirect(url_for("login"))
    product_dict = {}
    for user in products: # gets the product
        user_products = products[user]
        for product in user_products:
            if product_name == product["title"]:
                product_dict = product
                product_dict["username"] = user
                break
        if product_dict != {}: break

    if not product_name in users[session["username"]]["items in cart"]: # if the user don't have this product in his cart
        users[session["username"]]["items in cart"].append(product_name)
    save_all_users()
    reload_users()
    flash("Product added")
    return redirect(url_for("show_product",product_name=product_name))

@app.route("/buy now/<product_name>")
def buy_now(product_name):
    try:
        username = session["username"]
        if not product_name in users[username]["items ordered"]:
            users[username]["items ordered"].append(product_name)
        save_all_users()
        reload_users()
        flash("product is on the way")
        return redirect(url_for("show_product", product_name=product_name))
    except:
        return redirect(url_for("login"))
@app.route("/buy all")
def buy_all():
    try:
        username = session["username"]
        for product_name in users[username]["items in cart"]:
            if not product_name in users[username]["items ordered"]:
                users[username]["items ordered"].append(product_name)
        users[username]["items in cart"] = []
        save_all_users()
        reload_users()
        flash("products are on the way")
        return redirect(url_for("my_cart"))
    except:
        return redirect(url_for("home"))

@app.route("/login", methods=["POST","GET"])
def login():
    logged = "F"
    if "logged" in session:
        if session["logged"] == True:
            return redirect(url_for("home"))
    if request.method == "POST":
        try:
            what_to_search = request.form["what to search"]
            print("searched:",what_to_search)
            if what_to_search == "":
                flash("Text box cannot be empty")
                return render_template("login.html", logged=logged,problem="")
            else: # going to the page
                return render_template("login.html", logged=logged,problem="")
        except:pass
        username = request.form["username"]
        password = request.form["password"]
        problem = ""
        if username == "" and password == "": problem = "You didnt fill up the username and password!"
        elif username == "": problem = "Username textbox can not be empty!"
        elif password == "": problem = "Password textbox can not be empty!"
        try:
            if users[username]["password"] == password: # login successfully
                session["logged"] = True
                session["username"] = username
                return redirect(url_for("home"))
            else:
                problem = "Wrong username/password"
        except: problem = "Wrong username/password" # got error cause the username is not in the dict
        print(problem)
        if problem != "":
            return render_template("login.html", logged=logged,problem=problem)
        return redirect(url_for("login"))
    else:
        return render_template("login.html", logged=logged)
@app.route("/create user", methods=["POST","GET"])
def create_user():
    logged = "F"
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
    if request.method == "POST":
        problem = ""
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm password"]
        credit_card_num = request.form["credit card num"]
        if username == "" or password == "" or confirm_password == "" or credit_card_num == "": # if one of the textboxes are empty
            problem = "Username/Password/Credit card num is empty"
        elif "," in username or "," in password or "," in confirm_password: # if there is "," in the username/password/password(confirm)
            problem = "Username/password can't contain ,"
        elif password != confirm_password: # password not the same as password(confirm)
            problem = "Password and password(confirm) are not the same"
        elif len(credit_card_num) != 16: # credit_card_num long is not 16 (credit card num must be 16)
            problem = "credit card number must be 16 long"
        for num in credit_card_num: # if one of the characters in the credit card num is not a number
            try: int(num)
            except: 
                problem = "credit card number is incorrect"
                break
        if problem != "":
            return render_template("create user.html", logged=logged, problem=problem)
        else: # if everything is good so he logged in and resume to the home page
            good = save_user(username,password,credit_card_num) # return False if the username is taken
            reload_users() # reload the users dict
            if good == False: # return False if the username is taken
                return render_template("create user.html", logged=logged, problem="username is taken")
            else: # everything is good
                session["logged"] = True
                session["username"] = username
                return redirect(url_for("home"))
    else:
        return render_template("create user.html", logged=logged)

@app.route("/logout")
def logout():
    """removes from session and return to home page"""
    session.pop("logged")
    session.pop("username")
    return redirect(url_for("home"))

@app.errorhandler(404) # 404 page url
def error_404(e): # 404 page
    logged = "F"
    items_in_cart = ""
    if "logged" in session:
        if session["logged"] == True:
            logged = "T"
            items_in_cart = len(users[session["username"]]["items in cart"])
    print("p",items_in_cart,"P")
    return render_template("404page.html",logged=logged,in_cart=items_in_cart),404


app.run(debug=True)