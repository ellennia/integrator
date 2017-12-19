class Job():
    
    '''
        per_hour: How much per hour? If this is a one-time job(gig) then this var is the total amount paid.
        company: The company whose name user is working for
        job_title: User's job title
        is_gig: is it a recurring job, or a gig?
    '''
    def __init__(self, per_hour, company, job_title, is_gig):
        self.per_hour = per_hour
        self.company = company
        self.job_title = job_title
        self.is_gig = is_gig
