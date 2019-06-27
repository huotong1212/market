import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    // mode: 'history',
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/',
            component: resolve => require(['../components/common/Home.vue'], resolve),
            meta: { title: '自述文件' },
            children:[
                {
                    path: '/dashboard',
                    component: resolve => require(['../components/page/Dashboard.vue'], resolve),
                    meta: { title: '系统首页' }
                },
                // {
                //     path: '/icon',
                //     component: resolve => require(['../components/page/Icon.vue'], resolve),
                //     meta: { title: '自定义图标' }
                // },
                // {
                //     path: '/table',
                //     component: resolve => require(['../components/page/BaseTable.vue'], resolve),
                //     meta: { title: '基础表格' }
                // },
                {
                    path: '/tabs',
                    component: resolve => require(['../components/page/Tabs.vue'], resolve),
                    meta: { title: 'tab选项卡' }
                },
                {
                    path: '/userProfile',
                    component: resolve => require(['../components/user/userProfile.vue'], resolve),
                    meta: { title: '我的信息' }
                },
                // {
                //     path: '/form',
                //     component: resolve => require(['../components/page/BaseForm.vue'], resolve),
                //     meta: { title: '基本表单' }
                // },
                // {
                //     path: '/resume',
                //     component: resolve => require(['../components/resume/RetrieveResume.vue'], resolve),
                //     meta: { title: '创建简历' }
                // },
                {
                    path: '/myResume',
                    component: resolve => require(['../components/resume/MyResume.vue'], resolve),
                    meta: { title: '我的简历' }
                },
                {
                    path: '/resume',
                    component: resolve => require(['../components/resume/RetrieveResume.vue'], resolve),
                    meta: { title: '创建简历' }
                },
                // {
                //     // 富文本编辑器组件
                //     path: '/editor',
                //     component: resolve => require(['../components/page/VueEditor.vue'], resolve),
                //     meta: { title: '富文本编辑器' }
                // },
                // {
                //     // markdown组件
                //     path: '/markdown',
                //     component: resolve => require(['../components/page/Markdown.vue'], resolve),
                //     meta: { title: 'markdown编辑器' }
                // },
                // {
                //     // 图片上传组件
                //     path: '/upload',
                //     component: resolve => require(['../components/page/Upload.vue'], resolve),
                //     meta: { title: '文件上传' }
                // },
                // {
                //     // vue-schart组件
                //     path: '/charts',
                //     component: resolve => require(['../components/page/BaseCharts.vue'], resolve),
                //     meta: { title: 'schart图表' }
                // },
                {
                    // 拖拽列表组件
                    path: '/drag',
                    component: resolve => require(['../components/page/DragList.vue'], resolve),
                    meta: { title: '拖拽列表' }
                },
                {
                    // 拖拽Dialog组件
                    path: '/dialog',
                    component: resolve => require(['../components/page/DragDialog.vue'], resolve),
                    meta: { title: '拖拽弹框' }
                },
                {
                    // 国际化组件
                    path: '/i18n',
                    component: resolve => require(['../components/page/I18n.vue'], resolve),
                    meta: { title: '国际化' }
                },
                // {
                //     // 权限页面
                //     path: '/permission',
                //     component: resolve => require(['../components/page/Permission.vue'], resolve),
                //     meta: { title: '权限测试', permission: true }
                // },
                {
                    path: '/404',
                    component: resolve => require(['../components/page/404.vue'], resolve),
                    meta: { title: '404' }
                },
                // {
                //     path: '/403',
                //     component: resolve => require(['../components/page/403.vue'], resolve),
                //     meta: { title: '403' }
                // }
            ]
        },
        {
            path: '/showResume',
            name:'showResume',
            component: resolve => require(['../components/show/ResumeBody.vue'], resolve)
        },
        {
            path: '/login',
            component: resolve => require(['../components/page/Login.vue'], resolve)
        },
        {
            path: '/register',
            name:'register',
            component: resolve => require(['../components/page/Register.vue'], resolve)
        },
        {
            path: '/retrieve',
            name:'retrieve',
            component: resolve => require(['../components/page/RetrievePassword.vue'], resolve)
        },
        {
            path: '/setPassword',
            name:'setPassword',
            component: resolve => require(['../components/page/ResetPassword.vue'], resolve)
        },
        {
            path: '/bestResume',
            name:'bestResume',
            component: resolve => require(['../components/show/left-right-rtl.vue'], resolve)
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
})
