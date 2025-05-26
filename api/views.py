from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, permissions
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404
import google.generativeai as genai
from django.conf import settings
from PyPDF2 import PdfReader


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HelloView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": f"Hello {request.user.username}!"})

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Document.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        doc_file = self.request.FILES.get('file')
        extracted_text = ""
        if doc_file and doc_file.name.lower().endswith('.pdf'):
            try:
                pdf_reader = PdfReader(doc_file)
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text()
            except Exception as e:
                extracted_text = f"Error extracting PDF text: {e}"
        # (You can add handling for .txt, .docx, images with OCR, etc.)
        serializer.save(owner=self.request.user, extracted_text=extracted_text)

class AskQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        doc_id = request.data.get('doc_id')
        question = request.data.get('question')
        if not doc_id or not question:
            return Response({'error': 'doc_id and question are required'}, status=400)
        doc = get_object_or_404(Document, pk=doc_id, owner=request.user)
        if not doc.extracted_text:
            return Response({'error': 'No extracted text found for this document'}, status=400)
        # Use Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        prompt = f"Document text: {doc.extracted_text}\n\nQuestion: {question}\nAnswer:"
        try:
            response = model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            answer = f"Error: {str(e)}"
        return Response({'answer': answer})