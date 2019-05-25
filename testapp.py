from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
from doanhnghiep_database import user_collection
from single_database import canhan_collection
from bson.objectid import ObjectId

app.config["SECRET_KEY"] = "dasd2e12h3h12312i1hjmkb"

@app.route('/')
def index():
  return "Hello"

@app.route('/homepage')                                             
def test():
  return render_template("homepage.html")

@app.route("/doanhnghiep", methods = ["GET","POST"])                  # thêm homepage
def doanhnghiep():
  if "logged" in session:
    if session["logged"] == True:
      return redirect ("/yourspace")
    else:
      if request.method == "GET":
        return render_template("login_doanhnghiep.html")
      if request.method == "POST":
        form = request.form 
        username = form["username"]
        password = form["password"]                                      # thêm rating
        user_type = form["type"]
        if user_type == "Register":  
          user_space_name = form["space_name"]
          user_contact_number = form["contact_number"]                          # space_name phải khác nhau
          user_street_number = form ["street_number"]                    # autofill required input 
          user_street = form ["street"]
          user_district = form ["district"]
          user_detail = form ["detail"]
          user_price = form ["price"]          
          new_user = user_collection.find_one({ "username" : username })
          if new_user is not None:
            return redirect("/doanhnghiep")  #can lam noti ở đây hoăc dòng: chữ trùng tên ở html
          else:
            new_user = {
              "username" : username,
              "password" : password,
              "space_name" : user_space_name,
              "contact_number" : user_contact_number,
              "address" : {
                "street_number" : user_street_number,
                "street" : user_street,
                "district" : user_district,
              },
              "detail" : user_detail,
              "price" : user_price,
            }
            user_collection.insert_one(new_user)
            session["_id"] = str(new_user["_id"])
            session["logged"] = True
            return redirect ("/yourspace")
        if user_type == "Sign In":
          current_user = user_collection.find_one({ "username": username })
          if current_user is None:
            return redirect("/doanhnghiep")  #can lam noti ở đây hoăc dòng: chữ trùng tên ở html
          else:
            if current_user["password"] == password:
              session["_id"] = str(current_user["_id"])
              session["logged"] = True
              return redirect("/yourspace")
            else:
              return redirect("/doanhnghiep")  #can lam noti Ở đây hoặc dòng: đã nhập sai pass
  else:
    session["logged"] = False
    return render_template("login_doanhnghiep.html")

@app.route("/yourspace", methods = ["GET","POST"]) 
def your_space():
  user_list = user_collection.find_one({ "_id" : ObjectId(session["_id"]) })
  if request.method == "GET":
    return render_template ("your_space.html",user_list = user_list)
  elif request.method == "POST":
    form = request.form 
    new_value = { "$set": {
      "space_name" : form["space_name"],
      "contact_number" : form["contact_number"],
      "address" : {
        "street_number" : form["street_number"],
        "street" : form["street"],
        "district" : form["district"],
      },
      "detail" : form["detail"],
      "price" : form["price"], 
    } }
    user_collection.update_one(user_list,new_value)
    return render_template ("your_space.html",user_list = user_list)
@app.route("/canhan", methods = ["GET","POST"])
def canhan():
  if "logged" in session:
    if session["logged"] == True:
      return redirect ("/userspace")
    else:
      if request.method == "GET":
        return render_template("login_canhan.html")
      if request.method == "POST":
        form = request.form 
        username = form["username"]
        password = form["password"]
        user_type = form["type"]
        if user_type == "Register":    
          user_full_name = form["full_name"]
          user_age = form ["age"]
          user_district = form ["district"]
          user_salary = form ["salary"]        
          new_user = canhan_collection.find_one({ "username" : username })
          if new_user is not None:
            return redirect("/canhan")  
          else:
            new_user = {
              "username" : username,
              "password" : password,
              "full_name" : user_full_name,
              "age" : user_age,
              "district" : user_district,
              "salary" : user_salary,
            }
            canhan_collection.insert_one(new_user)
            session["_id"] = str(new_user["_id"])
            session["logged"] = True
            return redirect ("/userspace")
        if user_type == "Sign In":
          current_user = canhan_collection.find_one({ "username": username })
          if current_user is None:
            return redirect("/canhan")  
          else:
            if current_user["password"] == password:
              session["_id"] = str(current_user["_id"])
              session["logged"] = True
              return redirect("/userspace")
            else:
              return redirect("/canhan")  
  else:
    session["logged"] = False
    return render_template("login_canhan.html")

@app.route ("/userspace", methods = ["GET","POST"])
def userspace():
  user_list = canhan_collection.find_one({ "_id" : ObjectId(session["_id"]) })
  doanhnghiep_list = user_collection.find_one({ "address.district" : user_list["district"] })
  if request.method == "GET":
    search_result = [{"space_name" : "Không có kết quả" }]
    return render_template ("user_space.html",user_list = user_list,doanhnghiep_list = doanhnghiep_list, search_result = search_result)
  if request.method == "POST":
    form = request.form 
    search_name = form["search_by_name"]
    search_result = user_collection.find({ "$text": { "$search": search_name } })  
    if search_result == None:      # kiểm tra vì nếu không find ra gì không phải là None (chỉ đúng với find_one)
      search_result = [{"space_name" : "Không có kết quả" }]
      return render_template ("user_space.html",user_list = user_list,doanhnghiep_list = doanhnghiep_list,search_result = search_result)
    else:
      return render_template ("user_space.html",user_list = user_list,doanhnghiep_list = doanhnghiep_list,search_result = search_result)

@app.route("/userspace/search_result", methods = ["POST"])
def search_result():
  form = request.form 
  filter_district = form["district"]
  filter_price = form["price"]
  final_result = []
  def district_result():
    if filter_district == "No result":
      district_result =[]
    else:
      district_result = user_collection.find({ "address.district" : filter_district })
    return district_result
  def price_result():
    all_cospace = user_collection.find()
    price_result = []
    if filter_price == "No result":
      price_result.append({ "space_name" : "Không có kết quả" })
    if filter_price == "Dưới 50000":
      for cospace in all_cospace:
        if int(cospace["price"]) < 50000:
          price_result.append(cospace)
    if filter_price == "Từ 50000 tới 70000":
      for cospace in all_cospace:
        if 50000 <= int(cospace["price"]) <= 70000:
          price_result.append(cospace)
    if filter_price == "Trên 70000":
      for cospace in all_cospace:
        if int(cospace["price"]) > 70000:
          price_result.append(cospace)
    return price_result
  district_result = district_result()
  price_result = price_result()
  if district_result == []: # theem district_result == None
    final_result = price_result
  else:
    if price_result == [{ "space_name" : "Không có kết quả" }]:
      final_result = district_result
    elif price_result == []:
      pass
    else:
      for item in district_result:
        if item in price_result:
          final_result.append(item)
  if final_result == []:
    final_result.append({ "space_name" : "Không có kết quả" })

  return render_template("search_result.html",final_result = final_result)

@app.route ("/log_out")
def log_out():
  if "logged" in session:
    session["logged"] = False
    return render_template ("homepage.html")

@app.route ("/call_center", methods = ["POST"])
def call_center():
  form = request.form 
  space_name = form["choice"]
  return render_template("call_center.html", space_name = space_name)
  
if __name__ == '__main__':
  app.run(debug=True)
 
