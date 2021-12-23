from os import times, path
import os
from typing import List
from django.db.models.base import Model
from django.db.models.fields import BooleanField
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, FileResponse
from django.views.generic import (
    DetailView,
    CreateView,
)
import io
from datetime import date
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus.tables import TableStyle
from .models import Invoice
from .forms import InvoiceModelForm
from hospitals.models import Hospital
from timesheet.models import Timesheet

def get_invoice_total(timesheets):
    invoice_total = 0
    for item in timesheets:
        invoice_total += item.get_daily_total_earned()
    return invoice_total

# Create your views here.
@login_required
def invoice_detail_view(request, id):
    if request.method == 'GET':
        template_name = 'invoices/invoice_detail.html'
        invoice = get_object_or_404(Invoice, id=id)
        timesheets = invoice.timesheet_set.all()

        invoice_total = get_invoice_total(timesheets)

        return render(request, template_name, {
            'object': invoice, 
            'object_list': timesheets,
            'invoice_total': invoice_total,
            })

@login_required
def invoice_create_view(request, *args, **kwargs):
    template_name = 'invoices/invoice_create.html'
    
    if request.method == 'POST':
        form = InvoiceModelForm(request.POST or None)
        form.fields['hospital_name'].queryset = Hospital.objects.filter(username=request.user) # Doesn't cause multiple hospital error
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username = request.user
            obj.invoice_number = obj.create_invoice_number()
            obj.save()           

            # Attach the invoice ID (not invoice number) to the timesheet items
            timesheets = Timesheet.objects.filter(
                hospital_name=obj.hospital_name, 
                date_worked__range=[obj.date_from, obj.date_to], 
                invoice_number=None,
                )
            timesheets.update(invoice_number=obj.id)

            # Update the max_invoice_number with the hospital in order to create an invoice number
            hospital = Hospital.objects.get(
                name=obj.hospital_name,
                username = request.user
            )
            current_invoice_number = hospital.max_invoice_number
            hospital.save()

            form = InvoiceModelForm()
            
        return HttpResponseRedirect('/invoice/' + str(obj.id))
    else:
        form = InvoiceModelForm()
        form.fields['hospital_name'].queryset = Hospital.objects.filter(username=request.user)
    
    return render(request, template_name, {'form': form})  

@login_required
def invoice_list_view(request, *args, **kwargs):
    template_name = 'invoices/invoice_list.html'
    queryset = Invoice.objects.filter(username=request.user)
    context = {'object_list': queryset}
    return render(request, template_name, context)

@login_required
def invoice_pdf_view(request, id):
    LEFT_MARGIN = 20
    RIGHT_MARGIN = 610

    # Add timesheet line items
    invoice = get_object_or_404(Invoice, id=id)
    timesheets = invoice.timesheet_set.all()

    # Get hospital info
    hospital_info = get_object_or_404(Hospital, name=timesheets[0].hospital_name)

    # Register Calibri font
    pdfmetrics.registerFont(TTFont('Calibri', 'calibri-regular.ttf'))
    pdfmetrics.registerFont(TTFont('Calibri-Bold', 'calibri-bold.ttf'))

    # Create Bytestream buffer
    buffer = io.BytesIO()

    # Create a canvas
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)

    # Invoice Header
    pdf_canvas.setFont('Calibri-Bold', 48)
    pdf_canvas.drawString(LEFT_MARGIN, 740, 'Invoice')

    pdf_canvas.setFont('Calibri', 11)
    pdf_canvas.drawString(RIGHT_MARGIN - 120, 755, 'Date: ' + str(date.today()))
    pdf_canvas.drawString(RIGHT_MARGIN - 120, 740, 'Invoice # ' + invoice.invoice_number)

    # Mail To Info
    MAIL_AND_BILLING_Y_LOC = 710
    pdf_canvas.setFont('Calibri-Bold', 11)
    pdf_canvas.drawString(LEFT_MARGIN, MAIL_AND_BILLING_Y_LOC, "Mailing Info")
    pdf_canvas.line(LEFT_MARGIN + 70, MAIL_AND_BILLING_Y_LOC + 10, LEFT_MARGIN + 70, MAIL_AND_BILLING_Y_LOC - 60)

    pdf_canvas.setFont('Calibri', 11)
    pdf_canvas.drawString(LEFT_MARGIN + 75, MAIL_AND_BILLING_Y_LOC, hospital_info.name) 
    pdf_canvas.drawString(LEFT_MARGIN + 75, MAIL_AND_BILLING_Y_LOC - 15, hospital_info.address) 
    pdf_canvas.drawString(LEFT_MARGIN + 75, MAIL_AND_BILLING_Y_LOC - 30, hospital_info.city + ', ' + hospital_info.state + ' ' + hospital_info.zip_code) 
    pdf_canvas.drawString(LEFT_MARGIN + 75, MAIL_AND_BILLING_Y_LOC - 45, 'Phone #: ' + hospital_info.telephone) 
    pdf_canvas.drawString(LEFT_MARGIN + 75, MAIL_AND_BILLING_Y_LOC - 60, 'Email: ' + hospital_info.email) 

    # Billing Info
    pdf_canvas.setFont('Calibri-Bold', 11)
    pdf_canvas.drawString(LEFT_MARGIN + 306, MAIL_AND_BILLING_Y_LOC, "Billing Info")
    pdf_canvas.line(LEFT_MARGIN + 376, MAIL_AND_BILLING_Y_LOC + 10, LEFT_MARGIN + 376, MAIL_AND_BILLING_Y_LOC - 60)

    pdf_canvas.setFont('Calibri', 11)
    pdf_canvas.drawString(LEFT_MARGIN + 381, MAIL_AND_BILLING_Y_LOC, request.user.profile.company_name) 
    pdf_canvas.drawString(LEFT_MARGIN + 381, MAIL_AND_BILLING_Y_LOC - 15, request.user.profile.address) 
    pdf_canvas.drawString(LEFT_MARGIN + 381, MAIL_AND_BILLING_Y_LOC - 30, request.user.profile.city + ', ' + request.user.profile.state + ' ' + request.user.profile.zip_code) 
    pdf_canvas.drawString(LEFT_MARGIN + 381, MAIL_AND_BILLING_Y_LOC - 45, 'Phone #: ' + request.user.profile.telephone) 
    pdf_canvas.drawString(LEFT_MARGIN + 381, MAIL_AND_BILLING_Y_LOC - 60, 'Email: ' + request.user.profile.email) 
    
    # Invoice Body
    pdf_canvas.setFont('Calibri', 11)

    # Column Headings
    date_heading = 'Date'
    clock_in_heading = 'Clock In'
    clock_out_lunch_heading = 'Lunch Out'
    clock_in_lunch_heading = 'Lunch In'
    clock_out_heading = 'Clock Out'
    hours_worked_heading = 'Hours Worked'
    hourly_rate_heading = 'Hourly Rate'
    bonus_heading = 'Bonus'
    daily_total_heading = 'Daily Total'

    lines = [[date_heading, clock_in_heading, clock_out_lunch_heading, clock_in_lunch_heading, clock_out_heading, hours_worked_heading, hourly_rate_heading, bonus_heading, daily_total_heading]]
    for timesheet in timesheets:
        lines.append(
            (
                timesheet.date_worked, 
                timesheet.clock_in, 
                timesheet.clock_out_lunch, 
                timesheet.clock_in_lunch, 
                timesheet.clock_out, 
                timesheet.total_hours_worked, 
                timesheet.hourly_rate, 
                '{0: <2}'.format('$') + '{0: >7}'.format(str(timesheet.bonus_amount)), 
                '{0: <2}'.format('$') + '{0: >7}'.format(str(timesheet.get_daily_total_earned()))
            )
        )

    timesheet_table = Table(lines)
    timesheet_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (1000, 1000), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('FONT', (0, 0), (10, 0), 'Calibri-Bold'), # Bolds the column headers
        ('FONT', (0,1), (-1, -1), 'Calibri'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (7, 1), (-1, -1), 'RIGHT'), # Right align the last 2 columns (Bonus and Total Daily Amount)
        ('LINEBELOW', (0, 0), (10,0), 2, colors.black)
    ]))
    elements = []
    elements.append(timesheet_table)

    timesheet_table.wrapOn(pdf_canvas, 0, MAIL_AND_BILLING_Y_LOC - 220)
    timesheet_table.drawOn(pdf_canvas, LEFT_MARGIN, MAIL_AND_BILLING_Y_LOC - 220)

    # Invoice Footer
    pdf_canvas.setLineWidth(2)
    pdf_canvas.line(LEFT_MARGIN, 100, 580, 100)
    pdf_canvas.drawString(LEFT_MARGIN, 85, 'Thank you for your business!')
    pdf_canvas.drawString(LEFT_MARGIN, 65, 'Please make checks payable to ' + request.user.profile.company_name)
    pdf_canvas.drawString(400, 85, 'Total:')
    pdf_canvas.drawString(515, 85, '{0: <2}'.format('$') + '{0: >7}'.format(str(get_invoice_total(timesheets))))

    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=invoice.invoice_number)