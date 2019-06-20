// export default {
//   addNumAsynAciton ({commit}, payload) {
//     setTimeout(() => {
//       commit('addNumByAction', payload)
//     }, 1000)
//   },
//   updatemyprops ({commit}, payload) {
//     commit('updateMyProps', payload)
//   }
//
// }
import * as types from './mutation-types';
// 提交mutation
function makeAction (type) {
  return ({ commit }, ...args) => commit(type, ...args);
};

export const setInfo = makeAction(types.SET_INFO);
export const setResumeId = makeAction(types.SET_RESUME_ID);

export const setShopList = makeAction(types.SET_SHOPLIST);
