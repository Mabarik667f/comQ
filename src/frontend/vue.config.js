const { defineConfig } = require('@vue/cli-service');
const host = "127.0.0.1";
const port = 8000;

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/v1': {
        target: `http://${host}:${port}`,
        changeOrigin: true,
        logLevel: 'debug'
      },
      '/media': {
        target: `http://${host}:${port}`,
        changeOrigin: true,
        logLevel: 'debug'
      },
      '/socket': {
        target: `http://${host}:${port}`,
        ws: true,
        changeOrigin: true,
        logLevel: 'debug'
      }
    }
  }
});
