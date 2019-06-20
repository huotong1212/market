import Vue from 'vue'

// 1.导入vuex
import Vuex from 'vuex'
// import 'es6-promise/auto'

// 2.注入
Vue.use(Vuex)

import moduleA from './store/moduleA/index'

export default new Vuex.Store({
  // 五大组件
  modules: {
    a: moduleA
  }

  // state: {
  //   count: 1,
  //   msg: '学习vuex',
  //   sites: [
  //     { id: 1, text: 'Runoob' },
  //     { id: 2, text: 'Google' },
  //     { id: 3, text: 'Taobao' }
  //   ]
  // },
  // getters: {
  //   sites (state) {
  //     console.log(state)
  //     return state.sites
  //   },
  //   item: (state) => (i) => {
  //     return state.sites[i]
  //   }
  // },
  // mutations: {
  //   // addNum (state, num) {
  //   //   state.count += num
  //   // },
  //   // 不要再这里操作异步数据
  //   addNumAsyn (state, payload) {
  //     setTimeout(() => {
  //       state.count += payload.num
  //     }, 1000)
  //   },
  //   addNumByAction (state, payload) {
  //     state.count += payload.num
  //   },
  //   addNum (state, payload) {
  //     state.count += payload.num
  //   }
  // },
  // actions: {
  //   addNumAsynAciton ({commit}, payload) {
  //     setTimeout(() => {
  //       commit('addNumByAction', payload)
  //     }, 1000)
  //   }
  // }
})
