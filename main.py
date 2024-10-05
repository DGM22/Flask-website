from website import create_app #Importar funcion de init desde dodne se inicialisa la aplicacion 

app = create_app() #Usamos la funcion de init para declarar la variable app con el valor que retorna la funcion

#Usamos un if para saber si se esta corriendo el doc
if __name__ == '__main__':
    app.run(debug=True)

