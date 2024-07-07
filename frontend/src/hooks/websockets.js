const wsProtocol = window.location.protocol === 'https:' ? 'wss': 'ws';
const wsHost = '127.0.0.1'
const wsPort = '8000'

export default function getWebSocketURL(path) {
    return `${wsProtocol}://${wsHost}:${wsPort}/${path}`
}