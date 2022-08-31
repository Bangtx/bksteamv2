const HOME = { path: '/', name: 'Start' }
const CLASSROOM = { path: '/classroom/:classroomId', name: 'ClassRoom' }
const CLASS_HOME = { path: '/classroom/:classroomId/home', name: 'ClassHome' }
const ROLL_CALL = { path: '/classroom/:classroomId/roll_call', name: 'RollCall' }
const SCORE = { path: '/classroom/:classroomId/score', name: 'Score' }
const LEARN = { path: '/classroom/:classroomId/learn', name: 'Learn' }
const NOTI = { path: '/classroom/:classroomId/noti', name: 'Noti' }
const NOTI_STUDENT = { path: '/classroom/:classroomId/noti_student', name: 'NotiStudent' }
const HOME_WORK = { path: '/classroom/:classroomId/home_work', name: 'HomeWork' }
const HOME_WORK_FILE = { path: '/classroom/:classroomId/home_work_file', name: 'HomeWorkFile' }
const HOME_WORK_SCORE = { path: '/classroom/:classroomId/home_work_score', name: 'HomeWorkScore' }
const HOME_WORK_STUDENT = {
  path: '/classroom/:classroomId/home_work_student',
  name: 'HomeWorkStudent'
}
const HOME_WORK_FILE_STUDENT = {
  path: '/classroom/:classroomId/home_work_file_student',
  name: 'HomeWorkFileStudent'
}
const SELF_LEARNING = {
  path: '/classroom/:classroomId/register_self_learning',
  name: 'SelfLearning'
}
const Login = { path: '/login', name: 'Login' }
const Admin = { path: '/admin', name: 'Admin' }
const CLASS_MANAGEMENT = { path: '/admin/class_management', name: 'ClassManagement' }
const TEACHER_MANAGEMENT = { path: '/admin/teacher_management', name: 'TeacherManagement' }
const STUDENT_MANAGEMENT = { path: '/admin/student_management', name: 'StudentManagement' }

// const DISABLE_NAVIGATION = [Login.path]

export {
  HOME,
  Login,
  CLASSROOM,
  Admin,
  CLASS_HOME,
  ROLL_CALL,
  SCORE,
  NOTI,
  NOTI_STUDENT,
  LEARN,
  HOME_WORK,
  SELF_LEARNING,
  HOME_WORK_STUDENT,
  CLASS_MANAGEMENT,
  TEACHER_MANAGEMENT,
  STUDENT_MANAGEMENT,
  HOME_WORK_FILE,
  HOME_WORK_FILE_STUDENT,
  HOME_WORK_SCORE
}
