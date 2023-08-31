from config import Config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lib.not_found import NotFoundError

API_KEY = Config.CONFIG["Secrets"]["Google"]["API_KEY"]
SPREADSHEET_ID = Config.CONFIG["Google"]["SheetID"]


class SheetsService:
    SERVICE = build("sheets", "v4", developerKey=API_KEY)

    @staticmethod
    def fetch_students():
        range_names = ["Students!A2:A"]
        result = (
            SheetsService.SERVICE.spreadsheets()
            .values()
            .batchGet(spreadsheetId=SPREADSHEET_ID, ranges=range_names)
            .execute()
        )
        ranges = result.get("valueRanges", [])
        if len(ranges) == 0:
            return ranges
        wrapped_names = ranges[0].get("values", [])
        return {
            "students": list(map(lambda wrapped_name: wrapped_name[0], wrapped_names))
        }

    @staticmethod
    def fetch_student(student_name: str):
        student_name = student_name.lower()
        range_names = ["Students!A2:C", "Notes!A2:C"]
        result = (
            SheetsService.SERVICE.spreadsheets()
            .values()
            .batchGet(spreadsheetId=SPREADSHEET_ID, ranges=range_names)
            .execute()
        )
        ranges = result.get("valueRanges", [])
        if len(ranges) == 0:
            raise NotFoundError("Failed to fetch any students")

        student_data = ranges[0].get("values", [])
        notes_data = ranges[1].get("values", [])

        student_metadata = next(
            filter(lambda student: student[0].lower() == student_name, student_data),
            None,
        )
        if student_metadata is None:
            raise NotFoundError("Failed to find student")

        notes_data = list(
            filter(lambda note: note[0].lower() == student_name, notes_data)
        )
        notes_data.sort(key=lambda note: note[2])
        return {
            "name": student_metadata[0],
            "tracker": student_metadata[1],
            "startingRank": student_metadata[2],
            "notes": [
                {
                    "content": note[1],
                    "date": note[2],
                }
                for note in notes_data
            ],
        }
