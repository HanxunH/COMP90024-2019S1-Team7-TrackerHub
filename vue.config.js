module.exports = {
  lintOnSave: false,
  configureWebpack: {
    devtool: 'source-map'
  },
  chainWebpack: config => {

  },
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  devServer: { 
    disableHostCheck: true,
    host: '0.0.0.0',
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://www.ourNectarServer.com',
        ws: true,
        changeOrigin: true
      }
    }
  },
}
