from datetime import timedelta
from sqlalchemy.orm import Session
from app.crud.employee import calculate_emplyee_total_shift_hours
from app.crud.branch import get_branch, get_branch_employees, get_branch_areas
from app.exceptions.customError import CustomError
from app.utils.error_handler import handle_exception
import json
from services.ai_client import generate_shifts
from fastapi import status
from datetime import date, datetime


"""""
def build_weekly_shifts(branch_id: int, db: Session):
    try:
        branch = get_branch(db, branch_id)
        
        #Only 4 validation
        get_branch_employees(db, branch_id)
        get_branch_areas(db, branch_id)

        #ai_response = generate_shifts(generate_weekly_shift_prompt_for_area(branch))
        ai_response = generate_shifts(test_prompt(branch))
        print("AI response:", ai_response)
        shifts = json.loads(ai_response)
        
        return shifts
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            raise CustomError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="La IA devolvió una respuesta inválida")
                              
        handle_exception(e, "Interal error generating the shifts")

"""
    
def generate_weekly_shift_prompt_for_area(branch, db):
    start_date = get_next_monday()
    prompt = f"Generate all weekly shifts for the branch located at **{branch.address}**, from Monday {start_date} to Sunday {start_date + timedelta(days=6)}.\n"

    for area in branch.areas:
        prompt += f"\n### Area: {area.name} \n\n"
        
        prompt += f"- Opening time from {area.opening_time} to {area.closing_time}\n"
        prompt += f"- Minimum staff: {area.minimum_staff} | Maximum staff: {area.maximum_staff}\n\n"

        prompt += f"- Required roles: \n"
        for role in area.roles:
            prompt += f"\n  ## Role  {role.name}\n"
            prompt += "     - Eligible employees and their blocks:\n"
            for emp in role.employees:
                blocks = ", ".join(getattr(emp, 'blocks', [])) if hasattr(emp, 'blocks') else "no blocks"
                actual_shift_hours = calculate_emplyee_total_shift_hours(db, datetime.now().month, datetime.now().year, emp.id)
                prompt += f"       - {emp.name} | blocks: {blocks}\n"
                prompt += f"                         - {emp.monthly_hours} hours a month — Current month: {actual_shift_hours} hours assigned\n"
                prompt += f"                         - blocks: {blocks}\n"
    
    prompt += "\n---\n\n### Considerations:\n"

    prompt += """
    - Distribute shifts fairly among employees.
    - Respect the blocks (only if possible).
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
    
    ### EMPLOYEE WORKLOAD CONSTRAINTS:
• For each employee, provide:
    – Contracted hours per month.
    – Hours already worked this month.
• When generating shifts:
    1. Calculate remaining hours = contracted – worked.
    2. Assign shifts so the employee approaches—but does not exceed—their monthly target by more than 5–10 hours.
    3. Do not assign more than 40 hours per week per employee.

### DAYS OFF RULE:
• Each employee must have at least 2 full days off per week.
• Preferably, those days off are not consecutive unless required for coverage.

### ROTATION RULE:
• If a role has multiple eligible employees, assign in round-robin order.
• Balance total weekly hours when choosing among eligible employees.

    """
    print(prompt)
    return prompt

def build_weekly_shifts(branch_id: int, db: Session):
    try:
        branch = get_branch(db, branch_id)
        
        #Only 4 validation
        get_branch_employees(db, branch_id)
        get_branch_areas(db, branch_id)

        #ai_response = generate_shifts(generate_weekly_shift_prompt_for_area(branch))
        ai_response = generate_shifts(test_prompt(branch, db))
        print("AI response:", ai_response)
        shifts = json.loads(ai_response)
        
        return shifts
    except Exception as e:
        if isinstance(e, json.JSONDecodeError):
            raise CustomError(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="La IA devolvió una respuesta inválida")
                              
        handle_exception(e, "Interal error generating the shifts")

    
def test_prompt(branch, db):
    start_date = get_next_monday()
    end_date = start_date + timedelta(days=6)

    prompt = f"""
### OBJECTIVE:
Generate all weekly shift assignments for the following branch. Schedule from Monday {start_date} to Sunday {end_date}.

The goal is to:
- Cover all required roles within each area.
- Respect area schedules and staffing requirements.
- Assign employees fairly, respecting availability blocks (when possible).
- Output strictly in JSON format (see structure below).

---

### BRANCH CONFIGURATION:
Period: {start_date} to {end_date}
"""

    for area in branch.areas:
        prompt += f"""
---

### AREA: {area.name}

- Opening time: {area.opening_time}
- Closing time: {area.closing_time}
- Min staff: {area.minimum_staff}
- Max staff: {area.maximum_staff}

#### ROLES AND ELIGIBLE EMPLOYEES:
"""
        for role in area.roles:
            prompt += f"""  - Role: {role.name} | role_id: {role.id}
    Eligible Employees:
"""
            for emp in role.employees:
                blocks = ", ".join(getattr(emp, 'blocks', [])) if hasattr(emp, 'blocks') else "no blocks"
                actual_shift_hours = calculate_emplyee_total_shift_hours(db, datetime.now().month, datetime.now().year, emp.id)
                prompt += f"       - {emp.name} | id: {emp.id}\n"
                prompt += f"                         - {emp.monthly_hours} hours a month — Current month: {actual_shift_hours} hours assigned\n"
                prompt += f"                         - blocks: {blocks}\n"
    

    prompt += """
---

### CONSTRAINTS & CONSIDERATIONS:

- Distribute shifts fairly among employees.
- Prefer employees availability blocks when possible.
- Avoid assigning the same employee for full-week overload.
- Each area must meet its min/max staff limits per day.
- Each shift must fit within the area's opening/closing hours.

---

### OUTPUT FORMAT:

Respond ONLY with a JSON array in this format:

[
    {
        "start_date_time": "2025-07-14T08:00:00",
        "end_date_time": "2025-07-14T14:00:00",
        "date": "2025-07-14",
        "role_id": 1,
        "employee_id": 2
    }
]

### STRICT RULES:
- Do NOT include any explanations or surrounding text.
- ONLY return the JSON array.
- Ensure all fields are present and valid.
- Use ISO 8601 format for all date/time fields.

### EMPLOYEE WORKLOAD CONSTRAINTS:
• For each employee, provide:
    – Contracted hours per month.
    – Hours already worked this month.
• When generating shifts:
    1. Calculate remaining hours = contracted – worked.
    2. Assign shifts so the employee approaches—but does not exceed—their monthly target by more than 5–10 hours.
    3. Do not assign more than 40 hours per week per employee.

### DAYS OFF RULE:
• Each employee must have at least 2 full days off per week.
• Preferably, those days off are not consecutive unless required for coverage.

### ROTATION RULE:
• If a role has multiple eligible employees, assign in round-robin order.
• Balance total weekly hours when choosing among eligible employees.

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