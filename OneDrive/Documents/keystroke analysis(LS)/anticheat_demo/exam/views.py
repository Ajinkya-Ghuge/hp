import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import Submission
from .utils import analyze_keystrokes

def exam_page(request):
    if request.method == "POST":
        answer = request.POST.get("answer", "")
        start_time = request.POST.get("start_time", "0")
        end_time = request.POST.get("end_time", "0")
        keystroke_raw = request.POST.get("keystroke_data", "")

        # Debug: if JS didn't send data, still show something
        if not keystroke_raw:
            return HttpResponse("No keystroke data received from frontend!")

        try:
            keystroke_data = json.loads(keystroke_raw)
        except Exception as e:
            return HttpResponse(f"JSON parse error: {e}<br>Raw: {keystroke_raw}")

        risk = analyze_keystrokes(keystroke_data, start_time, end_time, answer)

        Submission.objects.create(
            answer=answer,
            keystroke_data=keystroke_data,
            start_time=int(start_time) if start_time.isdigit() else 0,
            end_time=int(end_time) if end_time.isdigit() else 0,
            risk_score=risk
        )

        # 🔥 Always show something (no blank page possible)
        return render(request, "result.html", {"risk": risk})

    return render(request, "exam.html")