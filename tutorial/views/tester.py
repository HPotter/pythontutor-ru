from json import dumps

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from tutorial.models import Problem, Submission
from tutorial.tester import run_test


def tester_submit(request):
    if 'user_code' not in request.POST or 'problem' not in request.POST:
        return HttpResponseBadRequest()

    problem = Problem.objects.get(urlname=request.POST['problem'])

    result = {
        'status': 'ok',
        'tests': [],
    }

    test_id = 0
    for test in problem.tests:
        test_result = run_test(request.POST['user_code'], test['input'], test['answer'])
        test_status = test_result.verdict_status()

        if test_status != 'ok' and result['status'] == 'ok':
            result['status'] = 'error'
            result['fail_test'] = test_id

        result['tests'].append(test_status)

        test_id += 1

    if request.user.get_profile().course and request.user.get_profile().course.get_ok_ac_policy_display() == 'use_accepted_instead_of_ok':
        if result['status'] == 'ok':
            result['status'] = 'accepted'

    submission = Submission(
        problem=problem,
        code=request.POST['user_code'],
        user=request.user,
        status={v: k for k, v in Submission.STATUS_CHOICES}[result['status']]
    )
    submission.save()

    return HttpResponse(dumps(result), content_type='application/json')
