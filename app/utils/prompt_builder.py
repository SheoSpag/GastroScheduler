from datetime import timedelta
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.crud.branch import get_branch
from app.crud.employee import get_all_employees
from services.ai_client import generate_shifts
from itertools import chain
import json



def build_weekly_shifts(branch_id: int, db: Session):
    
    branch = get_branch(db, branch_id)
    employees = get_all_employees(db)

    shifts = []
    
    for area in branch.areas:
        shifts.append(json.loads(generate_shifts(generate_weekly_shift_prompt_for_area(branch, area, employees))))
    
    
    return list(chain.from_iterable(shifts))
    
def generate_weekly_shift_prompt_for_area(branch, area, employees):
    start_date = get_next_monday()
    prompt = f"Generá los turnos semanales para el área **{area.name}** de la sucursal ubicada en **{branch.address}**, desde el lunes {start_date} hasta el domingo {start_date + timedelta(days=6)}.\n\n"

    prompt += "### Roles requeridos:\n"
    prompt += "\n".join(f"- {role.name}" for role in area.roles) + "\n\n"

    prompt += "### Empleados y bloqueos:\n"
    for emp in employees:
        bloqueos = ", ".join(getattr(emp, "blocks", [])) if hasattr(emp, "blocks") else "sin bloqueos"
        prompt += f"- {emp.name}: {bloqueos}\n"


    prompt += "\n---\n### Consideraciones:\n"

    prompt += """
    - Repartí los turnos de forma justa entre los empleados.
    - Respetá los bloqueos.
    - Evitá sobrecargar a un mismo empleado todos los días  (Esto solo si es posible).
    - Tene en cuenta tanto los horarios de apertura y cierre como la cantidad minima y maxima establecida en las areas
    
    ### Formato esperado:

    Respondé únicamente con un array JSON que contenga objetos con esta estructura:

    [

        {
            "start_date_time": "2025-07-14T08:00:00",
            "end_date_time": "2025-07-14T14:00:00",
            "date": "2025-07-14",
            "role_id": 1,
            "employee_id": 2
        },
        ...
    ]

    Asegurate de que:
    - Todos los campos estén presentes.
    - Las fechas y horas estén en formato ISO 8601 (YYYY-MM-DD y HH:MM:SS).
    - El array no esté envuelto en ningún texto adicional, ni explicaciones.


    """
    
    return prompt



def get_next_monday(from_date=None):
    if from_date is None:
        from_date = date.today()
    days_ahead = 0 - from_date.weekday() + 7  # 0 = lunes
    
    if days_ahead <= 0:
        days_ahead += 7
    return from_date + timedelta(days=days_ahead)