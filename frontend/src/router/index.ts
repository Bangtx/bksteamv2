import Vue from 'vue'
import VueRouter, {RouteConfig} from 'vue-router'

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import { urlPath } from '@/utils'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    ...urlPath.HOME,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Home/index.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.CLASS_HOME,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/ClassHome.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.ROLL_CALL,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/RollCall.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.SCORE,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/Score.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.NOTI,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/Noti.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.NOTI_STUDENT,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/NotificationStudent.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.HOME_WORK,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/HomeWordManual.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.SELF_LEARNING,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/RegisterSelfLearning.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.HOME_WORK_STUDENT,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/HomeWorkManualStudent.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.HOME_WORK_FILE,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/HomeWorkFile.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.HOME_WORK_FILE_STUDENT,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/HomeWorkFileStudent.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.HOME_WORK_SCORE,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Classroom/HomeWorkScore.vue'),
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('token')
      if (token && from.name !== to.name) {
        next()
        return
      }
      next({ name: 'Login' })
    }
  },
  {
    ...urlPath.Login,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Login/index.vue')
  },
  {
    ...urlPath.CLASS_MANAGEMENT,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Admin/ClassroomManagement.vue')
  },
  {
    ...urlPath.TEACHER_MANAGEMENT,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Admin/TeacherManagement.vue')
  },
  {
    ...urlPath.STUDENT_MANAGEMENT,
    component: () => import(/* webpackChunkName: "home" */ '../pages/Admin/StudentManagement.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
