from datetime import timedelta
from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import status
from app.crud.branch import get_branch
from services.ai_client import generate_shifts
from app.crud.branch import get_branch_areas, get_branch_employees
from app.exceptions.customError import CustomError
from app.utils.error_handler import handle_exception
import json



def build_weekly_shifts(branch_id: int, db: Session):
    try:
        branch = get_branch(db, branch_id)
        
        #Only 4 validation
        get_branch_employees(db, branch_id)
        get_branch_areas(db, branch_id)

        ai_response = generate_shifts(generate_weekly_shift_prompt_for_area(branch))
        shifts = json.loads(ai_response)
        
        return shifts
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            raise CustomError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="La IA devolvió una respuesta inválida")
                              
        handle_exception(e, "Interal error generating the shifts")

    
def generate_weekly_shift_prompt_for_area(branch):
    start_date = get_next_monday()
    prompt = f"Generá todos los turnos semanales para la sucursal ubicada en **{branch.address}**, desde el lunes {start_date} hasta el domingo {start_date + timedelta(days=6)}.\n\n"

    for area in branch.areas:
        prompt += f"### Area: {area.name} \n\n"

        prompt += f"- Roles requeridos: \n"
        for role in area.roles:
            prompt += f"\n### Role  {role.name}\n"
            prompt += "     - Empleados habilitados y sus bloqueos:\n"
            for emp in role.employees:
                bloqueos = ", ".join(getattr(emp, "blocks", [])) if hasattr(emp, "blocks") else "sin bloqueos"
                prompt += f"       - {emp.name} | bloqueos: {bloqueos}\n"
    
    prompt += "\n---\n\n### Consideraciones:\n"

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
    
    print(prompt)
    
    return prompt



def get_next_monday(from_date=None):
    if from_date is None:
        from_date = date.today()
    days_ahead = 0 - from_date.weekday() + 7  # 0 = lunes
    
    if days_ahead <= 0:
        days_ahead += 7
    return from_date + timedelta(days=days_ahead)