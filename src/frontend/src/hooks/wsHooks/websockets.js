import {ref} from "vue"
const websockets = ref({});

export const addWebSocket = (id, ws) => {
  websockets.value[id] = ws;
}

export const getWebSocketById = (id) => {
    return websockets.value[id];
}
