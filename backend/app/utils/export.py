import pandas as pd
from datetime import datetime
from typing import List
from fastapi.responses import StreamingResponse
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from ..schemas.schedule import ScheduleWithAssignments


def export_schedule_to_excel(schedule: ScheduleWithAssignments):
    """Export schedule to Excel format"""
    
    # Create a DataFrame for the schedule
    data = []
    headers = ["Date", "Employee", "Shift Position", "Notes"]
    
    for assignment in schedule.assignments:
        data.append([
            assignment.date.strftime("%Y-%m-%d"),
            assignment.employee.name,
            f"Shift {assignment.shift_position}",
            assignment.notes or ""
        ])
    
    df = pd.DataFrame(data, columns=headers)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=f"Schedule {schedule.year}-{schedule.month:02d}", index=False)
    
    output.seek(0)
    
    # Return streaming response
    return StreamingResponse(
        io.BytesIO(output.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f"attachment; filename=schedule_{schedule.year}_{schedule.month:02d}.xlsx"
        }
    )


def export_schedule_to_pdf(schedule: ScheduleWithAssignments):
    """Export schedule to PDF format"""
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    
    # Add title
    title = Paragraph(f"Schedule: {schedule.name}", title_style)
    elements.append(title)
    
    # Add schedule info
    info_text = f"Year: {schedule.year}, Month: {schedule.month}, Status: {schedule.status}"
    info_para = Paragraph(info_text, styles['Normal'])
    elements.append(info_para)
    elements.append(Spacer(1, 20))
    
    # Group assignments by date
    assignments_by_date = {}
    for assignment in schedule.assignments:
        date_str = assignment.date.strftime("%Y-%m-%d")
        if date_str not in assignments_by_date:
            assignments_by_date[date_str] = []
        assignments_by_date[date_str].append(assignment)
    
    # Create table for each date
    for date_str in sorted(assignments_by_date.keys()):
        # Date header
        date_header = Paragraph(f"Date: {date_str}", styles['Heading2'])
        elements.append(date_header)
        elements.append(Spacer(1, 10))
        
        # Create table for this date
        table_data = [["Employee", "Shift Position", "Notes"]]
        
        for assignment in assignments_by_date[date_str]:
            table_data.append([
                assignment.employee.name,
                f"Shift {assignment.shift_position}",
                assignment.notes or ""
            ])
        
        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Return streaming response
    return StreamingResponse(
        io.BytesIO(buffer.getvalue()),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=schedule_{schedule.year}_{schedule.month:02d}.pdf"
        }
    )


def create_monthly_calendar_view(schedule: ScheduleWithAssignments):
    """Create a monthly calendar view of the schedule"""
    
    # Create calendar data
    calendar_data = []
    
    # Get all dates in the month
    import calendar
    _, last_day = calendar.monthrange(schedule.year, schedule.month)
    
    # Group assignments by date
    assignments_by_date = {}
    for assignment in schedule.assignments:
        date_str = assignment.date.strftime("%Y-%m-%d")
        if date_str not in assignments_by_date:
            assignments_by_date[date_str] = []
        assignments_by_date[date_str].append(assignment)
    
    # Create calendar view
    for day in range(1, last_day + 1):
        current_date = datetime(schedule.year, schedule.month, day).date()
        date_str = current_date.strftime("%Y-%m-%d")
        
        day_assignments = assignments_by_date.get(date_str, [])
        
        # Group by shift position
        shifts = {}
        for assignment in day_assignments:
            shift_pos = assignment.shift_position
            if shift_pos not in shifts:
                shifts[shift_pos] = []
            shifts[shift_pos].append(assignment.employee.name)
        
        # Create shift summary
        shift_summary = []
        for shift_pos in sorted(shifts.keys()):
            employees = ", ".join(shifts[shift_pos])
            shift_summary.append(f"Shift {shift_pos}: {employees}")
        
        calendar_data.append({
            "date": current_date,
            "day": day,
            "assignments": day_assignments,
            "shift_summary": shift_summary
        })
    
    return calendar_data 