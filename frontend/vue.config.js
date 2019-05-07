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
        target: 'http://172.26.38.1:8080',
        ws: true,
        changeOrigin: true
      }
    }
  },
}
