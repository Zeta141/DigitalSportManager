from datetime import date, time, timedelta
from abc import ABC, abstractmethod



# CLASE PERSONA


class Persona(ABC):
    def __init__(self, nombre_pila, apellido_paterno, apellido_materno,
                 telefono, correo, estatus=True):
        self._nombre_pila = nombre_pila
        self._apellido_paterno = apellido_paterno
        self._apellido_materno = apellido_materno
        self._telefono = telefono
        self._correo = correo
        self._estatus = estatus

    def obtenerNombreCompleto(self):
        return f"{self._nombre_pila} {self._apellido_paterno} {self._apellido_materno}"

    @abstractmethod
    def mostrarInformacion(self):
        pass


# CLASE MIEMBRO

class Miembro(Persona):
    def __init__(self, nombre_pila, apellido_paterno, apellido_materno,
                 telefono, correo, numero_socio, fecha_registro,
                 fecha_nacimiento, estatus=True):
        super().__init__(nombre_pila, apellido_paterno, apellido_materno,
                         telefono, correo, estatus)
        self.__numero_socio = numero_socio
        self.__fecha_registro = fecha_registro
        self.__fecha_nacimiento = fecha_nacimiento
        self.membresias = []
        self.asistencias = []
        self.inscripciones = []
        self.reservas = []
        self.equipo = None

    @property
    def edad(self):
        hoy = date.today()
        return hoy.year - self.__fecha_nacimiento.year - (
            (hoy.month, hoy.day) <
            (self.__fecha_nacimiento.month, self.__fecha_nacimiento.day)
        )

    def calcularEdad(self):
        return self.edad

    def mostrarInformacion(self):
        return (f"Miembro: {self.obtenerNombreCompleto()}\n"
                f"Numero de socio: {self.__numero_socio}\n"
                f"Edad: {self.edad}\n"
                f"Telefono: {self._telefono}\n"
                f"Correo: {self._correo}")


# CLASE ENTRENADOR

class Entrenador(Persona):
    def __init__(self, nombre_pila, apellido_paterno, apellido_materno,
                 telefono, correo, clave_entrenador, especialidad,
                 estatus=True):
        super().__init__(nombre_pila, apellido_paterno, apellido_materno,
                         telefono, correo, estatus)
        self.__clave_entrenador = clave_entrenador
        self.__especialidad = especialidad
        self.equipos = []

    def mostrarInformacion(self):
        return (f"Entrenador: {self.obtenerNombreCompleto()}\n"
                f"Clave: {self.__clave_entrenador}\n"
                f"Especialidad: {self.__especialidad}")


# CLASE CATEGORIA

class Categoria:
    def __init__(self, clave_categoria, nombre_categoria,
                 edad_minima, edad_maxima):
        self.__clave_categoria = clave_categoria
        self.__nombre_categoria = nombre_categoria
        self.__edad_minima = edad_minima
        self.__edad_maxima = edad_maxima

    def esEdadValida(self, edad):
        return self.__edad_minima <= edad <= self.__edad_maxima

    def __str__(self):
        return f"{self.__nombre_categoria} ({self.__edad_minima}-{self.__edad_maxima} años)"


# ==========================================================
# CLASE EQUIPO
# ==========================================================

class Equipo:
    def __init__(self, clave_equipo, nombre_equipo, categoria,
                 entrenador=None, horario=None):
        self.__clave_equipo = clave_equipo
        self.__nombre_equipo = nombre_equipo
        self.categoria = categoria
        self.entrenador = entrenador
        self.horario = horario
        self.miembros = []

        if entrenador is not None:
            entrenador.equipos.append(self)

    def agregarMiembro(self, miembro):
        if not self.categoria.esEdadValida(miembro.calcularEdad()):
            raise ValueError("La edad del miembro no corresponde a la categoria.")

        if miembro in self.miembros:
            raise ValueError("El miembro ya pertenece a este equipo.")

        if miembro.equipo is not None:
            raise ValueError("El miembro ya pertenece a otro equipo.")

        self.miembros.append(miembro)
        miembro.equipo = self

    def quitarMiembro(self, miembro):
        if miembro not in self.miembros:
            raise ValueError("El miembro no pertenece a este equipo.")

        self.miembros.remove(miembro)
        miembro.equipo = None

    def __str__(self):
        return f"{self.__nombre_equipo} - {self.categoria}"


# ==========================================================
# CLASE TIPO_MEMBRESIA
# ==========================================================

class Tipo_Membresia:
    def __init__(self, clave_T_membresia, nombre_tipo,
                 duracion_dias, costo):
        self.__clave_T_membresia = clave_T_membresia
        self.__nombre_tipo = nombre_tipo
        self.__duracion_dias = duracion_dias
        self.__costo = costo

    @property
    def costo(self):
        return self.__costo

    @property
    def nombre_tipo(self):
        return self.__nombre_tipo

    def calcularFin(self, inicio):
        return inicio + timedelta(days=self.__duracion_dias)


# ==========================================================
# CLASE MEMBRESIA
# ==========================================================

class Membresia:
    def __init__(self, folio_membresia, fecha_inicio, tipo_membresia):
        self.__folio_membresia = folio_membresia
        self.__fecha_inicio = fecha_inicio
        self.tipo_membresia = tipo_membresia
        self.__fecha_fin = tipo_membresia.calcularFin(fecha_inicio)
        self.pagos = []

    @property
    def estado(self):
        return self.calcularEstado()

    def calcularEstado(self):
        if date.today() <= self.__fecha_fin:
            return "Activa"
        return "Vencida"

    def renovar(self):
        if self.calcularEstado() == "Activa":
            inicio = self.__fecha_fin + timedelta(days=1)
        else:
            inicio = date.today()

        self.__fecha_inicio = inicio
        self.__fecha_fin = self.tipo_membresia.calcularFin(inicio)

    def __str__(self):
        return (f"Membresia {self.__folio_membresia} | "
                f"{self.tipo_membresia.nombre_tipo} | "
                f"{self.calcularEstado()} | vence: {self.__fecha_fin}")


# ==========================================================
# CLASE PAGO
# ==========================================================

class Pago:
    def __init__(self, folio_pago, fecha_pago, monto,
                 metodo_pago, estado_pago="Pendiente"):
        self.__folio_pago = folio_pago
        self.__fecha_pago = fecha_pago
        self.__monto = monto
        self.__metodo_pago = metodo_pago
        self.__estado_pago = estado_pago

    def procesarPago(self):
        if self.__monto <= 0:
            raise ValueError("El monto debe ser mayor que cero.")

        if self.__estado_pago == "Reembolsado":
            raise ValueError("No se puede procesar un pago reembolsado.")

        self.__estado_pago = "Pagado"
        return True

    def generarComprobante(self):
        return (f"COMPROBANTE\nFolio: {self.__folio_pago}\n"
                f"Fecha: {self.__fecha_pago}\nMonto: ${self.__monto:.2f}\n"
                f"Metodo: {self.__metodo_pago}\nEstado: {self.__estado_pago}")

    def reembolsarPago(self):
        if self.__estado_pago != "Pagado":
            raise ValueError("Solo se puede reembolsar un pago realizado.")
        self.__estado_pago = "Reembolsado"


# ==========================================================
# CLASE ASISTENCIA
# ==========================================================

class Asistencia:
    def __init__(self, folio_asistencia, fecha, estado_asistencia=False,
                 horario=None):
        self.__folio_asistencia = folio_asistencia
        self.__fecha = fecha
        self.__estado_asistencia = estado_asistencia
        self.horario = horario

    def registrarAsistencia(self):
        self.__estado_asistencia = True

    def __str__(self):
        estado = "Presente" if self.__estado_asistencia else "Ausente"
        return f"{self.__fecha}: {estado}"


# ==========================================================
# CLASE HORARIO
# ==========================================================

class Horario:
    def __init__(self, codigo_horario, hora_inicio, hora_fin, dia_semana):
        if hora_inicio >= hora_fin:
            raise ValueError("La hora de inicio debe ser anterior a la hora final.")

        self.__codigo_horario = codigo_horario
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.__dia_semana = dia_semana

    @property
    def dia_semana(self):
        return self.__dia_semana

    def hayTraslape(self, horario):
        if self.__dia_semana.lower() != horario.dia_semana.lower():
            return False

        return (self.__hora_inicio < horario._Horario__hora_fin and
                horario._Horario__hora_inicio < self.__hora_fin)

    def __str__(self):
        return (f"{self.__dia_semana} "
                f"{self.__hora_inicio.strftime('%H:%M')}-"
                f"{self.__hora_fin.strftime('%H:%M')}")


# ==========================================================
# CLASE ACTIVIDAD
# ==========================================================

class Actividad:
    def __init__(self, codigo_actividad, nombre, descripcion, cupo_maximo,
                 horario=None):
        self.__codigo_actividad = codigo_actividad
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__cupo_maximo = cupo_maximo
        self.horario = horario
        self.inscripciones = []

    def hayCupo(self):
        return len(self.inscripciones) < self.__cupo_maximo

    def __str__(self):
        return f"{self.__nombre} ({len(self.inscripciones)}/{self.__cupo_maximo})"


# ==========================================================
# CLASE INSCRIPCION
# ==========================================================

class Inscripcion:
    def __init__(self, folio_inscripcion, fecha_inscripcion, actividad):
        self.__folio_inscripcion = folio_inscripcion
        self.__fecha_inscripcion = fecha_inscripcion
        self.__estado_inscripcion = "Activa"
        self.__fecha_baja = None
        self.actividad = actividad
        self.miembro = None

    def inscribir(self, miembro):
        if self.__estado_inscripcion != "Activa":
            raise ValueError("La inscripcion ya no esta activa.")

        if not self.actividad.hayCupo():
            raise ValueError("La actividad ya alcanzo su cupo maximo.")

        self.miembro = miembro
        miembro.inscripciones.append(self)
        self.actividad.inscripciones.append(self)

    def darDeBaja(self):
        if self.__estado_inscripcion == "Baja":
            raise ValueError("La inscripcion ya fue dada de baja.")

        self.__estado_inscripcion = "Baja"
        self.__fecha_baja = date.today()

        if self in self.actividad.inscripciones:
            self.actividad.inscripciones.remove(self)

        if self.miembro is not None and self in self.miembro.inscripciones:
            self.miembro.inscripciones.remove(self)


# ==========================================================
# CLASE ESPACIO_DEPORTIVO
# ==========================================================

class Espacio_Deportivo:
    def __init__(self, codigo_espacio, nombre_espacio, tipo,
                 capacidad, estado=True):
        self.__codigo_espacio = codigo_espacio
        self.__nombre_espacio = nombre_espacio
        self.__tipo = tipo
        self.__capacidad = capacidad
        self.__estado = estado
        self.reservas = []

    def estaDisponible(self, reserva):
        if not self.__estado:
            return False

        for reserva_existente in self.reservas:
            if reserva_existente.fecha == reserva.fecha:
                if (reserva.hora_inicio < reserva_existente.hora_fin and
                        reserva_existente.hora_inicio < reserva.hora_fin):
                    return False

        return True

    def __str__(self):
        return self.__nombre_espacio


# ==========================================================
# CLASE RESERVA
# ==========================================================

class Reserva:
    def __init__(self, num_reserva, fecha, hora_inicio, hora_fin,
                 espacio_deportivo):
        if hora_inicio >= hora_fin:
            raise ValueError("La hora de inicio debe ser anterior a la hora final.")

        self.__num_reserva = num_reserva
        self.__fecha = fecha
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.espacio_deportivo = espacio_deportivo
        self.miembro = None
        self.__estado = "Pendiente"

    @property
    def fecha(self):
        return self.__fecha

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @property
    def hora_fin(self):
        return self.__hora_fin

    def verificarDisponibilidad(self):
        return self.espacio_deportivo.estaDisponible(self)

    def crearReserva(self, miembro):
        if self.__estado != "Pendiente":
            raise ValueError("La reserva ya fue procesada.")

        if not self.verificarDisponibilidad():
            raise ValueError("El espacio no esta disponible en ese horario.")

        self.miembro = miembro
        self.espacio_deportivo.reservas.append(self)
        miembro.reservas.append(self)
        self.__estado = "Confirmada"

    def cancelarReserva(self):
        if self.__estado != "Confirmada":
            raise ValueError("Solo se pueden cancelar reservas confirmadas.")

        self.__estado = "Cancelada"

        if self in self.espacio_deportivo.reservas:
            self.espacio_deportivo.reservas.remove(self)

        if self.miembro is not None and self in self.miembro.reservas:
            self.miembro.reservas.remove(self)


# ==========================================================
# CLASE MATERIAL
# ==========================================================

class Material:
    def __init__(self, codigo_material, nombre_material,
                 cantidad_total, estado="Disponible"):
        self.__codigo_material = codigo_material
        self.__nombre_material = nombre_material
        self.__cantidad_total = cantidad_total
        self.__estado = estado

    def hayStock(self, cantidad):
        return cantidad > 0 and self.__cantidad_total >= cantidad

    def retirar(self, cantidad):
        if not self.hayStock(cantidad):
            raise ValueError("No hay suficiente material disponible.")
        self.__cantidad_total -= cantidad

    def __str__(self):
        return f"{self.__nombre_material}: {self.__cantidad_total} disponibles"


# ==========================================================
# CLASE NECESITA
# Relaciona un espacio deportivo con el material que requiere.
# ==========================================================

class Necesita:
    def __init__(self, cantidad_requerida, material):
        self.__cantidad_requerida = cantidad_requerida
        self.material = material

    def verificarMaterial(self):
        return self.material.hayStock(self.__cantidad_requerida)

    def surtirMaterial(self):
        if not self.verificarMaterial():
            raise ValueError("No hay material suficiente.")
        self.material.retirar(self.__cantidad_requerida)


# ==========================================================
# PROGRAMA PRINCIPAL DE PRUEBA
# ==========================================================

def main():
    print("====================================")
    print("       DIGITAL SPORT MANAGER")
    print("====================================")

    try:
        categoria = Categoria(1, "Juvenil", 13, 19)

        entrenador = Entrenador(
            "Carlos", "Ramirez", "Lopez",
            "6461234567", "carlos@club.com",
            "ENT001", "Futbol"
        )

        equipo = Equipo(1, "Lobos", categoria, entrenador)

        miembro = Miembro(
            "Luis", "Hernandez", "Garcia",
            "6469876543", "luis@correo.com",
            "SOC001", date.today(), date(2008, 5, 12)
        )

        equipo.agregarMiembro(miembro)

        tipo = Tipo_Membresia(1, "Mensual", 30, 350.00)
        membresia = Membresia("MEM001", date.today(), tipo)
        miembro.membresias.append(membresia)

        pago = Pago("PAG001", date.today(), tipo.costo, "Efectivo")
        pago.procesarPago()
        membresia.pagos.append(pago)

        horario = Horario(1, time(16, 0), time(18, 0), "Lunes")
        equipo.horario = horario

        actividad = Actividad(
            1, "Entrenamiento de futbol",
            "Entrenamiento general del equipo", 20, horario
        )

        inscripcion = Inscripcion("INS001", date.today(), actividad)
        inscripcion.inscribir(miembro)

        asistencia = Asistencia(1, date.today(), horario=horario)
        asistencia.registrarAsistencia()
        miembro.asistencias.append(asistencia)

        espacio = Espacio_Deportivo(1, "Cancha principal", "Futbol", 22)
        reserva = Reserva(
            "RES001", date.today(), time(18, 0), time(19, 0), espacio
        )
        reserva.crearReserva(miembro)

        balones = Material("MAT001", "Balon de futbol", 10)
        material_requerido = Necesita(2, balones)

        print("\n--- INFORMACION DEL MIEMBRO ---")
        print(miembro.mostrarInformacion())

        print("\n--- EQUIPO ---")
        print(equipo)
        print("Entrenador:", entrenador.obtenerNombreCompleto())
        print("Miembros:", len(equipo.miembros))

        print("\n--- MEMBRESIA ---")
        print(membresia)

        print("\n--- PAGO ---")
        print(pago.generarComprobante())

        print("\n--- ACTIVIDAD ---")
        print(actividad)

        print("\n--- ASISTENCIA ---")
        print(asistencia)

        print("\n--- RESERVA ---")
        print("Reserva confirmada en:", espacio)

        print("\n--- MATERIAL ---")
        print("¿Hay material suficiente?", material_requerido.verificarMaterial())
        material_requerido.surtirMaterial()
        print(balones)

        print("\nSistema de prueba ejecutado correctamente.")

    except ValueError as error:
        print("Error:", error)


if __name__ == "__main__":
    main()

#menu


def menu():
    categoria = Categoria(1, "Juvenil", 13, 19)

    entrenador = Entrenador(
        "Carlos", "Ramirez", "Lopez",
        "6461234567", "carlos@club.com",
        "ENT001", "Futbol"
    )

    equipo = Equipo(1, "Lobos", categoria, entrenador)

    miembro = Miembro(
        "Luis", "Hernandez", "Garcia",
        "6469876543", "luis@correo.com",
        "SOC001", date.today(), date(2008, 5, 12)
    )

    equipo.agregarMiembro(miembro)

    while True:
        print("\n----------------------------------------")
        print("       DIGITAL SPORT MANAGER")
        print("------------------------------------------")
        print("1. Mostrar informacion del miembro")
        print("2. Consultar entrenador")
        print("3. Consultar equipo")
        print("4. Consultar membresia")
        print("5. Consultar actividades")
        print("6. Consultar asistencias")
        print("7. Registrar reserva")
        print("8. Consultar material deportivo")
        print("9. Salir")
        print("======================================")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            print("\n--- INFORMACION DEL MIEMBRO ---")
            print(miembro.mostrarInformacion())

        elif opcion == "2":
            print("\n--- ENTRENADOR ---")
            print(entrenador.mostrarInformacion())

        elif opcion == "3":
            print("\n--- EQUIPO ---")
            print(equipo)
            print("Miembros:", len(equipo.miembros))

        elif opcion == "4":
            tipo = Tipo_Membresia(1, "Mensual", 30, 350.00)
            membresia = Membresia("MEM001", date.today(), tipo)
            print("\n--- MEMBRESIA ---")
            print(membresia)

        elif opcion == "5":
            actividad = Actividad(
                1, "Entrenamiento de futbol",
                "Entrenamiento general", 20
            )
            print("\n--- ACTIVIDADES ---")
            print(actividad)

        elif opcion == "6":
            print("\n--- ASISTENCIAS ---")
            if miembro.asistencias:
                for asistencia in miembro.asistencias:
                    print(asistencia)
            else:
                print("No hay asistencias registradas.")

        elif opcion == "7":
            espacio = Espacio_Deportivo(
                1, "Cancha principal", "Futbol", 22
            )

            reserva = Reserva(
                "RES001", date.today(),
                time(18, 0), time(19, 0), espacio
            )

            try:
                reserva.crearReserva(miembro)
                print("\nReserva realizada correctamente.")
                print("Espacio:", espacio)
            except ValueError as error:
                print("Error:", error)

        elif opcion == "8":
            balones = Material(
                "MAT001", "Balon de futbol", 10
            )
            print("\n--- MATERIAL DEPORTIVO ---")
            print(balones)

        elif opcion == "9":
            print("\nGracias por utilizar Digital Sport Manager.")
            break

        else:
            print("\nOpcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    menu()
