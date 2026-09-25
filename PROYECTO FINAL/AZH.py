import time
CARPETA = "PROYECTO FINAL/"
def ruta(nombre):
    return CARPETA + nombre
INICIALES = {
    "servicios.txt": [
        "Natural | 450.00",
        "Social | 600.00",
        "Noche | 750.00",
        "Novia | 1200.00",
        "XV años | 900.00",
        "Artístico | 850.00"
    ],
    "marcas.txt": [
        "MAC",
        "Dior",
        "Fenty Beauty",
        "Rare Beauty",
        "Make Up For Ever",
        "Benefit",
        "Estee Lauder",
        "Yves Saint Laurent"
    ],
    "notas.txt": [
        "Llegar 10 minutos antes.",
        "Avisar si necesitas cambiar la cita.",
        "El anticipo debe cubrirse antes de la cita."
    ],
    "citas.txt": []
}
MENU = [["1. Crear cita", "2. Mostrar servicios"],
        ["3. Mostrar marcas", "4. Instrucciones para las citas"],
        ["5. Formas de pago", "6. Cancelar una cita"],
        ["7. Mostrar citas", "8. Salir"]]
LETRAS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_áéíóúÁÉÍÓÚñÑ-"
def fecha_actual():
    reloj = time.localtime()
    return reloj[2], reloj[1], reloj[0]
def fecha_texto(fecha):
    dia, mes, anio = fecha
    return f"{dia:02d}/{mes:02d}/{anio:04d}"
def pedir_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        texto = input("No lo dejes vacío. " + mensaje).strip()
    return texto
def elegir(opciones, mensaje="Escribe el número de la opción y presiona Enter: "):
    for i in range(len(opciones)):
        print(f"{i + 1}. {opciones[i]}")
    while True:
        try:
            numero = int(input(mensaje))
            if 1 <= numero <= len(opciones):
                return numero - 1
        except ValueError:
            print("Escribe un número entero.")
        print("Elige una opción de la lista.")
def confirmar(mensaje):
    respuesta = pedir_texto(mensaje).lower()
    while respuesta not in ["si", "no"]:
        respuesta = pedir_texto("Escribe si o no: ").lower()
    return respuesta == "si"
def existe(nombre):
    try:
        with open(ruta(nombre), "r", encoding="utf-8") as archivo:
            archivo.read(0)
        return True
    except FileNotFoundError:
        return False
def leer(nombre):
    lineas = []
    with open(ruta(nombre), "r", encoding="utf-8") as archivo:
        for linea in archivo:
            texto = linea.strip()
            if texto == "" or texto[0] == "#" or texto.lower()[:6] == "fecha:":
                continue
            if texto.lower() not in ["marcas", "servicios", "notas"]:
                lineas.append(texto)
    return lineas
def escribir(nombre, contenido, modo):
    with open(ruta(nombre), modo, encoding="utf-8") as archivo:
        archivo.write(contenido)
        if contenido[-1:] != "\n":
            archivo.write("\n")
def preparar_archivos():
    for nombre in INICIALES:
        if not existe(nombre) or len(leer(nombre)) == 0:
            contenido = ""
            for linea in INICIALES[nombre]:
                contenido += linea + "\n"
            escribir(nombre, contenido, "w")
def precio_centavos(texto):
    partes = texto.strip().split(".")
    if len(partes) == 1:
        partes.append("00")
    if len(partes) != 2 or partes[0] == "" or len(partes[1]) not in [1, 2]:
        return -1
    for parte in partes:
        for caracter in parte:
            if caracter not in "0123456789":
                return -1
    if len(partes[1]) == 1:
        partes[1] += "0"
    precio = int(partes[0]) * 100 + int(partes[1])
    if 0 < precio <= 100000000:
        return precio
    return -1
def pedir_fecha_hora():
    while True:
        try:
            fecha = time.strptime(input("Fecha de cita, día/mes/año (ejemplo 30/09/2026): "), "%d/%m/%Y")
            hora = time.strptime(input("Hora en formato de 24 horas (ejemplo 16:30): "), "%H:%M")
            return (fecha[2], fecha[1], fecha[0]), f"{hora[3]:02d}:{hora[4]:02d}"
        except ValueError:
            print("Fecha u hora inválida. Ejemplo: 30/09/2026 y 16:30.")
def nombre_seguro(texto):
    nombre = ""
    for caracter in texto.strip().replace(" ", "_"):
        if caracter in LETRAS:
            nombre += caracter
    if nombre == "":
        nombre = "Cliente"
    return nombre[:60]
def guardar_cita(cliente, fecha, ticket):
    dia, mes, anio = fecha
    base = f"{anio:04d}-{mes:02d}-{dia:02d}_" + nombre_seguro(cliente)
    nombre = base + ".txt"
    numero = 2
    while existe(nombre):
        nombre = base + "_" + str(numero) + ".txt"
        numero += 1
    ticket += "Referencia para el depósito: " + nombre[:-4] + "\n"
    ticket += "╚" + "═" * 48 + "╝\n"
    escribir(nombre, ticket, "w")
    escribir("citas.txt", nombre, "a")
    print("Ticket guardado en", nombre)
def registrar_cita():
    preparar_archivos()
    cliente = pedir_texto("Nombre del cliente: ")
    fecha, hora = pedir_fecha_hora()
    servicios = leer("servicios.txt")
    marcas = leer("marcas.txt")
    print("\nSERVICIOS | Precios en MXN")
    servicio = servicios[elegir(servicios, "Ingresa el número del servicio que deseas: ")].split("|")
    print("\nMARCAS")
    marcas_elegidas = [marcas[elegir(marcas, "Ingresa el número de la marca que deseas: ")]]
    while confirmar("¿Quieres agregar otra marca? Escribe si o no: "):
        marca = marcas[elegir(marcas, "Ingresa el número de otra marca: ")]
        if marca not in marcas_elegidas:
            marcas_elegidas.append(marca)
    marca = ""
    for seleccion in marcas_elegidas:
        if marca != "":
            marca += ", "
        marca += seleccion
    print("\nNOTAS")
    for nota in leer("notas.txt"):
        print(nota)
    ticket = "╔══════════════ AZH | TICKET DE CITA ══════════════╗\nEstado: PENDIENTE DE PAGO\n" + f"Cliente: {cliente}\nFecha: {fecha_texto(fecha)}\nHora: {hora}\n"
    precio = precio_centavos(servicio[1].strip()) if len(servicio) > 1 else -1
    if precio < 0:
        print("Precio de servicio inválido.")
        return
    deposito = (precio + 1) // 2
    saldo = precio - deposito
    ticket += f"Servicio: {servicio[0].strip()}\nMarcas seleccionadas: {marca}\n"
    ticket += f"Precio del servicio: {precio / 100:.2f} MXN\n"
    ticket += f"Depósito previo (50%): {deposito / 100:.2f} MXN\n"
    ticket += f"Saldo para el día de la cita: {saldo / 100:.2f} MXN\nPago del saldo: tarjeta o efectivo, el día de la cita.\n"
    ticket += "Deposita el anticipo a la cuenta con clave: 67676767.\n"
    ticket += "Envía el comprobante a AZH; este ticket no acredita un pago.\n"
    print("\n" + ticket + "╚" + "═" * 48 + "╝\n")
    if confirmar("¿Guardar cita? (si/no): "):
        guardar_cita(cliente, fecha, ticket)
    else:
        print("Cita cancelada; no se creó un archivo.")
def mostrar_archivo(nombre, titulo):
    print("\n" + titulo)
    for linea in leer(nombre):
        print("- " + linea)
def mostrar_pago():
    print("\nFORMAS DE PAGO\nDeposita el 50% a la cuenta con clave 67676767.\nEl otro 50% se paga el día de la cita con tarjeta o efectivo.")
def cancelar_cita():
    citas = leer("citas.txt")
    if len(citas) == 0:
        print("Todavía no se ha realizado ninguna cita; no hay citas para cancelar.")
        return
    print("\nCITAS ACTIVAS: revisa el nombre, la fecha y la hora antes de elegir.")
    descripciones = []
    for nombre in citas:
        with open(ruta(nombre), "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
        descripciones.append(lineas[2].strip() + " | " + lineas[3].strip() + " | " + lineas[4].strip())
    posicion = elegir(descripciones)
    nombre = citas[posicion]
    if not confirmar("¿Confirmas cancelar " + nombre + "? (si/no): "):
        print("La cita sigue activa.")
        return
    with open(ruta(nombre), "r", encoding="utf-8") as archivo:
        ticket = archivo.read()
    ticket = ticket.replace("Estado: PENDIENTE DE PAGO", "Estado: CITA CANCELADA")
    escribir(nombre, ticket, "w")
    citas.pop(posicion)
    escribir("citas.txt", "\n".join(citas), "w")
    print("La cita quedó cancelada. El ticket se conservó como comprobante.")
def mostrar_citas():
    citas = leer("citas.txt")
    if len(citas) == 0:
        print("Todavía no hay citas registradas.")
        return
    ordenadas = []
    for nombre in citas:
        with open(ruta(nombre), "r", encoding="utf-8") as archivo:
            datos = archivo.readlines()
        ordenadas.append([nombre[:10], datos[4][6:11], datos[3][7:].strip(), datos[2][8:].strip(), datos[5][9:].strip()])
    ordenadas.sort()
    fecha_anterior = ""
    for cita in ordenadas:
        if cita[0] != fecha_anterior:
            print("\n╭─ Citas del", cita[2], "─╮")
            fecha_anterior = cita[0]
        print("Horario:", cita[1], "| Cliente:", cita[3], "| Servicio:", cita[4])
def cargar():
    print("Cargando AZH...")
    time.sleep(3)
def pedir_opcion():
    inicio = time.time()
    opcion = input("Selecciona una opción: ").strip()
    transcurrido = time.time() - inicio
    for minuto in range(1, 11):
        if minuto == 10 and transcurrido >= minuto * 60:
            print("Pasaron 10 minutos; se descarta la opción enviada.")
            return "inactivo"
    return opcion
def continuar():
    while True:
        respuesta = input("Escribe :) para regresar al menú o :( para salir: ").strip()
        if respuesta == ":)":
            return True
        if respuesta == ":(":
            return False
        print("Usa exactamente :) para volver o :( para salir del programa.")
def iniciar():
    preparar_archivos()
    usuario = pedir_texto("¡Hola! Escribe tu nombre o usuario : ")
    print("\nHola, " + usuario + ". ¡Bienvenida a la página de citas de maquillaje AZH!")
    print("Aquí puedes reservar tu maquillaje, consultar opciones y cancelar una cita.")
    print("Elige una opción escribiendo su número y presionando Enter.")
    print("Al terminar, escribe :) para volver al menú o :( para cerrar el programa.")
    print("Para reservar, ten listo el nombre del cliente, la fecha, la hora y la marca deseada.")
    cargar()
    while True:
        print("\n" + "═" * 52 + "\n       AZH | AGENDA DE MAQUILLAJE\n" + "═" * 52)
        print("Fecha de Operacion:", fecha_texto(fecha_actual()))
        for fila in MENU:
            print(fila[0], "|", fila[1])
        opcion = pedir_opcion()
        if opcion == "inactivo":
            print("Se cerró esta opción porque pasaron 10 minutos.")
            if not continuar():
                print("Gracias por visitar AZH, " + usuario + ". ¡Hasta pronto!")
                return
            continue
        try:
            if opcion == "1":
                registrar_cita()
            elif opcion == "2":
                mostrar_archivo("servicios.txt", "SERVICIOS AZH")
                print("Elige el número del servicio cuando registres tu cita.")
            elif opcion == "3":
                mostrar_archivo("marcas.txt", "MARCAS DISPONIBLES")
                print("Elige el número de la marca cuando registres tu cita.")
            elif opcion == "4":
                mostrar_archivo("notas.txt", "INSTRUCCIONES PARA LAS CITAS")
            elif opcion == "5":
                mostrar_pago()
            elif opcion == "6":
                print("Elige una cita por su número. Después confirma con si o no.")
                cancelar_cita()
            elif opcion == "7":
                mostrar_citas()
            elif opcion == "8":
                print("Gracias por visitar AZH, " + usuario + ". ¡Hasta pronto!")
                return
            else:
                print("Esa opción no existe. Escribe un número del 1 al 8.")
                continue
            if not continuar():
                print("Gracias por visitar AZH, " + usuario + ". ¡Hasta pronto!")
                return
        except OSError:
            print("No se pudo abrir o guardar un archivo. Revisa que todos estén en la misma carpeta.")
        except (ValueError, UnicodeError):
            print("Hay un dato inválido. Revisa lo que escribiste e inténtalo otra vez.")
try:
    iniciar()
except (KeyboardInterrupt, EOFError):
    print("\nPrograma cerrado.")
except (OSError, UnicodeError):
    print("No se pudo iniciar. Crea la carpeta PROYECTO FINAL junto a este programa y vuelve a intentarlo.")
