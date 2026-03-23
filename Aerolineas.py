import os
import pickle
import getpass
from datetime import datetime, date
import random
#admin@ventaspasajes.com
#admin123

# STRING: estado_vuelo,fecha_str,email,clave,tipo,nombre,pais,cod,cod_aero,origen,destino,fecha,hora,mensaje,asiento,col_letra,descuento,fecha_ini,ff,respuesta,entrada,texto,paises_validos,archivo,mensajes,usuario.tipo,usuario.email
# INT: vuelos_act,codigo_nove1,i, j, k, n, m, pos, idx,opc, op, opcion, opcion_menu,intentos, max_intentos,usuario.id, nuevo_usuario.id,admin.id,vuelo.codigo_vuelo,reserva.id, nueva.id,prom_id, pid,fila_num, asiento_num ,total_vuelos, total_pasajes, total_ingresos, total, vendidos, ingreso ,ocupados, reservados, libres, porcentaje,cantidad, cantidades, total_compras,rid (id de reserva).codigo (de vuelo o promoción),max_id, maximo
# FLOAT: precio, nueva.descuento,valor,ingreso,porcentaje
# BOOL: existe,existe, existe_admin, admin_presente,valido, encontrado, encontrado_admin, usuario_encontrado,activo, tiene_reservas, reserva_confirmada, reserva_encontrada,error_asiento, asiento_valido, descuento_valido,error_asiento, asiento_valido, descuento_valido,vuelo_encontrado, vuelo_activo, aerolinea_activa,vuelo.estado == "A" / "B",pais in paises_validos,fecha_valida,seguir,error,encontrado,reservas,promo,encontrada,aprobada
# archivo: usuarios, aerolineas, aerolineas_activas, vuelos, reservas, vuelos_activos,compras,promociones,codigos,nombres,cantidades,datos_de_aerolineas
# clases:Usuario,aerolinea,vuelo,reserva,promocion,novedad


# ==== RUTAS DE ARCHIVOS ====# Se definen las rutas de los archivos de datos
RUTA = "c:\\tp3\\"
if not os.path.exists(RUTA):# nos aseguramos que exista
    os.makedirs(RUTA)

ARCH_USUARIOS = RUTA + "Usuarios.dat" # informacion del usuario
ARCH_AEROLINEAS = RUTA + "aerolineas.dat"# informacion de la aerolinia disponibles
ARCH_VUELOS = RUTA + "Vuelos.dat"  # Renombrado a plural
ARCH_RESERVA = RUTA + "reservas.dat" # reservas realizadas
ARCH_NOVEDADES = RUTA + "novedades.dat"# novedades realizadas
ARCH_PROMOCIONES = RUTA + "promociones.dat"

# ==== DEFINICIÓN DE REGISTROS (CLASES) ====# Se definen las clases para cada tipo de registro
class Usuario:
    def __init__(self):
        self.id = 0
        self.email = ""
        self.clave = ""
        self.tipo = ""
        self.activo = True
        self.telefono = ""

class Aerolinea:
    def __init__(self):
        self.codigo_iata = ""
        self.nombre = ""
        self.pais = ""
        self.activo = True      

# Fila 0‑2 = asientos A, B, C ; índice 3 = pasillo ; 4‑6 = D, E, F
ASIENTOS_FILA = 7    # columnas (A, B, C, pasillo, D, E, F)
ASIENTOS_COLUMNAS = 40  # filas (1-40)

class Vuelo:
    def __init__(self):
        self.codigo_vuelo = 0
        self.cod_aerolinea = ""
        self.origen = ""
        self.destino = ""
        self.fecha = ""   # formato "dd/mm/yyyy"
        self.hora = ""    # formato "HH:MM"
        self.estado = "A"
        self.precio = 0.0
        # Matriz 40 × 7 (columnas), con “pasillo” en j = 3
        self.asientos = [["L"] * ASIENTOS_FILA for _ in range(ASIENTOS_COLUMNAS)]

class Novedad:
    def __init__(self):
        self.id = 0                   # int: Identificador único
        self.texto = " "               # str: Contenido de la novedad
        self.fecha_inicio = " "        # str: Fecha de inicio de vigencia
        self.fecha_fin = " "           # str: Fecha de fin de vigencia
        self.activo = True            # bool: Para baja lógica

class Reserva:
     def __init__(self):
         self.id = 0                   # int: Identificador único
         self.id_usuario = 0           # int: ID del usuario que hizo la reservas
         self.codigo_vuelo = 0         # int: Código del vuelo reservado (unificado a int)
         self.asiento = " "            # str: Asiento reservado (ej. "12A")
         self.estado = " "             # str: 'confirmada', 'cancelada', 'pendiente'
         self.fecha_reserva = ""       # str: Fecha de la reserva (dd/mm/yyyy)

class Promocion:
    def __init__(self):
        self.id = 0
        self.codigo_vuelo = 0
        self.descuento = 0.00
        self.fecha_inicio = " "
        self.fecha_fin = " "
        self.aprobada = False
        self.activo = True

# FUNCIONES DE ARCHIVOS(listo)
def cargar_lista(archivo):
    lista = []
    if not os.path.exists(archivo):
        print(f"Archivo {archivo} no existe. Se creará vacío.")
    else:
        try:
            with open(archivo, "rb") as f:
                datos = pickle.load(f)
                for elem in datos:
                    lista.append(elem)
        except (pickle.UnpicklingError, EOFError, AttributeError, ImportError, IndexError) as e:
            print(f"Error al cargar archivo {archivo}. El archivo puede estar dañado o vacío. {e}")
        except Exception as e:
            print(f"Error inesperado al cargar archivo {archivo}: {e}")
    return lista

def guardar_lista(archivo, lista):
    try:
        with open(archivo, "wb") as f:
            pickle.dump(lista, f)
    except Exception as e:
        print(f"Error al guardar archivo ({archivo}): {e}")

# ==== CREAR ADMIN POR DEFECTO ====(listo)
def crear_admin_por_defecto():
    usuarios = cargar_lista(ARCH_USUARIOS)

    # Validar si la lista de usuarios es válida
    if not isinstance(usuarios, list):
        print("Archivo de usuarios corrupto. Se reiniciará.")
        usuarios = []

    # Verificar si el admin ya existe
    admin_email = "admin@ventaspasajes.com"
    if not any(u.email == admin_email for u in usuarios):
        admin = Usuario()
        admin.id = 0
        admin.email = admin_email
        admin.clave = "admin123"
        admin.tipo = "administrador"
        admin.activo = True
        usuarios.append(admin)
        guardar_lista(ARCH_USUARIOS, usuarios)
        print("Administrador por defecto creado.")
       
# Ejecutar la función
crear_admin_por_defecto()

# ==== AUXILIARES ====(listo)
def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def en_construccion():
    input("🚧 En construcción. Enter para continuar...")
    limpiar()

def validar_numero(mensaje, tipo=int, minimo=None, maximo=None, positivo=False):
    while True:
        entrada = input(mensaje)
        try:
            valor = tipo(entrada)
            if positivo and valor <= 0:
                print("⚠️ El valor debe ser positivo.")
                input("presione enter para continuar...")
                limpiar()
                continue
            if minimo is not None and valor < minimo:
                print(f"⚠️ El valor debe ser mayor o igual a {minimo}.")
                input("presione enter para continuar...")
                limpiar()
                continue
            if maximo is not None and valor > maximo:
                print(f"⚠️ El valor debe ser menor o igual a {maximo}.")
                input("presione enter para continuar...")
                limpiar()
                continue
            return valor
        except ValueError:
            print(f"⚠️ Ingrese un valor {tipo.__name__} válido.")# el tipo es int(entero)

def pedir_fecha_en_rango(mensaje="Ingrese fecha (dd/mm/yyyy): ", desde=None, hasta=None):
    
    #Pide una fecha al usuario, valida formato y, si se indican, que esté entre 'desde' y 'hasta' (inclusive).
    #Retorna la fecha como string en formato dd/mm/yyyy.
    while True:
        fecha = input(mensaje)
        if fecha.strip() == "0":
            print("presionedo 0, salida de la operación.")
            limpiar()
            return None
        try:
            fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
            if desde:
                desde_dt = datetime.strptime(desde, "%d/%m/%Y")
                if fecha_dt < desde_dt:
                    print(f"⚠️ La fecha debe ser igual o posterior a {desde}.")
                    input("presione enter para continuar")
                    limpiar()
                    continue
            if hasta:
                hasta_dt = datetime.strptime(hasta, "%d/%m/%Y")
                if fecha_dt > hasta_dt:
                    print(f"⚠️ La fecha debe ser igual o anterior a {hasta}.")
                    input("presione enter para continuar")
                    limpiar()
                    continue
            return fecha
        except ValueError:
            print("⚠️ Fecha inválida. Use el formato dd/mm/yyyy y asegúrese de que la fecha exista.")
            input("presione enter para continuar")
            limpiar()

def obtener_aerolinea(codigo, aerolineas):
    #Busca una aerolínea por su código IATA.
    #Retorna el objeto Aerolinea si existe y está activa, sino None.
    for a in aerolineas:
        if a.codigo_iata.upper() == codigo.upper() and getattr(a, "activo", True):
            return a
    return None

def validar_hora():
    hora_valida = False
    hora = ""
    while not hora_valida:
        hora = input("Ingrese hora (HH:MM): ")
        if len(hora) == 5 and hora[2] == ':':
            try:
                hh = int(hora[0:2])
                mm = int(hora[3:5])
                if 0 <= hh < 24 and 0 <= mm < 60:
                    hora_valida = True
                else:
                    print("⚠️ Hora inválida. Intente nuevamente.")
                    print("presione enter para continuar")
                    limpiar()
            except ValueError:
                print("⚠️ Formato de hora inválido.")
                input("presione enter para continuar")
                limpiar()
        else:
            print("⚠️ Formato incorrecto. Use HH:MM.")
            input("presione enter para continuar")
            limpiar()
    return hora


#submenus(admin, ceo, usuario) 
def menu_admin():
    opc = 0
    while opc != 5:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Gestión de Aerolíneas")
        print("2. Aprobar/Denegar Promociones")
        print("3. Gestión de Novedades")
        print("4. Reportes")
        print("5. Cerrar sesión y volver al menú principal")

        opc = validar_numero("Seleccione una opción: ", int, 1, 5)

        if opc == 1:
            gestion_aerolineas()
        elif opc == 2:
            en_construccion()
        elif opc == 3:
            en_construccion() 
        elif opc == 4:
            en_construccion()
        elif opc == 5:
            limpiar()
            print(" Cerrando sesión...")
            input("Presione Enter para volver al menú principal...")
        else:
            print(" Opción inválida.")
            input("Presione Enter para continuar...")
            limpiar()

def menu_ceo():
    opc = 0
    while opc != 4:
        print("\n--- MENÚ CEO ---")
        print("1. Gestión de Vuelo")
        print("2. Gestión de Promociones")
        print("3. Reportes")
        print("4. Cerrar sesión y volver al menú principal")
        opc = validar_numero("Seleccione una opción: ", int, 1, 4)
        if opc == 1:
            menu_gestion_vuelos()
        elif opc == 2:
            gestion_promociones()
        elif opc == 3:
            reportes()
        elif opc == 4:
            limpiar()
            print("Cerrando sesión...")
            input("Presione Enter para volver al menú principal...")
        else:
            print("⚠️ Opción inválida.")
            input("Presione Enter para continuar...")
            limpiar()

def menu_usuario(usuario):
    opc = 0
    while opc != 6:
        print("╔════════════════════════════════════╗")
        print("║        🏠  MENÚ USUARIO  🏠        ║")
        print("╚════════════════════════════════════╝\n")
        print("1) Buscar Vuelos ")
        print("2) Buscar Asientos ")
        print("3) Gestionar reservas ")
        print("4) Ver Historial de Compras ")
        print("5) Ver Novedades ")
        print("6) Cerrar sesión ")
        opc = validar_numero("Seleccione una opción: ", int, 1, 6)
        if opc == 1:
            menu_buscar_vuelos()
        elif opc == 2:
            busc_asientos()
        elif opc == 3:
            menu_gestionar_Reserva(usuario)
        elif opc == 4:
            ver_historial_compras(usuario)
        elif opc == 5:
            en_construccion()
        elif opc == 6:
            limpiar()

# ==== ADMIN ====
def gestion_aerolineas():
    opc = 0
    while opc != 4:
        print("\n--- GESTIÓN DE AEROLÍNEAS ---")
        print("1. Alta")
        print("2. Modificación")
        print("3. Baja lógica")
        print("4. Volver")
        opc = validar_numero("Seleccione una opción: ", int, 1, 4)
        aerolineas = cargar_lista(ARCH_AEROLINEAS)
        if opc == 1:
            cod = input("Código IATA: ").upper()
            aero = obtener_aerolinea(cod, aerolineas)
            if aero:
                print("⚠️ Ya existe esa aerolínea.")
                input("Presione Enter para continuar...")
                limpiar()
            else:
                nombre = input("Nombre: ")
                pais = input("País (ej: ARG): ").upper()
                paises_validos = ["ARG", "CHI", "BRA"]
                if pais not in paises_validos:
                    print("⚠️ País inválido. Solo se permiten: ARG, CHI, BRA.")
                    input("Presione Enter para continuar...")
                    limpiar()
                else:
                    a = Aerolinea()
                    a.codigo_iata = cod
                    a.nombre = nombre
                    a.pais = pais
                    a.activo = True
                    aerolineas.append(a)
                    guardar_lista(ARCH_AEROLINEAS, aerolineas)
                    print("Alta realizada.")
                    input("Presione Enter para continuar...")
                    limpiar()
        elif opc == 2:
            cod = input("Código IATA a modificar: ").upper()
            aero = obtener_aerolinea(cod, aerolineas)
            if not aero:
                print("⚠️ No existe una aerolínea activa con ese código.")
                input("Presione Enter para continuar...")
                limpiar()
            else:
                a = aero
                nom = input(f"Nuevo nombre (actual: {a.nombre}): ")
                pais = input(f"Nuevo país (actual: {a.pais}): ").upper()
                paises_validos = ["ARG", "CHI", "BRA"]
                if pais != "" and pais not in paises_validos:
                    print("⚠️ País inválido. Solo se permiten: ARG, CHI, BRA.")
                    input("Presione Enter para continuar...")
                    limpiar()
                else:
                    if nom != "":
                        a.nombre = nom
                    if pais != "":
                        a.pais = pais
                    guardar_lista(ARCH_AEROLINEAS, aerolineas)
                    print("Modificación realizada.")
                    input("Presione Enter para continuar...")
                    limpiar()
        elif opc == 3:
            cod = input("Código IATA a dar de baja: ").upper()
            aero = obtener_aerolinea(cod, aerolineas)
            if not aero:
                print("⚠️ No existe una aerolínea activa con ese código.")
                input("Presione Enter para continuar...")
                limpiar()
            else:
                tiene_reservas = False
                vuelos = cargar_lista(ARCH_VUELOS)
                reservas = cargar_lista(ARCH_RESERVA)
                for v in vuelos:
                    if v.cod_aerolinea == cod and v.estado == "A":
                        for r in reservas:
                            if r.codigo_vuelo == v.codigo_vuelo and r.estado == "confirmada":
                                tiene_reservas = True
                if tiene_reservas:
                    print("No se puede dar de baja la aerolínea porque tiene vuelos con reservas confirmadas.")
                    input("Presione Enter para continuar...")
                    limpiar()
                else:
                    aero.activo = False
                    guardar_lista(ARCH_AEROLINEAS, aerolineas)
                    print("Baja lógica realizada.")
                    input("Presione Enter para continuar...")
                    limpiar()
# ==== CEO ====
# ==== GESTIÓN DE VUELOS====
def menu_gestion_vuelos():
    opc = 0
    while opc != 4:
        print("\n--- MENÚ GESTIÓN DE VUELOS ---")
        print("1. Crear vuelo")
        print("2. Modificar vuelo")
        print("3. Eliminar vuelo")
        print("4. Volver")
        opc = validar_numero("Seleccione una opción: ", int, 1, 4)
        if opc == 1:
            crear_vuelo()
        elif opc == 2:
            modificar_vuelo()
        elif opc == 3:
            eliminar_vuelo()
        elif opc == 4:
            input(" Presione Enter para continuar...")
            limpiar()

def listar_vuelos():
    vuelos = cargar_lista(ARCH_VUELOS)
    print("\n--- Vuelos cargados ---")
    for vuelo in vuelos:
        if vuelo.estado == "A":
            print(f"Código:{vuelo.codigo_vuelo} | Aerolínea:{vuelo.cod_aerolinea} | {vuelo.origen}->{vuelo.destino} {vuelo.fecha} {vuelo.hora} ${vuelo.precio:.2f}")
            

def listar_vuelos_aerolineas():
    vuelos = cargar_lista(ARCH_VUELOS)
    aerolineas = cargar_lista(ARCH_AEROLINEAS)

    codigos = []# lista de códigos IATA
    nombres = []# lista de nombres de aerolíneas
    cantidades = []# lista de cantidades de vuelos
    for a in aerolineas:
        if a.activo:
            codigos.append(a.codigo_iata)#append agrega un elemento al final de la lista
            nombres.append(a.nombre)
            cantidades.append(0)

    fecha_actual = datetime.now()# fecha actual
    for vuelo in vuelos:
        if vuelo.estado == "A":
            try:
                fecha_vuelo = datetime.strptime(vuelo.fecha, "%d/%m/%Y")# convertimos la fecha del vuelo a datetime(fecha_v es fecha vuelo)
            except ValueError:
                continue
            if fecha_vuelo > fecha_actual:
                i = 0
                encontrado = False
                while i < len(codigos) and not encontrado:
                    if codigos[i] == vuelo.cod_aerolinea:
                        cantidades[i] += 1
                        encontrado = True
                    i += 1
    print("\nCantidad de vuelos futuros por aerolínea:")
    for i in range(len(codigos)):
        print(f"Aerolínea: {nombres[i]} ({codigos[i]}) - Vuelos futuros: {cantidades[i]}")

    # Ordenamiento descendente manual (burbuja simple)
    n = len(cantidades)
    for i in range(n-1):
        for j in range(i+1, n):# recorremos desde i+1 hasta el final
            if cantidades[j] > cantidades[i]:
                cantidades[i], cantidades[j] = cantidades[j], cantidades[i]
                codigos[i], codigos[j] = codigos[j], codigos[i]
                nombres[i], nombres[j] = nombres[j], nombres[i]

    print("\n==========================")
    print("REPORTE DE VUELOS VIGENTES POR AEROLÍNEA")
    print("==========================")
    print(f"{'POS':<4} {'AEROLÍNEA':<25} {'VUELOS':<8}")
    print("-------------------------------------------")
    for i in range(len(codigos)):
        print(f"{i:<4} {nombres[i]:<25} {cantidades[i]:<8}")
    print("-------------------------------------------")
    total = sum(cantidades)
    print("Total vuelos vigentes:", total)
    if len(codigos) > 0:
        print("Mayor:", nombres[0], cantidades[0])
        print("Menor:", nombres[-1], cantidades[-1])

def inicializar_asientos_aleatorios(vuelo):
    vuelo.asientos = []# reiniciamos la matriz de asientos
    for _ in range(ASIENTOS_COLUMNAS):  # 40 filas
        fila = []
        for j in range(ASIENTOS_FILA):  # 7 columnas
            if j == 3:
                fila.append("X")  # Pasillo
            else:
                fila.append(random.choice(["L", "R", "O"]))# Asiento Libre, Reservado, Ocupado
        vuelo.asientos.append(fila)# agregamos la fila a la matriz

def crear_vuelo():
    limpiar()
    # Preguntar si quiere ver vuelos cargados
    if input("¿Mostrar vuelos actuales? (s/n): ").lower() == "s":
        listar_vuelos()

    vuelos = cargar_lista(ARCH_VUELOS)
    aerolineas = cargar_lista(ARCH_AEROLINEAS)
    aerolineas_activas = []
    i = 0
    while i < len(aerolineas):
        if aerolineas[i].activo:
            aerolineas_activas.append(aerolineas[i])
        i += 1
    if len(aerolineas_activas) == 0:
        print("No hay aerolíneas activas. No se puede crear un vuelo.")
        input(" Presione Enter para continuar...")
        limpiar()
    else:
        cod_aero = input("Código aerolínea: ").upper()
        aero = obtener_aerolinea(cod_aero, aerolineas)
        if not aero:
            print("Aerolínea no encontrada.")
            input(" Presione Enter para continuar...")
            limpiar()
        else:
            origen = input("Origen: ").upper()
            destino = input("Destino: ").upper()
            fecha = pedir_fecha_en_rango()
            try:
                fecha_dt = datetime.strptime(fecha, "%d/%m/%Y").date()
                hoy = datetime.now().date()
                if fecha_dt <= hoy:
                    print("No se puede crear un vuelo con fecha pasada.")
                    input(" Presione Enter para continuar...")
                    limpiar()
                else:
                    hora = validar_hora()
                    precio = validar_numero("Precio del vuelo: ", float, positivo=True)
                    vuelo = Vuelo()
                    vuelo.cod_aerolinea = cod_aero
                    vuelo.origen = origen
                    vuelo.destino = destino
                    vuelo.fecha = fecha
                    vuelo.hora = hora
                    vuelo.precio = precio
                    vuelo.estado = "A"
                    if len(vuelos) > 0:
                        maximo = vuelos[0].codigo_vuelo
                        j = 0
                        while j < len(vuelos):
                            if vuelos[j].codigo_vuelo > maximo:
                                maximo = vuelos[j].codigo_vuelo
                            j += 1
                        vuelo.codigo_vuelo = maximo + 1
                    else:
                        vuelo.codigo_vuelo = 1
                    inicializar_asientos_aleatorios(vuelo)
                    vuelos.append(vuelo)
                    guardar_lista(ARCH_VUELOS, vuelos)
                    print("Vuelo creado con código", vuelo.codigo_vuelo)
                    listar_vuelos_aerolineas()
            except Exception as e:
                print("Error en la fecha:", e)
                input(" Presione Enter para continuar...")
                limpiar()

def modificar_vuelo():
    mostrar_menu = True  # Bandera para controlar si seguimos con el menú o no

    if input("¿Mostrar vuelos actuales? (s/n): ").lower() == "s":
        listar_vuelos()

    vuelos = cargar_lista(ARCH_VUELOS)

    # Validar código de vuelo
    try:
        cod = int(input("Código de vuelo a modificar: "))
    except Exception:
        print("Código inválido.")
        input("Presione Enter para continuar...")
        limpiar()
        mostrar_menu = False  # No seguimos si el código es inválido

    vuelo = None
    if mostrar_menu:
        i = 0
        while i < len(vuelos) and vuelo is None:
            if vuelos[i].codigo_vuelo == cod:
                vuelo = vuelos[i]
            i += 1

        if vuelo is None:
            print("Vuelo no encontrado.")
            input("Presione Enter para continuar...")
            limpiar()
            mostrar_menu = False

    if mostrar_menu:
        if vuelo.estado == "B":
            resp = input("Este vuelo está dado de baja. ¿Reactivarlo? (s/n): ").lower()
            if resp == "s":
                vuelo.estado = "A"
                print("Vuelo reactivado.")
            else:
                print("No se modifica un vuelo dado de baja.")
                input("Presione Enter para continuar...")
                limpiar()
                mostrar_menu = False

    if mostrar_menu:
        opc = -1  # Inicializamos con un valor distinto de 0
        while opc != 0:
            print("Qué campo desea modificar:")
            print("1) Origen")
            print("2) Destino")
            print("3) Fecha")
            print("4) Hora")
            print("5) Precio")
            print("0) Salir")
            opc = validar_numero("Seleccione una opción: ", int, 0, 5)

            if opc == 1:
                vuelo.origen = input("Nuevo origen: ").upper()
            elif opc == 2:
                vuelo.destino = input("Nuevo destino: ").upper()
            elif opc == 3:
                vuelo.fecha = pedir_fecha_en_rango()
            elif opc == 4:
                vuelo.hora = validar_hora()
            elif opc == 5:
                vuelo.precio = validar_numero("Nuevo precio: ", float, positivo=True)

        guardar_lista(ARCH_VUELOS, vuelos)
        print("Modificación guardada.")
        input("Presione Enter para continuar...")
        limpiar()

        
def eliminar_vuelo():
    limpiar()
    if input("¿Mostrar vuelos actuales? (s/n): ").lower() == "s":
        listar_vuelos()

    vuelos = cargar_lista(ARCH_VUELOS)
    reservas = cargar_lista(ARCH_RESERVA)
    cod = -1
    try:
        cod = int(input("Código de vuelo a eliminar: "))
    except Exception:
        print("El código ingresado no es válido. Intente nuevamente.")
        input(" Presione Enter para continuar...")
        limpiar()
        cod = -1

    vuelo_encontrado = False
    i = 0
    while i < len(vuelos) and not vuelo_encontrado:
        if vuelos[i].codigo_vuelo == cod and vuelos[i].estado == "A":
            vuelo_encontrado = True
        else:
            i += 1

    if not vuelo_encontrado:
        print("No se encontró un vuelo activo con ese código.")
        input(" Presione Enter para continuar...")
        limpiar()
    else:
        reserva_confirmada = False
        j = 0
        while j < len(reservas) and not reserva_confirmada:
            r = reservas[j]
            cod_res = r.codigo_vuelo
            if isinstance(cod_res, str) and cod_res.isdigit():
                cod_res = int(cod_res)
            if cod_res == cod and r.estado == "confirmada":
                reserva_confirmada = True
            j += 1

        if reserva_confirmada:
            print("No se puede eliminar el vuelo porque tiene reservas confirmadas.")
            input(" Presione Enter para continuar...")
            limpiar()
        else:
            vuelos[i].estado = "B"
            guardar_lista(ARCH_VUELOS, vuelos)
            print("Vuelo eliminado lógicamente.")
            input(" Presione Enter para continuar...")
            limpiar()
# 📢 GESTIÓN DE PROMOCIONES
def gestion_promociones():
    opc = 0
    while opc != 4:
        print("╔══════════════════════════════════════════╗")
        print("║     💲  MENÚ DE GESTIÓN DE PROMOCIONES    ║")
        print("╚══════════════════════════════════════════╝\n")
        print("1. Crear Promoción")
        print("2. Modificar Promoción")
        print("3. Eliminar Promoción")
        print("4. Volver")

        opc = validar_numero("Seleccione una opción: ", int, 1, 4)
        if opc == 1:
            crear_promocion()
        elif opc == 2:
            modificar_promocion()
        elif opc == 3:
            eliminar_promocion()
        elif opc == 4:
            print("↩ Volviendo al menú anterior...")
        else:
            print("⚠️ Opción inválida.")
            input("Presione Enter para continuar...")
            limpiar()

def crear_promocion():
    limpiar()
    promociones = cargar_lista(ARCH_PROMOCIONES)
    vuelos = cargar_lista(ARCH_VUELOS)
    vuelos_activos = []
    i = 0
    while i < len(vuelos):
        if vuelos[i].estado == "A":
            vuelos_activos.append(vuelos[i])
        i += 1
    if len(vuelos_activos) == 0:
        print("No hay vuelos activos para asociar una promoción.")
        input(" Presione Enter para continuar...")
        limpiar()
    else:
        print("\n--- Vuelos disponibles ---")
        i = 0
        while i < len(vuelos_activos):
            v = vuelos_activos[i]
            print(f"{v.codigo_vuelo} - {v.origen} → {v.destino} {v.fecha} ${v.precio}")
            i += 1
        codigo = -1
        while codigo < 0:
            entrada = input("Ingrese código de vuelo para la promo: ")
            if entrada.isdigit():
                codigo = int(entrada)
            else:
                print("Código de vuelo inválido.")
        i = 0
        vuelo = None
        while i < len(vuelos) and vuelo is None:
            if vuelos[i].codigo_vuelo == codigo and vuelos[i].estado == "A":
                vuelo = vuelos[i]
            i += 1
        if vuelo is None:
            print("No existe un vuelo activo con ese código.")
            input(" Presione Enter para continuar...")
            limpiar()
        elif vuelo.estado != "A":
            print("No se puede crear una promoción para un vuelo dado de baja.")
            input(" Presione Enter para continuar...")
            limpiar()
        else:
            nueva = Promocion()
            nueva.codigo_vuelo = codigo
            nueva.descuento = validar_numero("Ingrese descuento (%): ", float, minimo=0, maximo=100)
            nueva.fecha_inicio = pedir_fecha_en_rango("Ingrese fecha inicio (dd/mm/yyyy): ")
            nueva.fecha_fin = pedir_fecha_en_rango("Ingrese fecha fin (dd/mm/yyyy): ", desde=nueva.fecha_inicio)
            try:
                fecha_inicio = datetime.strptime(nueva.fecha_inicio, "%d/%m/%Y")
                fecha_final = datetime.strptime(nueva.fecha_fin, "%d/%m/%Y")
                if fecha_inicio >= fecha_final:
                    print("La fecha de inicio no puede ser posterior a la fecha de fin.")
                    input(" Presione Enter para continuar...")
                    limpiar()
                else:
                    nueva.id = 1
                    i = 0
                    while i < len(promociones):
                        if promociones[i].id >= nueva.id:
                            nueva.id = promociones[i].id + 1
                        i += 1
                    promociones.append(nueva)
                    guardar_lista(ARCH_PROMOCIONES, promociones)
                    print("Promoción creada con ID", nueva.id)
                    input("Presione Enter para continuar...")
                    limpiar()
            except Exception:
                print("Error en formato de fechas. Use dd/mm/yyyy.")
                input(" Presione Enter para continuar...")
                limpiar()

def modificar_promocion():
    promociones = cargar_lista(ARCH_PROMOCIONES)
    listar_promociones()
    prom_id = -1
    prom_id = validar_numero("Ingrese ID de la promoción a modificar: ", int, minimo=1)
    promo = None
    i = 0
    while i < len(promociones) and promo is None:
        if promociones[i].id == prom_id and promociones[i].activo:
            promo = promociones[i]
        i += 1
    if promo is None:
        print("⚠️ No existe una promoción activa con ese ID.")
        input("Presione Enter para continuar...")
        limpiar()
    else:
        print("Deje vacío el campo si no quiere modificarlo.")
        descuento = input(f"Descuento actual {promo.descuento}%: ")
        if descuento != "":
            promo.descuento = validar_numero("Nuevo descuento (%): ", float, minimo=0, maximo=100)
        fecha_ini = input(f"Fecha inicio actual {promo.fecha_inicio} (dd/mm/yyyy): ")
        if fecha_ini != "":
            promo.fecha_inicio = pedir_fecha_en_rango("Nueva fecha inicio (dd/mm/yyyy): ")
        ff = input(f"Fecha fin actual {promo.fecha_fin} (dd/mm/yyyy): ")
        if ff != "":
            promo.fecha_fin = pedir_fecha_en_rango("Nueva fecha fin (dd/mm/yyyy): ", desde=promo.fecha_inicio)
        try:
            fecha_inicio = datetime.strptime(promo.fecha_inicio, "%d/%m/%Y")
            fecha_final = datetime.strptime(promo.fecha_fin, "%d/%m/%Y")
            if fecha_inicio > fecha_final:
                print("⚠️ La fecha de inicio no puede ser posterior a la fecha de fin.")
                input("Presione Enter para continuar...")
                limpiar()
            else:
                guardar_lista(ARCH_PROMOCIONES, promociones)
                print("Promoción modificada.")
                input("Presione Enter para continuar...")
                limpiar()
        except Exception:
            print("⚠️ Error al validar fechas.")
            input("Presione Enter para continuar...")
            limpiar()

def eliminar_promocion():
    promociones = cargar_lista(ARCH_PROMOCIONES)
    listar_promociones()
    pid = validar_numero("Ingrese ID de la promoción a eliminar: ", int, minimo=1)
    i = 0
    encontrada = False
    while i < len(promociones) and not encontrada:
        if promociones[i].id == pid and promociones[i].activo:
            promociones[i].activo = False
            guardar_lista(ARCH_PROMOCIONES, promociones)
            encontrada = True
        i += 1
    if not encontrada:
        print("⚠️ Promoción no encontrada o ya inactiva.")
        input("Presione Enter para continuar...")
        limpiar()
    
def listar_promociones():
    promociones = cargar_lista(ARCH_PROMOCIONES)
    print("\n--- LISTADO DE PROMOCIONES ---")
    total = 0
    for p in promociones:
        if p.activo:# mostramos solo promociones activas
            estado = "Aprobada" if p.aprobada else "Pendiente"
            print(f"ID:{p.id} Vuelo:{p.codigo_vuelo} {p.descuento}% "
                  f"Vigencia:{p.fecha_inicio} a {p.fecha_fin} Estado:{estado}")# mostramos los datos de la promoción
            total += 1
    if total == 0:
        print(" No hay promociones activas registradas.")
        input(" Presione Enter para continuar...")
        limpiar()
# ====reportes====
def reportes():
    opc = 0
    while opc != 3:
        print("╔════════════════════════════════════╗")
        print("║         📊  MENÚ DE REPORTES       ║")
        print("╚════════════════════════════════════╝\n")
        print("1) Reporte de Ventas 💰 (reservas confirmadas)")
        print("2) Reporte de Vuelos ✈️")
        print("3) Volver al Menú Principal 🔙")
        opc = validar_numero("Seleccione una opción: ", int, 1, 3)
         
        if opc == 1:
            cod_iata = input("Ingrese código IATA de la aerolínea: ").upper()
            reportes_aerolineas = cargar_lista(ARCH_AEROLINEAS)
            if not obtener_aerolinea(cod_iata, reportes_aerolineas):
                print("Aerolínea no encontrada.")
                input(" Presione Enter para continuar...")
                limpiar()
            else:
                reporte_ventas_aerolinea(cod_iata)
        elif opc == 2:
            cod_iata = input("Ingrese código IATA de la aerolínea: ").upper()
            reportes_aerolineas = cargar_lista(ARCH_AEROLINEAS)
            if obtener_aerolinea(cod_iata, reportes_aerolineas) is None:
                print("Aerolínea no encontrada.")
                input(" Presione Enter para continuar...")
                limpiar()
            else:
                reporte_ocupacion_vuelos(cod_iata)
        elif opc == 3:
            print("↩ Volviendo al menú anterior...")
            input(" Presione Enter para continuar...")
            limpiar()
        else:
            print(" Opción inválida.")
            input(" Presione Enter para continuar...")
            limpiar()

def reporte_ventas_aerolinea(cod_iata):
    vuelos = cargar_lista(ARCH_VUELOS)
    print(f"\nREPORTE DE VENTAS - AEROLÍNEA {cod_iata}\n")
    print("Vuelo  | Origen         | Destino        | Vendidos | Ingreso")
    print("---------------------------------------------------------------")

    total_pasajes = 0
    total_ingresos = 0
    hoy = datetime.now().date()

    i = 0
    while i < len(vuelos):
        v = vuelos[i]
        # Solo vuelos activos y futuros
        try:
            fecha_v = datetime.strptime(v.fecha, "%d/%m/%Y").date()
        except Exception:
            i += 1
            continue
        if v.cod_aerolinea == cod_iata and v.estado == "A" and fecha_v >= hoy:
            vendidos = 0
            fila = 0
            while fila < 40:
                asiento = 0
                while asiento < 7:
                    if v.asientos[fila][asiento] == "O":
                        vendidos += 1
                    asiento += 1
                fila += 1
            ingreso = vendidos * v.precio
            total_pasajes += vendidos
            total_ingresos += ingreso

            print(f"{v.codigo_vuelo:06} | {v.origen[:14]:<14} | {v.destino[:14]:<14} | {vendidos:8} | $ {ingreso:,.0f}")
        i += 1

    print("---------------------------------------------------------------")
    print(f"Total pasajes vendidos: {total_pasajes}")
    print(f"Total ingresos: $ {total_ingresos:,.0f}\n")#0f para no mostrar decimales

def reporte_ocupacion_vuelos(cod_iata):
    vuelos = cargar_lista(ARCH_VUELOS)
    print(f"\nREPORTE DE OCUPACIÓN DE VUELOS - AEROLÍNEA {cod_iata}\n")
    print("Vuelo  | Ocupados | Reservados | Libres | % Ocupación")
    print("------------------------------------------------------")
    hoy = datetime.now().date()
    i = 0
    while i < len(vuelos):
        v = vuelos[i]
        try:
            fecha_v = datetime.strptime(v.fecha, "%d/%m/%Y").date()
        except Exception:
            i += 1
            continue
        if v.cod_aerolinea == cod_iata and v.estado == "A" and fecha_v >= hoy:
            ocupados = 0
            reservados = 0
            libres = 0
            fila = 0
            while fila < 40:
                asiento = 0
                while asiento < 7:
                    estado = v.asientos[fila][asiento]
                    if estado == "L":
                        libres += 1
                    elif estado == "R":
                        reservados += 1
                    elif estado == "O":
                        ocupados += 1
                    asiento += 1
                fila += 1

            total = ocupados + reservados + libres
            porcentaje = (ocupados / total) * 100 if total > 0 else 0
            
            print(f"{v.codigo_vuelo:06} | {ocupados:8} | {reservados:10} | {libres:6} | {porcentaje:10.1f} %")
        i += 1
    print("------------------------------------------------------\n")

# ==== USUARIO ====
#==== BUSCAR VUELOS ====
def menu_buscar_vuelos():
    vuelos = cargar_lista(ARCH_VUELOS)
    aerolineas = cargar_lista(ARCH_AEROLINEAS)
    fecha_desde = pedir_fecha_en_rango("Ingrese fecha desde (dd/mm/yyyy): ")
    fecha_hasta = pedir_fecha_en_rango("Ingrese fecha hasta (dd/mm/yyyy): ", desde=fecha_desde)
    origen = input("Origen: ").upper()
    destino = input("Destino: ").upper()
    if origen == "" or destino == "":
        print("⚠️ Debe ingresar origen y destino.")
        input("Presione Enter para continuar...")
        limpiar()
        return
    busc_vuelos_rango(vuelos, aerolineas, fecha_desde, fecha_hasta, origen, destino)
    
def busc_vuelos_rango(vuelos, aerolineas, fecha_desde, fecha_hasta, origen, destino):
    print("=" * 100)
    print(f"LISTADO DE VUELOS DISPONIBLES EN EL SISTEMA".center(100))
    print("=" * 100)
    print(f"{'CÓDIGO':<8}{'AEROLÍNEA':<20}{'ORIGEN':<15}{'DESTINO':<15}{'FECHA':<12}{'HORA':<8}{'PRECIO':>12}{'ASIENTOS DISP.':>18}")
    print("-" * 100)
    total_vuelos = 0
    for vuelo in vuelos:
        if vuelo.estado == "A":
            fecha_ok = False
            try:
                fecha_vuelo = datetime.strptime(vuelo.fecha, "%d/%m/%Y")
                fecha_desde_dt = datetime.strptime(fecha_desde, "%d/%m/%Y")
                fecha_hasta_dt = datetime.strptime(fecha_hasta, "%d/%m/%Y")
                fecha_ok = fecha_desde_dt <= fecha_vuelo <= fecha_hasta_dt
            except Exception:
                fecha_ok = False
            if fecha_ok and vuelo.origen.upper() == origen and vuelo.destino.upper() == destino:
                aero = obtener_aerolinea(vuelo.cod_aerolinea, aerolineas)
                nombre_aerolinea = aero.nombre if aero else "Desconocida"
                libres = 0
                for fila in vuelo.asientos:# Contar asientos libres 
                    for asiento in fila:
                        if asiento == "L":
                            libres += 1
                print(f"{vuelo.codigo_vuelo:<8}{nombre_aerolinea:<20}{vuelo.origen:<15}{vuelo.destino:<15}{vuelo.fecha:<12}{vuelo.hora:<8}${vuelo.precio:>11,}{libres:>18}".replace(",", "."))
                total_vuelos += 1
    print("-" * 100)
    print(f"Total de vuelos: {total_vuelos}")

#==== BUSCAR ASIENTOS ====
def busc_asientos():
    limpiar()
    vuelos = cargar_lista(ARCH_VUELOS)
    print(" BUSCAR ASIENTOS\n")
    if len(vuelos) == 0:
        print("⚠️ No hay vuelos cargados.")
        input(" Presione Enter para continuar...")
        limpiar()

    cod = validar_numero("Ingrese el código de vuelo (0 para salir): ", int, minimo=0, maximo=9999)

    while cod != 0:  # mientras el código no sea 0
        pos = 0  # inicializamos la posición en 0
        vuelo_encontrado = None  # inicializamos el vuelo encontrado en None
        encontrado = False       # variable bandera

        while pos < len(vuelos) and not encontrado:  # mientras no haya encontrado el vuelo
            if vuelos[pos].codigo_vuelo == cod and vuelos[pos].estado == "A":
                vuelo_encontrado = vuelos[pos]
                encontrado = True
            pos += 1
        if vuelo_encontrado is not None:
            fecha_vuelo = datetime.strptime(vuelo_encontrado.fecha, "%d/%m/%Y").date()
            hoy = datetime.now().date()
            if fecha_vuelo >= hoy:
                print()
                print("🛫 VUELO VIGENTE ENCONTRADO:")
                print("Origen:", vuelo_encontrado.origen, "- Destino:", vuelo_encontrado.destino)
                print("Fecha:", vuelo_encontrado.fecha)
                print("Hora:", vuelo_encontrado.hora)
                print("Precio: $", vuelo_encontrado.precio)
                print("\nVisualización de Asientos (L=Libre, R=Reservado, O=Ocupado):")
                print("    A   B   C   |   D   E   F")
                print("  ─────────────────────────────")
                for fila in range(ASIENTOS_COLUMNAS):
                    linea = f"{fila+1:>2} "
                    for asiento in range(ASIENTOS_FILA):
                        if asiento == 3:
                            linea += " |"
                        estado = vuelo_encontrado.asientos[fila][asiento]
                        if estado == "L":
                            letra = "L"
                        elif estado == "R":
                            letra = "R"
                        elif estado == "O":
                            letra = "O"
                        elif estado == "X":
                            letra = " "
                        else:
                            letra = " "# Mostrar espacio en blanco para cualquier valor inesperado
                        linea += f" {letra} "
                    print(linea)
                print("  ─────────────────────────────\n")
                input(" Presione Enter para continuar...")
                limpiar()
            else:
                print("⚠️  El vuelo ya ha salido o no está vigente.")
                input(" Presione Enter para continuar...")
                limpiar()
        else:
            print("⚠️  El código de vuelo ingresado no existe.")
            input(" Presione Enter para continuar...")
            limpiar()
        print()
        cod = validar_numero("Ingrese otro código de vuelo (0 para salir): ", int, 0, 9999)
        input(" Presione Enter para continuar...")
        limpiar()
#==== GESTIÓN DE RESERVAS ====
def menu_gestionar_Reserva(usuario):
    opc = 0
    while opc != 4:
        print("╔════════════════════════════════════════╗")
        print("║        🧾  GESTIÓN DE reservas         ║")
        print("╚════════════════════════════════════════╝\n")
        print("1) Reservar Vuelo 💸")
        print("2) Consultar reservas 🔍")
        print("3) Cancelar reservas ❌")
        print("4) Volver al Menú Principal 🔙")
        opc = validar_numero("Seleccione una opción: ", int, 1, 4)
        if opc == 1:
                reservar_vuelo(usuario)  # Reservar Vuelo usuario
        elif opc == 2:
                consultar_Reserva()  # Consultar reservas
        elif opc == 3:
                cancelar_Reserva()  # Cancelar / Confirmar reservas
        elif opc == 4:
                limpiar()
                print(" Volviendo al Menú Principal...")

def reservar_vuelo(usuario):
    print("=== Reservar Vuelo ===")
    vuelos = cargar_lista(ARCH_VUELOS)
    reservas = cargar_lista(ARCH_RESERVA)
    listar_vuelos()
    cod = validar_numero("Ingrese código de vuelo: ", int, minimo=1)
    i = 0
    vuelo = None
    while i < len(vuelos) and vuelo is None:
        if vuelos[i].codigo_vuelo == cod and vuelos[i].estado == "A":
            vuelo = vuelos[i]
        i += 1
    if vuelo is None:
        print("⚠️ Vuelo no encontrado o no activo.")
        input(" Presione Enter para continuar...")
        limpiar()
    else:
        print("\nAsientos disponibles (L=Libre, R=Reservado, O=Ocupado):")
        i = 0
        while i < len(vuelo.asientos):
            linea = f"Fila {i+1:02}: "
            j = 0
            while j < len(vuelo.asientos[i]):
                if j == 3:
                    linea += "| "
                letra = vuelo.asientos[i][j] if vuelo.asientos[i][j] in "LRO" else " "
                linea += f"{letra} "
                j += 1
            print(linea)
            i += 1
        asiento_valido = False
        while not asiento_valido:
            print("Ingrese un asiento que este disponible entre A y F")
            print("Ingrese un asiento entre 1 y 40")
            asiento = input("Ingrese asiento (ej: 12A): ").upper()
            # Validar formato: al menos 2 caracteres, termina en letra válida, el resto es número
            if len(asiento) < 2 or not asiento[:-1].isdigit() or asiento[-1] not in "ABCDEF":
                print("⚠️ Formato de asiento inválido. Ejemplo válido: 12A")
                continue
            fila_num = int(asiento[:-1]) - 1
            col_letra = asiento[-1]
            col_map = {"A": 0, "B": 1, "C": 2, "D": 4, "E": 5, "F": 6}
            if not (0 <= fila_num < ASIENTOS_COLUMNAS):
                print(f"⚠️ Número de fila fuera de rango (1-{ASIENTOS_COLUMNAS}).")
                continue
            if col_letra not in col_map:
                print("⚠️ Letra de asiento inválida.")
                continue
            col = col_map[col_letra]
            if vuelo.asientos[fila_num][col] != "L":
                print("⚠️ Ese asiento no está disponible.")
                continue
            # Si todo está bien, reservar
            asiento_valido = True
            vuelo.asientos[fila_num][col] = "R"
            nueva = Reserva()
            nueva.id = 1
            j = 0
            while j < len(reservas):
                if reservas[j].id >= nueva.id:
                    nueva.id = reservas[j].id + 1
                j += 1
            nueva.id_usuario = usuario.id
            nueva.codigo_vuelo = vuelo.codigo_vuelo
            nueva.asiento = asiento
            nueva.estado = "confirmada"
            nueva.fecha_reserva = datetime.now().strftime("%d/%m/%Y")
            reservas.append(nueva)
            guardar_lista(ARCH_RESERVA, reservas)
            guardar_lista(ARCH_VUELOS, vuelos)
            print(f"Reserva confirmada. ID: {nueva.id}, Vuelo: {vuelo.codigo_vuelo}, Asiento: {asiento}")
            seguir = input("¿Desea realizar otra reserva? (S/N): ").upper()
            if seguir == "S":
                reservar_vuelo(usuario)
            else:
                print("Volviendo al menú anterior...")
                input("Presione Enter para continuar...")
                limpiar()

def consultar_Reserva():
    limpiar()
    print("=== Consultar reservas ===")
    reservas = cargar_lista(ARCH_RESERVA)
    if len(reservas) == 0:
        print("⚠️ No hay reservas encontradas.")
        input("Presione Enter para continuar...")
        limpiar()
    else:
        i = 0
        while i < len(reservas):
            print("─────────────────────────────")
            print(f"ID: {reservas[i].id}, Usuario: {reservas[i].id_usuario}, Vuelo: {reservas[i].codigo_vuelo}, Asiento: {reservas[i].asiento}, Estado: {reservas[i].estado}")
            print("─────────────────────────────")
            i += 1
        input("Presione Enter para continuar...")
        limpiar()

def cancelar_Reserva():
    limpiar()
    print("=== Cancelar reservas ===")
    reservas = cargar_lista(ARCH_RESERVA)
    vuelos = cargar_lista(ARCH_VUELOS)
    if len(reservas) == 0:
        print("⚠️ No hay reservas para cancelar.")
        input("Presione Enter para continuar...")
        limpiar()
    else:
        rid = validar_numero("Ingrese ID de la reservas a cancelar: ", int, minimo=1)
        i = 0
        reserva = None
        while i < len(reservas) and reserva is None:
            if reservas[i].id == rid:
                reserva = reservas[i]
            i += 1
        if reserva is None:
            print("⚠️ Reservas no encontrada.")
            input(" Presione Enter para continuar...")
            limpiar()
        elif reserva.estado != "confirmada":
            print(f"⚠️ Solo se pueden cancelar reservas confirmadas. Estado actual: {reserva.estado}")
            input(" Presione Enter para continuar...")
            limpiar()
        else:
            j = 0
            vuelo = None
            while j < len(vuelos) and vuelo is None:
                if vuelos[j].codigo_vuelo == reserva.codigo_vuelo:
                    vuelo = vuelos[j]
                j += 1
            if vuelo is None:
                print("⚠️ Vuelo asociado a la reservas no encontrado.")
                input(" Presione Enter para continuar...")
                limpiar()
            else:
                # CONTROL DE 72 HORAS ANTES DEL VUELO
                fecha_vuelo = datetime.strptime(vuelo.fecha, "%d/%m/%Y")
                hora_vuelo = datetime.strptime(vuelo.hora, "%H:%M")
                fecha_hora_vuelo = datetime.combine(fecha_vuelo.date(), hora_vuelo.time())
                ahora = datetime.now()
                diferencia = fecha_hora_vuelo - ahora
                if diferencia.total_seconds() < 72 * 3600:
                    print("No se puede cancelar la reserva porque faltan menos de 72 horas para el vuelo.")
                    input(" Presione Enter para continuar...")
                    limpiar()    
                else:
                    error_asiento = False
                    try:
                       fila_num = int(reserva.asiento[:-1]) - 1
                       col_letra = reserva.asiento[-1]
                       col_map = {"A":0, "B":1, "C":2, "D":4, "E":5, "F":6}
                       if col_letra in col_map and 0 <= fila_num < ASIENTOS_COLUMNAS:
                           col = col_map[col_letra]
                           vuelo.asientos[fila_num][col] = "L"
                       else:
                           error_asiento = True
                    except Exception:
                        error_asiento = True

                    if error_asiento:
                       print("Error al liberar asiento: asiento inválido.")
                       input(" Presione Enter para continuar...")
                       limpiar()
                    else:
                        reservas.remove(reserva)
                        guardar_lista(ARCH_RESERVA, reservas)
                        guardar_lista(ARCH_VUELOS, vuelos)
                        print("─────────────────────────────")
                        print(f"✅ reservas ID {rid} cancelada y asiento {reserva.asiento} liberado.")
                        print("─────────────────────────────") 
                        seguir = input("Desea continuar cancelando reservas? (S/N): ").upper()
                        if seguir == "S":
                            cancelar_Reserva()
                        else:
                            print("Volviendo al menú anterior")
                            input(" Presione Enter para continuar...")
                            limpiar()
#==== HISTORIAL DE COMPRAS ====
def ver_historial_compras(usuario):
    limpiar()
    print("=== 🧾 HISTORIAL DE COMPRAS ===")

    reservas = cargar_lista(ARCH_RESERVA)
    vuelos = cargar_lista(ARCH_VUELOS)

    # Filtra solo reservas confirmadas del usuario actual
    compras = [r for r in reservas if r.id_usuario == usuario.id and r.estado.lower() == "confirmada"]

    if not compras:
        print("⚠️  No se encontraron compras confirmadas para este usuario.")
        input("Presione Enter para continuar...")
        limpiar()
    else:
        print(f"\nHistorial de compras del usuario: {usuario.email}\n")
        print(f"{'ID RESERVA':<12}{'CÓD. VUELO':<12}{'ORIGEN':<15}{'DESTINO':<15}{'FECHA VUELO':<12}{'ASIENTO':<10}{'FECHA RES.':<12}")
        print("-" * 95)
        for r in compras:
            vuelo = None
            i = 0
            while i < len(vuelos) and vuelo is None:
                if vuelos[i].codigo_vuelo == r.codigo_vuelo:
                    vuelo = vuelos[i]
                i += 1
            if vuelo:
                print(f"{r.id:<12}{vuelo.codigo_vuelo:<12}{vuelo.origen:<15}{vuelo.destino:<15}{vuelo.fecha:<12}{r.asiento:<10}{getattr(r, 'fecha_reserva', ''):<12}")
        print("-" * 95)
        print(f"Total de compras confirmadas: {len(compras)}")
        input("Presione Enter para continuar...")
        limpiar()

#==== PRECARGAS de datos ====
def precargar_aerolineas():
    aerolineas = cargar_lista(ARCH_AEROLINEAS)
    codigos = ["AR", "LA", "FB", "G3", "IB", "SK"]# códigos IATA
    nombres = ["Aerolíneas Argentinas", "LATAM Airlines", "Flybondi", "GOL", "Iberia", "Sky Airline"]# nombres de las aerolíneas
    paises = ["ARG", "CHI", "ARG", "BRA", "ARG", "CHI"]#paises de origen de las aerolineas
    for i in range(len(codigos)):
        existe = any(a.codigo_iata == codigos[i] for a in aerolineas)
        if not existe:
            a = Aerolinea()
            a.codigo_iata = codigos[i]
            a.nombre = nombres[i]
            a.pais = paises[i]
            a.activo = True
            aerolineas.append(a)
    guardar_lista(ARCH_AEROLINEAS, aerolineas)

def precargar_vuelos():
    precargar_aerolineas()  # Asegura que las aerolíneas base existen
    vuelos = cargar_lista(ARCH_VUELOS)
    aerolineas = cargar_lista(ARCH_AEROLINEAS)
    # Solo precarga si no hay vuelos
    if len(vuelos) == 0:
        datos_de_aerolineas = [
            ("AR", "BUENOS AIRES", "MADRID", "15/07/2025", "08:30", 1101150),#lo ultimos es el precio del vuelo
            ("LA", "SANTIAGO", "LIMA", "16/07/2025", "10:15", 550000),
            ("SK", "MIAMI", "NUEVA YORK", "18/08/2025", "14:45", 800220),
            ("G3", "RIO JANEIRO", "BUENOS AIRES", "20/07/2025", "22:30", 670000),
            ("LA", "LIMA", "NUEVA YORK", "22/08/2025", "20:30", 1670000),
        ]
        codigo = 1
        for datos in datos_de_aerolineas:
            cod_aero, origen, destino, fecha, hora, precio = datos
            existe = any(a.codigo_iata == cod_aero and a.activo for a in aerolineas)
            if existe:
                v = Vuelo()
                v.codigo_vuelo = codigo
                v.cod_aerolinea = cod_aero
                v.origen = origen
                v.destino = destino
                v.fecha = fecha
                v.hora = hora
                v.precio = precio
                v.estado = "A"
                inicializar_asientos_aleatorios(v)
                vuelos.append(v)
                codigo += 1
        guardar_lista(ARCH_VUELOS, vuelos)

# Precarga automática de aerolineas y vuelos 
precargar_aerolineas()
precargar_vuelos()
# ==== PROGRAMA PRINCIPAL ====(listo)

def main():
    opc = 0
    usuario = None# variable para almacenar el usuario logueado
    while opc != 3:
        print("╔═══════════════════════════════════════════════════╗")
        print("║   🗣️   🔥        Bienvenido al Sistema              ║")
        print("╚═══════════════════════════════════════════════════╝\n")
        print("1. Ingresar con un usuario registrado")
        print("2. Registrarse")
        print("3. Salir")
        opc = validar_numero("Seleccione una opción: ", int, minimo=1, maximo=3)

        if opc == 1:
            usuario = ingresar_usuario()
            if usuario:
                if usuario.tipo == "ceo":
                    menu_ceo()
                elif usuario.tipo == "usuario":
                    menu_usuario(usuario)
                elif usuario.tipo == "administrador":
                    menu_admin()
                else:
                    print("⚠️ Tipo de usuario desconocido.")
                    input("Presione Enter para continuar...")
                    limpiar()
            else:
                usuario = None# si el login falla, volvemos a None
                print("⚠️ Se ha superado la cantidad de intentos permitidos.")
                print("Se volverá al menú principal")
                input("Presione Enter para continuar...")
                limpiar()
        elif opc == 2:
            registrar_usuario()
        elif opc == 3:
            print("👋 ¡Hasta luego! Gracias por usar el sistema.")
        else:
            print("⚠️ Opción inválida.")
            input("Presione Enter para continuar...")
            limpiar()
# ==== LOGIN Y REGISTRO ====(listo)

def registrar_usuario():
    usuarios = cargar_lista(ARCH_USUARIOS)
    email_valido = False
    while not email_valido:
        email = input("Ingrese el email del nuevo usuario (máx 100 caracteres): ").lower()
        if len(email) == 0 or len(email) > 100 or "@" not in email or "." not in email.split("@")[-1]:
            print("El email debe tener entre 1 y 100 caracteres y contener (@) y (.)")
            print("Ejemplo válido: juan@gmail.com")
            input(" Presione Enter para continuar...")
            limpiar()
        else:
            existe = False
            i = 0
            while i < len(usuarios):
                if usuarios[i].email == email:
                    existe = True
                i += 1
            if existe:
                print("Ya existe un usuario con ese email.")
                # No se registra, vuelve a pedir email
            else:
                email_valido = True

    clave = getpass.getpass("Ingrese la clave (exactamente 8 caracteres): ")
    while len(clave) != 8:
        print("La clave debe tener exactamente 8 caracteres.")
        clave = getpass.getpass("Ingrese la clave (exactamente 8 caracteres): ")

    tipo = input("Ingrese el tipo de usuario ('usuario', 'ceo'): ").lower()
    while tipo not in ["usuario", "ceo"]:
        print("Tipo inválido.")
        tipo = input("Ingrese el tipo de usuario ('usuario', 'ceo'): ").lower()

    telefono = input("Ingrese el teléfono: ")

    nuevo_usuario = Usuario()
    max_id = 0
    i = 0
    while i < len(usuarios):
        if usuarios[i].id > max_id:
            max_id = usuarios[i].id
        i += 1
    nuevo_usuario.id = max_id + 1
    nuevo_usuario.email = email
    nuevo_usuario.clave = clave
    nuevo_usuario.tipo = tipo
    nuevo_usuario.activo = True
    nuevo_usuario.telefono = telefono

    usuarios.append(nuevo_usuario)
    guardar_lista(ARCH_USUARIOS, usuarios)
    print("Usuario registrado exitosamente.")

def ingresar_usuario():
    usuarios = cargar_lista(ARCH_USUARIOS)
    intentos = 0
    usuario_encontrado = None
    while intentos < 3 and usuario_encontrado is None:
        email = input("Ingrese su email: ").lower()
        clave = getpass.getpass("Ingrese su clave: ")
        if len(email) == 0 or len(email) > 100 or "@" not in email or "." not in email.split("@")[-1]:
            print("El email debe tener entre 1 y 100 caracteres y contener (@) y (.)")
            intentos += 1
            print(f"Intentos restantes: {3 - intentos}")
        elif len(clave) != 8:
            print("La clave debe tener exactamente 8 caracteres.")
            intentos += 1
            print(f"Intentos restantes: {3 - intentos}")
        else:
            i = 0
            while i < len(usuarios):
                if usuarios[i].email == email and usuarios[i].clave == clave and usuarios[i].activo:
                    usuario_encontrado = usuarios[i]
                i += 1
            if usuario_encontrado is None:
                intentos += 1
                print(f"Usuario o clave incorrectos. Intentos restantes: {3 - intentos}")
    if usuario_encontrado is None:
        print("Acceso bloqueado por demasiados intentos fallidos.")
        usuario_encontrado = None
    else:
        print(f"\nBienvenido, {usuario_encontrado.email} ({usuario_encontrado.tipo})")
    return usuario_encontrado

if __name__ == "__main__":
    main()
