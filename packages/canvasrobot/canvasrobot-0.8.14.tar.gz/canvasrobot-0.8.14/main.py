import os
from canvasrobot import CanvasRobot, show_search_result, search_replace_show

TEST_COURSE = 34  # first create this test course in Canvas


def run():
    robot = CanvasRobot(reset_api_keys=False,
                        db_force_update=False)

    # robot.update_database_from_canvas()
    # result = robot.get_students_dibsa('PM_MACS', local=False)
    # result = robot.search_user('u144466', 'A.J.D.Hendriks@tilburguniversity.edu')
    # result2 = robot.enroll_in_course(search="", course_id=4230, username='u144466')
    # above needs ncdg sis_str version canvasapi
    robot.get_courses_in_account()
    robot.report_errors()


if __name__ == '__main__':
    path = os.path.dirname(__file__)
    run()
    # console = rich.console.Console(width=120, force_terminal=True)
