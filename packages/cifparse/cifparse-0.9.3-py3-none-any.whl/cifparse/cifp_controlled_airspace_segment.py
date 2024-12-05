from .cifp_controlled_airspace_point import CIFPControlledAirspacePoint
from .cifp_functions import clean_value

from sqlite3 import Cursor

TABLE_NAME = "controlled_airspace_segments"


class CIFPControlledAirspaceSegment:
    def __init__(self) -> None:
        self.multiple_code = None
        self.airspace_name = None
        self.points: list[CIFPControlledAirspacePoint] = []

    def from_lines(self, cifp_lines: list) -> None:
        initial_line = str(cifp_lines[0])
        self.multiple_code = initial_line[19:20].strip()
        self.airspace_name = initial_line[93:123].strip()

        for cifp_line in cifp_lines:
            point = CIFPControlledAirspacePoint()
            point.from_line(cifp_line)
            self.points.append(point)

    def create_db_table(db_cursor: Cursor) -> None:
        CIFPControlledAirspacePoint.create_db_table(db_cursor)

        drop_statement = f"DROP TABLE IF EXISTS `{TABLE_NAME}`;"
        db_cursor.execute(drop_statement)

        create_statement = f"""
            CREATE TABLE IF NOT EXISTS `{TABLE_NAME}` (
                `multiple_code`,
                `airspace_name`
            );
        """
        db_cursor.execute(create_statement)

    def to_db(self, db_cursor: Cursor) -> None:
        for item in self.points:
            item.to_db(db_cursor)

        insert_statement = f"""
            INSERT INTO `{TABLE_NAME}` (
                `multiple_code`,
                `airspace_name`
            ) VALUES (
                ?,?
            );
        """
        db_cursor.execute(
            insert_statement,
            (
                clean_value(self.multiple_code),
                clean_value(self.airspace_name),
            ),
        )

    def to_dict(self) -> dict:
        points = []
        for item in self.points:
            points.append(item.to_dict())

        return {
            "multiple_code": clean_value(self.multiple_code),
            "airspace_name": clean_value(self.airspace_name),
            "points": points,
        }
