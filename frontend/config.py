"""
anotaciones en clase
config base
Theme Mode : system toma el tema del sistema
tema de color
los colores son limitados
tem mode: system toma tema del sistema de la maquina
diccionario de colors. establece para todas las acciones

Archivo de configuración central que define constantes globales de la aplicación, 
como la URL base de la API REST backend, los parámetros de geometría de la ventana principal y 
la paleta de colores y temas cromáticos de la interfaz visual.
"""

API_BASE_URL = "http://127.0.0.1:8000/"

WINDOW_TITLE = "Pasteleria Mordere"
WINDOW_SIZE = "950x600"
MIN_WINDOW_SIZE = (800, 500)
THEME_MODE = "System"
COLOR_THEME = "dark-blue"

COLORS = {
    "bg_card": "#1e293b",
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",
    "success": "#10b981",
    "success_hover": "#059669",
    "danger": "#ef4444",
    "danger_hover": "#dc2626",
    "info": "#06b6d4",
    "info_hover": "#0891b2",
    "cancel": "#64748b",
    "cancel_hover": "#475569",
    "status_ok": "#10b981",
    "status_err": "#ef4444",
    "muted_text": "#94a3b8"
}