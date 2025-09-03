from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import os

from .models import PDFDocument, CardSettings
from .forms import PDFUploadForm, CardSettingsForm

@method_decorator([login_required, staff_member_required, csrf_protect], name='dispatch')
class AddFileView(View):
    def get(self, request):
        form = PDFUploadForm()
        return render(request, 'documents/add_file.html', {'form': form})

    def post(self, request):
        print("=== UPLOAD DEBUG START ===")
        print(f"User: {request.user}")
        print(f"Is staff: {request.user.is_staff}")
        print(f"POST data: {request.POST}")
        print(f"FILES data: {request.FILES}")
        print(f"Media root: {settings.MEDIA_ROOT}")

        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid():
            print("✅ Form is valid")

            pdf_document = form.save(commit=False)
            pdf_document.uploaded_by = request.user

            print(f"Before save - Title: {pdf_document.title}")
            print(f"Before save - Parent Card: {pdf_document.parent_card_id}")
            print(f"Before save - Subcard: {pdf_document.subcard_id}")
            print(f"Before save - File: {pdf_document.pdf_file}")

            pdf_document.save()

            print(f"✅ Document saved with ID: {pdf_document.id}")
            print(f"File path: {pdf_document.pdf_file.path}")
            print(f"File URL: {pdf_document.pdf_file.url}")
            print(f"File exists: {os.path.exists(pdf_document.pdf_file.path)}")

            messages.success(request, f'File "{pdf_document.title}" uploaded successfully!')
            return redirect('dashboard:admin_dashboard')
        else:
            print("❌ Form is NOT valid")
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                print(f"Field '{field}' errors: {errors}")

        print("=== UPLOAD DEBUG END ===")
        return render(request, 'documents/add_file.html', {'form': form})

@method_decorator([login_required, staff_member_required, csrf_protect], name='dispatch')
class CardSettingsView(View):
    def get(self, request):
        settings_obj = CardSettings.get_settings()
        form = CardSettingsForm(instance=settings_obj)
        return render(request, 'documents/card_settings.html', {'form': form, 'settings': settings_obj})

    def post(self, request):
        settings_obj = CardSettings.get_settings()
        form = CardSettingsForm(request.POST, instance=settings_obj)

        if form.is_valid():
            form.save()
            messages.success(request, 'Card settings updated successfully!')
            return redirect('dashboard:admin_dashboard')

        return render(request, 'documents/card_settings.html', {'form': form, 'settings': settings_obj})

@login_required
def view_pdf(request, document_id):
    document = get_object_or_404(PDFDocument, id=document_id)

    try:
        with open(document.pdf_file.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{document.get_filename()}"'
            return response
    except FileNotFoundError:
        raise Http404("PDF file not found")

@login_required
def download_pdf(request, document_id):
    document = get_object_or_404(PDFDocument, id=document_id)

    try:
        with open(document.pdf_file.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{document.get_filename()}"'
            return response
    except FileNotFoundError:
        raise Http404("PDF file not found")

@login_required
@staff_member_required
def delete_pdf(request, document_id):
    document = get_object_or_404(PDFDocument, id=document_id)

    if request.method == 'POST':
        title = document.title
        document.delete()
        messages.success(request, f'File "{title}" deleted successfully!')

    return redirect('dashboard:admin_dashboard')

@login_required
@staff_member_required
@csrf_protect
def delete_subcard(request, parent_id, subcard_id):
    if request.method == 'POST':
        docs_to_delete = PDFDocument.objects.filter(parent_card_id=parent_id, subcard_id=subcard_id)
        count = docs_to_delete.count()
        docs_to_delete.delete()
        messages.success(request, f"Deleted {count} document(s) under Parent {parent_id} / Subcard {subcard_id}.")
    return redirect('dashboard:admin_dashboard')