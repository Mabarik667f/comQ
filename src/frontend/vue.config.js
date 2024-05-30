// const {Cookies} = require('js-cookie');
const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/v1': {
        target: 'http://127.0.0.1:8000',
        logLevel: 'debug'
      },
      // '/ws': {
      //   target: 'ws://localhost:8000/ws/?token=' + [Cookies.get('access')],
      //   logLevel: 'debug'
      // }
    }
  }
})
