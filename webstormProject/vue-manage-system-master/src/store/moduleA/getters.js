export default {
  count (state) {
    return state.count
  },
  myProps (state) {
    return state.myProps
  },
  sites (state) {
    return state.sites
  },
  item: (state) => (i) => {
    return state.sites[i]
  }
}
