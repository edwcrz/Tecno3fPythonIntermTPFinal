"""
Es el punto de entrada principal para la ejecución de la aplicación cliente. 
Se encarga de instanciar la ventana principal del sistema e 
iniciar el bucle de eventos (Event Loop) de CustomTkinter para mantener la interfaz de usuario activa y responsiva.
"""
from frontend.app import MainWindow 

if __name__ == "__main__": 
    app = MainWindow() 
    app.mainloop() 