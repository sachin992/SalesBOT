# views.py
import re
import sqlparse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection

import os
import openai
import sqlparse
from openai import OpenAI

openai.api_key = "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"


# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ChatMessage
from .serializers import UserSerializer, ChatMessageSerializer

# -----------------------------
# User Registration
# -----------------------------
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------
# User Login
# -----------------------------
# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")
#         user = authenticate(username=username, password=password)
#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "token": str(refresh.access_token),
#                 "username": user.username
#             })
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            print(str(refresh.access_token))
            print(str(refresh))
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username
            })

        return Response({"error": "Invalid credentials"}, status=401)






# -----------------------------
# Save & fetch chat messages
# -----------------------------
class ChatView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        messages = ChatMessage.objects.filter(user=request.user).order_by("timestamp")
        serializer = ChatMessageSerializer(messages, many=True)
        return Response({"messages": serializer.data})

    def post(self, request):
        messages = request.data.get("messages", [])
        saved_messages = []
        for msg in messages:
            chat = ChatMessage.objects.create(
                user=request.user,
                role=msg.get("role"),
                content=msg.get("content")
            )
            saved_messages.append(chat)
        serializer = ChatMessageSerializer(saved_messages, many=True)
        return Response(serializer.data)









# -------------------------------
# 1️⃣ Clean SQL output
# -------------------------------
def clean_sql(sql_text: str) -> str:
    """Remove code fences, markdown, backticks, and extra whitespace."""
    sql_text = re.sub(r"```.*?```", "", sql_text, flags=re.DOTALL)
    sql_text = re.sub(r"^(sql|SQL|Sql)[:\n]*", "", sql_text).strip()
    sql_text = sql_text.replace("```", "").strip()
    return sql_text

# -------------------------------
# 2️⃣ Ensure only SELECT statements
# -------------------------------
def is_select_only(sql_text: str) -> bool:
    """Check SQL contains only SELECT statements."""
    parsed = sqlparse.parse(sql_text)
    if not parsed:
        return False
    stmt = parsed[0]
    for token in stmt.tokens:
        if token.ttype in sqlparse.tokens.DML and token.value.lower() != "select":
            return False
    return True

# -------------------------------
# 3️⃣ Verify tables/columns exist in schema
# -------------------------------
def validate_tables_columns(sql_text: str, schema_text: str) -> bool:
    """Check that all tables referenced exist in schema."""
    schema_lower = schema_text.lower()
    # Basic table check
    tables = re.findall(r"from\s+([`]?[\w]+[`]?)", sql_text, re.IGNORECASE)
    for t in tables:
        t_clean = t.replace("`", "").lower()
        if t_clean not in schema_lower:
            return False
    return True


openai.api_key = "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"



# Create client once
client = OpenAI(api_key=openai.api_key)


# -------------------------------
# 4️⃣ Execute SQL safely
# -------------------------------
def execute_sql(sql_text: str):
    with connection.cursor() as cursor:
        cursor.execute(sql_text)
        columns = [col[0] for col in cursor.description] if cursor.description else []
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
    return {"columns": columns, "rows": data}

# -------------------------------
# 5️⃣ Generate deterministic SQL with strict instructions
# -------------------------------
def generate_sql(schema_text: str, nl_query: str) -> str:
    system_prompt = f"""
You are an expert SQL generator for a MySQL sales database.

Rules:
1. ONLY generate SELECT statements. Do NOT generate INSERT, UPDATE, DELETE, DROP, or any other statements.
2. Use ONLY tables and columns from the schema below. Do NOT invent tables or columns.
3. Return ONLY the SQL query. NO explanation, comments, or extra text.
4. If the user question cannot be answered with the schema, return: SELECT NULL AS result;

Schema:
{schema_text}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": nl_query}
        ],
        temperature=0,  # deterministic
        max_tokens=300
    )
    sql_text = response.choices[0].message.content.strip()
    return clean_sql(sql_text)


import os


SCHEMA_CACHE_FILE = os.path.join(os.path.dirname(__file__), "cached_schema.txt")

def load_cached_schema_text():
    if not os.path.exists(SCHEMA_CACHE_FILE):
        raise FileNotFoundError("Schema cache not found. Run schema_ingest.py first.")
    
    with open(SCHEMA_CACHE_FILE, "r") as f:
        return f.read()


# -------------------------------
# 6️⃣ API View
# -------------------------------
@api_view(['POST'])
def query_view(request):
    nl_query = request.data.get("user_prompt", "")
    if not nl_query:
        return Response({"error": "Empty prompt"}, status=400)

    schema_text = load_cached_schema_text()

    sql_text = generate_sql(schema_text, nl_query)

    # Validate SQL
    if not is_select_only(sql_text):
        return Response({"error": "Non-SELECT statement generated", "sql": sql_text}, status=400)
    if not validate_tables_columns(sql_text, schema_text):
        return Response({"error": "SQL references unknown tables/columns", "sql": sql_text}, status=400)

    try:
        result = execute_sql(sql_text)
    except Exception as e:
        return Response({"error": str(e), "sql": sql_text}, status=500)

    return Response({"sql": sql_text, "result": result})
