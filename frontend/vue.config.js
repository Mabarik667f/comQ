const { defineConfig } = require('@vue/cli-service');
const path = require('path');
const dotenv = require('dotenv');

dotenv.config({path: path.resolve(__dirname, '../.env.docker')})

const host = process.env.VUE_APP_HOST || '127.0.0.1';
const port = process.env.VUE_APP_PORT || 8000;
const protocol = process.env.VUE_APP_PROTOCOL || 'http';


module.exports = defineConfig({
  productionSourceMap: true,
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
  },
  pwa: {
    manifestOptions: {
        icons: [
          {
            src: "./img/icons/file.png",
            sizes: "192x192",
            type: "image/png"
        },
        {
            src: "./img/icons/file.png",
            sizes: "512x512",
            type: "image/png"
        }
      ]
    }
  }
});
