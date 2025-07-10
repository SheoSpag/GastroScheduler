from datetime import timedelta

def build_prompt_for_area(branch, area, employees, weather_by_day, start_date):
    prompt = f"Generá los turnos semanales para el área **{area.name}** de la sucursal ubicada en **{branch.address}**, desde el lunes {start_date} hasta el domingo {start_date + timedelta(days=6)}.\n\n"

    prompt += "### Roles requeridos:\n"
    prompt += f"{area.roles}\n\n"

    prompt += "### Empleados y bloqueos:\n"
    for emp in employees:
        bloqueos = ", ".join(emp.get("blocks", [])) or "sin bloqueos"
        prompt += f"- {emp['name']}: {bloqueos}\n"
    
    prompt += "\n### Clima de la semana:\n"
    for i in range(7):
        date = start_date + timedelta(days=i)
        prompt += f"- {date.strftime('%A %d/%m/%Y')}: {weather_by_day.get(str(date), 'No disponible')}\n"

    prompt += """
    ### Consideraciones:
    - Si llueve, se espera menos clientela. Reducí la cantidad de personal si es posible.
    - Si hace buen clima (soleado), aumentá el personal disponible.
    - Repartí los turnos de forma justa entre los empleados.
    - Respetá los bloqueos.
    - Evitá sobrecargar a un mismo empleado todos los días  (Esto solo si es posible).
    - Cubrí todos los roles indicados por día y por turno (mañana, tarde, noche).

    ### Formato esperado:
    Fecha - Turno (mañana/tarde/noche) - Rol - Empleado  
    Ejemplo: 2025-07-14 - Mañana - Chef - Juan Pérez

    ### Al final:
    Explicá brevemente por qué hiciste esta distribución. Justificá cómo afectó el clima o los bloqueos a tu decisión.
    """
    return prompt
