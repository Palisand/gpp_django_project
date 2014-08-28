from django.shortcuts import render
from gpp_search import run_query


def index(request):
    context_dict = {'agencies': ['Aging', 'Buildings', 'Campaign Finance', 'Children\'s Services', 'City Council', 'City Clerk', 'City Planning', 'Citywide Admin Svcs', 'Civilian Complaint', 'Comm - Police Corr', 'Community Assistance', 'Comptroller', 'Conflicts of Interest', 'Consumer Affairs', 'Contracts', 'Correction', 'Criminal Justice Coordinator', 'Cultural Affairs', 'DOI - Investigation', 'Design/Construction', 'Disabilities', 'District Atty, NY County', 'Districting Commission', 'Domestic Violence', 'Economic Development', 'Education, Dept. of', 'Elections, Board of', 'Emergency Mgmt.', 'Employment', 'Empowerment Zone', 'Environmental - DEP', 'Environmental - OEC', 'Environmental - ECB', 'Equal Employment', 'Film/Theatre', 'Finance', 'Fire', 'FISA', 'Health and Mental Hyg.', 'HealthStat', 'Homeless Services', 'Hospitals - HHC', 'Housing - HPD', 'Human Rights', 'Human Rsrcs - HRA', 'Immigrant Affairs', 'Independent Budget', 'Info. Tech. and Telecom.', 'Intergovernmental', 'International Affairs', 'Judiciary Committee', 'Juvenile Justice', 'Labor Relations', 'Landmarks', 'Law Department', 'Library - Brooklyn', 'Library - New York', 'Library - Queens', 'Loft Board', 'Management and Budget', 'Mayor', 'Metropolitan Transportation Authority', 'NYCERS', 'Operations', 'Parks and Recreation', 'Payroll Administration', 'Police', 'Police Pension Fund', 'Probation', 'Public Advocate', 'Public Health', 'Public Housing-NYCHA', 'Records', 'Rent Guidelines', 'Sanitation', 'School Construction', 'Small Business Svcs', 'Sports Commission', 'Standards and Appeal', 'Tax Appeals Tribunal', 'Tax Commission', 'Taxi and Limousine', 'Transportation', 'Trials and Hearings', 'Veterans - Military', 'Volunteer Center', 'Voter Assistance', 'Youth & Community'],
                    'categories': ['Business and Consumers', 'Cultural/Entertainment', 'Education', 'Environment', 'Finance and Budget', 'Government Policy', 'Health', 'Housing and Buildings', 'Human Services', 'Labor Relations', 'Public Safety', 'Recreation/Parks', 'Sanitation', 'Technology', 'Transportation'],
                    'types': ['Annual Report', 'Audit Report', 'Bond Offering - Official Statements', 'Budget Report', 'Consultant Report', 'Guide - Manual', 'Hearing - Minutes', 'Legislative Document', 'Memoranda - Directive', 'Press Release', 'Serial Publication', 'Staff Report', 'Report']}
    return render(request, 'gpp/index.html', context_dict)


def results(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    # if request.method == 'GET':
    #     # everything else?

    context_dict = {'result_list': result_list,
                    'search': query}

    return render(request, 'gpp/results.html', context_dict)