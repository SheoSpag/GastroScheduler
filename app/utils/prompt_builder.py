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
    prompt = f"Generate all weekly shifts for the branch located at **{branch.address}**, from Monday {start_date} to Sunday {start_date + timedelta(days=6)}.\n\n"

    for area in branch.areas:
        prompt += f"### Area: {area.name} \n\n"

        prompt += f"- Required roles: \n"
        for role in area.roles:
            prompt += f"\n### Role  {role.name}\n"
            prompt += "     - Eligible employees and their blocks:\n"
            for emp in role.employees:
                blocks = ", ".join(getattr(emp, 'blocks', [])) if hasattr(emp, 'blocks') else "no blocks"
                prompt += f"       - {emp.name} | blocks: {blocks}\n"
    
    prompt += "\n---\n\n### Considerations:\n"

    prompt += """
    - Distribute shifts fairly among employees.
    - Respect the blocks.
    - Avoid overloading the same employee every day (only if possible).
    - Take into account both the opening and closing hours as well as the minimum and maximum staff required per area.
    
    ### Expected format:

    Respond only with a JSON array containing objects with the following structure:

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

    IMPORTANT: ONLY return the JSON array, no text, no explanations, no extra characters.  
    Date and datetime fields must be in ISO format.

    Make sure that:
    - All fields are present.
    - Dates and times are in ISO 8601 format (YYYY-MM-DD and HH:MM:SS).
    - The array is not wrapped in any extra text or explanations.

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