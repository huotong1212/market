import Vue from 'vue'
import * as types from './mutation-types';

export default {
  // addNum (state, num) {
  //   state.count += num
  // },
  // 不要再这里操作异步数据
  addNumAsyn (state, payload) {
    setTimeout(() => {
      state.count += payload.num
    }, 1000)
  },
  addNumByAction (state, payload) {
    state.count += payload.num
  },
  addNum (state, payload) {
    state.count += payload.num
  },
  updateMyProps (state, payload) {
    // state.myProps.name = payload.name
    Vue.set(state.myProps, 'name', payload.name)
  },

  [types.SET_INFO] (state, payload) {
    Vue.set(state.userInfo, 'username', payload.username)
    Vue.set(state.userInfo, 'token', payload.token)
  },
  [types.SET_RESUME_ID] (state, id) {
    state.resumeId = id
  },
  setResumeName (state, name) {
    state.resumeName = name
  },
  setLang (state, lang) {
    state.lang = lang
  },
}
