import Vue from 'vue'

const toHex = (st) => {
  let hash = 0
  if (st.length === 0) return hash
  for (let i = 0; i < st.length; i++) {
    hash = st.charCodeAt(i) + ((hash << 5) - hash)
    hash = Math.abs(hash & hash)
  }
  let color = '#'
  for (let i = 0; i < 3; i++) {
    const value = ((hash >> (i * 8)) % 126) + 129
    color += ('00' + value.toString(16)).substr(-2)
  }
  return color
}

Vue.prototype.$toHex = toHex
