from flask import Flask # incluimos todo lo necesario para el uso de flask
from flask import render_template, request, redirect, flash, url_for # incluimos para el renderizado de template 
from flaskext.mysql import MySQL #comunica con mysql
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='/static') # creamos la aplicacion 

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='licoriche'
app.config['MYSQL_DATABASE_Db']='estudiantes'
mysql.init_app(app)

# settings
app.secret_key = "mysecretkey"

###--###--ROUTES--###--###
@app.route('/')
def mainpage():
    return render_template('estudiantes/main.html')

@app.route('/acerca')
def acercapage():
    return render_template('estudiantes/acerca.html')

@app.route('/index')
def index():
    sql="SELECT * FROM `estudiantes`.`consultas`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    consultas=cursor.fetchall()
    print(consultas)
    return render_template('estudiantes/index.html',consultas=consultas)

@app.route('/respuestas')
def answers():
    sql="SELECT `consultas`.`Consulta`, `consultas`.`id`, `Respuestas`.`Respuesta`, `Respuestas`.`Nombre` FROM `estudiantes`.`consultas` JOIN  `estudiantes`.`Respuestas` ON `consultas`.`id` = `Respuestas`.`id_consulta`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    consultas=cursor.fetchall()
    print(consultas)
    return render_template('estudiantes/respuestas.html',consultas=consultas)

@app.route('/create')
def create():
    return render_template('estudiantes/create.html')

@app.route('/store', methods=['POST'])
def storage():
    if "storechaki" in request.form:
        _nombre=request.form['txtNombre']
        _correo=request.form['txtPosicion']
        _foto=request.form['txtFoto']
        sql="INSERT INTO `estudiantes`.`genes`(`id`, `nombre`,`posicion`,`clasificacion`) VALUES (null,%s,%s,%s);"
        datos=(_nombre,_correo,_foto) 
        conn=mysql.connect()
        cursor=conn.cursor()
        cursor.execute(sql,datos)
        conn.commit()
        return render_template('estudiantes/create1.html')
    elif "condiciones" in request.form:
        try:
            _nombre=request.form['txtNombre']
            _apellido=request.form['txtApellido']
            _correo=request.form['txtCorreo']
            _consulta=request.form['txtConsulta']
            _foto=request.files['txtFoto']
            now=datetime.now()
            tiempo=now.strftime("%Y%H%M%S")
            if _foto.filename !='':
                nuevoNombreFoto=tiempo+_foto.filename
                _foto.save("uploads/"+nuevoNombreFoto)
            sql="INSERT INTO `estudiantes`.`consultas` (`Nombre`, `Apellido`,`Correo`,`Consulta`,`Imagen`) VALUES (%s,%s,%s,%s,%s);"
            datos=(_nombre,_apellido,_correo,_consulta,nuevoNombreFoto)
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sql,datos)
            conn.commit()
            flash('Consulta agregada al foro!')
            return render_template('estudiantes/create.html')
        except UnboundLocalError:
            flash('ATENCION!!!! ----- NO ADJUNTO NINGUNA IMAGEN!')
            return render_template('estudiantes/create.html')
    else:
            _nombre=request.form['txtNombre']
            _apellido=request.form['txtApellido']
            _correo=request.form['txtCorreo']
            _consulta=request.form['txtConsulta']
            sql="INSERT INTO `estudiantes`.`consultas` (`Nombre`, `Apellido`,`Correo`,`Consulta`) VALUES (%s,%s,%s,%s);"
            datos=(_nombre,_apellido,_correo,_consulta)
            conn=mysql.connect()
            cursor=conn.cursor()
            cursor.execute(sql,datos)
            conn.commit()
            flash('Consulta agregada al foro!')
            return render_template('estudiantes/create.html')
    
        
@app.route('/destroy/<int:id>')
def destroy(id):
    sql="DELETE FROM `estudiantes`.`consultas` WHERE id=%s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,(id))
    conn.commit()
    flash('Consulta eliminada!')
    return redirect(url_for('index'))

@app.route('/resp/<int:id>')
def resp(id):
    sql="SELECT * FROM `estudiantes`.`consultas`  WHERE id=%s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,id)
    conn.commit()
    consultas=cursor.fetchall()
    print(consultas)
    return render_template("estudiantes/resp.html", consultas=consultas)

@app.route('/update',  methods=['POST'])     
def update():                             
    _nombre=request.form['txtnombre']
    _respuesta=request.form['txtRespuesta']
    id=request.form['txtPregunta']
    sql="INSERT INTO `estudiantes`.`Respuestas` (`Nombre`,`id_consulta`,`Respuesta`) VALUES (%s,%s,%s);"
    datos=(_nombre,id,_respuesta)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    flash('Respuesta agregada exitosamente!')
    
    return redirect(url_for('index'))


###########GENES
@app.route('/index1')
def index1():
    
    sql="SELECT * FROM `estudiantes`.`genes`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    genes=cursor.fetchall()
    print(genes)
    conn.commit()
    return render_template('estudiantes/index1.html', genes=genes) #renderizar el archivo

@app.route('/create1')
def create1():
    return render_template('estudiantes/create1.html')


@app.route('/destroy1/<int:id>')
def destroy1(id):
   
    sql="DELETE FROM `estudiantes`.`genes` WHERE id=%s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,(id))
    conn.commit()
    
    
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    sql="SELECT * FROM `estudiantes`.`genes`  WHERE id=%s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,id)
    genes=cursor.fetchall()
    conn.commit()
    consultas=cursor.fetchall()
    
    return render_template("estudiantes/edit.html", genes=genes)

@app.route('/update1', methods=['POST'])

def update1():
    _nombre=request.form['txtNombre']
    _correo=request.form['txtPosicion']
    
    id=request.form['txtId']
    sql="UPDATE `estudiantes`.`genes` SET `nombre`=%s , `posicion`=%s WHERE id=%s"
    datos=(_nombre,_correo,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/index1')

if __name__=='__main__':
    app.run(debug=True)