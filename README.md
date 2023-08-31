# StudentTrackerBackend

Backend support for read only view of [Valorant Student Tracker](https://github.com/braddotcoffee/ValorantStudentTracker). This backend
supports pulling student notes from the Google Sheets API and returning them to frontend.

1. Rate limit student requests to 100 per day
2. **Only** connect to the known Student Tracking Google Sheet
3. All student notes are still considered to be **public**. No authentication will be required to read a note.

# Table of Contents

1. [Usage](#usage-example)
2. [API Documentation](#api-documentation)
3. [How To Run](#how-to-run)

# Usage Example

```python
import requests
import json

response = requests.get("http://localhost:5000/list_students")
student_response = json.loads(response.content)

for student in student_response["students"]:
    print(f"{student} has gained RR thanks to Woohoojin")
```

# API Documentation

## Students

**URL** : `/list_students`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Rate limit** : 100 requests per day

**Description** : Returns a list of all student usernames currently in the tracking sheet.

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "students": [
        "Student 1 Username",
        "Student 2 Username"
    ]
}
```

## Error Response

**Code** : `429 Too Many Requests`

**Content examples**

For the 101st request made in a given day.

```
Too Many Requests
100 per 1 day
```

## Notes

**URL** : `/student?name=<student_name>`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Rate limit** : 100 requests per day

**Description** : Returns a student overview including all of their notes. Notes will be sorted most-recent note first

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
    "student": [
        "name": "Student Username",
        "tracker": "https://tracker.gg/student",
        "startingRank": "Diamond 1",
        "notes": [
            {
                "date": "2023-08-30T00:00:00",
                "content": "Click better"
            },
            {
                "date": "2023-08-29T00:00:00",
                "content": "Click better"
            }
        ]
    ]
}
```

## Error Responses

**Code** : `400 Bad Request`

**Content examples**

If `?name=<student_name>` is not included in the request query params.

```
404 Not Found
```

**Code** : `404 Not Found`

**Content examples**

If the requested `<student_name>` does not appear in the Valorant Tracker Google Sheet.

```
404 Not Found
```

**Code** : `429 Too Many Requests`

**Content examples**

For the 101st request made in a given day.

```
Too Many Requests
100 per 1 day
```

# How To Run

To run this project you can pull the Docker image directly from GitHub packages:

```bash
docker pull ghcr.io/braddotcoffee/valorantstudenttrackerbackend:main
docker tag ghcr.io/braddotcoffee/valorantstudenttrackerbackend:main student-tracker-backend
```

Or build it locally:
```bash
docker build . -t student-tracker-backend
```


## Create Your Config

Define a `config.yaml` and `secrets.yaml` file to specify your Google API Key and Spreadsheet ID.
**Your Spreadsheet ID must be to a publicly viewable spreadsheet.**

### config.yaml
```yaml
Google:
    SheetID: <your_sheet_id>
```

### secrets.yaml
```yaml
Google:
    API_KEY: <your_api_key>
```

## Running with Docker Compose (Recommended)

Copy the contents of [compose.yaml](compose.yaml) to your local directory and run
```bash
docker compose up
```

## Running with Docker CLI
Mount the `config.yaml` and `secrets.yaml` file as part of `docker run`. 

```bash
docker run -p 5000:5000 \
    --name student-tracker-backend \
    --mount type=bind,source="$(pwd)"/secrets.yaml,target=/secrets.yaml,readonly \
    --mount type=bind,source="$(pwd)"/config.yaml,target=/config.yaml,readonly \
    student-tracker-backend
```