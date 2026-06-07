from urllib import request

from django.shortcuts import render
import base64
from django.core.files.storage import FileSystemStorage
from .models import Resume  
from .models import Resume
from django.shortcuts import render, redirect



def homepage(request):
    return render(request, 'homepage.html')

def dashboard(request):
    resumes = Resume.objects.all()

    return render(request, 'dashboard.html', {
        'resumes': resumes
    }) 

def view_resume(request, id):
    resume = Resume.objects.get(id=id)

    # Convert string back to list
    skills = resume.skills.split(", ")
    projects = resume.projects.split(", ")

    context = {
        'name': resume.name,
        'skills': skills,
        'projects': projects,
        'education': resume.education,
        'experience': resume.experience,
        'photo_url': resume.photo.url if resume.photo else None
    }

    return render(request, resume.template, context)

def edit_resume(request, id):
    resume = Resume.objects.get(id=id)

    if request.method == "POST":
        resume.name = request.POST.get('name')
        resume.education = request.POST.get('education')
        resume.experience = request.POST.get('experience')

        skills_list = request.POST.getlist('skills[]')
        projects_list = request.POST.getlist('projects[]')

        resume.skills = ", ".join(skills_list)
        resume.projects = ", ".join(projects_list)

        photo = request.FILES.get('photo')
        if photo:
            resume.photo = photo

        resume.save()

        return redirect('/dashboard/')

    # convert string → list for form
    skills = resume.skills.split(", ")
    projects = resume.projects.split(", ")

    return render(request, 'edit.html', {
        'resume': resume,
        'skills': skills,
        'projects': projects
    })


ALLOWED_TEMPLATES = [
    'template1.html',
    'template2.html',
    'template3.html',
    'template4.html',
]

def home(request):
    if request.method != 'POST':
        return render(request, 'form.html')
 
    # Personal Info
    name             = request.POST.get('name', '').strip()
    job_title        = request.POST.get('job_title', '').strip()
    email            = request.POST.get('email', '').strip()
    phone            = request.POST.get('phone', '').strip()
    location         = request.POST.get('location', '').strip()
    linkedin         = request.POST.get('linkedin', '').strip()
    github           = request.POST.get('github', '').strip()
    website          = request.POST.get('website', '').strip()
    summary          = request.POST.get('summary', '').strip()
    years_experience = request.POST.get('years_experience', '').strip()
    skill_category   = request.POST.get('skill_category', '').strip()
 
    # Photo Upload 
    photo = request.FILES.get('photo')
    photo_url = None

    if photo:
        image_data = photo.read()
        encoded = base64.b64encode(image_data).decode('utf-8')

        photo_url = f"data:{photo.content_type};base64,{encoded}"
 
    # Skills & Languages 
    skills    = [s.strip() for s in request.POST.getlist('skills[]')    if s.strip()]
    languages = [l.strip() for l in request.POST.getlist('languages[]') if l.strip()]
    interests = [i.strip() for i in request.POST.getlist('interests[]') if i.strip()]
 
    # Certifications & Awards 
    certifications = [c.strip() for c in request.POST.getlist('certifications[]') if c.strip()]
    awards         = [a.strip() for a in request.POST.getlist('awards[]')         if a.strip()]
 
    # Work Experience
    exp_titles    = request.POST.getlist('exp_title[]')
    exp_companies = request.POST.getlist('exp_company[]')
    exp_starts    = request.POST.getlist('exp_start[]')
    exp_ends      = request.POST.getlist('exp_end[]')
    exp_locations = request.POST.getlist('exp_location[]')
    exp_descs     = request.POST.getlist('exp_description[]')
 
    experiences = []
    for i in range(len(exp_titles)):
        title = exp_titles[i].strip() if i < len(exp_titles) else ''
        if not title:
            continue
        experiences.append({
            'title':       title,
            'company':     exp_companies[i].strip()  if i < len(exp_companies)  else '',
            'start':       exp_starts[i].strip()     if i < len(exp_starts)     else '',
            'end':         exp_ends[i].strip()       if i < len(exp_ends)       else '',
            'location':    exp_locations[i].strip()  if i < len(exp_locations)  else '',
            'description': exp_descs[i].strip()      if i < len(exp_descs)      else '',
        })
 
    # Education 
    edu_degrees      = request.POST.getlist('edu_degree[]')
    edu_institutions = request.POST.getlist('edu_institution[]')
    edu_years        = request.POST.getlist('edu_year[]')
    edu_scores       = request.POST.getlist('edu_score[]')
 
    educations = []
    for i in range(len(edu_degrees)):
        degree = edu_degrees[i].strip() if i < len(edu_degrees) else ''
        if not degree:
            continue
        educations.append({
            'degree':      degree,
            'institution': edu_institutions[i].strip() if i < len(edu_institutions) else '',
            'year':        edu_years[i].strip()        if i < len(edu_years)        else '',
            'score':       edu_scores[i].strip()       if i < len(edu_scores)       else '',
        })
 
    # Projects
    proj_names = request.POST.getlist('proj_name[]')
    proj_techs = request.POST.getlist('proj_tech[]')
    proj_links = request.POST.getlist('proj_link[]')
    proj_descs = request.POST.getlist('proj_description[]')
 
    projects = []
    for i in range(len(proj_names)):
        name_ = proj_names[i].strip() if i < len(proj_names) else ''
        if not name_:
            continue
        projects.append({
            'name':        name_,
            'tech':        proj_techs[i].strip() if i < len(proj_techs) else '',
            'link':        proj_links[i].strip()  if i < len(proj_links)  else '',
            'description': proj_descs[i].strip()  if i < len(proj_descs)  else '',
        })
 
    # Template
    template = request.POST.get('template', 'template1.html')
    if template not in ALLOWED_TEMPLATES:
        template = 'template1.html'
 
    # Save to DB
    
    exp_str  = ' | '.join(
        f"{e['title']} at {e['company']} ({e['start']}–{e['end']})"
        for e in experiences
    )
    edu_str  = ' | '.join(
        f"{e['degree']} at {e['institution']} ({e['year']})"
        for e in educations
    )
    proj_str = ', '.join(p['name'] for p in projects)
 
    Resume.objects.create(
        name       = name,
        skills     = ', '.join(skills),
        projects   = proj_str,
        education  = edu_str,
        experience = exp_str,
        template   = template,
        photo      = photo,         
    )
 
    # Build context & render resume 
    context = {
        # Personal
        'name':             name,
        'job_title':        job_title,
        'email':            email,
        'phone':            phone,
        'location':         location,
        'linkedin':         linkedin,
        'github':           github,
        'website':          website,
        'summary':          summary,
        'years_experience': years_experience,
        'skill_category':   skill_category,
        'photo_url':        photo_url,
 
        # Lists
        'skills':           skills,
        'languages':        languages,
        'interests':        interests,
        'certifications':   certifications,
        'awards':           awards,
 
        # Structured sections
        'experiences':      experiences,
        'educations':       educations,
        'projects':         projects,
    }
 
    return render(request, template, context)


def generate_resume(request):
    if request.method == 'POST':
     
        selected_template = request.POST.get('template')

        allowed_templates = ['template1.html', 'template2.html','template3.html','template4.html']

        if selected_template in allowed_templates:
          
            return render(request, selected_template) 
        
        else:
           
            return render(request, 'template1.html')

    return redirect('form.html')

