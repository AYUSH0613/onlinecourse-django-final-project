from django.shortcuts import render
from .models import Course, Submission, Choice

def submit(request, course_id):

    course = Course.objects.get(id=course_id)

    selected_choices = request.POST.getlist('choice')

    submission = Submission.objects.create()

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)

    return render(request, 'exam_result.html', {'course': course})


def show_exam_result(request, course_id):

    course = Course.objects.get(id=course_id)

    submissions = Submission.objects.all()

    score = 0

    for submission in submissions:
        for choice in submission.choices.all():
            if choice.is_correct:
                score += 1

    context = {
        'course': course,
        'score': score
    }

    return render(request, 'exam_result.html', context)
