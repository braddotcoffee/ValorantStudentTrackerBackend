from config import Config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lib.not_found import NotFoundError

API_KEY = Config.CONFIG["Secrets"]["Google"]["API_KEY"]
SPREADSHEET_ID = Config.CONFIG["Google"]["SheetID"]


class SheetsService:
    SERVICE = build("sheets", "v4", developerKey=API_KEY)

    @staticmethod
    def fetch_students(spreadsheet_id: str = None):
        if spreadsheet_id is None:
            spreadsheet_id = SPREADSHEET_ID
        range_names = ["Students!A2:A"]
        result = (
            SheetsService.SERVICE.spreadsheets()
            .values()
            .batchGet(spreadsheetId=spreadsheet_id, ranges=range_names)
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
    def fetch_student(student_name: str, spreadsheet_id: str = None):
        if spreadsheet_id is None:
            spreadsheet_id = SPREADSHEET_ID

        student_name = student_name.lower()
        range_names = ["Students!A2:D", "Notes!A2:E"]
        result = (
            SheetsService.SERVICE.spreadsheets()
            .values()
            .batchGet(spreadsheetId=spreadsheet_id, ranges=range_names)
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
        return SheetsService._build_student_response(student_metadata, notes_data)

    @staticmethod
    def _build_student_response(
        student_metadata: list[str], notes_data: list[str]
    ) -> dict:
        student = {
            "name": student_metadata[0],
            "tracker": student_metadata[1],
            "startingRank": student_metadata[2],
        }

        if len(student_metadata) >= 4:
            student["startingRR"] = student_metadata[3]

        student["notes"] = [
            SheetsService._build_note_response(note) for note in notes_data
        ]
        return student

    @staticmethod
    def _build_note_response(note: list[str]) -> dict:
        note_dict = {
            "content": note[1],
            "date": note[2],
        }
        if len(note) >= 4:
            note_dict["currentRank"] = note[3]
        if len(note) >= 5:
            note_dict["currentRR"] = note[4]

        return note_dict
