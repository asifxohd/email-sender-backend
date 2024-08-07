import os
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage
from django.conf import settings
from .serializers import FileUploadSerializer


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            self.process_file(file)
            return Response({"message": "Emails sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_file(self, file):
        df = pd.read_excel(file)
        subject = 'Job Application: Full Stack Developer'
        resume_path = '/Users/asifxohd/Desktop/EmailSender/sendmailview/files/Muhammed Asif Resume.pdf'
        
        for index, row in df.iterrows():
            to_address = row['Email']
            body = f"""
            Dear {row['Name']},

            I am writing to express my interest in the Full Stack Developer position at your company. 
            Please find attached my resume and cover letter for your consideration.

            Best regards,
            Muhammed Asif
            """

            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [to_address]
            )
            email.attach_file(resume_path)
            email.send()
