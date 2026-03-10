from django.shortcuts import render

def submit(request, course_id):
    return render(request, "exam_result.html")

def show_exam_result(request, course_id):
    return render(request, "exam_result.html")
