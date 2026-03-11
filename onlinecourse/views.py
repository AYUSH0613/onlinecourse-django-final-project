from django.shortcuts import render, get_object_or_404
from .models import Course, Enrollment, Submission, Choice, Question


def submit(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)

    selected_choices = request.POST.getlist('choice')

    submission = Submission.objects.create(enrollment=enrollment)

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)

    return show_exam_result(request, course_id)


def show_exam_result(request, course_id):

    course = get_object_or_404(Course, pk=course_id)
    enrollment = Enrollment.objects.get(user=request.user, course=course)
    submission = Submission.objects.filter(enrollment=enrollment).last()

    questions = Question.objects.filter(lesson__course=course)

    total_score = 0
    possible_score = len(questions)

    for question in questions:
        if submission.is_get_score(question):
            total_score += 1

    grade = (total_score / possible_score) * 100

    context = {
        'course': course,
        'grade': grade,
        'possible': possible_score,
        'score': total_score
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
