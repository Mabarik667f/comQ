const { defineConfig } = require('@vue/cli-service');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config({path: path.resolve(__dirname, '../.env')})

const host = process.env.VUE_APP_HOST || '127.0.0.1';
const port = process.env.VUE_APP_PORT || 8000;
const protocol = process.env.VUE_APP_PROTOCOL || 'http';
console.log(`${protocol}://${host}:${port}`)


module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/v1': {
        target: `${protocol}://${host}:${port}`,
        changeOrigin: true,
        logLevel: 'debug'
      },
      '/media': {
        target: `${protocol}://${host}:${port}`,
        changeOrigin: true,
        logLevel: 'debug'
      }
    }
  }
});
