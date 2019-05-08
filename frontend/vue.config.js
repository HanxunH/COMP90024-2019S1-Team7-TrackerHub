module.exports = {
  lintOnSave: true,
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
<<<<<<< HEAD
      '^/api': {
        target: 'http://172.26.38.1:8080',
=======
      '/api': {
        target: 'http://172.26.37.225',
>>>>>>> 1e9e9fda926e127c023c0264b7917cbd6726f596
        ws: true,
        changeOrigin: true,
        secure: false
      }
    }
  },
}
