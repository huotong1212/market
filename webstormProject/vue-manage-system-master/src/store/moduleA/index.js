import Vue from 'vue'

// 1.导入vuex
import Vuex from 'vuex'
import state from './state'
import getters from './getters'
import mutations from './mutations'
import * as actions from './actions'

Vue.use(Vuex)
export default {
  state,
  getters,
  mutations,
  actions
}
