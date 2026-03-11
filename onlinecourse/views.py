from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, Enrollment, Question, Choice, Submission


@login_required
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    context = {
        'course': course
    }

    return render(
        request,
        'onlinecourse/course_details_bootstrap.html',
        context
    )


@login_required
def submit(request, course_id):

    course = get_object_or_404(Course, pk=course_id)

    enrollment = Enrollment.objects.get(
        user=request.user,
        course=course
    )

    # get selected answers
    selected_choices = request.POST.getlist('choice')

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        submission.choices.add(choice)

    return show_exam_result(request, course_id)


@login_required
def show_exam_result(request, course_id):

    course = get_object_or_404(Course, pk=course_id)

    enrollment = Enrollment.objects.get(
        user=request.user,
        course=course
    )

    submission = Submission.objects.filter(
        enrollment=enrollment
    ).last()

    # selected choices
    selected_ids = submission.choices.values_list(
        'id',
        flat=True
    )

    questions = Question.objects.filter(
        lesson__course=course
    )

    total_score = 0
    possible_score = len(questions)

    for question in questions:
        if submission.is_get_score(question):
            total_score += 1

    grade = round((total_score / possible_score) * 100, 2)

    context = {
        'course': course,
        'grade': grade,
        'score': total_score,
        'possible': possible_score,
        'selected_ids': selected_ids,
        'questions': questions
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
