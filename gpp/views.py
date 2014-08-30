from django.shortcuts import render
from gpp_search import run_query
from math import ceil


AGENCIES = ['Aging', 'Buildings', 'Campaign Finance', 'Children\'s Services', 'City Council', 'City Clerk', 'City Planning', 'Citywide Admin Svcs', 'Civilian Complaint', 'Comm - Police Corr', 'Community Assistance', 'Comptroller', 'Conflicts of Interest', 'Consumer Affairs', 'Contracts', 'Correction', 'Criminal Justice Coordinator', 'Cultural Affairs', 'DOI - Investigation', 'Design/Construction', 'Disabilities', 'District Atty, NY County', 'Districting Commission', 'Domestic Violence', 'Economic Development', 'Education, Dept. of', 'Elections, Board of', 'Emergency Mgmt.', 'Employment', 'Empowerment Zone', 'Environmental - DEP', 'Environmental - OEC', 'Environmental - ECB', 'Equal Employment', 'Film/Theatre', 'Finance', 'Fire', 'FISA', 'Health and Mental Hyg.', 'HealthStat', 'Homeless Services', 'Hospitals - HHC', 'Housing - HPD', 'Human Rights', 'Human Rsrcs - HRA', 'Immigrant Affairs', 'Independent Budget', 'Info. Tech. and Telecom.', 'Intergovernmental', 'International Affairs', 'Judiciary Committee', 'Juvenile Justice', 'Labor Relations', 'Landmarks', 'Law Department', 'Library - Brooklyn', 'Library - New York', 'Library - Queens', 'Loft Board', 'Management and Budget', 'Mayor', 'Metropolitan Transportation Authority', 'NYCERS', 'Operations', 'Parks and Recreation', 'Payroll Administration', 'Police', 'Police Pension Fund', 'Probation', 'Public Advocate', 'Public Health', 'Public Housing-NYCHA', 'Records', 'Rent Guidelines', 'Sanitation', 'School Construction', 'Small Business Svcs', 'Sports Commission', 'Standards and Appeal', 'Tax Appeals Tribunal', 'Tax Commission', 'Taxi and Limousine', 'Transportation', 'Trials and Hearings', 'Veterans - Military', 'Volunteer Center', 'Voter Assistance', 'Youth & Community']
CATEGORIES = ['Business and Consumers', 'Cultural/Entertainment', 'Education', 'Environment', 'Finance and Budget', 'Government Policy', 'Health', 'Housing and Buildings', 'Human Services', 'Labor Relations', 'Public Safety', 'Recreation/Parks', 'Sanitation', 'Technology', 'Transportation']
TYPES = ['Annual Report', 'Audit Report', 'Bond Offering - Official Statements', 'Budget Report', 'Consultant Report', 'Guide - Manual', 'Hearing - Minutes', 'Legislative Document', 'Memoranda - Directive', 'Press Release', 'Serial Publication', 'Staff Report', 'Report']


def index(request):
    request.session['query'] = '' # temporary defensive]

    context_dict = {'agencies': AGENCIES,
                    'categories': CATEGORIES,
                    'types': TYPES}

    return render(request, 'gpp/index.html', context_dict)


def results(request):
    query = ''
    num_pages = 0
    if 'start' not in request.session:
        request.session['start'] = 0
    if 'size' not in request.session:
        request.session['size'] = 10

    if request.method == 'POST':

        if request.POST.get('query'):
            query = request.POST['query'].strip()
            request.session['query'] = query
        elif request.session.get('query'):
            query = request.session['query']

        request.session['agencies'] = request.POST.getlist('agencies[]')
        request.session['categories'] = request.POST.getlist('categories[]')
        request.session['types'] = request.POST.getlist('types[]')

    if request.method == 'GET':

        request.session['start'] = 0

        if request.session.get('query'):
            query = request.session['query']

        if 'page_id' in request.GET:
            request.session['start'] = int(request.session['size']) * (int(request.GET['page_id']) - 1)

        # if 'size' in request.GET:
        #     request.session['size'] = request.GET['size']

        request.session['size'] = request.GET.get('size', request.session.get('size'))

    results, num_results = run_query(query,
                                     request.session['agencies'],
                                     request.session['categories'],
                                     request.session['types'],
                                     request.session['start'],
                                     request.session['size'])

    request.session['results'] = results
    request.session['num_results'] = num_results

    if results:
        num_pages = int(ceil(num_results/float(request.session['size'])))

    context_dict = {'agencies': AGENCIES,
                    'categories': CATEGORIES,
                    'types': TYPES,
                    'results': results,
                    'num_results': num_results,
                    'pages': range(1, num_pages+1),
                    'query': query}

    return render(request, 'gpp/results.html', context_dict)