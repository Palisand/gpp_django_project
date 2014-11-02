from django.shortcuts import render
from gpp_search import run_query
from math import ceil

AGENCIES = ['Aging', 'Buildings', 'Campaign Finance', 'Children\'s Services', 'City Council', 'City Clerk', 'City Planning', 'Citywide Admin Svcs', 'Civilian Complaint', 'Comm - Police Corr', 'Community Assistance', 'Comptroller', 'Conflicts of Interest', 'Consumer Affairs', 'Contracts', 'Correction', 'Criminal Justice Coordinator', 'Cultural Affairs', 'DOI - Investigation', 'Design/Construction', 'Disabilities', 'District Atty, NY County', 'Districting Commission', 'Domestic Violence', 'Economic Development', 'Education, Dept. of', 'Elections, Board of', 'Emergency Mgmt.', 'Employment', 'Empowerment Zone', 'Environmental - DEP', 'Environmental - OEC', 'Environmental - ECB', 'Equal Employment', 'Film/Theatre', 'Finance', 'Fire', 'FISA', 'Health and Mental Hyg.', 'HealthStat', 'Homeless Services', 'Hospitals - HHC', 'Housing - HPD', 'Human Rights', 'Human Rsrcs - HRA', 'Immigrant Affairs', 'Independent Budget', 'Info. Tech. and Telecom.', 'Intergovernmental', 'International Affairs', 'Judiciary Committee', 'Juvenile Justice', 'Labor Relations', 'Landmarks', 'Law Department', 'Library - Brooklyn', 'Library - New York', 'Library - Queens', 'Loft Board', 'Management and Budget', 'Mayor', 'Metropolitan Transportation Authority', 'NYCERS', 'Operations', 'Parks and Recreation', 'Payroll Administration', 'Police', 'Police Pension Fund', 'Probation', 'Public Advocate', 'Public Health', 'Public Housing-NYCHA', 'Records', 'Rent Guidelines', 'Sanitation', 'School Construction', 'Small Business Svcs', 'Sports Commission', 'Standards and Appeal', 'Tax Appeals Tribunal', 'Tax Commission', 'Taxi and Limousine', 'Transportation', 'Trials and Hearings', 'Veterans - Military', 'Volunteer Center', 'Voter Assistance', 'Youth & Community']
CATEGORIES = ['Business and Consumers', 'Cultural/Entertainment', 'Education', 'Environment', 'Finance and Budget', 'Government Policy', 'Health', 'Housing and Buildings', 'Human Services', 'Labor Relations', 'Public Safety', 'Recreation/Parks', 'Sanitation', 'Technology', 'Transportation']
TYPES = ['Annual Report', 'Audit Report', 'Bond Offering - Official Statements', 'Budget Report', 'Consultant Report', 'Guide - Manual', 'Hearing - Minutes', 'Legislative Document', 'Memoranda - Directive', 'Press Release', 'Serial Publication', 'Staff Report', 'Report']


def index(request):
    request.session['query'] = ''

    context_dict = {'agencies': AGENCIES,
                    'categories': CATEGORIES,
                    'types': TYPES}

    return render(request, 'gpp/index.html', context_dict)


def results(request):
    # set initial values
    if 'query' not in request.session:
        request.sessionp['query'] = ''
    if 'size' not in request.session:
        request.session['size'] = 10
    if 'num_pages' not in request.session:
        request.session['num_pages'] = 0
    if 'sort' not in request.session:
        request.session['sort'] = 'relevance'

    request.session['start'] = 0
    request.session['page'] = 1

    if request.method == 'POST':

        if request.POST.get('query'):
            request.session['query'] = request.POST['query'].strip()

        request.session['agencies'] = request.POST.getlist('agencies[]')
        request.session['categories'] = request.POST.getlist('categories[]')
        request.session['types'] = request.POST.getlist('types[]')

    if request.method == 'GET':

        if 'page' in request.GET:
            request.session['start'] = int(request.session['size']) * (int(request.GET['page']) - 1)
            request.session['page'] = request.GET['page']

        request.session['size'] = request.GET.get('size', request.session.get('size'))

        request.session['sort'] = request.GET.get('sort', request.session.get('sort'))

    # all information gathered -> run_query
    request.session['results'], request.session['results_total'] = run_query(
        request.session['query'],
        request.session['agencies'],
        request.session['categories'],
        request.session['types'],
        request.session['start'],
        request.session['size'],
        request.session['sort'])

    request.session['num_pages'] = int(ceil(request.session['results_total']/float(request.session['size'])))

    context_dict = {'agencies': AGENCIES,
                    'categories': CATEGORIES,
                    'types': TYPES,
                    'results': request.session['results'],
                    'results_start': request.session['start'] + 1,
                    'results_end': request.session['start'] + len(request.session['results']),
                    'results_total': request.session['results_total'],
                    'records': range(1, request.session['results_total']+1),
                    'page': request.session['page'],
                    'query': request.session['query']}

    return render(request, 'gpp/results.html', context_dict)