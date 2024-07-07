const wsProtocol = window.location.protocol === 'https:' ? 'wss': 'ws';
const wsHost = 'localhost'
// const wsPort = 9000

export default function getWebSocketURL(path) {
    return `${wsProtocol}://${wsHost}/${path}`
}