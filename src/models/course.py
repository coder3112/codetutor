from datetime import datetime

from piccolo import columns
from piccolo.table import Table


class CourseModel(Table, tablename="courses"):
    """
    The course model has following fields:
    - **title**: Title of course
    - **instructor**: Instructor of Course(Many to Many relation)
    - **videos**: JSONField which has metadata about videos
    - **created_at**: Time at which course was created
    - **modified_at**: Time at which course was last updated.
    """

    title = columns.Varchar(unique=True, required=True)
    instructor = columns.Varchar(required=True)
    videos = columns.JSONB()
    created_at = columns.Timestamp(required=True, default=datetime.now())
    modified_at = columns.Date(required=True)
