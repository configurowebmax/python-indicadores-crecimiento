"""
=====================================================================
 Indicadores de Crecimiento
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_indicadores_crecimiento_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Indicadores de Crecimiento."""

    def __init__(self, anterior, actual):
        self.anterior = float(anterior)
        self.actual = float(actual)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        if self.anterior == 0:
            return {"error": "El valor anterior no puede ser 0."}
        crecimiento = (self.actual - self.anterior) / self.anterior * 100
        return {"crecimiento": crecimiento}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["crecimiento"] < 0:
            return "❌ Crecimiento negativo. Estás retrocediendo."
        elif resultados["crecimiento"] < 10:
            return "📈 Crecimiento moderado."
        return "🚀 ¡Excelente crecimiento!"



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("anterior"), input_float("actual"))
    r = c.calcular()
    if "error" in r:
        mostrar(f'❌ {r["error"]}', clase="is-error"); return
    html = f"""
      <div class="result-value">📊 Crecimiento: {fmt_pct(r["crecimiento"])}</div>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "anterior": input_float("anterior"),
            "actual": input_float("actual"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
            if "anterior" in datos:
                document.querySelector("#anterior").value = datos["anterior"]
            if "actual" in datos:
                document.querySelector("#actual").value = datos["actual"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
