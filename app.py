from flask import Flask, redirect, url_for, request,render_template
import json
import os
from forms import ContactForm
import pymongo
from pymongo import MongoClient
from flask import flash
import shutil
import socket
import ast
import zipfile

port=5001
ip="127.0.0.1"


cluster = MongoClient("mongodb+srv://SNSTeam:1234@mycluster.wrkyk.mongodb.net/IAS_Project?retryWrites=true&w=majority")
 
db = cluster["IAS_Project"]
admin_info = db["admin_info"]
user_info = db["user_info"]
deploy_info = db["deployment_info"]

app = Flask(__name__, template_folder='template')
app.secret_key = 'development key'

#--------------------------------------------------------------------------------------------------------------------

@app.route('/register_success1')
def register_success1():
   flash('User Already Exist', 'error')
   return render_template('login.html')
   #return redirect('http://localhost:5000/login')

@app.route('/register_success2')
def register_success2():
   flash('User created successfully', 'error')
   return render_template('login.html')
   #return redirect("http://localhost:5000/login")

@app.route('/login_error1')
def login_error1():
   flash("No such id exists","error")
   #return redirect('http://localhost:5000/register')
   return render_template('register.html')

@app.route('/login_error2')
def login_error2():
   flash("Wrong password","error")
   #return redirect('http://localhost:5000/login')
   return render_template('login.html')

@app.route('/login_success1')
def login_success1():
   #flash("No such id exists","error")
   #return redirect('http://localhost:5000/admin')
   return render_template('admin.html')


@app.route('/login_success2')
def login_success2():
   #flash("No such id exists","error")
   return redirect('http://localhost:5000/user')

@app.route('/admin_success1')
def admin_success1():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success2')
def admin_success2():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success3')
def admin_success3():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success4')
def admin_success4():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/admin_success5')
def admin_success5():
   #flash("No such id exists","error")
   return render_template('admin.html')

@app.route('/user_success1')
def user_success1():
   #flash("No such id exists","error")
   #return render_template('admin.html')
   return redirect('http://localhost:5000/user')
#-------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------/login--------------------------------------------------------------------
@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      #print("Hello")
      user = request.form['uid']
      pswd = request.form['pswd']
      types = request.form['user_type']
      print(user,pswd,types)
      if types == "Application Admin":
         
         results = admin_info.find({"_id":user})
         flag=0
         for mp in results:
            if (flag==1 or flag==2):
               break
            if (user==mp["_id"]):
               flag=1
               if pswd==mp["password"]:
                  flag=2
                  break


         if flag==0:
            print("No such id exists")
            return redirect(url_for('login_error1'))


            
         elif flag==2:
            print("__________________Welcome "+user+"__________________")
            return redirect(url_for('login_success1'))
            
         else:
            print("Wrong password")
            return redirect(url_for('login_error2'))
      
      
      else:
         print(2)
         results = user_info.find({"_id":user})         
         flag=0
         for mp in results:
            if (flag==1 or flag==2):
               break
            if (user==mp["_id"]):
               flag=1
               if pswd==mp["password"]:
                  flag=2
                  break

         if flag==0:
            print("No such id exists")
            return redirect(url_for('login_error1'))
         elif flag==2:
            print("__________________Welcome "+user+"__________________")
            return redirect(url_for('login_success2'))
         else:
            print("Wrong password")
            return redirect(url_for('login_error2'))
#------------------------------------------------------------------------------------------------------------------------------




#----------------------------------------------------------/register--------------------------------------------------------------
@app.route('/register',methods = ['POST', 'GET'])
def register():
   if request.method == 'POST':
      print("Hello")
      user = request.form['uid']
      pswd = request.form['pswd']
      types = request.form['user_type']
      print(user,pswd,types)
      if types == "Application Admin":
         print(1)
         mp={user:pswd}
         results = admin_info.find({"_id":user})
         flag=0
         for mp in results:
            if (user==mp["_id"]):
               flag=1

         if flag==1:
            print("User Already exists")
            #flash('User Already Exist', 'error')
            #return render_template('login.html')
            return redirect(url_for('register_success1'))
            
         else:
            admin_info.insert_one( { "_id": user, "password": pswd } )
            print("User created successfully")
            #flash('User created successfully', 'success')
            #return render_template('login.html')
            return redirect(url_for('register_success2'))
            
      else:
         print(2)
         mp={user:pswd}
            
         results = user_info.find({"_id":user})
         flag=0
         for mp in results:
            if (user==mp["_id"]):
               flag=1

         if flag==1:
            print("User Already exists")
            #flash('User Already Exist')
            #return render_template('login.html')
            return redirect(url_for('register_success1'))
         else:
            user_info.insert_one( { "_id": user, "password": pswd } )
            print("User created successfully")
            #flash('User created successfully')
            #return render_template('login.html')
            return redirect(url_for('register_success2'))
      

#------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------/admin---------------------------------------------------------------
app.config['Files_upload']="/home/ayush/IIITH/SEM2/IAS/Project/Files_upload"

@app.route('/admin',methods=['POST','GET'])
def admin():
   if request.method == 'POST':

      if request.form['admin_option'] == "Install The Sensor Class (Sensor Catalogue)":
         #print("1")
         t=request.files['myfile']
         print(t)
         #return redirect(request.url)
         fname=request.files['myfile'].filename
         print(fname)
         t.save(os.path.join(app.config["Files_upload"],t.filename))
         #res=t.read()
         path=app.config['Files_upload']+"/"+fname
         print(path)
         f=open(path)
         data=json.load(f)
         print(data,type (data))

         # string me convert krke bhej do socket programming ke through
         #------------------------socket programming---------------------------------

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="admin"
         s+="*"
         s+="1"
         s+="*"
         s+=str(data)
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         res=res.replace("'",'"')
         res=json.loads(res) #dict
         print(res["msg"])
         m=res["msg"]
         flash(m,"error")
         clientfd.close()
         return redirect(url_for('admin_success1'))

         #------------------------socket programming khtm-------------------------------------------


      elif request.form['admin_option'] == "Install The Sensor Instance":
         #print("2")
         t=request.files['myfile']
         print(t)
         #return redirect(request.url)
         fname=request.files['myfile'].filename
         print(fname)
         t.save(os.path.join(app.config["Files_upload"],t.filename))
         #res=t.read()
         path=app.config['Files_upload']+"/"+fname
         print(path)
         f=open(path)
         data=json.load(f)
         print(data,type (data))

         # string me convert krke bhej do socket programming ke through
         #------------------------socket programming---------------------------------

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="admin"
         s+="*"
         s+="2"
         s+="*"
         s+=str(data)
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         res=res.replace("'",'"')
         lst=ast.literal_eval(res)
         #print(lst)
         for i in range(len(lst)):
            #print(type(lst[i]))
            t=json.dumps(lst[i])
            #print(t)
            t=json.loads(t)
            #print(t)
            #print(type(t))
            a=t["msg"]
            #b=t['msg']
            #print(a)
            k=i+1
            m=""
            m+="For instance "
            m+=str(k)
            m+=" --> "
            m+=a
            flash(m,"error")
            print("For instance "+str(k)+" --> "+a)
         print()
         #flash(m,"error")
         clientfd.close()
         return redirect(url_for('admin_success2'))

         #------------------------socket programming khtm-------------------------------------------


      elif request.form['admin_option'] == "Upload The Application":
         print("3")
         t=request.files['myfile']
         print(t)
         #return redirect(request.url)
         fname=request.files['myfile'].filename
         print(fname)
         t.save(os.path.join(app.config["Files_upload"],t.filename))
         t=fname.split(".")
         #path=app.config['Files_upload']+"/"+t[0]
         path=app.config['Files_upload']
         fpath=app.config['Files_upload']+"/"+fname
         print(fpath)
         print("************")
         print(path)
         path_to_zip_file=fpath
         with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(path)

         #shutil.unpack_archive(fpath,path,"zip")
         curr_loc=app.config["Files_upload"]+"/"+t[0]
         for root, dirs, f in os.walk(curr_loc):
            for filename in f:
               if "json" in filename:
                  config_file=filename
                  break
         config_path=curr_loc+"/"+config_file
         fd=open(config_path)
         data=json.load(fd)
         print(data)

         #------------------------socket programming---------------------------------

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="admin"
         s+="*"
         s+="3"
         s+="*"
         s+=str(data)
         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         clientfd.close()
         lst=ast.literal_eval(res)

         if False not in lst:
            #s+="The Application is deployed"
            try:
               deploy_info.insert_one( { "_id": t[0]} )
               s=""
               s+="The Application "+str(t[0])+" is deployed"
               flash(s,"error")
               return redirect(url_for('admin_success3'))
   
            except:
               s=""
               s+="The Application "+str(t[0])+" is already deployed"
               flash(s,"error")
               return redirect(url_for('admin_success4'))

         else:
            s=""
            s+="The Application cannot be deployed because some of the sensors are not installed"
            flash(s,"error")
            return redirect(url_for('admin_success5'))
         
         
         

         #------------------------socket programming khtm-------------------------------------------
      

#-------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------/user-----------------------------------------------------------------
@app.route('/user',methods=['POST','GET'])
def user():
   form=ContactForm()
   if request.method == "POST":
      if request.method == 'GET':
         return render_template('user.html', form = form)
      else:
         #print(23)
         selected_app=form.application_option.data
         print(selected_app)
         t1=request.files['myfile1']
         print(t1)
         #return redirect(request.url)
         fname1=request.files['myfile1'].filename
         print(fname1)
         t1.save(os.path.join(app.config["Files_upload"],t1.filename))
         #res=t.read()
         path1=app.config['Files_upload']+"/"+fname1
         print(path1)
         f1=open(path1)
         data1=json.load(f1)
         print(data1,type (data1))

         t2=request.files['myfile2']
         print(t2)
         #return redirect(request.url)
         fname2=request.files['myfile2'].filename
         print(fname2)
         t2.save(os.path.join(app.config["Files_upload"],t2.filename))
         #res=t.read()
         path2=app.config['Files_upload']+"/"+fname2
         print(path2)
         f2=open(path2)
         data2=json.load(f2)
         print(data2,type (data2))

         #------------------------socket programming---------------------------------

 

         clientfd=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         clientfd.connect((ip,port))
         s="app"
         s+="*"
         s+="user"
         s+="*"
         s+=str(data1) #kumal1
         s+="*"
         s+=str(data2) #archit
         s+="*"
         s+=selected_app
         s+="*"

         curr_loc=app.config["Files_upload"]
         curr_loc+="/"
         curr_loc+=selected_app
         for root, dirs, f in os.walk(curr_loc):
            for filename in f:
               if ".py" in filename:
                  py_file=filename
                  break
         f=open(curr_loc+"/"+py_file)
         content=f.read()
         s+=str(content)

         clientfd.sendall(s.encode())
         res=clientfd.recv(50000).decode()
         #final response recvd
         flash(res,"error")
         return redirect(url_for('user_success1'))

         

 

         #####add while integrate



   elif request.method == "GET":
      return render_template('user.html', form = form)
   return "khtm"
#----------------------------------------------------------------------------------------------------------------------------------



#---------------------------------------------------------/temp----------------------------------------------------------------
@app.route('/temp',methods=['POST','GET'])
def temp():
   if request.method == "POST":
      return "jdgn"

#--------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
   app.run(debug = True)