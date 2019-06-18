//引入vue
// import Vue from 'vue';
import axios from 'axios';

//全局状态控制引入
// import store from '../store/store';
//
// import * as types from '../store/mutation-types';
// import router from '../router'

// http request 拦截器
axios.interceptors.request.use(
  config => {
    // if (store.state.userInfo.token) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
    //   config.headers.Authorization = `JWT ${store.state.userInfo.token}`;
    // }
      console.log('进入了全局请求拦截器')
      let token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6Imh1b3RvbmciLCJleHAiOjE1NjE0NTc1MjEsImVtYWlsIjoiODI0MDExMTQyQHFxLmNvbSJ9.qe9cEMrTqQyWbpsakZdbe-bDUey9f5mNTqgf_37k748"
      config.headers.Authorization = `JWT ${token}`;
      return config;
  },
  err => {
    return Promise.reject(err);
  });


// http response 拦截器
axios.interceptors.response.use(
  undefined,
  error => {
    let res = error.response;
    switch (res.status) {
      case 401:
        // 返回 401 清除token信息并跳转到登录页面
        // store.commit(types.LOGOUT);
        //router.replace({
        //  path: '/app/login',
        //  query: {redirect: router.currentRoute.fullPath}
        //})
		console.log('未登录 或者token过期');
      case 403:
        console.log('您没有该操作权限');
        // alert('您没有该操作权限');
      case 500:
        console.log('服务器错误');
        // alert('服务器错误');
    }
    return Promise.reject(error.response.data)   // 返回接口返回的错误信息
});

