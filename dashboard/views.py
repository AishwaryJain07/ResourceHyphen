from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views import View
from collections import defaultdict

from documents.models import PDFDocument

@method_decorator(login_required, name='dispatch')
class UserDashboardView(View):
    def get(self, request):
        documents = PDFDocument.objects.all().order_by('parent_card_id', 'subcard_id', '-uploaded_at')
        
        organized_docs = defaultdict(lambda: defaultdict(list))
        for doc in documents:
            organized_docs[doc.parent_card_id][doc.subcard_id].append(doc)
        
        organized_docs = dict(organized_docs)
        for parent_id in organized_docs:
            organized_docs[parent_id] = dict(organized_docs[parent_id])
        
        # Get recent PDFs for display
        recent_pdfs = PDFDocument.objects.all().order_by('parent_card_id', 'subcard_id','-uploaded_at')
        
        context = {
            'organized_docs': organized_docs,
            'parent_cards': range(1, 11),
            'subcards': range(1, 11),
            'recent_pdfs': recent_pdfs,
            'is_admin': False,
        }
        
        return render(request, 'dashboard/user_dashboard.html', context)

@method_decorator([login_required, staff_member_required], name='dispatch')
class AdminDashboardView(View):
    def get(self, request):
        documents = PDFDocument.objects.all().order_by('parent_card_id', 'subcard_id', '-uploaded_at')
        
        organized_docs = defaultdict(lambda: defaultdict(list))
        for doc in documents:
            organized_docs[doc.parent_card_id][doc.subcard_id].append(doc)
        
        organized_docs = dict(organized_docs)
        for parent_id in organized_docs:
            organized_docs[parent_id] = dict(organized_docs[parent_id])
        
        # Get recent PDFs for display
        recent_pdfs = PDFDocument.objects.all().order_by('parent_card_id', 'subcard_id','-uploaded_at')
        
        context = {
            'organized_docs': organized_docs,
            'parent_cards': range(1, 11),
            'subcards': range(1, 11),
            'recent_pdfs': recent_pdfs,
            'is_admin': True,
        }
        
        return render(request, 'dashboard/admin_dashboard.html', context)