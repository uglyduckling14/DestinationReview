# Assignment 3: Destinations

## Description:

Build an application that uses session-based authentication and where users own their data and can share it publicly.

## Requirements:

### Models:

User:
    name: string
    email: string unique
    password_hash: string

Session:
    one-to-one relationship with user
    token:string

Destination:
    name: string
    review: string //user review of destination
    rating: number // between 1-5
    has a many to one relationship with user
    share_publicly: boolean //allows user to share if destination gets shared with others.

### Endpoints:

GET /
    Renders 5 most recent publicly shared destinations and info. Links to users/new and sessions/new page. If user is signed in, link to /destinations instead

GET /users/new
    Renders page that allows uer to create an account, logs them in, and redirects to /destinations page. Should submit a POST request to /users endpoint

GET /sessions/new
    Renders page to sign into existing account. Redirects to /destinations page and submits a POST request to /session endpoint

POST /users
    Accepts new data and validates:
        Valid user email (contains @)
        Valid password (must be at least 8 characters and contain a number)
        Create a user:
            If errors respons with 400 error with description
        Create a session for user
        Writes token to cookie
        Redirects to /destinations page

POST /sessions
    Accepts data for existing user:
        Find user by email:
            If non-existent return 404
        Validate password:
            If not valid return 404
        Create session for user
        Writes token to cookie
        Redirects to /destinations page

POST /sessions/destroy
    Destroys current session and redirects to / page

GET /destinations
    Renders all lists of current users destinations. Each destination should have a /destinations/:id endpoint. Should have a link to /destinations/new

GET /destinations/new
    Renders form to create a new destination. Should POST to /destinations

POST /destinations
    Accepts form data for new destination. Creates destination into database. Redirects to /destinations

GET /destinations/:id
    Renders page that is prepopulated with info for destination user can edit. Should POST to /destinations/:id. If it does not belong to user/not exist return 404. Has a delete button which POSTs to destinations/:id/destroy

POST /destinations/:id
    Accepts data to update destination specified by :id. If user owns destination, update and redirect to /destinations. Else return 404

POST /destinations/:id/destroy
    Deletes destination specified by user and redirect to /destinations. Else return 404

### Authentication:

Should implement session-based authentication

### Middleware:
Should implement "session_middleware" that reads session token from cookie and finds which user it belongs to.
    Read session_token out of cookie
    Find session by token
        If no session is found then skip to step 4
    Get the user from session and attach it to request
    If URI maps to endpoint requires user to be logged in and there is no session, redirect them to /session/new
        else call new middleware and return result
Hardcode list of URIs that don't require user log in and only call next middleware if there is not session for those cases

### Front End:
See endpoints

## Pseudocode:

### Models:

class User(models.Model):
    name = models.CharField(max length)
    email = models.CharField(max length)
    password_hash = models.CharField(min length 8)
    token: token

    def checkValidEmail(value):
        if email contains @ and does not exist elsewhere:
            return true
        return false
    
    def checkValidPassword(value):
        if password contains number and greater length than 8:
            return true
        return false

class Session:
    token = string
    user: User

class Destination:
    name:string
    review:string
    rating:number
    share_publicly:boolean
    user:User

### Endpoints:

GET /:
for destination in destination_set_public: //only 5
    create destination widget
        if user is not logged in:
            add link to users/new and sessions/new
        else:
            link to /destinations

GET /users/new:
